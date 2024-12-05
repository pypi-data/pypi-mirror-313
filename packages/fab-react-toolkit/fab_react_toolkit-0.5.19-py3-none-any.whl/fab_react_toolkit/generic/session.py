from typing import List, Type

from flask_appbuilder.models.generic import GenericModel
from flask_appbuilder.models.generic import GenericSession as FABGenericSession


class GenericSession(FABGenericSession):
    """
    This class is a subclass of **flask_appbuilder.models.generic.GenericSession** with a few modifications.
    Override at least the **all** and **load_data** method.

    **GenericSession** will implement filter and orders
    based on your data generation on the **all** method.
    """
    model: Type[GenericModel]

    def __init__(self):
        super().__init__()
        items = self.load_data()
        for item in items:
            self.add(item)

    def load_data(self) -> List[GenericModel]:
        """
        Loads data for the session.

        This method is responsible for loading data required for the session.
        It should be implemented in the derived classes.

        Returns:
            List[GenericModel]: A list of items to be stored in the session.

        Raises:
            NotImplementedError: This method should be implemented in the derived classes.
        """
        raise NotImplementedError

    def edit(self, pk, item):
        """
        Edit an item in the session.

        Args:
            pk (int): The primary key of the item to be edited.
            item (object): The updated item.

        Returns:
            None
        """
        old_item = self.get(pk)
        store = self.store.get(self.query_class)
        store.insert(
            store.index(old_item), item)
        store.remove(old_item)

    def delete(self, pk):
        """
        Delete an item from the session.

        Args:
            pk (int): The primary key of the item to be deleted.

        Returns:
            None
        """
        item = self.get(pk)
        store = self.store.get(self.query_class)
        store.remove(item)

    def yield_per(self, _: int):
        """
        Should actually yield results in batches of size **yield_per**. But this is not needed in this case.
        """
        _, data = self.all()
        return data
