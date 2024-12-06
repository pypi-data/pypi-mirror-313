__all__ = ['FSR_API_CONSTANTS',]


# -- IMPORTS --

# -- Standard libraries --
from enum import Enum

# -- 3rd party libraries --

# -- Internal libraries --


class FSR_API_CONSTANTS(Enum):
    """An enum to store FS Register API-level constants.

    Examples
    --------
    >>> FSR_API_CONSTANTS.BASEURL.value
    'https://register.fca.org.uk/services'
    >>> FSR_API_CONSTANTS.API_VERSION.value
    'V0.1'
    """

    BASEURL = 'https://register.fca.org.uk/services'
    API_VERSION = 'V0.1'
