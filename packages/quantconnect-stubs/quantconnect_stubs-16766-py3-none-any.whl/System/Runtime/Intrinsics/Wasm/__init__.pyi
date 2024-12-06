from typing import overload
from enum import Enum
import abc
import typing

import System
import System.Runtime.Intrinsics
import System.Runtime.Intrinsics.Wasm


class PackedSimd(System.Object, metaclass=abc.ABCMeta):
    """Provides access to the WebAssembly packed SIMD instructions via intrinsics."""

    IS_SUPPORTED: bool
    """Gets a value that indicates whether the APIs in this class are supported."""

    @staticmethod
    @overload
    def abs(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.abs"""
        ...

    @staticmethod
    @overload
    def abs(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.abs"""
        ...

    @staticmethod
    @overload
    def abs(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.abs"""
        ...

    @staticmethod
    @overload
    def abs(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.abs"""
        ...

    @staticmethod
    @overload
    def abs(value: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """i32x4.abs"""
        ...

    @staticmethod
    @overload
    def abs(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.abs"""
        ...

    @staticmethod
    @overload
    def abs(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f64x2.abs"""
        ...

    @staticmethod
    @overload
    def abs(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def abs(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def abs(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def abs(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def abs(value: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        ...

    @staticmethod
    @overload
    def abs(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def abs(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def add(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.add"""
        ...

    @staticmethod
    @overload
    def add(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.add"""
        ...

    @staticmethod
    @overload
    def add(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.add"""
        ...

    @staticmethod
    @overload
    def add(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.add"""
        ...

    @staticmethod
    @overload
    def add(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.add"""
        ...

    @staticmethod
    @overload
    def add(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.add"""
        ...

    @staticmethod
    @overload
    def add(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.add"""
        ...

    @staticmethod
    @overload
    def add(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.add"""
        ...

    @staticmethod
    @overload
    def add(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """i32x4.add"""
        ...

    @staticmethod
    @overload
    def add(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """i32x4.add"""
        ...

    @staticmethod
    @overload
    def add(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.add"""
        ...

    @staticmethod
    @overload
    def add(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f64x2.add"""
        ...

    @staticmethod
    @overload
    def add(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def add(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def add(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def add(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def add(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def add(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def add(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def add(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def add(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        ...

    @staticmethod
    @overload
    def add(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        ...

    @staticmethod
    @overload
    def add(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def add(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def add_pairwise_widening(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.extadd_pairwise_i8x16_s"""
        ...

    @staticmethod
    @overload
    def add_pairwise_widening(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.extadd_pairwise_i8x16_u"""
        ...

    @staticmethod
    @overload
    def add_pairwise_widening(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.extadd_pairwise_i16x8_s"""
        ...

    @staticmethod
    @overload
    def add_pairwise_widening(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.extadd_pairwise_i16x8_u"""
        ...

    @staticmethod
    @overload
    def add_pairwise_widening(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def add_pairwise_widening(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def add_pairwise_widening(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def add_pairwise_widening(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def add_saturate(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.add.sat.s"""
        ...

    @staticmethod
    @overload
    def add_saturate(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.add.sat.u"""
        ...

    @staticmethod
    @overload
    def add_saturate(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.add.sat.s"""
        ...

    @staticmethod
    @overload
    def add_saturate(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.add.sat.u"""
        ...

    @staticmethod
    @overload
    def add_saturate(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def add_saturate(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def add_saturate(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def add_saturate(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def all_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        """i8x16.all_true"""
        ...

    @staticmethod
    @overload
    def all_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        """i8x16.all_true"""
        ...

    @staticmethod
    @overload
    def all_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        """i16x8.all_true"""
        ...

    @staticmethod
    @overload
    def all_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        """i16x8.all_true"""
        ...

    @staticmethod
    @overload
    def all_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        """i32x4.all_true"""
        ...

    @staticmethod
    @overload
    def all_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        """i32x4.all_true"""
        ...

    @staticmethod
    @overload
    def all_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        """i64x2.all_true"""
        ...

    @staticmethod
    @overload
    def all_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        """i64x2.all_true"""
        ...

    @staticmethod
    @overload
    def all_true(value: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> bool:
        """i32x4.all_true"""
        ...

    @staticmethod
    @overload
    def all_true(value: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> bool:
        """i32x4.all_true"""
        ...

    @staticmethod
    @overload
    def all_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        ...

    @staticmethod
    @overload
    def all_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        ...

    @staticmethod
    @overload
    def all_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        ...

    @staticmethod
    @overload
    def all_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        ...

    @staticmethod
    @overload
    def all_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        ...

    @staticmethod
    @overload
    def all_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        ...

    @staticmethod
    @overload
    def all_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        ...

    @staticmethod
    @overload
    def all_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        ...

    @staticmethod
    @overload
    def all_true(value: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> bool:
        ...

    @staticmethod
    @overload
    def all_true(value: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> bool:
        ...

    @staticmethod
    @overload
    def And(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.and"""
        ...

    @staticmethod
    @overload
    def And(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.and"""
        ...

    @staticmethod
    @overload
    def And(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.and"""
        ...

    @staticmethod
    @overload
    def And(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.and"""
        ...

    @staticmethod
    @overload
    def And(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.and"""
        ...

    @staticmethod
    @overload
    def And(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.and"""
        ...

    @staticmethod
    @overload
    def And(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.and"""
        ...

    @staticmethod
    @overload
    def And(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.and"""
        ...

    @staticmethod
    @overload
    def And(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """v128.and"""
        ...

    @staticmethod
    @overload
    def And(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """v128.and"""
        ...

    @staticmethod
    @overload
    def And(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """v128.and"""
        ...

    @staticmethod
    @overload
    def And(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """v128.and"""
        ...

    @staticmethod
    @overload
    def And(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def And(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def And(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def And(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def And(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def And(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def And(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def And(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def And(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def And(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def And(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        ...

    @staticmethod
    @overload
    def And(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        ...

    @staticmethod
    @overload
    def and_not(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.andnot"""
        ...

    @staticmethod
    @overload
    def and_not(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.andnot"""
        ...

    @staticmethod
    @overload
    def and_not(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.andnot"""
        ...

    @staticmethod
    @overload
    def and_not(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.andnot"""
        ...

    @staticmethod
    @overload
    def and_not(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.andnot"""
        ...

    @staticmethod
    @overload
    def and_not(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.andnot"""
        ...

    @staticmethod
    @overload
    def and_not(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.andnot"""
        ...

    @staticmethod
    @overload
    def and_not(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.andnot"""
        ...

    @staticmethod
    @overload
    def and_not(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """v128.andnot"""
        ...

    @staticmethod
    @overload
    def and_not(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """v128.andnot"""
        ...

    @staticmethod
    @overload
    def and_not(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """v128.andnot"""
        ...

    @staticmethod
    @overload
    def and_not(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """v128.andnot"""
        ...

    @staticmethod
    @overload
    def and_not(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def and_not(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def and_not(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def and_not(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def and_not(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def and_not(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def and_not(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def and_not(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def and_not(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def and_not(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def and_not(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        ...

    @staticmethod
    @overload
    def and_not(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        ...

    @staticmethod
    @overload
    def any_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        """v128.any_true"""
        ...

    @staticmethod
    @overload
    def any_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        """v128.any_true"""
        ...

    @staticmethod
    @overload
    def any_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        """v128.any_true"""
        ...

    @staticmethod
    @overload
    def any_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        """v128.any_true"""
        ...

    @staticmethod
    @overload
    def any_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        """v128.any_true"""
        ...

    @staticmethod
    @overload
    def any_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        """v128.any_true"""
        ...

    @staticmethod
    @overload
    def any_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        """v128.any_true"""
        ...

    @staticmethod
    @overload
    def any_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        """v128.any_true"""
        ...

    @staticmethod
    @overload
    def any_true(value: System.Runtime.Intrinsics.Vector128[float]) -> bool:
        """v128.any_true"""
        ...

    @staticmethod
    @overload
    def any_true(value: System.Runtime.Intrinsics.Vector128[float]) -> bool:
        """v128.any_true"""
        ...

    @staticmethod
    @overload
    def any_true(value: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> bool:
        """v128.any_true"""
        ...

    @staticmethod
    @overload
    def any_true(value: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> bool:
        """v128.any_true"""
        ...

    @staticmethod
    @overload
    def any_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        ...

    @staticmethod
    @overload
    def any_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        ...

    @staticmethod
    @overload
    def any_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        ...

    @staticmethod
    @overload
    def any_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        ...

    @staticmethod
    @overload
    def any_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        ...

    @staticmethod
    @overload
    def any_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        ...

    @staticmethod
    @overload
    def any_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        ...

    @staticmethod
    @overload
    def any_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        ...

    @staticmethod
    @overload
    def any_true(value: System.Runtime.Intrinsics.Vector128[float]) -> bool:
        ...

    @staticmethod
    @overload
    def any_true(value: System.Runtime.Intrinsics.Vector128[float]) -> bool:
        ...

    @staticmethod
    @overload
    def any_true(value: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> bool:
        ...

    @staticmethod
    @overload
    def any_true(value: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> bool:
        ...

    @staticmethod
    @overload
    def average_rounded(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.avgr.u"""
        ...

    @staticmethod
    @overload
    def average_rounded(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.avgr.u"""
        ...

    @staticmethod
    @overload
    def average_rounded(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def average_rounded(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def bitmask(value: System.Runtime.Intrinsics.Vector128[int]) -> int:
        """i8x16.bitmask"""
        ...

    @staticmethod
    @overload
    def bitmask(value: System.Runtime.Intrinsics.Vector128[int]) -> int:
        """i8x16.bitmask"""
        ...

    @staticmethod
    @overload
    def bitmask(value: System.Runtime.Intrinsics.Vector128[int]) -> int:
        """i16x8.bitmask"""
        ...

    @staticmethod
    @overload
    def bitmask(value: System.Runtime.Intrinsics.Vector128[int]) -> int:
        """i16x8.bitmask"""
        ...

    @staticmethod
    @overload
    def bitmask(value: System.Runtime.Intrinsics.Vector128[int]) -> int:
        """i32x4.bitmask"""
        ...

    @staticmethod
    @overload
    def bitmask(value: System.Runtime.Intrinsics.Vector128[int]) -> int:
        """i32x4.bitmask"""
        ...

    @staticmethod
    @overload
    def bitmask(value: System.Runtime.Intrinsics.Vector128[int]) -> int:
        """i64x2.bitmask"""
        ...

    @staticmethod
    @overload
    def bitmask(value: System.Runtime.Intrinsics.Vector128[int]) -> int:
        """i64x2.bitmask"""
        ...

    @staticmethod
    @overload
    def bitmask(value: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> int:
        """i32x4.bitmask"""
        ...

    @staticmethod
    @overload
    def bitmask(value: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> int:
        """i32x4.bitmask"""
        ...

    @staticmethod
    @overload
    def bitmask(value: System.Runtime.Intrinsics.Vector128[int]) -> int:
        ...

    @staticmethod
    @overload
    def bitmask(value: System.Runtime.Intrinsics.Vector128[int]) -> int:
        ...

    @staticmethod
    @overload
    def bitmask(value: System.Runtime.Intrinsics.Vector128[int]) -> int:
        ...

    @staticmethod
    @overload
    def bitmask(value: System.Runtime.Intrinsics.Vector128[int]) -> int:
        ...

    @staticmethod
    @overload
    def bitmask(value: System.Runtime.Intrinsics.Vector128[int]) -> int:
        ...

    @staticmethod
    @overload
    def bitmask(value: System.Runtime.Intrinsics.Vector128[int]) -> int:
        ...

    @staticmethod
    @overload
    def bitmask(value: System.Runtime.Intrinsics.Vector128[int]) -> int:
        ...

    @staticmethod
    @overload
    def bitmask(value: System.Runtime.Intrinsics.Vector128[int]) -> int:
        ...

    @staticmethod
    @overload
    def bitmask(value: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> int:
        ...

    @staticmethod
    @overload
    def bitmask(value: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> int:
        ...

    @staticmethod
    @overload
    def bitwise_select(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int], select: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.bitselect"""
        ...

    @staticmethod
    @overload
    def bitwise_select(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int], select: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.bitselect"""
        ...

    @staticmethod
    @overload
    def bitwise_select(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int], select: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.bitselect"""
        ...

    @staticmethod
    @overload
    def bitwise_select(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int], select: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.bitselect"""
        ...

    @staticmethod
    @overload
    def bitwise_select(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int], select: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.bitselect"""
        ...

    @staticmethod
    @overload
    def bitwise_select(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int], select: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.bitselect"""
        ...

    @staticmethod
    @overload
    def bitwise_select(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int], select: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.bitselect"""
        ...

    @staticmethod
    @overload
    def bitwise_select(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int], select: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.bitselect"""
        ...

    @staticmethod
    @overload
    def bitwise_select(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float], select: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """v128.bitselect"""
        ...

    @staticmethod
    @overload
    def bitwise_select(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float], select: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """v128.bitselect"""
        ...

    @staticmethod
    @overload
    def bitwise_select(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr], select: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """v128.bitselect"""
        ...

    @staticmethod
    @overload
    def bitwise_select(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr], select: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """v128.bitselect"""
        ...

    @staticmethod
    @overload
    def bitwise_select(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int], select: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def bitwise_select(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int], select: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def bitwise_select(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int], select: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def bitwise_select(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int], select: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def bitwise_select(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int], select: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def bitwise_select(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int], select: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def bitwise_select(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int], select: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def bitwise_select(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int], select: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def bitwise_select(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float], select: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def bitwise_select(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float], select: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def bitwise_select(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr], select: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        ...

    @staticmethod
    @overload
    def bitwise_select(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr], select: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        ...

    @staticmethod
    @overload
    def ceiling(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.ceil"""
        ...

    @staticmethod
    @overload
    def ceiling(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f64x2.ceil"""
        ...

    @staticmethod
    @overload
    def ceiling(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def ceiling(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def compare_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.eq"""
        ...

    @staticmethod
    @overload
    def compare_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.eq"""
        ...

    @staticmethod
    @overload
    def compare_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.eq"""
        ...

    @staticmethod
    @overload
    def compare_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.eq"""
        ...

    @staticmethod
    @overload
    def compare_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.eq"""
        ...

    @staticmethod
    @overload
    def compare_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.eq"""
        ...

    @staticmethod
    @overload
    def compare_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.eq"""
        ...

    @staticmethod
    @overload
    def compare_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.eq"""
        ...

    @staticmethod
    @overload
    def compare_equal(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.eq"""
        ...

    @staticmethod
    @overload
    def compare_equal(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f64x2.eq"""
        ...

    @staticmethod
    @overload
    def compare_equal(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """i32x4.eq"""
        ...

    @staticmethod
    @overload
    def compare_equal(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """i32x4.eq"""
        ...

    @staticmethod
    @overload
    def compare_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_equal(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def compare_equal(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def compare_equal(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        ...

    @staticmethod
    @overload
    def compare_equal(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        ...

    @staticmethod
    @overload
    def compare_greater_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.gt_s"""
        ...

    @staticmethod
    @overload
    def compare_greater_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.gt_u"""
        ...

    @staticmethod
    @overload
    def compare_greater_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.gt_s"""
        ...

    @staticmethod
    @overload
    def compare_greater_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.gt_u"""
        ...

    @staticmethod
    @overload
    def compare_greater_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.gt_s"""
        ...

    @staticmethod
    @overload
    def compare_greater_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.gt_u"""
        ...

    @staticmethod
    @overload
    def compare_greater_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.gt_s"""
        ...

    @staticmethod
    @overload
    def compare_greater_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.gt_u"""
        ...

    @staticmethod
    @overload
    def compare_greater_than(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.gt"""
        ...

    @staticmethod
    @overload
    def compare_greater_than(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f64x2.gt"""
        ...

    @staticmethod
    @overload
    def compare_greater_than(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """i32x4.gt_s"""
        ...

    @staticmethod
    @overload
    def compare_greater_than(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """i32x4.gt_u"""
        ...

    @staticmethod
    @overload
    def compare_greater_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_greater_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_greater_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_greater_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_greater_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_greater_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_greater_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_greater_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_greater_than(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def compare_greater_than(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def compare_greater_than(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        ...

    @staticmethod
    @overload
    def compare_greater_than(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        ...

    @staticmethod
    @overload
    def compare_greater_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.ge_s"""
        ...

    @staticmethod
    @overload
    def compare_greater_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.ge_u"""
        ...

    @staticmethod
    @overload
    def compare_greater_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.ge_s"""
        ...

    @staticmethod
    @overload
    def compare_greater_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.ge_u"""
        ...

    @staticmethod
    @overload
    def compare_greater_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.ge_s"""
        ...

    @staticmethod
    @overload
    def compare_greater_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.ge_u"""
        ...

    @staticmethod
    @overload
    def compare_greater_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.ge_s"""
        ...

    @staticmethod
    @overload
    def compare_greater_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.ge_s"""
        ...

    @staticmethod
    @overload
    def compare_greater_than_or_equal(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.ge"""
        ...

    @staticmethod
    @overload
    def compare_greater_than_or_equal(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f64x2.ge"""
        ...

    @staticmethod
    @overload
    def compare_greater_than_or_equal(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """i32x4.ge_s"""
        ...

    @staticmethod
    @overload
    def compare_greater_than_or_equal(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """i32x4.ge_u"""
        ...

    @staticmethod
    @overload
    def compare_greater_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_greater_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_greater_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_greater_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_greater_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_greater_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_greater_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_greater_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_greater_than_or_equal(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def compare_greater_than_or_equal(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def compare_greater_than_or_equal(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        ...

    @staticmethod
    @overload
    def compare_greater_than_or_equal(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        ...

    @staticmethod
    @overload
    def compare_less_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.lt_s"""
        ...

    @staticmethod
    @overload
    def compare_less_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.lt_u"""
        ...

    @staticmethod
    @overload
    def compare_less_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.lt_s"""
        ...

    @staticmethod
    @overload
    def compare_less_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.lt_u"""
        ...

    @staticmethod
    @overload
    def compare_less_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.lt_s"""
        ...

    @staticmethod
    @overload
    def compare_less_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.lt_u"""
        ...

    @staticmethod
    @overload
    def compare_less_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.lt_s"""
        ...

    @staticmethod
    @overload
    def compare_less_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.lt_u"""
        ...

    @staticmethod
    @overload
    def compare_less_than(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.lt"""
        ...

    @staticmethod
    @overload
    def compare_less_than(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f64x2.lt"""
        ...

    @staticmethod
    @overload
    def compare_less_than(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """i32x4.lt_s"""
        ...

    @staticmethod
    @overload
    def compare_less_than(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """i32x4.lt_u"""
        ...

    @staticmethod
    @overload
    def compare_less_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_less_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_less_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_less_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_less_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_less_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_less_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_less_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_less_than(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def compare_less_than(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def compare_less_than(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        ...

    @staticmethod
    @overload
    def compare_less_than(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        ...

    @staticmethod
    @overload
    def compare_less_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.le_s"""
        ...

    @staticmethod
    @overload
    def compare_less_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.le_u"""
        ...

    @staticmethod
    @overload
    def compare_less_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.le_s"""
        ...

    @staticmethod
    @overload
    def compare_less_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.le_u"""
        ...

    @staticmethod
    @overload
    def compare_less_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.le_s"""
        ...

    @staticmethod
    @overload
    def compare_less_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.le_u"""
        ...

    @staticmethod
    @overload
    def compare_less_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.le_s"""
        ...

    @staticmethod
    @overload
    def compare_less_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.le_u"""
        ...

    @staticmethod
    @overload
    def compare_less_than_or_equal(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.le"""
        ...

    @staticmethod
    @overload
    def compare_less_than_or_equal(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f64x2.le"""
        ...

    @staticmethod
    @overload
    def compare_less_than_or_equal(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """i32x4.le_s"""
        ...

    @staticmethod
    @overload
    def compare_less_than_or_equal(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """i32x4.le_u"""
        ...

    @staticmethod
    @overload
    def compare_less_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_less_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_less_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_less_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_less_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_less_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_less_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_less_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_less_than_or_equal(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def compare_less_than_or_equal(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def compare_less_than_or_equal(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        ...

    @staticmethod
    @overload
    def compare_less_than_or_equal(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        ...

    @staticmethod
    @overload
    def compare_not_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.ne"""
        ...

    @staticmethod
    @overload
    def compare_not_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.ne"""
        ...

    @staticmethod
    @overload
    def compare_not_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.ne"""
        ...

    @staticmethod
    @overload
    def compare_not_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.ne"""
        ...

    @staticmethod
    @overload
    def compare_not_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.ne"""
        ...

    @staticmethod
    @overload
    def compare_not_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.ne"""
        ...

    @staticmethod
    @overload
    def compare_not_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.ne"""
        ...

    @staticmethod
    @overload
    def compare_not_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.ne"""
        ...

    @staticmethod
    @overload
    def compare_not_equal(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.ne"""
        ...

    @staticmethod
    @overload
    def compare_not_equal(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f64x2.ne"""
        ...

    @staticmethod
    @overload
    def compare_not_equal(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """i32x4.ne"""
        ...

    @staticmethod
    @overload
    def compare_not_equal(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """i32x4.ne"""
        ...

    @staticmethod
    @overload
    def compare_not_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_not_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_not_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_not_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_not_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_not_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_not_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_not_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def compare_not_equal(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def compare_not_equal(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def compare_not_equal(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        ...

    @staticmethod
    @overload
    def compare_not_equal(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        ...

    @staticmethod
    @overload
    def convert_narrowing_saturate_signed(lower: System.Runtime.Intrinsics.Vector128[int], upper: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.narrow_i16x8_s"""
        ...

    @staticmethod
    @overload
    def convert_narrowing_saturate_signed(lower: System.Runtime.Intrinsics.Vector128[int], upper: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.narrow_i32x4_s"""
        ...

    @staticmethod
    @overload
    def convert_narrowing_saturate_signed(lower: System.Runtime.Intrinsics.Vector128[int], upper: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def convert_narrowing_saturate_signed(lower: System.Runtime.Intrinsics.Vector128[int], upper: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def convert_narrowing_saturate_unsigned(lower: System.Runtime.Intrinsics.Vector128[int], upper: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.narrow_i16x8_u"""
        ...

    @staticmethod
    @overload
    def convert_narrowing_saturate_unsigned(lower: System.Runtime.Intrinsics.Vector128[int], upper: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.narrow_i32x4_u"""
        ...

    @staticmethod
    @overload
    def convert_narrowing_saturate_unsigned(lower: System.Runtime.Intrinsics.Vector128[int], upper: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def convert_narrowing_saturate_unsigned(lower: System.Runtime.Intrinsics.Vector128[int], upper: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def convert_to_double_lower(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f64x2.convert_low_i32x4_s"""
        ...

    @staticmethod
    @overload
    def convert_to_double_lower(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f64x2.convert_low_i32x4_u"""
        ...

    @staticmethod
    @overload
    def convert_to_double_lower(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f64x2.promote_low_f32x4"""
        ...

    @staticmethod
    @overload
    def convert_to_double_lower(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def convert_to_double_lower(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def convert_to_double_lower(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def convert_to_int_32_saturate(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.trunc_sat_f32x4_s"""
        ...

    @staticmethod
    @overload
    def convert_to_int_32_saturate(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.trunc_sat_f64x2_s_zero"""
        ...

    @staticmethod
    @overload
    def convert_to_int_32_saturate(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def convert_to_int_32_saturate(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def convert_to_single(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.convert_i32x4_s"""
        ...

    @staticmethod
    @overload
    def convert_to_single(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.convert_i32x4_u"""
        ...

    @staticmethod
    @overload
    def convert_to_single(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.demote_f64x2_zero"""
        ...

    @staticmethod
    @overload
    def convert_to_single(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def convert_to_single(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def convert_to_single(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def convert_to_u_int_32_saturate(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.trunc_sat_f32x4_u"""
        ...

    @staticmethod
    @overload
    def convert_to_u_int_32_saturate(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.trunc_sat_f64x2_u_zero"""
        ...

    @staticmethod
    @overload
    def convert_to_u_int_32_saturate(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def convert_to_u_int_32_saturate(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def divide(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.div"""
        ...

    @staticmethod
    @overload
    def divide(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f64x2.div"""
        ...

    @staticmethod
    @overload
    def divide(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def divide(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def dot(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.dot_i16x8_s"""
        ...

    @staticmethod
    @overload
    def dot(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def extract_scalar(value: System.Runtime.Intrinsics.Vector128[int], index: int) -> int:
        """i8x16.extract_lane_s"""
        ...

    @staticmethod
    @overload
    def extract_scalar(value: System.Runtime.Intrinsics.Vector128[int], index: int) -> int:
        """i8x16.extract_lane_u"""
        ...

    @staticmethod
    @overload
    def extract_scalar(value: System.Runtime.Intrinsics.Vector128[int], index: int) -> int:
        """i16x8.extract_lane_s"""
        ...

    @staticmethod
    @overload
    def extract_scalar(value: System.Runtime.Intrinsics.Vector128[int], index: int) -> int:
        """i16x8.extract_lane_u"""
        ...

    @staticmethod
    @overload
    def extract_scalar(value: System.Runtime.Intrinsics.Vector128[int], index: int) -> int:
        """i32x4.extract_lane"""
        ...

    @staticmethod
    @overload
    def extract_scalar(value: System.Runtime.Intrinsics.Vector128[int], index: int) -> int:
        """i32x4.extract_lane"""
        ...

    @staticmethod
    @overload
    def extract_scalar(value: System.Runtime.Intrinsics.Vector128[int], index: int) -> int:
        """i64x2.extract_lane"""
        ...

    @staticmethod
    @overload
    def extract_scalar(value: System.Runtime.Intrinsics.Vector128[int], index: int) -> int:
        """i64x2.extract_lane"""
        ...

    @staticmethod
    @overload
    def extract_scalar(value: System.Runtime.Intrinsics.Vector128[float], index: int) -> float:
        """f32x4.extract_lane"""
        ...

    @staticmethod
    @overload
    def extract_scalar(value: System.Runtime.Intrinsics.Vector128[float], index: int) -> float:
        """f64x2.extract_lane"""
        ...

    @staticmethod
    @overload
    def extract_scalar(value: System.Runtime.Intrinsics.Vector128[System.IntPtr], index: int) -> System.IntPtr:
        """i32x4.extract_lane"""
        ...

    @staticmethod
    @overload
    def extract_scalar(value: System.Runtime.Intrinsics.Vector128[System.UIntPtr], index: int) -> System.UIntPtr:
        """i32x4.extract_lane"""
        ...

    @staticmethod
    @overload
    def extract_scalar(value: System.Runtime.Intrinsics.Vector128[int], index: int) -> int:
        ...

    @staticmethod
    @overload
    def extract_scalar(value: System.Runtime.Intrinsics.Vector128[int], index: int) -> int:
        ...

    @staticmethod
    @overload
    def extract_scalar(value: System.Runtime.Intrinsics.Vector128[int], index: int) -> int:
        ...

    @staticmethod
    @overload
    def extract_scalar(value: System.Runtime.Intrinsics.Vector128[int], index: int) -> int:
        ...

    @staticmethod
    @overload
    def extract_scalar(value: System.Runtime.Intrinsics.Vector128[int], index: int) -> int:
        ...

    @staticmethod
    @overload
    def extract_scalar(value: System.Runtime.Intrinsics.Vector128[int], index: int) -> int:
        ...

    @staticmethod
    @overload
    def extract_scalar(value: System.Runtime.Intrinsics.Vector128[int], index: int) -> int:
        ...

    @staticmethod
    @overload
    def extract_scalar(value: System.Runtime.Intrinsics.Vector128[int], index: int) -> int:
        ...

    @staticmethod
    @overload
    def extract_scalar(value: System.Runtime.Intrinsics.Vector128[float], index: int) -> float:
        ...

    @staticmethod
    @overload
    def extract_scalar(value: System.Runtime.Intrinsics.Vector128[float], index: int) -> float:
        ...

    @staticmethod
    @overload
    def extract_scalar(value: System.Runtime.Intrinsics.Vector128[System.IntPtr], index: int) -> System.IntPtr:
        ...

    @staticmethod
    @overload
    def extract_scalar(value: System.Runtime.Intrinsics.Vector128[System.UIntPtr], index: int) -> System.UIntPtr:
        ...

    @staticmethod
    @overload
    def floor(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.floor"""
        ...

    @staticmethod
    @overload
    def floor(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f64x2.floor"""
        ...

    @staticmethod
    @overload
    def floor(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def floor(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def load_scalar_and_insert(address: typing.Any, vector: System.Runtime.Intrinsics.Vector128[int], index: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load8_lane"""
        ...

    @staticmethod
    @overload
    def load_scalar_and_insert(address: typing.Any, vector: System.Runtime.Intrinsics.Vector128[int], index: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load8_lane"""
        ...

    @staticmethod
    @overload
    def load_scalar_and_insert(address: typing.Any, vector: System.Runtime.Intrinsics.Vector128[int], index: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load16_lane"""
        ...

    @staticmethod
    @overload
    def load_scalar_and_insert(address: typing.Any, vector: System.Runtime.Intrinsics.Vector128[int], index: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load16_lane"""
        ...

    @staticmethod
    @overload
    def load_scalar_and_insert(address: typing.Any, vector: System.Runtime.Intrinsics.Vector128[int], index: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load32_lane"""
        ...

    @staticmethod
    @overload
    def load_scalar_and_insert(address: typing.Any, vector: System.Runtime.Intrinsics.Vector128[int], index: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load32_lane"""
        ...

    @staticmethod
    @overload
    def load_scalar_and_insert(address: typing.Any, vector: System.Runtime.Intrinsics.Vector128[int], index: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load64_lane"""
        ...

    @staticmethod
    @overload
    def load_scalar_and_insert(address: typing.Any, vector: System.Runtime.Intrinsics.Vector128[int], index: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load64_lane"""
        ...

    @staticmethod
    @overload
    def load_scalar_and_insert(address: typing.Any, vector: System.Runtime.Intrinsics.Vector128[float], index: int) -> System.Runtime.Intrinsics.Vector128[float]:
        """v128.load32_lane"""
        ...

    @staticmethod
    @overload
    def load_scalar_and_insert(address: typing.Any, vector: System.Runtime.Intrinsics.Vector128[float], index: int) -> System.Runtime.Intrinsics.Vector128[float]:
        """v128.load64_lane"""
        ...

    @staticmethod
    @overload
    def load_scalar_and_insert(address: typing.Any, vector: System.Runtime.Intrinsics.Vector128[System.IntPtr], index: int) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """v128.load32_lane"""
        ...

    @staticmethod
    @overload
    def load_scalar_and_insert(address: typing.Any, vector: System.Runtime.Intrinsics.Vector128[System.UIntPtr], index: int) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """v128.load32_lane"""
        ...

    @staticmethod
    @overload
    def load_scalar_and_insert(address: typing.Any, vector: System.Runtime.Intrinsics.Vector128[int], index: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def load_scalar_and_insert(address: typing.Any, vector: System.Runtime.Intrinsics.Vector128[int], index: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def load_scalar_and_insert(address: typing.Any, vector: System.Runtime.Intrinsics.Vector128[int], index: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def load_scalar_and_insert(address: typing.Any, vector: System.Runtime.Intrinsics.Vector128[int], index: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def load_scalar_and_insert(address: typing.Any, vector: System.Runtime.Intrinsics.Vector128[int], index: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def load_scalar_and_insert(address: typing.Any, vector: System.Runtime.Intrinsics.Vector128[int], index: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def load_scalar_and_insert(address: typing.Any, vector: System.Runtime.Intrinsics.Vector128[int], index: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def load_scalar_and_insert(address: typing.Any, vector: System.Runtime.Intrinsics.Vector128[int], index: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def load_scalar_and_insert(address: typing.Any, vector: System.Runtime.Intrinsics.Vector128[float], index: int) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def load_scalar_and_insert(address: typing.Any, vector: System.Runtime.Intrinsics.Vector128[float], index: int) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def load_scalar_and_insert(address: typing.Any, vector: System.Runtime.Intrinsics.Vector128[System.IntPtr], index: int) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        ...

    @staticmethod
    @overload
    def load_scalar_and_insert(address: typing.Any, vector: System.Runtime.Intrinsics.Vector128[System.UIntPtr], index: int) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        ...

    @staticmethod
    @overload
    def load_scalar_and_splat_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load8_splat"""
        ...

    @staticmethod
    @overload
    def load_scalar_and_splat_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load8_splat"""
        ...

    @staticmethod
    @overload
    def load_scalar_and_splat_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load16_splat"""
        ...

    @staticmethod
    @overload
    def load_scalar_and_splat_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load16_splat"""
        ...

    @staticmethod
    @overload
    def load_scalar_and_splat_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load32_splat"""
        ...

    @staticmethod
    @overload
    def load_scalar_and_splat_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load32_splat"""
        ...

    @staticmethod
    @overload
    def load_scalar_and_splat_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load64_splat"""
        ...

    @staticmethod
    @overload
    def load_scalar_and_splat_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load64_splat"""
        ...

    @staticmethod
    @overload
    def load_scalar_and_splat_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[float]:
        """v128.load64_splat"""
        ...

    @staticmethod
    @overload
    def load_scalar_and_splat_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[float]:
        """v128.load64_splat"""
        ...

    @staticmethod
    @overload
    def load_scalar_and_splat_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """v128.load64_splat"""
        ...

    @staticmethod
    @overload
    def load_scalar_and_splat_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """v128.load64_splat"""
        ...

    @staticmethod
    @overload
    def load_scalar_and_splat_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def load_scalar_and_splat_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def load_scalar_and_splat_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def load_scalar_and_splat_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def load_scalar_and_splat_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def load_scalar_and_splat_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def load_scalar_and_splat_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def load_scalar_and_splat_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def load_scalar_and_splat_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def load_scalar_and_splat_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def load_scalar_and_splat_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        ...

    @staticmethod
    @overload
    def load_scalar_and_splat_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        ...

    @staticmethod
    @overload
    def load_scalar_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load32.zero"""
        ...

    @staticmethod
    @overload
    def load_scalar_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load32.zero"""
        ...

    @staticmethod
    @overload
    def load_scalar_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load64.zero"""
        ...

    @staticmethod
    @overload
    def load_scalar_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load64.zero"""
        ...

    @staticmethod
    @overload
    def load_scalar_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[float]:
        """v128.load32.zero"""
        ...

    @staticmethod
    @overload
    def load_scalar_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[float]:
        """v128.load64.zero"""
        ...

    @staticmethod
    @overload
    def load_scalar_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """v128.load32.zero"""
        ...

    @staticmethod
    @overload
    def load_scalar_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """v128.load32.zero"""
        ...

    @staticmethod
    @overload
    def load_scalar_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def load_scalar_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def load_scalar_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def load_scalar_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def load_scalar_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def load_scalar_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def load_scalar_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        ...

    @staticmethod
    @overload
    def load_scalar_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        ...

    @staticmethod
    @overload
    def load_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load"""
        ...

    @staticmethod
    @overload
    def load_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load"""
        ...

    @staticmethod
    @overload
    def load_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load"""
        ...

    @staticmethod
    @overload
    def load_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load"""
        ...

    @staticmethod
    @overload
    def load_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load"""
        ...

    @staticmethod
    @overload
    def load_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load"""
        ...

    @staticmethod
    @overload
    def load_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load"""
        ...

    @staticmethod
    @overload
    def load_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load"""
        ...

    @staticmethod
    @overload
    def load_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[float]:
        """v128.load"""
        ...

    @staticmethod
    @overload
    def load_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[float]:
        """v128.load"""
        ...

    @staticmethod
    @overload
    def load_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """v128.load"""
        ...

    @staticmethod
    @overload
    def load_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """v128.load"""
        ...

    @staticmethod
    @overload
    def load_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def load_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def load_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def load_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def load_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def load_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def load_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def load_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def load_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def load_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def load_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        ...

    @staticmethod
    @overload
    def load_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        ...

    @staticmethod
    @overload
    def load_widening_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load8x8_s"""
        ...

    @staticmethod
    @overload
    def load_widening_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load8x8_u"""
        ...

    @staticmethod
    @overload
    def load_widening_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load16x4_s"""
        ...

    @staticmethod
    @overload
    def load_widening_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load16x4_u"""
        ...

    @staticmethod
    @overload
    def load_widening_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load32x2_s"""
        ...

    @staticmethod
    @overload
    def load_widening_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load32x2_u"""
        ...

    @staticmethod
    @overload
    def load_widening_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def load_widening_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def load_widening_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def load_widening_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def load_widening_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def load_widening_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def max(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.max.s"""
        ...

    @staticmethod
    @overload
    def max(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.max.u"""
        ...

    @staticmethod
    @overload
    def max(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.max.s"""
        ...

    @staticmethod
    @overload
    def max(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.max.u"""
        ...

    @staticmethod
    @overload
    def max(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.max.s"""
        ...

    @staticmethod
    @overload
    def max(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.max.u"""
        ...

    @staticmethod
    @overload
    def max(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.max"""
        ...

    @staticmethod
    @overload
    def max(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f64x2.max"""
        ...

    @staticmethod
    @overload
    def max(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def max(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def max(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def max(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def max(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def max(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def max(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def max(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def min(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.min.s"""
        ...

    @staticmethod
    @overload
    def min(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.min.u"""
        ...

    @staticmethod
    @overload
    def min(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.min.s"""
        ...

    @staticmethod
    @overload
    def min(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.min.u"""
        ...

    @staticmethod
    @overload
    def min(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.min.s"""
        ...

    @staticmethod
    @overload
    def min(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.min.u"""
        ...

    @staticmethod
    @overload
    def min(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.min"""
        ...

    @staticmethod
    @overload
    def min(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f64x2.min"""
        ...

    @staticmethod
    @overload
    def min(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def min(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def min(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def min(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def min(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def min(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def min(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def min(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def multiply(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.mul"""
        ...

    @staticmethod
    @overload
    def multiply(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.mul"""
        ...

    @staticmethod
    @overload
    def multiply(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.mul"""
        ...

    @staticmethod
    @overload
    def multiply(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.mul"""
        ...

    @staticmethod
    @overload
    def multiply(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.mul"""
        ...

    @staticmethod
    @overload
    def multiply(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.mul"""
        ...

    @staticmethod
    @overload
    def multiply(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """i32x4.mul"""
        ...

    @staticmethod
    @overload
    def multiply(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """i32x4.mul"""
        ...

    @staticmethod
    @overload
    def multiply(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.mul"""
        ...

    @staticmethod
    @overload
    def multiply(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f64x2.mul"""
        ...

    @staticmethod
    @overload
    def multiply(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def multiply(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def multiply(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def multiply(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def multiply(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def multiply(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def multiply(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        ...

    @staticmethod
    @overload
    def multiply(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        ...

    @staticmethod
    @overload
    def multiply(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def multiply(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def multiply_rounded_saturate_q_15(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.q15mulr.sat.s"""
        ...

    @staticmethod
    @overload
    def multiply_rounded_saturate_q_15(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def multiply_widening_lower(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.extmul_low_i8x16_s"""
        ...

    @staticmethod
    @overload
    def multiply_widening_lower(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.extmul_low_i8x16_u"""
        ...

    @staticmethod
    @overload
    def multiply_widening_lower(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.extmul_low_i16x8_s"""
        ...

    @staticmethod
    @overload
    def multiply_widening_lower(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.extmul_low_i16x8_u"""
        ...

    @staticmethod
    @overload
    def multiply_widening_lower(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.extmul_low_i32x4_s"""
        ...

    @staticmethod
    @overload
    def multiply_widening_lower(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.extmul_low_i32x4_u"""
        ...

    @staticmethod
    @overload
    def multiply_widening_lower(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def multiply_widening_lower(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def multiply_widening_lower(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def multiply_widening_lower(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def multiply_widening_lower(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def multiply_widening_lower(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def multiply_widening_upper(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.extmul_high_i8x16_s"""
        ...

    @staticmethod
    @overload
    def multiply_widening_upper(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.extmul_high_i8x16_u"""
        ...

    @staticmethod
    @overload
    def multiply_widening_upper(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.extmul_high_i16x8_s"""
        ...

    @staticmethod
    @overload
    def multiply_widening_upper(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.extmul_high_i16x8_u"""
        ...

    @staticmethod
    @overload
    def multiply_widening_upper(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.extmul_high_i32x4_s"""
        ...

    @staticmethod
    @overload
    def multiply_widening_upper(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.extmul_high_i32x4_u"""
        ...

    @staticmethod
    @overload
    def multiply_widening_upper(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def multiply_widening_upper(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def multiply_widening_upper(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def multiply_widening_upper(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def multiply_widening_upper(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def multiply_widening_upper(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def negate(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.neg"""
        ...

    @staticmethod
    @overload
    def negate(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.neg"""
        ...

    @staticmethod
    @overload
    def negate(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.neg"""
        ...

    @staticmethod
    @overload
    def negate(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.neg"""
        ...

    @staticmethod
    @overload
    def negate(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.neg"""
        ...

    @staticmethod
    @overload
    def negate(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.neg"""
        ...

    @staticmethod
    @overload
    def negate(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.neg"""
        ...

    @staticmethod
    @overload
    def negate(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.neg"""
        ...

    @staticmethod
    @overload
    def negate(value: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """i32x4.neg"""
        ...

    @staticmethod
    @overload
    def negate(value: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """i32x4.neg"""
        ...

    @staticmethod
    @overload
    def negate(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.neg"""
        ...

    @staticmethod
    @overload
    def negate(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f64x2.neg"""
        ...

    @staticmethod
    @overload
    def negate(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def negate(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def negate(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def negate(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def negate(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def negate(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def negate(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def negate(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def negate(value: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        ...

    @staticmethod
    @overload
    def negate(value: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        ...

    @staticmethod
    @overload
    def negate(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def negate(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def Not(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.not"""
        ...

    @staticmethod
    @overload
    def Not(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.not"""
        ...

    @staticmethod
    @overload
    def Not(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.not"""
        ...

    @staticmethod
    @overload
    def Not(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.not"""
        ...

    @staticmethod
    @overload
    def Not(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.not"""
        ...

    @staticmethod
    @overload
    def Not(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.not"""
        ...

    @staticmethod
    @overload
    def Not(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.not"""
        ...

    @staticmethod
    @overload
    def Not(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.not"""
        ...

    @staticmethod
    @overload
    def Not(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """v128.not"""
        ...

    @staticmethod
    @overload
    def Not(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """v128.not"""
        ...

    @staticmethod
    @overload
    def Not(value: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """v128.not"""
        ...

    @staticmethod
    @overload
    def Not(value: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """v128.not"""
        ...

    @staticmethod
    @overload
    def Not(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def Not(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def Not(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def Not(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def Not(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def Not(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def Not(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def Not(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def Not(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def Not(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def Not(value: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        ...

    @staticmethod
    @overload
    def Not(value: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        ...

    @staticmethod
    @overload
    def Or(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.or"""
        ...

    @staticmethod
    @overload
    def Or(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.or"""
        ...

    @staticmethod
    @overload
    def Or(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.or"""
        ...

    @staticmethod
    @overload
    def Or(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.or"""
        ...

    @staticmethod
    @overload
    def Or(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.or"""
        ...

    @staticmethod
    @overload
    def Or(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.or"""
        ...

    @staticmethod
    @overload
    def Or(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.or"""
        ...

    @staticmethod
    @overload
    def Or(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.or"""
        ...

    @staticmethod
    @overload
    def Or(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """v128.or"""
        ...

    @staticmethod
    @overload
    def Or(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """v128.or"""
        ...

    @staticmethod
    @overload
    def Or(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """v128.or"""
        ...

    @staticmethod
    @overload
    def Or(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """v128.or"""
        ...

    @staticmethod
    @overload
    def Or(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def Or(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def Or(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def Or(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def Or(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def Or(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def Or(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def Or(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def Or(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def Or(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def Or(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        ...

    @staticmethod
    @overload
    def Or(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        ...

    @staticmethod
    @overload
    def pop_count(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.popcnt"""
        ...

    @staticmethod
    @overload
    def pop_count(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def pseudo_max(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.pmax"""
        ...

    @staticmethod
    @overload
    def pseudo_max(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f64x2.pmax"""
        ...

    @staticmethod
    @overload
    def pseudo_max(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def pseudo_max(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def pseudo_min(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.pmin"""
        ...

    @staticmethod
    @overload
    def pseudo_min(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f64x2.pmin"""
        ...

    @staticmethod
    @overload
    def pseudo_min(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def pseudo_min(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def replace_scalar(vector: System.Runtime.Intrinsics.Vector128[int], imm: int, value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.replace_lane"""
        ...

    @staticmethod
    @overload
    def replace_scalar(vector: System.Runtime.Intrinsics.Vector128[int], imm: int, value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.replace_lane"""
        ...

    @staticmethod
    @overload
    def replace_scalar(vector: System.Runtime.Intrinsics.Vector128[int], imm: int, value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.replace_lane"""
        ...

    @staticmethod
    @overload
    def replace_scalar(vector: System.Runtime.Intrinsics.Vector128[int], imm: int, value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.replace_lane"""
        ...

    @staticmethod
    @overload
    def replace_scalar(vector: System.Runtime.Intrinsics.Vector128[int], imm: int, value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.replace_lane"""
        ...

    @staticmethod
    @overload
    def replace_scalar(vector: System.Runtime.Intrinsics.Vector128[int], imm: int, value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.replace_lane"""
        ...

    @staticmethod
    @overload
    def replace_scalar(vector: System.Runtime.Intrinsics.Vector128[int], imm: int, value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.replace_lane"""
        ...

    @staticmethod
    @overload
    def replace_scalar(vector: System.Runtime.Intrinsics.Vector128[int], imm: int, value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.replace_lane"""
        ...

    @staticmethod
    @overload
    def replace_scalar(vector: System.Runtime.Intrinsics.Vector128[float], imm: int, value: float) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.replace_lane"""
        ...

    @staticmethod
    @overload
    def replace_scalar(vector: System.Runtime.Intrinsics.Vector128[float], imm: int, value: float) -> System.Runtime.Intrinsics.Vector128[float]:
        """f64x2.replace_lane"""
        ...

    @staticmethod
    @overload
    def replace_scalar(vector: System.Runtime.Intrinsics.Vector128[System.IntPtr], imm: int, value: System.IntPtr) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """i32x4.replace_lane"""
        ...

    @staticmethod
    @overload
    def replace_scalar(vector: System.Runtime.Intrinsics.Vector128[System.UIntPtr], imm: int, value: System.UIntPtr) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """i32x4.replace_lane"""
        ...

    @staticmethod
    @overload
    def replace_scalar(vector: System.Runtime.Intrinsics.Vector128[int], imm: int, value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def replace_scalar(vector: System.Runtime.Intrinsics.Vector128[int], imm: int, value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def replace_scalar(vector: System.Runtime.Intrinsics.Vector128[int], imm: int, value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def replace_scalar(vector: System.Runtime.Intrinsics.Vector128[int], imm: int, value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def replace_scalar(vector: System.Runtime.Intrinsics.Vector128[int], imm: int, value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def replace_scalar(vector: System.Runtime.Intrinsics.Vector128[int], imm: int, value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def replace_scalar(vector: System.Runtime.Intrinsics.Vector128[int], imm: int, value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def replace_scalar(vector: System.Runtime.Intrinsics.Vector128[int], imm: int, value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def replace_scalar(vector: System.Runtime.Intrinsics.Vector128[float], imm: int, value: float) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def replace_scalar(vector: System.Runtime.Intrinsics.Vector128[float], imm: int, value: float) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def replace_scalar(vector: System.Runtime.Intrinsics.Vector128[System.IntPtr], imm: int, value: System.IntPtr) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        ...

    @staticmethod
    @overload
    def replace_scalar(vector: System.Runtime.Intrinsics.Vector128[System.UIntPtr], imm: int, value: System.UIntPtr) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        ...

    @staticmethod
    @overload
    def round_to_nearest(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.nearest"""
        ...

    @staticmethod
    @overload
    def round_to_nearest(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f64x2.nearest"""
        ...

    @staticmethod
    @overload
    def round_to_nearest(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def round_to_nearest(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def shift_left(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.shl"""
        ...

    @staticmethod
    @overload
    def shift_left(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.shl"""
        ...

    @staticmethod
    @overload
    def shift_left(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.shl"""
        ...

    @staticmethod
    @overload
    def shift_left(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.shl"""
        ...

    @staticmethod
    @overload
    def shift_left(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.shl"""
        ...

    @staticmethod
    @overload
    def shift_left(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.shl"""
        ...

    @staticmethod
    @overload
    def shift_left(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.shl"""
        ...

    @staticmethod
    @overload
    def shift_left(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.shl"""
        ...

    @staticmethod
    @overload
    def shift_left(value: System.Runtime.Intrinsics.Vector128[System.IntPtr], count: int) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """i32x4.shl"""
        ...

    @staticmethod
    @overload
    def shift_left(value: System.Runtime.Intrinsics.Vector128[System.UIntPtr], count: int) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """i32x4.shl"""
        ...

    @staticmethod
    @overload
    def shift_left(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def shift_left(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def shift_left(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def shift_left(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def shift_left(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def shift_left(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def shift_left(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def shift_left(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def shift_left(value: System.Runtime.Intrinsics.Vector128[System.IntPtr], count: int) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        ...

    @staticmethod
    @overload
    def shift_left(value: System.Runtime.Intrinsics.Vector128[System.UIntPtr], count: int) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        ...

    @staticmethod
    @overload
    def shift_right_arithmetic(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.shr_s"""
        ...

    @staticmethod
    @overload
    def shift_right_arithmetic(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.shr_s"""
        ...

    @staticmethod
    @overload
    def shift_right_arithmetic(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.shr_s"""
        ...

    @staticmethod
    @overload
    def shift_right_arithmetic(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.shr_s"""
        ...

    @staticmethod
    @overload
    def shift_right_arithmetic(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.shr_s"""
        ...

    @staticmethod
    @overload
    def shift_right_arithmetic(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.shr_s"""
        ...

    @staticmethod
    @overload
    def shift_right_arithmetic(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.shr_s"""
        ...

    @staticmethod
    @overload
    def shift_right_arithmetic(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.shr_s"""
        ...

    @staticmethod
    @overload
    def shift_right_arithmetic(value: System.Runtime.Intrinsics.Vector128[System.IntPtr], count: int) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """i32x4.shr_s"""
        ...

    @staticmethod
    @overload
    def shift_right_arithmetic(value: System.Runtime.Intrinsics.Vector128[System.UIntPtr], count: int) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """i32x4.shr_s"""
        ...

    @staticmethod
    @overload
    def shift_right_arithmetic(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def shift_right_arithmetic(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def shift_right_arithmetic(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def shift_right_arithmetic(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def shift_right_arithmetic(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def shift_right_arithmetic(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def shift_right_arithmetic(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def shift_right_arithmetic(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def shift_right_arithmetic(value: System.Runtime.Intrinsics.Vector128[System.IntPtr], count: int) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        ...

    @staticmethod
    @overload
    def shift_right_arithmetic(value: System.Runtime.Intrinsics.Vector128[System.UIntPtr], count: int) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        ...

    @staticmethod
    @overload
    def shift_right_logical(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.shr_u"""
        ...

    @staticmethod
    @overload
    def shift_right_logical(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.shr_u"""
        ...

    @staticmethod
    @overload
    def shift_right_logical(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.shr_u"""
        ...

    @staticmethod
    @overload
    def shift_right_logical(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.shr_u"""
        ...

    @staticmethod
    @overload
    def shift_right_logical(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.shr_u"""
        ...

    @staticmethod
    @overload
    def shift_right_logical(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.shr_u"""
        ...

    @staticmethod
    @overload
    def shift_right_logical(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.shr_u"""
        ...

    @staticmethod
    @overload
    def shift_right_logical(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.shr_u"""
        ...

    @staticmethod
    @overload
    def shift_right_logical(value: System.Runtime.Intrinsics.Vector128[System.IntPtr], count: int) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """i32x4.shr_u"""
        ...

    @staticmethod
    @overload
    def shift_right_logical(value: System.Runtime.Intrinsics.Vector128[System.UIntPtr], count: int) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """i32x4.shr_u"""
        ...

    @staticmethod
    @overload
    def shift_right_logical(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def shift_right_logical(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def shift_right_logical(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def shift_right_logical(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def shift_right_logical(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def shift_right_logical(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def shift_right_logical(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def shift_right_logical(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def shift_right_logical(value: System.Runtime.Intrinsics.Vector128[System.IntPtr], count: int) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        ...

    @staticmethod
    @overload
    def shift_right_logical(value: System.Runtime.Intrinsics.Vector128[System.UIntPtr], count: int) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        ...

    @staticmethod
    @overload
    def sign_extend_widening_lower(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.extend_low_i8x16_s"""
        ...

    @staticmethod
    @overload
    def sign_extend_widening_lower(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.extend_low_i8x16_s"""
        ...

    @staticmethod
    @overload
    def sign_extend_widening_lower(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.extend_low_i16x8_s"""
        ...

    @staticmethod
    @overload
    def sign_extend_widening_lower(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.extend_low_i16x8_s"""
        ...

    @staticmethod
    @overload
    def sign_extend_widening_lower(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.extend_low_i32x4_s"""
        ...

    @staticmethod
    @overload
    def sign_extend_widening_lower(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.extend_low_i32x4_s"""
        ...

    @staticmethod
    @overload
    def sign_extend_widening_lower(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def sign_extend_widening_lower(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def sign_extend_widening_lower(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def sign_extend_widening_lower(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def sign_extend_widening_lower(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def sign_extend_widening_lower(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def sign_extend_widening_upper(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.extend_high_i8x16_s"""
        ...

    @staticmethod
    @overload
    def sign_extend_widening_upper(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.extend_high_i8x16_s"""
        ...

    @staticmethod
    @overload
    def sign_extend_widening_upper(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.extend_high_i16x8_s"""
        ...

    @staticmethod
    @overload
    def sign_extend_widening_upper(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.extend_high_i16x8_s"""
        ...

    @staticmethod
    @overload
    def sign_extend_widening_upper(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.extend_high_i32x4_s"""
        ...

    @staticmethod
    @overload
    def sign_extend_widening_upper(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.extend_high_i32x4_s"""
        ...

    @staticmethod
    @overload
    def sign_extend_widening_upper(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def sign_extend_widening_upper(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def sign_extend_widening_upper(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def sign_extend_widening_upper(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def sign_extend_widening_upper(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def sign_extend_widening_upper(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def splat(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.splat or v128.const"""
        ...

    @staticmethod
    @overload
    def splat(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.splat or v128.const"""
        ...

    @staticmethod
    @overload
    def splat(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.splat or v128.const"""
        ...

    @staticmethod
    @overload
    def splat(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.splat or v128.const"""
        ...

    @staticmethod
    @overload
    def splat(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.splat or v128.const"""
        ...

    @staticmethod
    @overload
    def splat(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.splat or v128.const"""
        ...

    @staticmethod
    @overload
    def splat(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.splat or v128.const"""
        ...

    @staticmethod
    @overload
    def splat(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.splat or v128.const"""
        ...

    @staticmethod
    @overload
    def splat(value: float) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.splat or v128.const"""
        ...

    @staticmethod
    @overload
    def splat(value: float) -> System.Runtime.Intrinsics.Vector128[float]:
        """f64x2.splat or v128.const"""
        ...

    @staticmethod
    @overload
    def splat(value: System.IntPtr) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """i32x4.splat or v128.const"""
        ...

    @staticmethod
    @overload
    def splat(value: System.UIntPtr) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """i32x4.splat or v128.const"""
        ...

    @staticmethod
    @overload
    def splat(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def splat(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def splat(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def splat(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def splat(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def splat(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def splat(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def splat(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def splat(value: float) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def splat(value: float) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def splat(value: System.IntPtr) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        ...

    @staticmethod
    @overload
    def splat(value: System.UIntPtr) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        ...

    @staticmethod
    @overload
    def sqrt(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.sqrt"""
        ...

    @staticmethod
    @overload
    def sqrt(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f64x2.sqrt"""
        ...

    @staticmethod
    @overload
    def sqrt(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def sqrt(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def store(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int]) -> None:
        """v128.store"""
        ...

    @staticmethod
    @overload
    def store(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int]) -> None:
        """v128.store"""
        ...

    @staticmethod
    @overload
    def store(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int]) -> None:
        """v128.store"""
        ...

    @staticmethod
    @overload
    def store(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int]) -> None:
        """v128.store"""
        ...

    @staticmethod
    @overload
    def store(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int]) -> None:
        """v128.store"""
        ...

    @staticmethod
    @overload
    def store(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int]) -> None:
        """v128.store"""
        ...

    @staticmethod
    @overload
    def store(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int]) -> None:
        """v128.store"""
        ...

    @staticmethod
    @overload
    def store(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int]) -> None:
        """v128.store"""
        ...

    @staticmethod
    @overload
    def store(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[float]) -> None:
        """v128.store"""
        ...

    @staticmethod
    @overload
    def store(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[float]) -> None:
        """v128.store"""
        ...

    @staticmethod
    @overload
    def store(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> None:
        """v128.store"""
        ...

    @staticmethod
    @overload
    def store(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> None:
        """v128.store"""
        ...

    @staticmethod
    @overload
    def store(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int]) -> None:
        ...

    @staticmethod
    @overload
    def store(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int]) -> None:
        ...

    @staticmethod
    @overload
    def store(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int]) -> None:
        ...

    @staticmethod
    @overload
    def store(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int]) -> None:
        ...

    @staticmethod
    @overload
    def store(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int]) -> None:
        ...

    @staticmethod
    @overload
    def store(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int]) -> None:
        ...

    @staticmethod
    @overload
    def store(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int]) -> None:
        ...

    @staticmethod
    @overload
    def store(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int]) -> None:
        ...

    @staticmethod
    @overload
    def store(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[float]) -> None:
        ...

    @staticmethod
    @overload
    def store(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[float]) -> None:
        ...

    @staticmethod
    @overload
    def store(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> None:
        ...

    @staticmethod
    @overload
    def store(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> None:
        ...

    @staticmethod
    @overload
    def store_selected_scalar(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int], index: int) -> None:
        """v128.store8_lane"""
        ...

    @staticmethod
    @overload
    def store_selected_scalar(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int], index: int) -> None:
        """v128.store8_lane"""
        ...

    @staticmethod
    @overload
    def store_selected_scalar(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int], index: int) -> None:
        """v128.store16_lane"""
        ...

    @staticmethod
    @overload
    def store_selected_scalar(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int], index: int) -> None:
        """v128.store16_lane"""
        ...

    @staticmethod
    @overload
    def store_selected_scalar(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int], index: int) -> None:
        """v128.store32_lane"""
        ...

    @staticmethod
    @overload
    def store_selected_scalar(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int], index: int) -> None:
        """v128.store32_lane"""
        ...

    @staticmethod
    @overload
    def store_selected_scalar(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int], index: int) -> None:
        """v128.store64_lane"""
        ...

    @staticmethod
    @overload
    def store_selected_scalar(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int], index: int) -> None:
        """v128.store64_lane"""
        ...

    @staticmethod
    @overload
    def store_selected_scalar(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[float], index: int) -> None:
        """v128.store32_lane"""
        ...

    @staticmethod
    @overload
    def store_selected_scalar(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[float], index: int) -> None:
        """v128.store64_lane"""
        ...

    @staticmethod
    @overload
    def store_selected_scalar(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[System.IntPtr], index: int) -> None:
        """v128.store32_lane"""
        ...

    @staticmethod
    @overload
    def store_selected_scalar(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[System.UIntPtr], index: int) -> None:
        """v128.store32_lane"""
        ...

    @staticmethod
    @overload
    def store_selected_scalar(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int], index: int) -> None:
        ...

    @staticmethod
    @overload
    def store_selected_scalar(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int], index: int) -> None:
        ...

    @staticmethod
    @overload
    def store_selected_scalar(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int], index: int) -> None:
        ...

    @staticmethod
    @overload
    def store_selected_scalar(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int], index: int) -> None:
        ...

    @staticmethod
    @overload
    def store_selected_scalar(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int], index: int) -> None:
        ...

    @staticmethod
    @overload
    def store_selected_scalar(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int], index: int) -> None:
        ...

    @staticmethod
    @overload
    def store_selected_scalar(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int], index: int) -> None:
        ...

    @staticmethod
    @overload
    def store_selected_scalar(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int], index: int) -> None:
        ...

    @staticmethod
    @overload
    def store_selected_scalar(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[float], index: int) -> None:
        ...

    @staticmethod
    @overload
    def store_selected_scalar(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[float], index: int) -> None:
        ...

    @staticmethod
    @overload
    def store_selected_scalar(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[System.IntPtr], index: int) -> None:
        ...

    @staticmethod
    @overload
    def store_selected_scalar(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[System.UIntPtr], index: int) -> None:
        ...

    @staticmethod
    @overload
    def subtract(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.sub"""
        ...

    @staticmethod
    @overload
    def subtract(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.sub"""
        ...

    @staticmethod
    @overload
    def subtract(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.sub"""
        ...

    @staticmethod
    @overload
    def subtract(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.sub"""
        ...

    @staticmethod
    @overload
    def subtract(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.sub"""
        ...

    @staticmethod
    @overload
    def subtract(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.sub"""
        ...

    @staticmethod
    @overload
    def subtract(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.sub"""
        ...

    @staticmethod
    @overload
    def subtract(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.sub"""
        ...

    @staticmethod
    @overload
    def subtract(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """i32x4.sub"""
        ...

    @staticmethod
    @overload
    def subtract(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """i32x4.sub"""
        ...

    @staticmethod
    @overload
    def subtract(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.sub"""
        ...

    @staticmethod
    @overload
    def subtract(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f64x2.sub"""
        ...

    @staticmethod
    @overload
    def subtract(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def subtract(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def subtract(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def subtract(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def subtract(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def subtract(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def subtract(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def subtract(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def subtract(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        ...

    @staticmethod
    @overload
    def subtract(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        ...

    @staticmethod
    @overload
    def subtract(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def subtract(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def subtract_saturate(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.sub.sat.s"""
        ...

    @staticmethod
    @overload
    def subtract_saturate(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.sub.sat.u"""
        ...

    @staticmethod
    @overload
    def subtract_saturate(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.sub.sat.s"""
        ...

    @staticmethod
    @overload
    def subtract_saturate(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.sub.sat.u"""
        ...

    @staticmethod
    @overload
    def subtract_saturate(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def subtract_saturate(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def subtract_saturate(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def subtract_saturate(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def swizzle(vector: System.Runtime.Intrinsics.Vector128[int], indices: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.swizzle"""
        ...

    @staticmethod
    @overload
    def swizzle(vector: System.Runtime.Intrinsics.Vector128[int], indices: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.swizzle"""
        ...

    @staticmethod
    @overload
    def swizzle(vector: System.Runtime.Intrinsics.Vector128[int], indices: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def swizzle(vector: System.Runtime.Intrinsics.Vector128[int], indices: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def truncate(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.trunc"""
        ...

    @staticmethod
    @overload
    def truncate(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f64x2.trunc"""
        ...

    @staticmethod
    @overload
    def truncate(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def truncate(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def xor(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.xor"""
        ...

    @staticmethod
    @overload
    def xor(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.xor"""
        ...

    @staticmethod
    @overload
    def xor(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.xor"""
        ...

    @staticmethod
    @overload
    def xor(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.xor"""
        ...

    @staticmethod
    @overload
    def xor(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.xor"""
        ...

    @staticmethod
    @overload
    def xor(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.xor"""
        ...

    @staticmethod
    @overload
    def xor(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.xor"""
        ...

    @staticmethod
    @overload
    def xor(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.xor"""
        ...

    @staticmethod
    @overload
    def xor(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """v128.xor"""
        ...

    @staticmethod
    @overload
    def xor(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """v128.xor"""
        ...

    @staticmethod
    @overload
    def xor(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """v128.xor"""
        ...

    @staticmethod
    @overload
    def xor(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """v128.xor"""
        ...

    @staticmethod
    @overload
    def xor(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def xor(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def xor(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def xor(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def xor(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def xor(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def xor(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def xor(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def xor(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def xor(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        ...

    @staticmethod
    @overload
    def xor(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        ...

    @staticmethod
    @overload
    def xor(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        ...

    @staticmethod
    @overload
    def zero_extend_widening_lower(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.extend_low_i8x16_u"""
        ...

    @staticmethod
    @overload
    def zero_extend_widening_lower(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.extend_low_i8x16_u"""
        ...

    @staticmethod
    @overload
    def zero_extend_widening_lower(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.extend_low_i16x8_u"""
        ...

    @staticmethod
    @overload
    def zero_extend_widening_lower(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.extend_low_i16x8_u"""
        ...

    @staticmethod
    @overload
    def zero_extend_widening_lower(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.extend_low_i32x4_u"""
        ...

    @staticmethod
    @overload
    def zero_extend_widening_lower(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.extend_low_i32x4_u"""
        ...

    @staticmethod
    @overload
    def zero_extend_widening_lower(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def zero_extend_widening_lower(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def zero_extend_widening_lower(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def zero_extend_widening_lower(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def zero_extend_widening_lower(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def zero_extend_widening_lower(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def zero_extend_widening_upper(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.extend_high_i8x16_u"""
        ...

    @staticmethod
    @overload
    def zero_extend_widening_upper(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.extend_high_i8x16_u"""
        ...

    @staticmethod
    @overload
    def zero_extend_widening_upper(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.extend_high_i16x8_u"""
        ...

    @staticmethod
    @overload
    def zero_extend_widening_upper(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.extend_high_i16x8_u"""
        ...

    @staticmethod
    @overload
    def zero_extend_widening_upper(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.extend_high_i32x4_u"""
        ...

    @staticmethod
    @overload
    def zero_extend_widening_upper(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i64x2.extend_high_i32x4_u"""
        ...

    @staticmethod
    @overload
    def zero_extend_widening_upper(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def zero_extend_widening_upper(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def zero_extend_widening_upper(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def zero_extend_widening_upper(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def zero_extend_widening_upper(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...

    @staticmethod
    @overload
    def zero_extend_widening_upper(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        ...


