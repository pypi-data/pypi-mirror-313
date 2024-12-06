"""
pybind bla
"""
from __future__ import annotations
import numpy
import typing
__all__ = ['CheckPerformance', 'FlatMatrixC', 'FlatMatrixD', 'FlatVectorC', 'FlatVectorD', 'InnerProduct', 'Mat2C', 'Mat2D', 'Mat3C', 'Mat3D', 'Matrix', 'MatrixC', 'MatrixD', 'Norm', 'SliceVectorC', 'SliceVectorD', 'SparseVector', 'Vec1D', 'Vec2D', 'Vec3D', 'Vector', 'VectorC', 'VectorD']
class FlatMatrixC:
    @typing.overload
    def Height(self) -> int:
        """
        Return height of matrix
        """
    @typing.overload
    def Height(self) -> int:
        """
        Returns height of the matrix
        """
    def Identity(self) -> ...:
        ...
    def Norm(self) -> float:
        """
        Returns L2-norm
        """
    def NumPy(self) -> typing.Any:
        """
        Return NumPy object
        """
    @typing.overload
    def Width(self) -> int:
        """
        Return width of matrix
        """
    @typing.overload
    def Width(self) -> int:
        """
        Returns width of the matrix
        """
    @typing.overload
    def __add__(self, mat: FlatMatrixC) -> ...:
        ...
    @typing.overload
    def __add__(self, mat: FlatMatrixD) -> ...:
        ...
    def __buffer__(self, flags):
        """
        Return a buffer object that exposes the underlying memory of the object.
        """
    @typing.overload
    def __getitem__(self, arg0: tuple) -> typing.Any:
        ...
    @typing.overload
    def __getitem__(self, arg0: int) -> VectorC:
        ...
    @typing.overload
    def __getitem__(self, arg0: slice) -> ...:
        ...
    def __iadd__(self, arg0: FlatMatrixC) -> FlatMatrixC:
        ...
    def __imul__(self, arg0: complex) -> FlatMatrixC:
        ...
    def __isub__(self, arg0: FlatMatrixC) -> ...:
        ...
    @typing.overload
    def __len__(self) -> int:
        """
        Return height of matrix
        """
    @typing.overload
    def __len__(self) -> int:
        ...
    @typing.overload
    def __mul__(self, mat: FlatMatrixC) -> ...:
        ...
    @typing.overload
    def __mul__(self, vec: FlatVectorC) -> VectorC:
        ...
    @typing.overload
    def __mul__(self, values: complex) -> ...:
        ...
    @typing.overload
    def __mul__(self, mat: FlatMatrixD) -> ...:
        ...
    @typing.overload
    def __mul__(self, vec: FlatVectorD) -> VectorC:
        ...
    @typing.overload
    def __mul__(self, value: float) -> ...:
        ...
    def __neg__(self) -> ...:
        ...
    def __radd__(self, mat: FlatMatrixD) -> ...:
        ...
    def __release_buffer__(self, buffer):
        """
        Release the buffer object that exposes the underlying memory of the object.
        """
    def __repr__(self) -> str:
        ...
    @typing.overload
    def __rmul__(self, value: complex) -> ...:
        ...
    @typing.overload
    def __rmul__(self, mat: FlatMatrixD) -> ...:
        ...
    @typing.overload
    def __rmul__(self, value: float) -> ...:
        ...
    def __rsub__(self, mat: FlatMatrixD) -> ...:
        ...
    @typing.overload
    def __setitem__(self, arg0: tuple, arg1: FlatMatrixC) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: tuple, arg1: complex) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: tuple, arg1: FlatVectorC) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: int, arg1: VectorC) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: int, arg1: complex) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: FlatMatrixC) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: complex) -> None:
        ...
    def __str__(self) -> str:
        ...
    @typing.overload
    def __sub__(self, mat: FlatMatrixC) -> ...:
        ...
    @typing.overload
    def __sub__(self, mat: FlatMatrixD) -> ...:
        ...
    @property
    def A(self) -> VectorC:
        """
        Returns matrix as vector
        """
    @property
    def C(self) -> ...:
        """
        Return conjugate matrix
        """
    @property
    def H(self) -> ...:
        """
        Return conjugate and transposed matrix
        """
    @property
    def I(self) -> ...:
        ...
    @property
    def T(self) -> ...:
        """
        Return transpose of matrix
        """
    @property
    def diag(self) -> VectorC:
        ...
    @diag.setter
    def diag(self, arg1: FlatVectorC) -> None:
        ...
    @property
    def h(self) -> int:
        """
        Height of the matrix
        """
    @property
    def shape(self) -> tuple[int, int]:
        """
        Shape of the matrix
        """
    @property
    def w(self) -> int:
        """
        Width of the matrix
        """
