"""importer helper for pyquiri"""

try:
    from . import pyquiri
except ImportError as err:
    raise ImportError(
        "could not import pyquiri"
    ) from err
