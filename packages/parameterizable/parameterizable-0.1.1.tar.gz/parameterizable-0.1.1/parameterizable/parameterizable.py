""" Module for parameterizable classes.

This module provides the functionality for work with parameterizable classes:
classes that have (hyper) parameters which define object's configuration,
but not its internal contents or data. Such parameters are typically
passed to the .__init__() method.
"""



from typing import Any

CLASSNAME_METAPARAM_KEY = "__class__.__name__"

_known_parameterizable_classes = dict()


class ParameterizableClass:
    """ Base class for parameterizable classes.

    This class provides the basic functionality for parameterizable classes:
    classes that have (hyper) parameters which define object's configuration,
    and which are typically passed to the .__init__() method.
    The class provides an API for getting parameters' values from an object,
    and for converting the parameters to and from a dictionary.

    This class is not meant to be used directly, but to be subclassed
    by classes that need to be parameterizable.
    """
    def __init__(self):
        register_parameterizable_class(self)

    def __get_metaparams__(self) -> dict[str, Any]:
        """ Get the meta-parameters of the object as a dictionary.

        Meta-parameters are the parameters that define the object's
        configuration (but not its internal contents or data)
        plus information about its type.
        """
        metaparams = self.get_params()
        metaparams[CLASSNAME_METAPARAM_KEY] = self.__class__.__name__
        return metaparams

    @classmethod
    def __get_default_metaparams__(cls) -> dict[str, Any]:
        """ Get the default meta-parameters of the class as a dictionary.

        Default meta-parameters are the values that are used to
        configure an object if no arguments are explicitly passed
        to the .__init__() method, plus information about the object's type.
        """
        metaparams = cls().__get_metaparams__()
        return metaparams

    def get_params(self) -> dict[str, Any]:
        """ Get the parameters of the object as a dictionary.

        These parameters define the object's configuration,
        but not its internal contents or data. They are typically passed
        to the .__init__() method of the object at the time of its creation.
        """
        params = dict()
        return params

    @classmethod
    def get_default_params(cls) -> dict[str, Any]:
        """ Get the default parameters of the class as a dictionary.

        Default parameters are the values that are used to
        configure an object if no arguments are explicitly passed to
        the .__init__() method.
        """
        params = cls().get_params()
        return params


def get_object_from_metaparams(metaparams: dict[str, Any]) -> Any:
    """ Create an object from a dictionary of meta-parameters.

    This function creates an object from a dictionary of meta-parameters.
    The meta-parameters should have been created by the .__get_metaparams__()
    method of a ParameterizableClass object.
    """
    assert isinstance(metaparams, dict)
    assert CLASSNAME_METAPARAM_KEY in metaparams
    params = dict()
    class_name = metaparams[CLASSNAME_METAPARAM_KEY]
    object_class = _known_parameterizable_classes[class_name]
    for key, value in metaparams.items():
        if "." in key:
            continue
        if isinstance(value, dict) and CLASSNAME_METAPARAM_KEY in value:
            params[key] = get_object_from_metaparams(value)
        else:
            params[key] = value
    object = object_class(**params)
    return object


def get_params_from_metaparams(metaparams: dict[str, Any]) -> dict[str, Any]:
    """ Get the parameters from a dictionary of meta-parameters.

    This function extracts the parameters from a dictionary of meta-parameters.
    The meta-parameters should have been created by the .__get_metaparams__()
    method of a ParameterizableClass object. This function simply removes the
    information about objects' types from the input dictionary.
    """
    assert isinstance(metaparams, dict)
    params = dict()
    for key, value in metaparams.items():
        assert isinstance(key, str)
        if "." in key:
            continue
        if isinstance(value,dict):
            params[key] = get_params_from_metaparams(value)
        else:
            params[key] = value
    return params


def is_parameterizable(cls: Any) -> bool:
    """ Check if a class is parameterizable.

    This function checks if a class is parameterizable, i.e. if it has
    the necessary methods to get and set parameters.

    The easiest way to make a class parameterizable is to subclass
    the ParameterizableClass class.
    """
    if not type(cls) == type:
        return False
    if not hasattr(cls, "__get_metaparams__"):
        return False
    if not callable(cls.__get_metaparams__):
        return False
    if not hasattr(cls, "get_params"):
        return False
    if not callable(cls.get_params):
        return False
    if not hasattr(cls, "__get_default_metaparams__"):
        return False
    if not callable(cls.__get_default_metaparams__):
        return False
    if not hasattr(cls, "get_default_params"):
        return False
    if not callable(cls.get_default_params):
        return False
    return True


def _smoketest_parameterizable_class(cls: Any):
    """ Run a smoketest on a parameterizable class.

    This function runs a basic unit test on a parameterizable class.
    """
    assert is_parameterizable(cls)
    default_params = cls().get_default_params()
    params = cls().get_params()
    assert isinstance(default_params, dict)
    assert isinstance(params, dict)
    assert default_params == params
    return True


def _smoketest_known_parameterizable_classes():
    """ Run a smoketest on all known parameterizable classes.

    This function runs a basic unit test on all known parameterizable classes.
    """
    for class_name, cls in _known_parameterizable_classes.items():
        _smoketest_parameterizable_class(cls)


def register_parameterizable_class(obj: Any):
    """ Register a parameterizable class.

    This function registers a parameterizable class so that it can be
    used with the get_object_from_metaparams()
    """
    if (obj.__name__ in _known_parameterizable_classes
            and _known_parameterizable_classes[obj.__name__] == obj):
        return
    elif not is_parameterizable(obj):
        raise ValueError("Object is not parameterizable")

    _known_parameterizable_classes[obj.__name__] = obj