class FlatMatrixD:
    def Height(self) -> int:
        """
        Return height of matrix
        """
    def Identity(self) -> ...:
        ...
    def Inverse(self, arg0: FlatMatrixD) -> None:
        ...
    def Norm(self) -> float:
        """
        Returns L2-norm
        """
    def NumPy(self) -> typing.Any:
        """
        Return NumPy object
        """
    def Width(self) -> int:
        """
        Return width of matrix
        """
    def __add__(self, mat: FlatMatrixD) -> ...:
        ...
    def __buffer__(self, flags):
        """
        Return a buffer object that exposes the underlying memory of the object.
        """
    @typing.overload
    def __getitem__(self, arg0: tuple) -> typing.Any:
        ...
    @typing.overload
    def __getitem__(self, arg0: int) -> VectorD:
        ...
    @typing.overload
    def __getitem__(self, arg0: slice) -> ...:
        ...
    def __iadd__(self, arg0: FlatMatrixD) -> FlatMatrixD:
        ...
    def __imul__(self, arg0: float) -> FlatMatrixD:
        ...
    def __isub__(self, arg0: FlatMatrixD) -> ...:
        ...
    def __len__(self) -> int:
        """
        Return height of matrix
        """
    @typing.overload
    def __mul__(self, mat: FlatMatrixD) -> ...:
        ...
    @typing.overload
    def __mul__(self, vec: FlatVectorD) -> VectorD:
        ...
    @typing.overload
    def __mul__(self, values: float) -> ...:
        ...
    def __neg__(self) -> ...:
        ...
    def __release_buffer__(self, buffer):
        """
        Release the buffer object that exposes the underlying memory of the object.
        """
    def __repr__(self) -> str:
        ...
    def __rmul__(self, value: float) -> ...:
        ...
    @typing.overload
    def __setitem__(self, arg0: tuple, arg1: FlatMatrixD) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: tuple, arg1: float) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: tuple, arg1: FlatVectorD) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: int, arg1: VectorD) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: int, arg1: float) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: FlatMatrixD) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: float) -> None:
        ...
    def __str__(self) -> str:
        ...
    def __sub__(self, mat: FlatMatrixD) -> ...:
        ...
    @property
    def A(self) -> VectorD:
        """
        Returns matrix as vector
        """
    @A.setter
    def A(self, arg1: VectorD) -> None:
        ...
    @property
    def C(self) -> ...:
        """
        return conjugate of matrix
        """
    @property
    def H(self) -> ...:
        """
        return transpose of matrix
        """
    @property
    def I(self) -> ...:
        ...
    @property
    def T(self) -> ...:
        """
        return transpose of matrix
        """
    @property
    def diag(self) -> VectorD:
        ...
    @diag.setter
    def diag(self, arg1: FlatVectorD) -> None:
        ...
    @property
    def h(self) -> int:
        """
        Height of the matrix
        """
    @property
    def shape(self) -> tuple[int, int]:
        """
        Shape of the matrix
        """
    @property
    def w(self) -> int:
        """
        Width of the matrix
        """
