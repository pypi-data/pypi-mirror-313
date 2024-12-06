import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def read_resource_file(package, resource):
    try:
        # For Python 3.9 and later
        from importlib.resources import files
        resource_path = files(package) / resource
        with open(resource_path, encoding='utf-8') as file:
            return file.read()
    except ImportError:
        try:
            # For Python 3.7 and 3.8
            from importlib.resources import path
            with path(package, resource) as resource_path:
                with open(resource_path, encoding='utf-8') as file:
                    return file.read()
        except ImportError:
            # Fallback for older Python versions without importlib.resources
            import pkg_resources
            resource_path = pkg_resources.resource_filename(package, resource)
            with open(resource_path, encoding='utf-8') as file:
                return file.read()
    raise ImportError("No compatible importlib.resources implementation found.")