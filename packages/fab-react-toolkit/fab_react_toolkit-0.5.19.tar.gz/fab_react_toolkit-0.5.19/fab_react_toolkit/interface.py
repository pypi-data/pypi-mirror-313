from flask_appbuilder.models.sqla.interface import SQLAInterface as FABSQLAInterface
from .filters import SQLAFilterConverter


class SQLAInterface(FABSQLAInterface):
    filter_converter_class = SQLAFilterConverter

    def get_values_map_item(self, item, show_columns):
        return {col: self._get_attr_value(item, col) for col in show_columns}