class FlatVectorC:
    def Get(self, pos: int) -> complex:
        """
        Return value at given position
        """
    def InnerProduct(self, y: FlatVectorC, conjugate: bool = True) -> complex:
        """
        Returns InnerProduct with other object
        """
    def Norm(self) -> float:
        """
        Returns L2-norm
        """
    def NumPy(self) -> typing.Any:
        """
        Return NumPy object
        """
    def Range(self, arg0: int, arg1: int) -> FlatVectorC:
        ...
    def Set(self, pos: int, value: complex) -> None:
        """
        Set value at given position
        """
    def __add__(self, vec: FlatVectorC) -> ...:
        ...
    def __buffer__(self, flags):
        """
        Return a buffer object that exposes the underlying memory of the object.
        """
    @typing.overload
    def __getitem__(self, pos: int) -> complex:
        """
        Return value at given position
        """
    @typing.overload
    def __getitem__(self, inds: slice) -> ...:
        """
        Return values at given positions
        """
    @typing.overload
    def __getitem__(self, ind: list) -> ...:
        """
        Return values at given positions
        """
    def __iadd__(self, arg0: FlatVectorC) -> FlatVectorC:
        ...
    @typing.overload
    def __imul__(self, arg0: complex) -> FlatVectorC:
        ...
    @typing.overload
    def __imul__(self, arg0: float) -> FlatVectorC:
        ...
    def __init__(self, arg0: int, arg1: complex) -> None:
        ...
    def __isub__(self, arg0: FlatVectorC) -> ...:
        ...
    def __iter__(self) -> typing.Iterator[complex]:
        ...
    def __len__(self) -> int:
        """
        Return length of the array
        """
    def __mul__(self, value: complex) -> ...:
        ...
    def __neg__(self) -> ...:
        ...
    def __release_buffer__(self, buffer):
        """
        Release the buffer object that exposes the underlying memory of the object.
        """
    def __repr__(self) -> str:
        ...
    def __rmul__(self, value: complex) -> ...:
        ...
    @typing.overload
    def __setitem__(self, pos: int, value: complex) -> None:
        """
        Set value at given position
        """
    @typing.overload
    def __setitem__(self, inds: slice, rv: FlatVectorC) -> None:
        """
        Set values at given positions
        """
    @typing.overload
    def __setitem__(self, inds: slice, value: complex) -> None:
        """
        Set value at given positions
        """
    @typing.overload
    def __setitem__(self, inds: slice, value: numpy.ndarray[numpy.complex128]) -> None:
        """
        Set value at given positions
        """
    def __str__(self) -> str:
        ...
    def __sub__(self, vec: FlatVectorC) -> ...:
        ...
    @property
    def imag(self) -> ...:
        ...
    @imag.setter
    def imag(self, arg1: float) -> None:
        ...
    @property
    def real(self) -> ...:
        ...
    @real.setter
    def real(self, arg1: float) -> None:
        ...
