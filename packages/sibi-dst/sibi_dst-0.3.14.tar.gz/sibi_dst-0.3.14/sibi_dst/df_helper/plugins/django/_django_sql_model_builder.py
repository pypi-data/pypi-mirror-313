#  Copyright (c) 2023. ISTMO Center S.A.  All Rights Reserved
#
import keyword
import re
from functools import lru_cache

from django.apps import apps
from django.db import connections
from django.db import models
from django.db.models.constants import LOOKUP_SEP

FIELD_MAP = {
    "AutoField": models.AutoField,
    "BigAutoField": models.BigAutoField,
    "BigIntegerField": models.BigIntegerField,
    "BinaryField": models.BinaryField,
    "BooleanField": models.BooleanField,
    "CharField": models.CharField,
    "DateField": models.DateField,
    "DateTimeField": models.DateTimeField,
    "DecimalField": models.DecimalField,
    "DurationField": models.DurationField,
    "EmailField": models.EmailField,
    "FileField": models.FileField,
    "FilePathField": models.FilePathField,
    "FloatField": models.FloatField,
    "ImageField": models.ImageField,
    "IntegerField": models.IntegerField,
    "GenericIPAddressField": models.GenericIPAddressField,
    "NullBooleanField": models.NullBooleanField,
    "PositiveIntegerField": models.PositiveIntegerField,
    "PositiveSmallIntegerField": models.PositiveSmallIntegerField,
    "SlugField": models.SlugField,
    "SmallIntegerField": models.SmallIntegerField,
    "TextField": models.TextField,
    "TimeField": models.TimeField,
    "URLField": models.URLField,
    "UUIDField": models.UUIDField,
    # For related fields, they may need to be handled depending on use cases
    "ForeignKey": models.ForeignKey,
    "OneToOneField": models.OneToOneField,
    "ManyToManyField": models.ManyToManyField,
}
# the following is the name of the app that will be used to associate the created on-the-fly model.
# It must be registered in INSTALLED_APPS in settings.py to prevent django from throwing an error
# when a model is reloaded.

apps_label = "datacubes"


