"""Validators for DAPI."""

from .activerecord import ActiveRecordDapiValidator
from .base import BaseDapiValidator, DapiValidator  # pylint: disable=unused-import
from .dbt import DbtDapiValidator
from .fallback import FallbackDapiValidator
from .prisma import PrismaDapiValidator
from .pynamodb import PynamodbDapiValidator
from .sequelize import SequelizeDapiValidator
from .sqlalchemy import SqlAlchemyDapiValidator
from .typeorm import TypeOrmDapiValidator

DAPI_INTEGRATIONS_VALIDATORS = {
    "activerecord": ActiveRecordDapiValidator,
    "dbt": DbtDapiValidator,
    "prisma": PrismaDapiValidator,
    "pynamodb": PynamodbDapiValidator,
    "sqlalchemy": SqlAlchemyDapiValidator,
    "sequelize": SequelizeDapiValidator,
    "typeorm": TypeOrmDapiValidator,
}


ALWAYS_RUN_DAPI_VALIDATORS = {
    FallbackDapiValidator,
}