class FlatVectorD:
    def Get(self, pos: int) -> float:
        """
        Return value at given position
        """
    def InnerProduct(self, y: FlatVectorD, conjugate: bool = True) -> float:
        """
        Returns InnerProduct with other object
        """
    def MinMax(self, ignore_inf: bool = False) -> tuple[float, float]:
        ...
    def Norm(self) -> float:
        """
        Returns L2-norm
        """
    def NumPy(self) -> typing.Any:
        """
        Return NumPy object
        """
    def Range(self, arg0: int, arg1: int) -> FlatVectorD:
        ...
    def Set(self, pos: int, value: float) -> None:
        """
        Set value at given position
        """
    def __add__(self, vec: FlatVectorD) -> ...:
        ...
    def __buffer__(self, flags):
        """
        Return a buffer object that exposes the underlying memory of the object.
        """
    @typing.overload
    def __getitem__(self, pos: int) -> float:
        """
        Return value at given position
        """
    @typing.overload
    def __getitem__(self, inds: slice) -> ...:
        """
        Return values at given positions
        """
    @typing.overload
    def __getitem__(self, ind: list) -> ...:
        """
        Return values at given positions
        """
    def __iadd__(self, arg0: FlatVectorD) -> FlatVectorD:
        ...
    def __imul__(self, arg0: float) -> FlatVectorD:
        ...
    def __init__(self, arg0: int, arg1: float) -> None:
        ...
    def __isub__(self, arg0: FlatVectorD) -> ...:
        ...
    def __iter__(self) -> typing.Iterator[float]:
        ...
    def __len__(self) -> int:
        """
        Return length of the array
        """
    def __mul__(self, value: float) -> ...:
        ...
    def __neg__(self) -> ...:
        ...
    def __release_buffer__(self, buffer):
        """
        Release the buffer object that exposes the underlying memory of the object.
        """
    def __repr__(self) -> str:
        ...
    def __rmul__(self, value: float) -> ...:
        ...
    @typing.overload
    def __setitem__(self, pos: int, value: float) -> None:
        """
        Set value at given position
        """
    @typing.overload
    def __setitem__(self, inds: slice, rv: FlatVectorD) -> None:
        """
        Set values at given positions
        """
    @typing.overload
    def __setitem__(self, inds: slice, value: float) -> None:
        """
        Set value at given positions
        """
    @typing.overload
    def __setitem__(self, inds: slice, value: numpy.ndarray[numpy.float64]) -> None:
        """
        Set value at given positions
        """
    def __str__(self) -> str:
        ...
    def __sub__(self, vec: FlatVectorD) -> ...:
        ...
class Mat2C:
    def NumPy(self) -> typing.Any:
        """
        Return NumPy object
        """
    def __buffer__(self, flags):
        """
        Return a buffer object that exposes the underlying memory of the object.
        """
    def __getitem__(self, arg0: tuple) -> complex:
        ...
    def __release_buffer__(self, buffer):
        """
        Release the buffer object that exposes the underlying memory of the object.
        """
class Mat2D:
    def NumPy(self) -> typing.Any:
        """
        Return NumPy object
        """
    def __buffer__(self, flags):
        """
        Return a buffer object that exposes the underlying memory of the object.
        """
    def __getitem__(self, arg0: tuple) -> float:
        ...
    def __release_buffer__(self, buffer):
        """
        Release the buffer object that exposes the underlying memory of the object.
        """
class Mat3C:
    def NumPy(self) -> typing.Any:
        """
        Return NumPy object
        """
    def __buffer__(self, flags):
        """
        Return a buffer object that exposes the underlying memory of the object.
        """
    def __getitem__(self, arg0: tuple) -> complex:
        ...
    def __release_buffer__(self, buffer):
        """
        Release the buffer object that exposes the underlying memory of the object.
        """
class Mat3D:
    def NumPy(self) -> typing.Any:
        """
        Return NumPy object
        """
    def __buffer__(self, flags):
        """
        Return a buffer object that exposes the underlying memory of the object.
        """
    def __getitem__(self, arg0: tuple) -> float:
        ...
    def __release_buffer__(self, buffer):
        """
        Release the buffer object that exposes the underlying memory of the object.
        """
class MatrixC(FlatMatrixC):
    def NumPy(self) -> typing.Any:
        """
        Return NumPy object
        """
    def __buffer__(self, flags):
        """
        Return a buffer object that exposes the underlying memory of the object.
        """
    def __iadd__(self, arg0: MatrixC) -> MatrixC:
        ...
    def __imul__(self, arg0: complex) -> MatrixC:
        ...
    def __init__(self, n: int, m: int) -> None:
        """
        Makes matrix of dimension n x m
        """
    def __isub__(self, arg0: MatrixC) -> MatrixC:
        ...
    def __release_buffer__(self, buffer):
        """
        Release the buffer object that exposes the underlying memory of the object.
        """
