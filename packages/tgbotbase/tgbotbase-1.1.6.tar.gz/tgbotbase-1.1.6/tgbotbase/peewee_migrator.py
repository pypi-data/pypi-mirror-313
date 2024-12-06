from typing import Union
from tgbotbase.utils import logger
from playhouse.migrate import PostgresqlMigrator, SqliteMigrator
from peewee import DatabaseProxy
# migrations = {
#     '0.0.1': {
#         Transaction: {
#             'tx_hash': {
#                 'method': 'add',
#                 'field': Transaction.tx_hash
#             },
#             'chain_id': {
#                 'method': 'add',
#                 'field': Transaction.chain_id
#             },
#             'yoo_id': {
#                 'method': 'drop',
#             },
#             'trx_ts': {
#                 'method': 'rename',
#                 'new_name': 'payment_id',
#             }
#         }
#     }
# }
def migrate(migrator: Union[PostgresqlMigrator, SqliteMigrator], db: DatabaseProxy, migrations: dict):
    """
    Example:
    ```python
    from tgbotbase.peewee_migrator import migrate
    # db = DatabaseProxy() // Any database
    migrator = PostgresqlMigrator(db) # migrator for your type of database

    migrations = {
        '0.0.1': {
            Transaction: {
                'tx_hash': {
                    'method': 'add',
                    'field': Transaction.tx_hash
                },
                'chain_id': {
                    'method': 'add',
                    'field': Transaction.chain_id
                },
                'yoo_id': {
                    'method': 'drop',
                },
                'trx_ts': {
                    'method': 'rename',
                    'new_name': 'payment_id',
                }
            }
        }
    }

    ```

    migrate(migrator, db, migrations)
    """
    for m_ver, migration in migrations.items():
        logger.warning(f"Found migration v{m_ver}")
        ops = []

        for model, data in migration.items():
            for column_name, mig_data in data.items():
                
                match mig_data["method"]:
                    case "add":
                        try:
                            model.select(mig_data["field"]).execute()
                        except Exception as e:
                            if 'does not exist' in str(e) or 'no such column' in str(e):
                                ops.append(migrator.add_column(model._meta.table_name, column_name, mig_data["field"]))
                            else:
                                logger.error(f"[{mig_data['method']}] Migration error: {e}")
                    case "drop":
                        try:
                            cols = [x.name for x in db.get_columns(model._meta.table_name)]
                            if column_name in cols:
                                ops.append(migrator.drop_column(model._meta.table_name, column_name))
                            else:
                                logger.error(f"[{mig_data['method']}] Migration error: Column {column_name} does not exist")
                        except Exception as e:
                            logger.error(f"[{mig_data['method']}] Migration error: {e}")

                    case "rename":
                        try:
                            cols = [x.name for x in db.get_columns(model._meta.table_name)]
                            if column_name in cols:
                                ops.append(migrator.rename_column(
                                    model._meta.table_name, 
                                    column_name,
                                    mig_data["new_name"]
                                ))
                            else:
                                logger.error(f"[{mig_data['method']}] Migration error: Column {column_name} does not exist")
                        
                        except Exception as e:
                            logger.error(f"[{mig_data['method']}] Migration error: {e}")

                    case "alter":
                        if isinstance(migrator, SqliteMigrator):
                            logger.warning(f"[{mig_data['method']}] SqliteMigrator -> Skipping migration for {model} to {mig_data['field']}")
                            continue

                        try:
                            cols = [x.name for x in db.get_columns(model._meta.table_name)]
                            if column_name.split('::')[0] in cols:
                                ops.append(migrator.alter_column_type(model._meta.table_name, column_name, mig_data["field"]))
                            else:
                                logger.error(f"[{mig_data['method']}] Migration error: Column {column_name} does not exist")
                        except Exception as e:
                            logger.error(f"[{mig_data['method']}] Migration error: {e}")

        if ops:
            logger.success("Migrated with ops:\n" + '\n'.join([f'{op.migrator}, {op.method}, {op.args}, {op.kwargs}' for op in ops]))
            migrate(*ops)
        else:
            logger.debug("Migration was already completed")
