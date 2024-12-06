from _typeshed import Incomplete
from amsdal.schemas.manager import SchemaManager as SchemaManager
from amsdal_models.classes.manager import ClassManager
from amsdal_utils.config.manager import AmsdalConfigManager as AmsdalConfigManager
from amsdal_utils.models.data_models.core import DictSchema, TypeData as TypeData
from amsdal_utils.models.data_models.schema import PropertyData as PropertyData
from pathlib import Path
from pydantic import BaseModel
from typing import Any

logger: Incomplete

class FixtureData(BaseModel):
    class_name: str
    external_id: str
    data: dict[str, Any]

class FixturesManager:
    """
    Manager class for handling fixture data.

    This class is responsible for loading, processing, and applying fixture data
    to the database. It supports nested object construction, data processing,
    and file fixture handling.
    """
    fixtures_path: Incomplete
    fixtures: Incomplete
    _created_cache: Incomplete
    data_to_process: Incomplete
    _class_manager: Incomplete
    _config_manager: Incomplete
    _schema_manager: Incomplete
    def __init__(self, fixtures_path: Path, class_manager: ClassManager, config_manager: AmsdalConfigManager, schema_manager: SchemaManager) -> None: ...
    def load_fixtures(self) -> None:
        """
        Loads fixture data from the specified path.

        This method reads fixture data from a JSON file located at the `fixtures_path`.
        It populates the `fixtures` dictionary with the loaded data, where each fixture
        is indexed by its external ID.

        Returns:
            None
        """
    def construct_nested_object(self, external_id: Any) -> Any:
        """
        Constructs a nested object reference from the given external ID.

        This method takes an external ID and constructs a nested object reference
        dictionary. If the external ID is a dictionary containing an '_object_id' key,
        it extracts the ID. If the external ID is not a string or integer, it returns
        the external ID as is.

        Args:
            external_id (Any): The external ID to construct the nested object reference from.

        Returns:
            Any: A dictionary representing the nested object reference or the original
            external ID if it is not a string or integer.
        """
    def _process_object_data(self, model_properties: dict[str, PropertyData], data: dict[str, Any]) -> dict[str, Any]: ...
    def _process_object_value(self, field_configuration: PropertyData | DictSchema | TypeData, value: Any) -> Any: ...
    def process_fixture_object_data(self, class_name: str, external_id: str, data: dict[str, Any]) -> None:
        """
        Processes and saves fixture object data to the database.

        This method takes the class name, external ID, and data dictionary of a fixture object,
        processes the data according to the class schema, and saves the object to the database.
        If the object already exists, it updates the existing object with the new data.

        Args:
            class_name (str): The name of the class to which the fixture object belongs.
            external_id (str): The external ID of the fixture object.
            data (dict[str, Any]): The data dictionary of the fixture object.

        Returns:
            None
        """
    def process_fixture(self, fixture: dict[str, Any]) -> None:
        """
        Processes a single fixture and adds it to the processing queue.

        This method takes a fixture dictionary, checks if the fixture already exists in the database,
        and either updates the existing fixture or creates a new one. It then adds the fixture data
        to the processing queue for further processing.

        Args:
            fixture (dict[str, Any]): The fixture dictionary containing the external ID, class name,
            and data of the fixture.

        Returns:
            None
        """
    def apply_fixtures(self) -> None:
        """
        Applies all loaded fixtures to the database.

        This method processes each fixture in the `fixtures` dictionary in the order
        specified by their 'order' value. It calls the `process_fixture` method for
        each fixture and then processes the data in the processing queue.

        Returns:
            None
        """
    def _process_data(self) -> None: ...
    def apply_file_fixtures(self) -> None:
        """
        Applies file fixtures from the specified directory.

        This method processes file fixtures located in the 'files' directory adjacent to the
        `fixtures_path`. It iterates through each file, reads its content, and processes it
        as a fixture. If the file fixture already exists in the database, it updates the
        existing fixture; otherwise, it creates a new one.

        Returns:
            None
        """
    def _process_file_fixture(self, file_path: Path, file_key: str) -> None: ...

class AsyncFixturesManager:
    """
    Manager class for handling fixture data.

    This class is responsible for loading, processing, and applying fixture data
    to the database. It supports nested object construction, data processing,
    and file fixture handling.
    """
    fixtures_path: Incomplete
    fixtures: Incomplete
    _created_cache: Incomplete
    data_to_process: Incomplete
    _class_manager: Incomplete
    _config_manager: Incomplete
    _schema_manager: Incomplete
    def __init__(self, fixtures_path: Path, class_manager: ClassManager, config_manager: AmsdalConfigManager, schema_manager: SchemaManager) -> None: ...
    def load_fixtures(self) -> None:
        """
        Loads fixture data from the specified path.

        This method reads fixture data from a JSON file located at the `fixtures_path`.
        It populates the `fixtures` dictionary with the loaded data, where each fixture
        is indexed by its external ID.

        Returns:
            None
        """
    def construct_nested_object(self, external_id: Any) -> Any:
        """
        Constructs a nested object reference from the given external ID.

        This method takes an external ID and constructs a nested object reference
        dictionary. If the external ID is a dictionary containing an '_object_id' key,
        it extracts the ID. If the external ID is not a string or integer, it returns
        the external ID as is.

        Args:
            external_id (Any): The external ID to construct the nested object reference from.

        Returns:
            Any: A dictionary representing the nested object reference or the original
            external ID if it is not a string or integer.
        """
    def _process_object_data(self, model_properties: dict[str, PropertyData], data: dict[str, Any]) -> dict[str, Any]: ...
    def _process_object_value(self, field_configuration: PropertyData | DictSchema | TypeData, value: Any) -> Any: ...
    async def process_fixture_object_data(self, class_name: str, external_id: str, data: dict[str, Any]) -> None:
        """
        Processes and saves fixture object data to the database.

        This method takes the class name, external ID, and data dictionary of a fixture object,
        processes the data according to the class schema, and saves the object to the database.
        If the object already exists, it updates the existing object with the new data.

        Args:
            class_name (str): The name of the class to which the fixture object belongs.
            external_id (str): The external ID of the fixture object.
            data (dict[str, Any]): The data dictionary of the fixture object.

        Returns:
            None
        """
    async def process_fixture(self, fixture: dict[str, Any]) -> None:
        """
        Processes a single fixture and adds it to the processing queue.

        This method takes a fixture dictionary, checks if the fixture already exists in the database,
        and either updates the existing fixture or creates a new one. It then adds the fixture data
        to the processing queue for further processing.

        Args:
            fixture (dict[str, Any]): The fixture dictionary containing the external ID, class name,
            and data of the fixture.

        Returns:
            None
        """
    async def apply_fixtures(self) -> None:
        """
        Applies all loaded fixtures to the database.

        This method processes each fixture in the `fixtures` dictionary in the order
        specified by their 'order' value. It calls the `process_fixture` method for
        each fixture and then processes the data in the processing queue.

        Returns:
            None
        """
    async def _process_data(self) -> None: ...
    async def apply_file_fixtures(self) -> None:
        """
        Applies file fixtures from the specified directory.

        This method processes file fixtures located in the 'files' directory adjacent to the
        `fixtures_path`. It iterates through each file, reads its content, and processes it
        as a fixture. If the file fixture already exists in the database, it updates the
        existing fixture; otherwise, it creates a new one.

        Returns:
            None
        """
    async def _process_file_fixture(self, file_path: Path, file_key: str) -> None: ...