class MatrixD(FlatMatrixD):
    def NumPy(self) -> typing.Any:
        """
        Return NumPy object
        """
    def __buffer__(self, flags):
        """
        Return a buffer object that exposes the underlying memory of the object.
        """
    def __iadd__(self, arg0: MatrixD) -> MatrixD:
        ...
    def __imul__(self, arg0: float) -> MatrixD:
        ...
    def __init__(self, n: int, m: int) -> None:
        """
        Makes matrix of dimension n x m
        """
    def __isub__(self, arg0: MatrixD) -> MatrixD:
        ...
    def __release_buffer__(self, buffer):
        """
        Release the buffer object that exposes the underlying memory of the object.
        """
class SliceVectorC:
    def Get(self, pos: int) -> complex:
        """
        Return value at given position
        """
    def InnerProduct(self, y: SliceVectorC, conjugate: bool = True) -> complex:
        """
        Returns InnerProduct with other object
        """
    def Norm(self) -> float:
        """
        Returns L2-norm
        """
    def NumPy(self) -> typing.Any:
        """
        Return NumPy object
        """
    def Range(self, arg0: int, arg1: int) -> SliceVectorC:
        ...
    def Set(self, pos: int, value: complex) -> None:
        """
        Set value at given position
        """
    def __add__(self, vec: SliceVectorC) -> ...:
        ...
    def __buffer__(self, flags):
        """
        Return a buffer object that exposes the underlying memory of the object.
        """
    @typing.overload
    def __getitem__(self, pos: int) -> complex:
        """
        Return value at given position
        """
    @typing.overload
    def __getitem__(self, inds: slice) -> ...:
        """
        Return values at given positions
        """
    @typing.overload
    def __getitem__(self, ind: list) -> ...:
        """
        Return values at given positions
        """
    def __iadd__(self, arg0: SliceVectorC) -> SliceVectorC:
        ...
    @typing.overload
    def __imul__(self, arg0: complex) -> SliceVectorC:
        ...
    @typing.overload
    def __imul__(self, arg0: float) -> SliceVectorC:
        ...
    def __isub__(self, arg0: SliceVectorC) -> ...:
        ...
    def __iter__(self) -> typing.Iterator[complex]:
        ...
    def __len__(self) -> int:
        """
        Return length of the array
        """
    def __mul__(self, value: complex) -> ...:
        ...
    def __neg__(self) -> ...:
        ...
    def __release_buffer__(self, buffer):
        """
        Release the buffer object that exposes the underlying memory of the object.
        """
    def __repr__(self) -> str:
        ...
    def __rmul__(self, value: complex) -> ...:
        ...
    @typing.overload
    def __setitem__(self, pos: int, value: complex) -> None:
        """
        Set value at given position
        """
    @typing.overload
    def __setitem__(self, inds: slice, rv: SliceVectorC) -> None:
        """
        Set values at given positions
        """
    @typing.overload
    def __setitem__(self, inds: slice, value: complex) -> None:
        """
        Set value at given positions
        """
    @typing.overload
    def __setitem__(self, inds: slice, value: numpy.ndarray[numpy.complex128]) -> None:
        """
        Set value at given positions
        """
    def __str__(self) -> str:
        ...
    def __sub__(self, vec: SliceVectorC) -> ...:
        ...
