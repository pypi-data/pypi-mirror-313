import itertools

import dask.dataframe as dd
import django
import pandas as pd
from django.core.cache import cache
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.db.models import Field
from django.utils.encoding import force_str as force_text


class ReadFrameDask:
    FieldDoesNotExist = (
        django.core.exceptions.FieldDoesNotExist
        if django.VERSION < (1, 8)
        else django.core.exceptions.FieldDoesNotExist
    )

    def __init__(
            self,
            qs,
            **kwargs,
    ):
        self.qs = qs
        self.coerce_float = kwargs.setdefault("coerce_float", False)
        self.chunk_size = kwargs.setdefault("chunk_size", 1000)
        self.verbose = kwargs.setdefault("verbose", True)

    @staticmethod
    def replace_from_choices(choices):
        def inner(values):
            return [choices.get(v, v) for v in values]

        return inner

    @staticmethod
    def get_model_name(model):
        return model._meta.model_name

    @staticmethod
    def get_related_model(field):
        model = None
        if hasattr(field, "related_model") and field.related_model:
            model = field.related_model
        elif hasattr(field, "rel") and field.rel:
            model = field.rel.to
        return model

    @classmethod
    def get_base_cache_key(cls, model):
        return (
            f"dask_{model._meta.app_label}_{cls.get_model_name(model)}_%s_rendering"
        )

    @classmethod
    def replace_pk(cls, model):
        base_cache_key = cls.get_base_cache_key(model)

        def get_cache_key_from_pk(pk):
            return None if pk is None else base_cache_key % str(pk)

        def inner(pk_series):
            pk_series = pk_series.astype(object).where(pk_series.notnull(), None)
            cache_keys = pk_series.apply(get_cache_key_from_pk, convert_dtype=False)
            unique_cache_keys = list(filter(None, cache_keys.unique()))
            if not unique_cache_keys:
                return pk_series

            out_dict = cache.get_many(unique_cache_keys)
            if len(out_dict) < len(unique_cache_keys):
                out_dict = dict(
                    [
                        (base_cache_key % obj.pk, force_text(obj))
                        for obj in model.objects.filter(
                        pk__in=list(filter(None, pk_series.unique()))
                    )
                    ]
                )
                cache.set_many(out_dict)
            return list(map(out_dict.get, cache_keys))

        return inner

    @classmethod
    def build_update_functions(cls, fieldnames, fields):
        for fieldname, field in zip(fieldnames, fields):
            if not isinstance(field, Field):
                yield fieldname, None
            else:
                if field.choices:
                    choices = dict([(k, force_text(v)) for k, v in field.flatchoices])
                    yield fieldname, cls.replace_from_choices(choices)
                elif field.get_internal_type() == "ForeignKey":
                    yield fieldname, cls.replace_pk(cls.get_related_model(field))

    @classmethod
    def update_with_verbose(cls, df, fieldnames, fields):
        for fieldname, function in cls.build_update_functions(fieldnames, fields):
            if function is not None:
                df[fieldname] = df[fieldname].map_partitions(lambda x: function(x))

    @classmethod
    def to_fields(cls, qs, fieldnames):
        """Get fields from a queryset based on the given fieldnames."""
        for fieldname in fieldnames:
            model = qs.model
            for fieldname_part in fieldname.split("__"):
                try:
                    field = model._meta.get_field(fieldname_part)
                except cls.FieldDoesNotExist:
                    try:
                        rels = model._meta.get_all_related_objects_with_model()
                    except AttributeError:
                        field = fieldname
                    else:
                        for relobj, _ in rels:
                            if relobj.get_accessor_name() == fieldname_part:
                                field = relobj.field
                                model = field.model
                                break
                else:
                    model = cls.get_related_model(field)
            yield field

    @staticmethod
    def is_values_queryset(qs):
        try:
            return qs._iterable_class == django.db.models.query.ValuesIterable
        except:
            return False

    @staticmethod
    def object_to_dict(obj, fields=None):
        """Convert a Django model instance to a dictionary based on specified fields."""
        if obj is None:
            return {}  # Return an empty dictionary if obj is None
        if not fields:
            obj.__dict__.pop("_state", None)  # Remove _state safely
            return obj.__dict__
        return {field: obj.__dict__.get(field) for field in fields if field is not None}

    @staticmethod
    def infer_dtypes_from_django(qs):
        """Infers Dask data types based on Django queryset model fields, with support for nullable integers."""
        django_to_dask_dtype = {
            'AutoField': 'Int64',  # Use nullable integer
            'BigAutoField': 'Int64',
            'BigIntegerField': 'Int64',
            'BooleanField': 'bool',
            'CharField': 'object',
            'DateField': 'datetime64[ns]',
            'DateTimeField': 'datetime64[ns]',
            'DecimalField': 'float64',
            'FloatField': 'float64',
            'IntegerField': 'Int64',  # Use nullable integer
            'PositiveIntegerField': 'Int64',
            'SmallIntegerField': 'Int64',
            'TextField': 'object',
            'TimeField': 'object',
            'UUIDField': 'object',
            'ForeignKey': 'Int64',  # Use nullable integer for FK fields
        }

        dtypes = {}
        # Handle model fields
        for field in qs.model._meta.get_fields():
            # Skip reverse relationships and non-concrete fields
            if not getattr(field, 'concrete', False):
                continue

            # Check for AutoField or BigAutoField explicitly
            if isinstance(field, (models.AutoField, models.BigAutoField)):
                dtypes[field.name] = 'Int64'  # Nullable integer for autoincremented fields
            else:
                # Use field type to infer dtype
                field_type = field.get_internal_type()
                dtypes[field.name] = django_to_dask_dtype.get(field_type, 'object')

        # Handle annotated fields
        for annotation_name, annotation in qs.query.annotation_select.items():
            if hasattr(annotation, 'output_field'):
                field_type = annotation.output_field.get_internal_type()
                dtype = django_to_dask_dtype.get(field_type, 'object')
            else:
                dtype = 'object'  # Default to object for untyped annotations
            dtypes[annotation_name] = dtype

        return dtypes

    def read_frame(self, fillna_value=None):
        qs = self.qs
        coerce_float = self.coerce_float
        verbose = self.verbose
        chunk_size = self.chunk_size

        fields = qs.model._meta.fields
        fieldnames = [f.name for f in fields]
        fieldnames += list(qs.query.annotation_select.keys())
        fieldnames = tuple(fieldnames)
        # Infer dtypes from Django fields
        dtypes = self.infer_dtypes_from_django(qs)
        if fieldnames:
            dtypes = {field: dtype for field, dtype in dtypes.items() if field in fieldnames}

        # Create partitions for Dask by iterating through chunks
        partitions = []
        iterator = iter(qs.iterator(chunk_size=chunk_size))

        while True:
            chunk = list(itertools.islice(iterator, chunk_size))
            if not chunk:
                break

            # Convert chunk to DataFrame with inferred dtypes
            df = pd.DataFrame.from_records(
                [self.object_to_dict(obj, fieldnames) for obj in chunk],
                columns=fieldnames,
                coerce_float=coerce_float,
            )
            # Handle NaN values before casting, if specified
            if fillna_value is not None:
                df = df.fillna(fillna_value)

            # Convert timezone-aware columns to timezone-naive if needed
            for col in df.columns:
                if isinstance(df[col].dtype, pd.DatetimeTZDtype):
                    df[col] = df[col].dt.tz_localize(None)

            # Convert to the appropriate data types
            df = df.astype(dtypes)
            partitions.append(dd.from_pandas(df, npartitions=1))

        # Concatenate partitions into a single Dask DataFrame
        # Ensure all partitions have the same columns

        dask_df = dd.concat(partitions, axis=0, ignore_index=True)

        if verbose:
            self.update_with_verbose(dask_df, fieldnames, fields)

        return dask_df
