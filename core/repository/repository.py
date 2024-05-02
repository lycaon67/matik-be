import logging
from django.db.models import Model
from rest_framework.serializers import Serializer
from rest_framework.exceptions import ValidationError
from django.db.models import Q as QueryFilter, Value
from core.constants import identifer as idf
# from core.constants import identifer as idf
from core.util import common
from django.db.models import Max


LOGGER = logging.getLogger("arv_logger")


class Module:
    """Class for module properties"""

    def __init__(self, name, model: Model = None, serializer: Serializer = None):
        """Initializes module properties.

        Arguments:
            - name (str): Defines module name.
            - model (django.db.models.Model): Defines the Django model to interact with.
            - serializer (rest_framework.serializers.Serializers): Defines the model's serializer
        """
        LOGGER.debug("Initializes Module")
        self._name = name
        self._model = model
        self._serializer = serializer

    @property
    def name(self):
        """Property getter for name"""
        return self._name

    @property
    def model(self):
        """Property getter for model"""
        return self._model

    @property
    def serializer(self):
        """Property getter for serializer"""
        return self._serializer

    @serializer.setter
    def serializer(self, serializer):
        """Property setter for serializer"""
        self._serializer = serializer

    @model.setter
    def model(self, model):
        """Property setter for model"""
        self._model = model


class Repository():
    """
    Base class for crud functionalities
    """

    def __init__(self, module: Module):
        """Initializes the base repository class

        Arguments:
            - request (obj): A dictionary that contains the data
            - object_identifier (str): Defines instance identifier. Use as key in
                constructing response.
            - instance_id_key (str): Defines the key that holds the instance id.
            - module (Module): Defines the module properties
        """
        self._module = module

        LOGGER.debug(f"Initializes Repository service")

    @property
    def module(self):
        """Property getter for module"""
        return self._module

    def find_all(self):
        """
        Returns all serialized data from instances
        """
        LOGGER.debug(f"Performing find all.")

        model = self._module.model
        serializer = self._module.serializer

        instances = model.objects.all()
        serialized = serializer(instances, many=True)

        return serialized.data

    def find_last(self):
        """
        Returns the last record in a table
        """
        LOGGER.debug("Performing find last")

        model = self._module.model
        serializer = self._module.serializer

        instances = model.objects.all().last()

        serialized = serializer(instances)

        return serialized.data

    def save(self, data):
        """
        handles saving of data to database
        """
        LOGGER.debug(f"Creating {self._module}")

        model = self._module.model
        serializer = self._module.serializer

        serialized = serializer(data=data)
        serialized.is_valid(raise_exception=True)

        return serialized.save()

    def update(self, updated_data, source_data):
        "handles update data"
        LOGGER.debug(f"Updating {self._module.model}")

        model = self._module.model
        serializer = self._module.serializer

        serialized = serializer(source_data, data=updated_data, partial=True)
        serialized.is_valid(raise_exception=True)

        return serialized.save()

    def find_by_criteria(self, criteria: QueryFilter):
        """Retrieves the data based on the criteria provided.

        Returns:
            - The object instance
        """
        LOGGER.debug(
            "Performing find by criteria with filters {0}".format(criteria))

        model = self._module.model
        serializer = self._module.serializer

        instances = model.objects.filter(criteria)
        serialized = serializer(instances, many=True)

        return {
            idf.INSTANCES: instances,
            idf.SERIALIZED: serialized.data
        }

    def find_by_id(self, id):
        """
        Retrieve data based from id
        """
        LOGGER.debug(f"Performing find by id {id}")
        response = {}

        criteria = QueryFilter(id=id)

        response = self.find_by_criteria(criteria)

        try:
            instance = common.get_value(idf.INSTANCES, response)[0]
            serialized = common.get_value(idf.SERIALIZED, response)[0]

            response = {
                idf.INSTANCES: instance,
                idf.SERIALIZED: serialized
            }
        except IndexError:
            LOGGER.debug(f"Cannot find id {id}")

        return response

    def save_or_update(self, data, criteria):
        """
        Save an instance if it doess not exists
        Otherwise, update
        """
        model = self._module.model
        serializer = self._module.serializer

        try:
            return self.save(data)
        except ValidationError:
            # if data cannot be saved, then update data
            response = self.find_by_criteria(criteria)
            instance = common.get_value(idf.INSTANCES, response)[0]

            return self.update(data, instance)

    def switch_model(self, custom_model: Model):
        """
        Replaces the default model with a custom model
        """
        self._module.model = custom_model

    def find_all_dynamic(self):
        """
        Find all objects without using serializer for dynamic
        """
        model = self._module.model

        return model.objects.all()

    def delete(self, criteria):
        """
        Deletes an instance based on criteria given
        """
        LOGGER.debug(
            "Performing delete with filters {0}".format(criteria))

        response = self.find_by_criteria(criteria)

        try:
            obj_instance = common.get_value(idf.INSTANCES, response)

            for inst in obj_instance:
                inst.delete()

        except IndexError:
            LOGGER.debug("Cannot delete, cannot find matching criteria")
            raise IndexError("Cannot delete, cannot find criteria")