class SliceVectorD:
    def Get(self, pos: int) -> float:
        """
        Return value at given position
        """
    def InnerProduct(self, y: SliceVectorD, conjugate: bool = True) -> float:
        """
        Returns InnerProduct with other object
        """
    def MinMax(self, ignore_inf: bool = False) -> tuple[float, float]:
        ...
    def Norm(self) -> float:
        """
        Returns L2-norm
        """
    def NumPy(self) -> typing.Any:
        """
        Return NumPy object
        """
    def Range(self, arg0: int, arg1: int) -> SliceVectorD:
        ...
    def Set(self, pos: int, value: float) -> None:
        """
        Set value at given position
        """
    def __add__(self, vec: SliceVectorD) -> ...:
        ...
    def __buffer__(self, flags):
        """
        Return a buffer object that exposes the underlying memory of the object.
        """
    @typing.overload
    def __getitem__(self, pos: int) -> float:
        """
        Return value at given position
        """
    @typing.overload
    def __getitem__(self, inds: slice) -> ...:
        """
        Return values at given positions
        """
    @typing.overload
    def __getitem__(self, ind: list) -> ...:
        """
        Return values at given positions
        """
    def __iadd__(self, arg0: SliceVectorD) -> SliceVectorD:
        ...
    def __imul__(self, arg0: float) -> SliceVectorD:
        ...
    def __init__(self, arg0: FlatVectorD) -> None:
        ...
    def __isub__(self, arg0: SliceVectorD) -> ...:
        ...
    def __iter__(self) -> typing.Iterator[float]:
        ...
    def __len__(self) -> int:
        """
        Return length of the array
        """
    def __mul__(self, value: float) -> ...:
        ...
    def __neg__(self) -> ...:
        ...
    def __release_buffer__(self, buffer):
        """
        Release the buffer object that exposes the underlying memory of the object.
        """
    def __repr__(self) -> str:
        ...
    def __rmul__(self, value: float) -> ...:
        ...
    @typing.overload
    def __setitem__(self, pos: int, value: float) -> None:
        """
        Set value at given position
        """
    @typing.overload
    def __setitem__(self, inds: slice, rv: SliceVectorD) -> None:
        """
        Set values at given positions
        """
    @typing.overload
    def __setitem__(self, inds: slice, value: float) -> None:
        """
        Set value at given positions
        """
    @typing.overload
    def __setitem__(self, inds: slice, value: numpy.ndarray[numpy.float64]) -> None:
        """
        Set value at given positions
        """
    def __str__(self) -> str:
        ...
    def __sub__(self, vec: SliceVectorD) -> ...:
        ...
class SparseVector:
    def InnerProduct(self, arg0: FlatVectorD) -> float:
        ...
    def __getitem__(self, arg0: int) -> float:
        ...
    def __init__(self, arg0: int) -> None:
        ...
    def __setitem__(self, arg0: int, arg1: float) -> None:
        ...
    def __str__(self) -> str:
        ...
class Vec1D:
    def Get(self, pos: int) -> float:
        """
        Return value at given position
        """
    def InnerProduct(self, y: Vec1D, conjugate: bool = True) -> float:
        """
        Returns InnerProduct with other object
        """
    def Norm(self) -> float:
        """
        Returns L2-norm
        """
    def __add__(self, vec: Vec1D) -> Vec1D:
        ...
    @typing.overload
    def __getitem__(self, inds: slice) -> Vec1D:
        """
        Return values at given positions
        """
    @typing.overload
    def __getitem__(self, ind: list) -> Vec1D:
        """
        Return values at given positions
        """
    @typing.overload
    def __getitem__(self, pos: int) -> float:
        """
        Return value at given position
        """
    def __mul__(self, value: float) -> Vec1D:
        ...
    def __neg__(self) -> Vec1D:
        ...
    def __rmul__(self, value: float) -> Vec1D:
        ...
    @typing.overload
    def __setitem__(self, inds: slice, rv: Vec1D) -> None:
        """
        Set values at given positions
        """
    @typing.overload
    def __setitem__(self, inds: slice, value: float) -> None:
        """
        Set value at given positions
        """
    @typing.overload
    def __setitem__(self, inds: slice, value: numpy.ndarray[numpy.float64]) -> None:
        """
        Set value at given positions
        """
    def __sub__(self, vec: Vec1D) -> Vec1D:
        ...
