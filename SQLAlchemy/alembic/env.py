import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig

from conf.db import engine
from conf.models import Base

# Настройка объекта конфигурации Alembic для доступа к значениям из .ini файла (Alembic Config object for accessing .ini file values)
config = context.config

# Настройка логирования с использованием параметров из файла конфигурации (Setting up logging using config file settings)
fileConfig(config.config_file_name)

# Поддержка автогенерации миграций (Autogenerate support)
target_metadata = Base.metadata


def run_migrations_offline():
    """
    Запуск миграций в 'offline' режиме (Running migrations in 'offline' mode)
    Используется только URL для подключения (Using only the URL for connection)
    Все команды миграции будут выполнены как SQL-запросы (All migration commands will be executed as SQL queries)
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """
    Запуск миграций в 'online' режиме (Running migrations in 'online' mode)
    Создается Engine и устанавливается соединение с базой данных (Creating an Engine and establishing a connection to the database)
    Все команды миграции будут выполнены через это соединение (All migration commands will be executed through this connection)
    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url"))

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# Определение режима миграции: offline или online (Determining migration mode: offline or online)
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()


