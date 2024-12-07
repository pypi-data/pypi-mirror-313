def add_migration(migration_func, cls, from_version):
    try:
        assert cls.__dict__["_validate_version"]
    except KeyError:
        raise ValueError(
            "Cannot add migration to un-versioned object. To version, add a '_validate_version: bool = True' attribute."
        )

    # Add migration to class
    _vobj__migrations = cls._vobj__migrations.copy()
    _vobj__migrations.append((from_version, migration_func, cls))

    # Sort by migration version
    cls._vobj__migrations = sorted(_vobj__migrations)


def migration(cls, from_version):
    """
    Decorator for adding a migration function to an object class. Use this
    decorator on any function or method that should be used for migrating an
    object from one version to another. This is an equivalent alternative to the
    versionedobject.object.add_migration function.

    :param cls: Class object to add migration to
    :param from_version: Version to migrate from. If you are migrating an object that\
        previously had no version number, use 'None' here.
    :param to_version: Version to migrate to
    """

    def _inner_migration(migration_func):
        add_migration(migration_func, cls, from_version)

    return _inner_migration


# @migration(JobStepConfig, "0.0.0")
# def passthrough_sample_migration(values: Dict[str, Any]) -> Dict[str, Any]:
#     return values
