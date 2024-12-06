from numpydantic.interface.hdf5 import H5ArrayPath
from numpydantic.interface.hdf5 import H5Proxy
from numpy import ndarray as Numpyndarray
import typing
import pathlib
NDArray = H5ArrayPath | typing.Tuple[typing.Union[pathlib.Path, str], str] | H5Proxy | Numpyndarray