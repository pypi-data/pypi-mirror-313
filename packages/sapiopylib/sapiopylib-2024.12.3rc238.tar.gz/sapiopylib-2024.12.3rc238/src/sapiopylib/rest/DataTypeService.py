from __future__ import annotations

from typing import Any, Dict, List
from weakref import WeakValueDictionary

from sapiopylib.rest.User import SapioUser
from sapiopylib.rest.pojo.datatype.DataType import DataTypeDefinition, DataTypeParser
from sapiopylib.rest.pojo.datatype.DataTypeLayout import DataTypeLayoutParser, DataTypeLayout
from sapiopylib.rest.pojo.datatype.FieldDefinition import FieldDefinitionParser, AbstractVeloxFieldDefinition
from sapiopylib.rest.pojo.datatype.TemporaryDataType import TemporaryDataType


class DataTypeManager:
    """
    Obtain information about data types in the system.
    """
    user: SapioUser

    __instances: WeakValueDictionary[SapioUser, DataTypeManager] = WeakValueDictionary()
    __initialized: bool

    def __new__(cls, user: SapioUser):
        """
        Observes singleton pattern per record model manager object.

        :param user: The user that will make the webservice request to the application.
        """
        obj = cls.__instances.get(user)
        if not obj:
            obj = object.__new__(cls)
            obj.__initialized = False
            cls.__instances[user] = obj
        return obj

    def __init__(self, user: SapioUser):
        """
        Obtains a data type manager to query data type definitions.

        :param user: The user that will make the webservice request to the application.
        """
        if self.__initialized:
            return
        self.user = user
        self.__initialized = True

    def get_field_definition_list(self, data_type_name: str) -> List[AbstractVeloxFieldDefinition] | None:
        """
        Get the field definitions for every field on the provided data type. These fields can be
        used to know what fields will be returned when getting records of this type.

        :param data_type_name: The data type name of a data type in the system.
        :return: A list of the field definitions for every field on the provided data type, or None if data type does not exist.
        """
        sub_path: str = self.user.build_url(['datatypemanager', 'veloxfieldlist', data_type_name])
        response = self.user.get(sub_path)
        self.user.raise_for_status(response)
        if response.status_code == 204:
            return None
        json_list: List[Dict[str, Any]] = response.json()
        return [FieldDefinitionParser.to_field_definition(x) for x in json_list]

    def get_data_type_name_list(self) -> List[str]:
        """
        Get all data type names that exist in the system. These data type names can be used to determine which
        data record can be queried or created in the system and to query information about specific data types.

        :return: A list of all data type names from the system.
        """
        sub_path: str = '/datatypemanager/datatypenamelist'
        response = self.user.get(sub_path)
        self.user.raise_for_status(response)
        json_list: List[str] = response.json()
        return json_list

    def get_data_type_definition(self, data_type_name: str) -> DataTypeDefinition | None:
        """
        Get the data type definition for the given data type. The data type definition can be used to determine a data
        type's display name, plural name, allowable record relationships, and more.

        :param data_type_name: The data type name of a data type in the system.
        :return: The data type definition of the given data type. Return None if data type does not exist.
        """
        sub_path: str = self.user.build_url(['datatypemanager', 'datatypedefinition', data_type_name])
        response = self.user.get(sub_path)
        self.user.raise_for_status(response)
        if response.status_code == 204:
            return None
        json_dct = response.json()
        return DataTypeParser.parse_data_type_definition(json_dct)

    def get_data_type_layout_list(self, data_type_name: str) -> List[DataTypeLayout] | None:
        """
        Get all available layouts for the provided data type name. Layouts are how records are displayed to users in the
        system. They can be used by TemporaryDataTypes and DataRecordDialogRequests to control how client callbacks are
        displayed to the user.

        :param data_type_name: The data type name of a data type in the system.
        :return: A list of all data type layouts for the provided data type. Return None if data type does not exist.
        """
        sub_path: str = self.user.build_url(['datatypemanager', 'layout', data_type_name])
        response = self.user.get(sub_path)
        self.user.raise_for_status(response)
        if response.status_code == 204:
            return None
        json_list: List[Dict[str, Any]] = response.json()
        return [DataTypeLayoutParser.parse_layout(x) for x in json_list]

    def get_default_layout(self, data_type_name: str) -> DataTypeLayout | None:
        """
        Get the default layout for the provided data type name.
        :param data_type_name: The data type name of a data type in the system we are retrieving default layout for.
        """
        sub_path: str = self.user.build_url(['datatypemanager', 'defaultlayout', data_type_name])
        response = self.user.get(sub_path)
        self.user.raise_for_status(response)
        if response.status_code == 204:
            return None
        return DataTypeLayoutParser.parse_layout(response.json())

    def get_temporary_data_type(self, data_type_name: str, layout_name: str | None = None) -> TemporaryDataType | None:
        """
        Get temporary data type for an existing data type in Sapio.
        This object can be used in interactions in client callback methods.
        :param data_type_name: The data type name to obtain the temporary data type object.
        :param layout_name: If not specified, we will return the default layout for current user.
        Otherwise, we will return the temporary type filled with the specified layout.
        :return The temporary data type of the default or provided layout for the data type. Return None if data type does not exist.
        """
        sub_path: str = self.user.build_url(['datatypemanager', 'temporarydatatype', data_type_name])
        if not layout_name:
            layout_name = ""
        response = self.user.get(sub_path, params={"layoutName": layout_name})
        self.user.raise_for_status(response)
        if response.status_code == 204:
            return None
        json_dict: Dict[str, Any] = response.json()
        return TemporaryDataType.from_json(json_dict)

    def test_temporary_data_type_translation(self, temp_dt_to_test: TemporaryDataType):
        """
        Translate the temporary data type fully into java temporary data type and translate back into JSON again. Nothing else will run in this operation.
        This is created to help unit testing of client POJO structures.
        :param temp_dt_to_test: The temporary data type to test translations for.
        :return: The returned temporary data type that hopefully matches the original one.
        """
        sub_path: str = self.user.build_url(['datatypemanager', 'test', 'temporarydatatype'])
        response = self.user.post(sub_path, payload=temp_dt_to_test.to_json())
        self.user.raise_for_status(response)
        return TemporaryDataType.from_json(response.json())