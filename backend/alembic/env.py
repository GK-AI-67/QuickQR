from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))
from app.core.database import Base as MainBase
from app.lost_and_found_qr.models.lost_and_found_qr_db import LostAndFoundQRDB, Base as LostAndFoundQRBase
from app.lost_and_found_qr.models.user_qr_mpg_db import UserQRMPGDB, Base as UserQRMPGBase
from app.lost_and_found_qr.models.user_dtls_db import UserDtlsDB, Base as UserDtlsBase
from app.lost_and_found_qr.models.lost_and_found_scanner_db import LostAndFoundScannerDB, Base as LostAndFoundScannerBase

# Combine all metadata for Alembic autogenerate
from sqlalchemy import MetaData
metadata = MetaData()
for m in [MainBase.metadata, LostAndFoundQRBase.metadata, UserQRMPGBase.metadata, UserDtlsBase.metadata, LostAndFoundScannerBase.metadata]:
    for t in m.tables.values():
        if t.name not in metadata.tables:
            metadata._add_table(t.name, t.schema, t)
target_metadata = metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
        include_schemas=True,
        render_as_batch=True,
        # Only add, never drop
        process_revision_directives=lambda context, revision, directives: _prevent_drop_ops(directives)
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            include_schemas=True,
            render_as_batch=True,
            # Only add, never drop
            process_revision_directives=lambda context, revision, directives: _prevent_drop_ops(directives)
        )

        with context.begin_transaction():
            context.run_migrations()

def _prevent_drop_ops(directives):
    from alembic.operations.ops import DropTableOp, DropColumnOp, DropConstraintOp, DropIndexOp
    script = directives[0]
    new_upgrade_ops = []
    for op in script.upgrade_ops.ops:
        if not isinstance(op, (DropTableOp, DropColumnOp, DropConstraintOp, DropIndexOp)):
            new_upgrade_ops.append(op)
    script.upgrade_ops.ops = new_upgrade_ops


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