class Vec2D:
    def Get(self, pos: int) -> float:
        """
        Return value at given position
        """
    def InnerProduct(self, y: Vec2D, conjugate: bool = True) -> float:
        """
        Returns InnerProduct with other object
        """
    def Norm(self) -> float:
        """
        Returns L2-norm
        """
    def __add__(self, vec: Vec2D) -> Vec2D:
        ...
    @typing.overload
    def __getitem__(self, inds: slice) -> Vec2D:
        """
        Return values at given positions
        """
    @typing.overload
    def __getitem__(self, ind: list) -> Vec2D:
        """
        Return values at given positions
        """
    @typing.overload
    def __getitem__(self, pos: int) -> float:
        """
        Return value at given position
        """
    def __init__(self, arg0: float, arg1: float) -> None:
        ...
    def __mul__(self, value: float) -> Vec2D:
        ...
    def __neg__(self) -> Vec2D:
        ...
    def __rmul__(self, value: float) -> Vec2D:
        ...
    @typing.overload
    def __setitem__(self, inds: slice, rv: Vec2D) -> None:
        """
        Set values at given positions
        """
    @typing.overload
    def __setitem__(self, inds: slice, value: float) -> None:
        """
        Set value at given positions
        """
    @typing.overload
    def __setitem__(self, inds: slice, value: numpy.ndarray[numpy.float64]) -> None:
        """
        Set value at given positions
        """
    def __sub__(self, vec: Vec2D) -> Vec2D:
        ...
class Vec3D:
    def Get(self, pos: int) -> float:
        """
        Return value at given position
        """
    def InnerProduct(self, y: Vec3D, conjugate: bool = True) -> float:
        """
        Returns InnerProduct with other object
        """
    def Norm(self) -> float:
        """
        Returns L2-norm
        """
    def __add__(self, vec: Vec3D) -> Vec3D:
        ...
    @typing.overload
    def __getitem__(self, inds: slice) -> Vec3D:
        """
        Return values at given positions
        """
    @typing.overload
    def __getitem__(self, ind: list) -> Vec3D:
        """
        Return values at given positions
        """
    @typing.overload
    def __getitem__(self, pos: int) -> float:
        """
        Return value at given position
        """
    def __init__(self, arg0: float, arg1: float, arg2: float) -> None:
        ...
    def __mul__(self, value: float) -> Vec3D:
        ...
    def __neg__(self) -> Vec3D:
        ...
    def __rmul__(self, value: float) -> Vec3D:
        ...
    @typing.overload
    def __setitem__(self, inds: slice, rv: Vec3D) -> None:
        """
        Set values at given positions
        """
    @typing.overload
    def __setitem__(self, inds: slice, value: float) -> None:
        """
        Set value at given positions
        """
    @typing.overload
    def __setitem__(self, inds: slice, value: numpy.ndarray[numpy.float64]) -> None:
        """
        Set value at given positions
        """
    def __sub__(self, vec: Vec3D) -> Vec3D:
        ...
class VectorC(FlatVectorC):
    def NumPy(self) -> typing.Any:
        """
        Return NumPy object
        """
    def __buffer__(self, flags):
        """
        Return a buffer object that exposes the underlying memory of the object.
        """
    def __iadd__(self, arg0: VectorC) -> VectorC:
        ...
    def __imul__(self, arg0: complex) -> VectorC:
        ...
    def __init__(self, arg0: int) -> None:
        ...
    def __isub__(self, arg0: VectorC) -> VectorC:
        ...
    def __release_buffer__(self, buffer):
        """
        Release the buffer object that exposes the underlying memory of the object.
        """
class VectorD(FlatVectorD):
    def NumPy(self) -> typing.Any:
        """
        Return NumPy object
        """
    def __buffer__(self, flags):
        """
        Return a buffer object that exposes the underlying memory of the object.
        """
    def __iadd__(self, arg0: VectorD) -> VectorD:
        ...
    def __imul__(self, arg0: float) -> VectorD:
        ...
    @typing.overload
    def __init__(self, arg0: SliceVectorD) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: int) -> None:
        ...
    def __isub__(self, arg0: VectorD) -> VectorD:
        ...
    def __release_buffer__(self, buffer):
        """
        Release the buffer object that exposes the underlying memory of the object.
        """
def CheckPerformance(n: int, m: int, k: int) -> None:
    ...
def InnerProduct(x: typing.Any, y: typing.Any, **kwargs) -> typing.Any:
    """
    Compute InnerProduct
    """
