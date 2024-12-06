
from pydantic import BaseModel, model_validator, Field

from typing import Optional, Dict, Union, List
dataframe_params: Dict[str, Union[None, str, bool, int, None]] = {
    "fieldnames": None,
    "index_col": None,
    "coerce_float": False,
    "verbose": True,
    "datetime_index": False,
    "column_names": None,
    "chunk_size": 1000,
}
# dataframe_options is a dictionary that provides additional options for modifying a pandas DataFrame.
# These options include parameters for handling duplicate values, sorting, grouping, and other DataFrame operations.

dataframe_options: Dict[str, Union[bool, str, int, None]] = {
    "debug": False,  # Whether to print debug information
    "duplicate_expr": None,  # Expression for identifying duplicate values
    "duplicate_keep": 'last',  # How to handle duplicate values ('first', 'last', or False)
    "sort_field": None,  # Field to use for sorting the DataFrame
    "group_by_expr": None,  # Expression for grouping the DataFrame
    "group_expr": None  # Expression for aggregating functions to the grouped DataFrame
}

LOOKUP_SEP = "__"

class ParamsConfig(BaseModel):
    field_map: Optional[Dict] = Field(default_factory=dict)
    legacy_filters: bool = False
    sticky_filters: Dict[str, Union[str, bool, int, float]] = Field(default_factory=dict)
    filters: Dict[str, Union[str, Dict, bool, int, float]] = Field(default_factory=dict)
    df_params: Dict[str, Union[tuple, str, bool, None]] = Field(default_factory=dict)
    df_options: Dict[str, Union[bool, str, None]] = Field(default_factory=dict)
    params: Dict[str, Union[str, bool, int, float, List[Union[str, int, bool, float]]]] = Field(default_factory=dict)

    @model_validator(mode='after')
    def check_params(self):
        if self.params is not None:
            self.parse_params(self.params)
        return self

    def parse_params(self, params):
        self.legacy_filters = params.pop('legacy_filters', self.legacy_filters)
        self.field_map = params.pop('field_map', self.field_map)
        self.sticky_filters = params.pop('params', self.sticky_filters)
        df_params, df_options, filters = {}, {}, {}
        for k, v in params.items():
            if k in dataframe_params.keys():
                df_params.update({k: v})
            elif k in dataframe_options.keys():
                df_options.update({k: v})
            else:
                filters.update({k: v})
        self.filters = {**self.sticky_filters, **filters}
        self.df_params = {**self.df_params, **df_params}
        self.df_options = {**self.df_options, **df_options}
        if self.legacy_filters:
            self.convert_legacy_filters()

    def convert_legacy_filters(self):
        if not self.legacy_filters or not self.field_map or not self.filters:
            return
        # create a reverse map of the field_map
        reverse_map = {v: k for k, v in self.field_map.items()}

        new_filters = {}
        for filter_field, value in self.filters.items():
            # split the filter_field if LOOKUP_SEP exists
            parts = filter_field.split(LOOKUP_SEP, 1)

            # replace each part with its legacy equivalent if it exists
            new_parts = [reverse_map.get(part, part) for part in parts]

            # join the parts back together and add to the new filters
            new_filter_field = LOOKUP_SEP.join(new_parts)
            new_filters[new_filter_field] = value

        self.filters = new_filters