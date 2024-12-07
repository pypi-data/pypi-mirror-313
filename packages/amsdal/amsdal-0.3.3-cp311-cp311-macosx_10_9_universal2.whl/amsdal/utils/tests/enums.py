from enum import Enum


class DbExecutionType(str, Enum):
    lakehouse_only = 'lakehouse_only'
    include_state_db = 'include_state_db'


class StateOption(str, Enum):
    sqlite = 'sqlite'
    postgres = 'postgres'


class LakehouseOption(str, Enum):
    postgres = 'postgres'
    postgres_immutable = 'postgres-immutable'
    sqlite = 'sqlite'
    sqlite_immutable = 'sqlite-immutable'
