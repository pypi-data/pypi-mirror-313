from datetime import datetime
from typing import Any, Optional

from flask_appbuilder.models.filters import Filters
from flask_appbuilder.models.generic.interface import \
    GenericInterface as FABGenericInterface
from flask_appbuilder.models.sqla.interface import (get_column_root_relation,
                                                    is_column_dotted)
from marshmallow.fields import *

from .filters import GenericFilterConverter
from .schema import GenericSchema


class GenericInterface(FABGenericInterface):
    filter_converter_class = GenericFilterConverter
    schema: GenericSchema

    def __init__(self, obj, session=None):
        super().__init__(obj, session)
        cols = self.obj.properties
        field_dict = {col: self._get_field(col) for col in cols}
        self.schema = GenericSchema()
        self.schema.fields = field_dict

    def query(self, filters=None, order_column="", order_direction="", page=None, page_size=None, **kwargs):
        return super().query(filters, order_column, order_direction, page, page_size)

    def get_user_columns_list(self):
        return [col for col in super().get_user_columns_list() if col != self.obj.pk]

    def get(self, id, filters: Filters | None = None, select_columns: list[str] | None = None, outer_default_load: bool = False):
        return super().get(id)

    def edit(self, item, **kwargs):
        pk = getattr(item, self.obj.pk)
        return self.session.edit(pk, item)

    def delete(self, item, **kwargs):
        pk = getattr(item, self.obj.pk)
        return self.session.delete(pk)

    def get_inner_filters(self, filters: Optional[Filters]) -> Filters:
        """
        Inner filters are non dotted columns and
        one to many or one to one relations

        :param filters: All filters
        :return: New filtered filters to apply to an inner query
        """
        inner_filters = Filters(self.filter_converter_class, self)
        _filters = []
        if filters:
            for flt, value in zip(filters.filters, filters.values):
                if not is_column_dotted(flt.column_name):
                    _filters.append((flt.column_name, flt.__class__, value))
                elif self.is_relation_many_to_one(
                    get_column_root_relation(flt.column_name)
                ) or self.is_relation_one_to_one(
                    get_column_root_relation(flt.column_name)
                ):
                    _filters.append((flt.column_name, flt.__class__, value))
            inner_filters.add_filter_list(_filters)
        return inner_filters

    def apply_filters(self, query: Any, filters: Optional[Filters]) -> Any:
        if filters:
            return filters.apply_all(query)
        return query

    def is_boolean(self, col_name):
        return self.obj.properties[col_name].col_type == bool

    def is_date(self, col_name):
        return self.obj.properties[col_name].col_type == datetime

    def _get_field(self, col_name):
        """
        Get the appropriate field class based on the column name.

        Args:
            col_name (str): The name of the column.

        Returns:
            Field: An instance of the appropriate field class based on the column type.
        """
        required = self.is_nullable(col_name)
        unique = self.is_unique(col_name)
        field = Raw

        if self.is_string(col_name):
            field = String
        elif self.is_integer(col_name):
            field = Integer
        elif self.is_boolean(col_name):
            field = Boolean
        elif self.is_date(col_name):
            field = DateTime

        field = field(required=required, unique=unique)
        field.name = col_name
        return field
