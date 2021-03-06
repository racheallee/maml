"""
Utilities to serialize and deserialize maml object
"""
import pickle
from typing import Any


def serialize_maml_object(instance):
    """
    Serialize maml objects
    Args:
        instance (maml object): object to serialize

    Returns:
        for object that has `get_config` method, return the dictionary after `get_config`,
        otherwise return str name.

    """
    if instance is None:
        return None
    if hasattr(instance, 'get_config'):
        return {
            'class_name': instance.__class__.__name__,
            'config': instance.get_config()
        }
    if hasattr(instance, '__name__'):
        return instance.__name__
    else:
        raise ValueError('Cannot serialize', instance)


def deserialize_maml_object(identifier, module_objects=None,
                            printable_module_name='object'):
    """
    Deserialize maml object from dict, str or callable

    Args:
        identifier (dict, str): the identifier to deserialize
        module_objects (dict): objects in the module
        printable_module_name (str): name for print

    Returns:
        deserialized maml object

    """
    if isinstance(identifier, dict):
        # dealing with configuration dictionary
        config = identifier
        if 'class_name' not in config or 'config' not in config:
            raise ValueError('Improper config format: ' + str(config))
        class_name = config['class_name']
        module_objects = module_objects or {}
        cls = module_objects.get(class_name)
        if cls is None:
            raise ValueError('Unknown ' + printable_module_name +
                             ': ' + class_name)
        return cls(**config['config'])

    elif isinstance(identifier, str):
        function_name = identifier
        fn = module_objects.get(function_name)
        if fn is None:
            raise ValueError('Unknown ' + printable_module_name +
                             ':' + function_name)
        return fn


def load_pickle(filename: str) -> Any:
    """
    Load pickled file to objection

    Args:
        filename: filename

    Returns: obj

    """
    with open(filename, 'rb') as f:
        return pickle.load(f)


def to_pickle(obj: Any, filename: str) -> None:
    """
    Dump picklable object to file

    Args:
        obj: object
        filename: file name

    """
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)
