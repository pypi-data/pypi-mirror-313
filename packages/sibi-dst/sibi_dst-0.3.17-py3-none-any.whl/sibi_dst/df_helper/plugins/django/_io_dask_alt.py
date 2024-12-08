import itertools
import dask.dataframe as dd
import pandas as pd

from django.core.cache import cache
from django.db import models
from django.db.models import Field
from django.utils.encoding import force_str as force_text
import django
from django.core.exceptions import FieldDoesNotExist

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

    @staticmethod
    def replace_from_choices(choices):
        def inner(values):
            return [choices.get(v, v) for v in values]

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
        fieldnames = tuple(qs.model._meta.get_fields())
        dtypes = self.infer_dtypes_from_django(qs)
        chunk_size = self.chunk_size
        verbose = self.verbose

        # Use values to directly fetch required fields
        qs = qs.values(*fieldnames)

        # Create partitions for Dask
        partitions = []
        iterator = qs.iterator(chunk_size=chunk_size)
        for chunk in itertools.islice(iterator, chunk_size):
            df = pd.DataFrame.from_records(chunk, columns=fieldnames)

            # Handle NaN values
            if fillna_value:
                df = df.fillna(fillna_value)

            # Optimize timezone conversions
            for col in df.columns:
                if isinstance(df[col].dtype, pd.DatetimeTZDtype):
                    df[col] = df[col].dt.tz_localize(None)

            # Optimize dtype conversion
            df = df.convert_dtypes()

            # Convert to Dask DataFrame
            partitions.append(dd.from_pandas(df, npartitions=1))

        # Combine all partitions
        dask_df = dd.concat(partitions, axis=0, ignore_index=True)

        # Apply verbose updates
        if verbose:
            self.update_with_verbose(dask_df, fieldnames, qs.model._meta.fields)

        return dask_df