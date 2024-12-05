from flask_appbuilder.api import BaseApi, BaseModelApi
from flask_appbuilder.models.generic import GenericColumn

from ..api import FABModelRestApi, ModelRestApi
from .filters import *
from .interface import *
from .schema import *
from .session import *


class GenericApi(ModelRestApi):
    # Type interface for the datamodel
    datamodel: GenericInterface

    def __init__(self) -> None:
        super(BaseApi, self).__init__()
        super(BaseModelApi, self).__init__()
        super(FABModelRestApi, self).__init__()
        name = self.resource_name or self.__class__.__name__.lower()
        self.list_title = name.capitalize()
        self.quick_filters = self.quick_filters or []
        self.filter_options = self.filter_options or {}
        self.search_model_schema_name = f"{self.__class__.__name__}.search"

        self.search_query_rel_fields = self.search_query_rel_fields or dict()

        self._add_relation_column_order()
        self._add_function_list_columns()

    def _init_model_schemas(self) -> None:
        """
        Initializes the model schemas for list, search, show, add, and edit operations.

        This method retrieves the schema from the datamodel and assigns it to the respective
        model schemas for list, search, show, add, and edit operations.

        Returns:
            None
        """
        self.list_model_schema = self.datamodel.schema
        self.search_model_schema = self.datamodel.schema
        self.show_model_schema = self.datamodel.schema
        self.add_model_schema = self.datamodel.schema
        self.edit_model_schema = self.datamodel.schema