class DjangoSqlModelBuilder:
    def __init__(self, **kwargs):
        self.connection_name = None
        self.table = None
        self.model = None
        self.__parse_builder(**kwargs)

    def __parse_builder(self, **kwargs):
        self.connection_name = kwargs.get("connection_name", None)
        self.table = kwargs.get("table", None)
        self.model = None
        if not self.connection_name:
            raise ValueError("Connection name is required")
        if not self.table:
            raise ValueError("Table name is required")
        return self

    @lru_cache(maxsize=None)
    def build_model(self):
        model = None
        model_fields = self.get_model_fields()
        model_name = self.table2model(self.table)
        if model_fields:
            try:
                model = apps.get_model(apps_label, model_name)
            except LookupError:
                model = self.create_model(model_name, model_fields)
        return model

    def create_model(self, name, fields) -> type:
        def parse_args(arg_string):
            arg_dict = {}
            # Match keyword arguments in the form key=value
            for match in re.finditer(r"(\w+)=(\w+)", arg_string):
                key, value = match.groups()
                # Try to convert value to an integer, if possible
                try:
                    value = int(value)
                except ValueError:
                    # If it's not an integer, leave it as a string
                    pass
                arg_dict[key] = value
            return arg_dict

        class Meta:
            pass

        setattr(Meta, "db_table", self.table)
        setattr(Meta, "managed", False)
        setattr(Meta, "app_label", apps_label)

        model = None
        attrs = {
            "Meta": Meta,
            "__module__": f"{apps_label}.models",
            "objects": models.Manager(),
        }
        if fields:
            for field_name, field_type in fields.items():
                field_type, args = field_type.replace("models.", "").split("(", 1)
                args = args.rstrip(")")
                field_params = parse_args(args)
                field_class = FIELD_MAP[field_type]
                attrs[field_name] = field_class(**field_params)
            model = type(name, (models.Model,), attrs)

        return model

    @staticmethod
    def table2model(table_name):
        return "".join([x.title() for x in table_name.split("_")])

    def get_model_fields(self):
        connection = connections[self.connection_name]
        if connection is None:
            raise ValueError("Connection %s not found" % self.connection_name)
        current_model = None
        try:
            with connection.cursor() as cursor:
                if hasattr(connection, "introspection"):
                    table_info = connection.introspection.get_table_list(cursor)
                    table_info = {
                        info.name: info
                        for info in table_info
                        if info.name == self.table
                    }
                    if len(table_info) == 0:
                        raise ValueError("Table %s not found" % self.table)
                    try:
                        relations = connection.introspection.get_relations(
                            cursor, self.table
                        )
                    except NotImplementedError:
                        relations = {}
                    try:
                        constraints = connection.introspection.get_constraints(
                            cursor, self.table
                        )
                    except NotImplementedError:
                        constraints = {}
                    if hasattr(connection.introspection, "get_primary_columns"):
                        primary_key_columns = (
                            connection.introspection.get_primary_columns(
                                cursor, self.table
                            )
                        )
                        primary_key_column = (
                            primary_key_columns[0] if primary_key_columns else None
                        )
                    else:
                        primary_key_columns = []
                        primary_key_column = (
                            connection.introspection.get_primary_key_column(
                                cursor, self.table
                            )
                        )

                    unique_columns = [
                        c["columns"][0]
                        for c in constraints.values()
                        if c["unique"] and len(c["columns"]) == 1
                    ]
                    table_description = connection.introspection.get_table_description(
                        cursor, self.table
                    )

                used_column_names = []  # Holds column names used in the table so far
                column_to_field_name = {}  # Maps column names to names of model fields
                current_model = {}
                for row in table_description:
                    comment_notes = (
                        []
                    )  # Holds Field notes, to be displayed in a Python comment.
                    extra_params = {}  # Holds Field parameters such as 'db_column'.
                    column_name = row.name
                    # we dont want to use model relations
                    # is_relation = column_name in relations
                    is_relation = False
                    att_name, params, notes = self.normalize_col_name(
                        column_name, used_column_names, is_relation
                    )
                    extra_params.update(params)
                    comment_notes.extend(notes)

                    used_column_names.append(att_name)
                    column_to_field_name[column_name] = att_name

                    # Add primary_key and unique, if necessary.
                    if column_name == primary_key_column:
                        extra_params["primary_key"] = True
                        if len(primary_key_columns) > 1:
                            comment_notes.append(
                                "The composite primary key (%s) found, that is not "
                                "supported. The first column is selected."
                                % ", ".join(primary_key_columns)
                            )
                    elif column_name in unique_columns:
                        extra_params["unique"] = True

                    field_type, field_params, field_notes = self.get_field_type(
                        connection, row
                    )
                    extra_params.update(field_params)
                    comment_notes.extend(field_notes)

                    field_type += "("

                    if att_name == "id" and extra_params == {"primary_key": True}:
                        if field_type == "AutoField(":
                            continue
                        elif (
                            field_type
                            == connection.features.introspected_field_types["AutoField"]
                            + "("
                        ):
                            comment_notes.append("AutoField?")

                    # Add 'null' and 'blank', if the 'null_ok' flag was present in the
                    # table description.
                    if row.null_ok:  # If it's NULL...
                        extra_params["blank"] = True
                        extra_params["null"] = True

                    field_desc = "%s%s" % (
                        "" if "." in field_type else "models.",
                        field_type,
                    )
                    if field_type.startswith(("ForeignKey(", "OneToOneField(")):
                        field_desc += ", models.DO_NOTHING"

                    # Add comment.
                    if (
                        hasattr(connection.features, "supports_comments")
                        and row.comment
                    ):
                        extra_params["db_comment"] = row.comment
                    # if connection.features.supports_comments and row.comment:
                    #    extra_params["db_comment"] = row.comment

                    if extra_params:
                        if not field_desc.endswith("("):
                            field_desc += ", "
                        field_desc += ", ".join(
                            "%s=%r" % (k, v) for k, v in extra_params.items()
                        )
                    field_desc += ")"
                    if comment_notes:
                        field_desc += "  # " + " ".join(comment_notes)
                    current_model[att_name] = field_desc
        except Exception as e:
            print(e)
            raise e
        return current_model

    @staticmethod
    def normalize_col_name(col_name, used_column_names, is_relation):
        """
        Modify the column name to make it Python-compatible as a field name
        """
        field_params = {}
        field_notes = []

        new_name = col_name.lower()
        if new_name != col_name:
            field_notes.append("Field name made lowercase.")

        if is_relation:
            if new_name.endswith("_id"):
                new_name = new_name.removesuffix("_id")
            else:
                field_params["db_column"] = col_name

        new_name, num_repl = re.subn(r"\W", "_", new_name)
        if num_repl > 0:
            field_notes.append("Field renamed to remove unsuitable characters.")

        if new_name.find(LOOKUP_SEP) >= 0:
            while new_name.find(LOOKUP_SEP) >= 0:
                new_name = new_name.replace(LOOKUP_SEP, "_")
            if col_name.lower().find(LOOKUP_SEP) >= 0:
                # Only add the comment if the double underscore was in the original name
                field_notes.append(
                    "Field renamed because it contained more than one '_' in a row."
                )
        # Commented this because we want to keep the original name regardless of the name given
        # if new_name.startswith("_"):
        #    new_name = "field%s" % new_name
        #    field_notes.append("Field renamed because it started with '_'.")

        if new_name.endswith("_"):
            new_name = "%sfield" % new_name
            field_notes.append("Field renamed because it ended with '_'.")

        if keyword.iskeyword(new_name):
            new_name += "_field"
            field_notes.append("Field renamed because it was a Python reserved word.")

        if new_name[0].isdigit():
            new_name = "number_%s" % new_name
            field_notes.append(
                "Field renamed because it wasn't a valid Python identifier."
            )

        if new_name in used_column_names:
            num = 0
            while "%s_%d" % (new_name, num) in used_column_names:
                num += 1
            new_name = "%s_%d" % (new_name, num)
            field_notes.append("Field renamed because of name conflict.")

        if col_name != new_name and field_notes:
            field_params["db_column"] = col_name

        return new_name, field_params, field_notes

    @staticmethod
    def get_field_type(connection, row):
        """
        Given the database connection, the table name, and the cursor row
        description, this routine will return the given field type name, as
        well as any additional keyword parameters and notes for the field.
        """
        field_params = {}
        field_notes = []

        try:
            field_type = connection.introspection.get_field_type(row.type_code, row)
        except KeyError:
            field_type = "TextField"
            field_notes.append("This field type is a guess.")

        # Add max_length for all CharFields.
        if field_type == "CharField" and row.display_size:
            size = int(row.display_size)
            if size and size > 0:
                field_params["max_length"] = size

        if field_type in {"CharField", "TextField"} and row.collation:
            field_params["db_collation"] = row.collation

        if field_type == "DecimalField":
            if row.precision is None or row.scale is None:
                field_notes.append(
                    "max_digits and decimal_places have been guessed, as this "
                    "database handles decimal fields as float"
                )
                field_params["max_digits"] = (
                    row.precision if row.precision is not None else 10
                )
                field_params["decimal_places"] = (
                    row.scale if row.scale is not None else 5
                )
            else:
                field_params["max_digits"] = row.precision
                field_params["decimal_places"] = row.scale

        return field_type, field_params, field_notes
