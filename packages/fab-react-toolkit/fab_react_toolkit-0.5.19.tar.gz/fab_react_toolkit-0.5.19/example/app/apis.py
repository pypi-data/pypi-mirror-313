import random
from typing import List

from app import appbuilder, db
from app.models import *

from fab_react_toolkit import ModelRestApi, SQLAInterface
from fab_react_toolkit.generic import *


class AssetApi(ModelRestApi):
    resource_name = "assets"
    datamodel = SQLAInterface(Asset)
    page_size = 200
    description_columns = {
        'name': 'Name of the asset',
        'owner_id': 'ID of the asset owner',
        'owner': 'Owner of the asset',
        'date_time': 'Date time of the asset',
        'date': 'Date of the asset',
    }
    quick_filters = [
        {
            "name": "asset_name",
            "label": "Asset Name",
            "column": "name",
            "type": "multiselect",
            "options": [{"value": f"asset&{i}", "label": f"asset&{i}"} for i in range(10)]
        }
    ]

    def bulk_update_time(self, id_list):
        try:
            updated = db.session.query(Asset).filter(Asset.id.in_(id_list)).update(
                {Asset.date_time: db.func.now()}, synchronize_session=False)
            db.session.commit()
            return self.response(200, message=f"Updated {updated} records")
        except Exception as e:
            db.session.rollback()
            print(e)
            return self.response(500, message=str(e))


class ApplicationApi(ModelRestApi):
    resource_name = "applications"
    datamodel = SQLAInterface(Application)
    description_columns = {
        'name': 'Name of the Application',
        'description': 'Description'
    }
    quick_filters = [
        {
            "name": "application_name",
            "label": "Application Name",
            "column": "name",
            "type": "multiselect",
            "options": [{"value": f"application_{i}", "label": f"application_{i}"} for i in range(10)]
        }
    ]


class UnitApi(ModelRestApi):
    resource_name = "units"
    datamodel = SQLAInterface(Unit)
    description_columns = {
        'name': 'Name of the unit'
    }
    quick_filters = [
        {
            "name": "unit_name",
            "label": "Unit Name",
            "column": "name",
            "type": "multiselect",
            "options": [{"value": f"unit_{i}", "label": f"unit_{i}"} for i in range(10)]
        }
    ]


class StringPkApi(ModelRestApi):
    resource_name = "stringpk"

    datamodel = SQLAInterface(StringPk)

    def pre_add(self, item) -> None:
        """
        If criticality != green then close green status    
        """
        print(item.name)
        item.id = item.name
        pass


class PSModel(GenericModel):
    id = GenericColumn(int, primary_key=True)
    first_name = GenericColumn(str, nullable=False)
    last_name = GenericColumn(str, nullable=False)
    email = GenericColumn(str, nullable=False)
    logged_in = GenericColumn(bool)


class PSSession(GenericSession):

    def load_data(self) -> List[GenericModel]:
        # Load 1000 records
        items = []

        for i in range(1000):
            model = PSModel()
            model.id = i
            model.first_name = str(i) + " " + random.choice(
                ['John', 'Jane', 'Doe', 'Alice', 'Bob'])
            model.last_name = random.choice(
                ['Doe', 'Smith', 'Johnson', 'Brown', 'Williams'])
            model.email = f"{model.first_name.lower()}.{model.last_name.lower()}@example.com"
            model.logged_in = random.choice([True, False])
            items.append(model)
        return items


class PSApi(GenericApi):
    resource_name = "generic_datasource"
    base_order = ('id', 'desc')
    add_columns = ['first_name']
    datamodel = GenericInterface(PSModel, PSSession())


appbuilder.add_api(AssetApi)
appbuilder.add_api(ApplicationApi)
appbuilder.add_api(UnitApi)
appbuilder.add_api(StringPkApi)
appbuilder.add_api(PSApi)
