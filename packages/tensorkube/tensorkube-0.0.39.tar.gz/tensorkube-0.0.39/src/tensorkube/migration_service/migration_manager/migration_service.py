import importlib.metadata
from importlib import resources
from typing import Optional

import click
from kubernetes import config, client
from tensorkube.services.k8s_service import get_tensorkube_cluster_context_name


def get_current_tensorkube_version():
    return importlib.metadata.version('tensorkube')


def version_to_tuple(version_str):
    # Split the version string by '.' and convert each component to an integer
    return tuple(map(int, version_str.split('.')))


def set_current_cli_version_to_cluster(context_name: Optional[str] = None):
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)
    v1 = client.CoreV1Api(k8s_api_client)
    config_map = client.V1ConfigMap(metadata=client.V1ObjectMeta(name="tensorkube-migration", namespace="default"),
                                    data={"version": get_current_tensorkube_version()})
    try:
        v1.replace_namespaced_config_map("tensorkube-migration", "default", config_map)
    except client.exceptions.ApiException as e:
        if e.status == 404:
            v1.create_namespaced_config_map("default", config_map)
        else:
            raise e


def get_cluster_tensorkube_version(context_name: Optional[str] = None):
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)
    v1 = client.CoreV1Api(k8s_api_client)
    try:
        config_map = v1.read_namespaced_config_map("tensorkube-migration", "default")
        return config_map.data['version']
    except client.exceptions.ApiException as e:
        if e.status == 404:
            return None
        else:
            raise e


def load_migrations():
    # Get a reference to the migrations directory
    migrations_dir = resources.files('tensorkube.migration_service').joinpath('migrations')

    # List all Python files in the directory, excluding __init__.py
    migration_files = [f.name for f in migrations_dir.iterdir() if f.name.endswith('.py') and f.name != '__init__.py']

    # Sort migrations based on the leading numbers in the filenames
    migrations = sorted(migration_files, key=lambda x: tuple(map(int, x.split('_')[:3])))

    cluster_tensorkube_version = get_cluster_tensorkube_version()
    click.echo(f"Cluster TensorKube version: {cluster_tensorkube_version}")
    if cluster_tensorkube_version is None:
        cluster_tensorkube_version = '0.0.0'

    migrations = filter(lambda migration: tuple(map(int, migration.split('_')[:3])) > version_to_tuple(cluster_tensorkube_version),
        migrations)

    return [migration.replace('.py', '') for migration in migrations]


def apply_migration(migration_name):
    # Adjust the module path to reflect the structure starting from the project root
    migration_module_path = f"tensorkube.migration_service.migrations.{migration_name}"
    migration_module = importlib.import_module(migration_module_path)
    migration_module.apply()


def migrate_tensorkube():
    migrations = load_migrations()
    for migration in migrations:
        click.echo(f"Applying migration {migration}...")
        apply_migration(migration)
    set_current_cli_version_to_cluster()
    click.echo("Migration completed successfully.")

def test_mig():
    migrations = load_migrations()[0]
    migration_module_path = f"tensorkube.migration_service.migrations.{migrations}"
    migration_module = importlib.import_module(migration_module_path)
    migration_module.test_migration()