@typing.overload
def Matrix(height: int, width: int | None = None, complex: bool = False) -> typing.Any:
    """
    Creates a matrix of given height and width.
    
    Parameters:
    
    height : int
      input height
    
    width : int
      input width
    
    complex : bool
      input complex values
    """
@typing.overload
def Matrix(buffer: typing_extensions.Buffer, copy: bool = True) -> typing.Any:
    ...
@typing.overload
def Matrix(arg0: list[list[float]]) -> MatrixD:
    ...
@typing.overload
def Matrix(arg0: list[list[complex]]) -> MatrixC:
    ...
def Norm(x: typing.Any) -> typing.Any:
    """
    Compute Norm
    """
@typing.overload
def Vector(length: int, complex: bool = False) -> typing.Any:
    """
    Parameters:
    
    length : int
      input length
    
    complex : bool
      input complex values
    """
@typing.overload
def Vector(buffer: typing_extensions.Buffer, copy: bool = True) -> typing.Any:
    ...
@typing.overload
def Vector(arg0: list[float]) -> VectorD:
    ...
@typing.overload
def Vector(arg0: list[complex]) -> VectorC:
    ...
def __timing__(what: int, n: int, m: int, k: int, lapack: bool = False, doubleprec: bool = True, maxits: int = 10000000000) -> list[tuple[str, float]]:
    """
    Available options timings are:
              -1 .. this help
              0 ... run all timings
              1 ... A = B,   A,B = n*m,   A = aligned, fixed dist
              2 ... A = 0,   A = n*m,     but sliced
              3 ... A = B^t, A = n*m, 
              5 ... y = A*x,   A = n*m
              6 ... y = A^t*x,   A = n*m
              7 ... y += A^t*x(ind),   A = n*m
              10 .. C = A * B,   A=n*m, B=m*k, C=n*k
              11 .. C += A * B,   A=n*m, B=m*k, C=n*k
              // "20 .. C = A * B    A=n*m, B=n*k', C=n*k', k'=round(k), B aligned
              20 .. X = T * X       T=n*n triangular, X=n*m "
              21 .. X = T^-1 * X     T=n*n triangular, X=n*m "
              22 .. T^-1             T=n*n triangular"
              50 .. C += A * B^t,   A=n*k, B=m*k, C=n*m
              51 .. C += A * B^t,   A=n*k, B=m*k, C=n*m,  A,B aligned
              52 .. C = A * B^t,   A=n*k, B=m*k, C=n*m
              60 .. C -= A^t * D B,  A=n*k, B=n*m, C = k*m, D=diag
              61 .. C = A^t B,  A=n*k, B=n*m, C = k*m
              70 .. C += A B^t,  A=n*k, B=m*k, C = n*m, A,B SIMD
    	  80 .. (x,y)        inner product, size n
              100.. MultAddKernel  C += A * B,  A=4*n, B=n*3SW
              101.. MultAddKernel  C += A * B,  A=4*n, B=n*3SW, B aligned
              110.. MultAddKernel2  C += A * B,  A=4*n, B=n*m, m multiple of 3*SW
              111.. MultAddKernel2  C += A * B,  A=4*n, B=n*m, m multiple of 3*SW, B aligned
              150.. ScalKernel     C = A * B^t,  A=4*n, B = 3*n
              151.. ScalKernel     C = A * B^t,  A=4*n, B = 3*n\\n, A,B aligned
              200.. CalcInverse        A = nxn
              201.. CalcInverse by LU  A = nxn          
              205.. LDL                A = nxn
              210.. CalcInverseLapack  A = nxn
              300.. CalcSVD            A = nxn
              410 .. Complex MatVec    A<RowMajor> = nxn FlatVector x,y
              411 .. Complex MatVec    A<RowMajor> = nxn SliceVector x,y
              412 .. Complex MatVec    A<ColMajor> = nxn FlatVector x,y
              413 .. Complex MatVec    A<ColMajor> = nxn SliceVector x,y
    """
