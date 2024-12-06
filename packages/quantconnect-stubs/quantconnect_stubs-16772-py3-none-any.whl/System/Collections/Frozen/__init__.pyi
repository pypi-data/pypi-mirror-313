from typing import overload
from enum import Enum
import abc
import typing

import System
import System.Collections
import System.Collections.Frozen
import System.Collections.Generic
import System.Collections.Immutable

T = typing.Any
TKey = typing.Any
TValue = typing.Any

System_Collections_Frozen_FrozenSet_Create_T = typing.TypeVar("System_Collections_Frozen_FrozenSet_Create_T")
System_Collections_Frozen_FrozenSet_T = typing.TypeVar("System_Collections_Frozen_FrozenSet_T")
System_Collections_Frozen_FrozenSet_GetAlternateLookup_TAlternate = typing.TypeVar("System_Collections_Frozen_FrozenSet_GetAlternateLookup_TAlternate")
System_Collections_Frozen_FrozenSet_ToFrozenSet_T = typing.TypeVar("System_Collections_Frozen_FrozenSet_ToFrozenSet_T")
System_Collections_Frozen_AlternateLookup_TAlternate = typing.TypeVar("System_Collections_Frozen_AlternateLookup_TAlternate")
System_Collections_Frozen_FrozenDictionary_TKey = typing.TypeVar("System_Collections_Frozen_FrozenDictionary_TKey")
System_Collections_Frozen_FrozenDictionary_TValue = typing.TypeVar("System_Collections_Frozen_FrozenDictionary_TValue")
System_Collections_Frozen_FrozenDictionary_GetAlternateLookup_TAlternateKey = typing.TypeVar("System_Collections_Frozen_FrozenDictionary_GetAlternateLookup_TAlternateKey")
System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TKey = typing.TypeVar("System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TKey")
System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TValue = typing.TypeVar("System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TValue")
System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TSource = typing.TypeVar("System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TSource")
System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TElement = typing.TypeVar("System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TElement")


class FrozenDictionary(typing.Generic[System_Collections_Frozen_FrozenDictionary_TKey, System_Collections_Frozen_FrozenDictionary_TValue], System.Object, System.Collections.Generic.IDictionary[System_Collections_Frozen_FrozenDictionary_TKey, System_Collections_Frozen_FrozenDictionary_TValue], System.Collections.Generic.IReadOnlyDictionary[System_Collections_Frozen_FrozenDictionary_TKey, System_Collections_Frozen_FrozenDictionary_TValue], System.Collections.IDictionary, typing.Iterable[System.Collections.Generic.KeyValuePair[System_Collections_Frozen_FrozenDictionary_TKey, System_Collections_Frozen_FrozenDictionary_TValue]], metaclass=abc.ABCMeta):
    """Provides a set of initialization methods for instances of the FrozenDictionary{TKey, TValue} class."""

    class Enumerator:
        """Enumerates the elements of a FrozenDictionary{TKey, TValue}."""

        @property
        def current(self) -> System.Collections.Generic.KeyValuePair[System_Collections_Frozen_FrozenDictionary_TKey, System_Collections_Frozen_FrozenDictionary_TValue]:
            ...

        def move_next(self) -> bool:
            ...

    EMPTY: System.Collections.Frozen.FrozenDictionary[System_Collections_Frozen_FrozenDictionary_TKey, System_Collections_Frozen_FrozenDictionary_TValue]
    """Gets an empty FrozenDictionary{TKey, TValue}."""

    @property
    def comparer(self) -> System.Collections.Generic.IEqualityComparer[System_Collections_Frozen_FrozenDictionary_TKey]:
        """Gets the comparer used by this dictionary."""
        ...

    @property
    def keys(self) -> System.Collections.Immutable.ImmutableArray[System_Collections_Frozen_FrozenDictionary_TKey]:
        """Gets a collection containing the keys in the dictionary."""
        ...

    @property
    def values(self) -> System.Collections.Immutable.ImmutableArray[System_Collections_Frozen_FrozenDictionary_TValue]:
        """Gets a collection containing the values in the dictionary."""
        ...

    @property
    def count(self) -> int:
        """Gets the number of key/value pairs contained in the dictionary."""
        ...

    def __getitem__(self, key: System_Collections_Frozen_FrozenDictionary_TKey) -> typing.Any:
        """
        Gets a reference to the value associated with the specified key.
        
        :param key: The key of the value to get.
        :returns: A reference to the value associated with the specified key.
        """
        ...

    def contains_key(self, key: System_Collections_Frozen_FrozenDictionary_TKey) -> bool:
        """
        Determines whether the dictionary contains the specified key.
        
        :param key: The key to locate in the dictionary.
        :returns: true if the dictionary contains an element with the specified key; otherwise, false.
        """
        ...

    @overload
    def copy_to(self, destination: typing.List[System.Collections.Generic.KeyValuePair[System_Collections_Frozen_FrozenDictionary_TKey, System_Collections_Frozen_FrozenDictionary_TValue]], destination_index: int) -> None:
        """
        Copies the elements of the dictionary to an array of type KeyValuePair{TKey, TValue}, starting at the specified .
        
        :param destination: The array that is the destination of the elements copied from the dictionary.
        :param destination_index: The zero-based index in  at which copying begins.
        """
        ...

    @overload
    def copy_to(self, destination: System.Span[System.Collections.Generic.KeyValuePair[System_Collections_Frozen_FrozenDictionary_TKey, System_Collections_Frozen_FrozenDictionary_TValue]]) -> None:
        """
        Copies the elements of the dictionary to a span of type KeyValuePair{TKey, TValue}.
        
        :param destination: The span that is the destination of the elements copied from the dictionary.
        """
        ...

    def get_alternate_lookup(self) -> System.Collections.Frozen.AlternateLookup[System_Collections_Frozen_FrozenDictionary_GetAlternateLookup_TAlternateKey]:
        """
        Gets an instance of a type that may be used to perform operations on a FrozenDictionary{TKey, TValue}
        using a TAlternateKey as a key instead of a TKey.
        
        :returns: The created lookup instance.
        """
        ...

    def get_enumerator(self) -> System.Collections.Frozen.FrozenDictionary.Enumerator:
        """
        Returns an enumerator that iterates through the dictionary.
        
        :returns: An enumerator that iterates through the dictionary.
        """
        ...

    def get_value_ref_or_null_ref(self, key: System_Collections_Frozen_FrozenDictionary_TKey) -> typing.Any:
        """
        Gets either a reference to a TValue in the dictionary or a null reference if the key does not exist in the dictionary.
        
        :param key: The key used for lookup.
        :returns: A reference to a TValue in the dictionary or a null reference if the key does not exist in the dictionary.
        """
        ...

    @staticmethod
    @overload
    def to_frozen_dictionary(source: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TKey, System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TValue]], comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TKey] = None) -> System.Collections.Frozen.FrozenDictionary[System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TKey, System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TValue]:
        """
        Creates a FrozenDictionary{TKey, TValue} with the specified key/value pairs.
        
        :param source: The key/value pairs to use to populate the dictionary.
        :param comparer: The comparer implementation to use to compare keys for equality. If null, EqualityComparer{TKey}.Default is used.
        :returns: A FrozenDictionary{TKey, TValue} that contains the specified keys and values.
        """
        ...

    @staticmethod
    @overload
    def to_frozen_dictionary(source: System.Collections.Generic.IEnumerable[System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TSource], key_selector: typing.Callable[[System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TSource], System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TKey], comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TKey] = None) -> System.Collections.Frozen.FrozenDictionary[System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TKey, System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TSource]:
        """
        Creates a FrozenDictionary{TKey, TSource} from an IEnumerable{TSource} according to specified key selector function.
        
        :param source: An IEnumerable{TSource} from which to create a FrozenDictionary{TKey, TSource}.
        :param key_selector: A function to extract a key from each element.
        :param comparer: An IEqualityComparer{TKey} to compare keys.
        :returns: A FrozenDictionary{TKey, TElement} that contains the keys and values selected from the input sequence.
        """
        ...

    @staticmethod
    @overload
    def to_frozen_dictionary(source: System.Collections.Generic.IEnumerable[System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TSource], key_selector: typing.Callable[[System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TSource], System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TKey], element_selector: typing.Callable[[System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TSource], System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TElement], comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TKey] = None) -> System.Collections.Frozen.FrozenDictionary[System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TKey, System_Collections_Frozen_FrozenDictionary_ToFrozenDictionary_TElement]:
        """
        Creates a FrozenDictionary{TKey, TElement} from an IEnumerable{TSource} according to specified key selector and element selector functions.
        
        :param source: An IEnumerable{TSource} from which to create a FrozenDictionary{TKey, TElement}.
        :param key_selector: A function to extract a key from each element.
        :param element_selector: A transform function to produce a result element value from each element.
        :param comparer: An IEqualityComparer{TKey} to compare keys.
        :returns: A FrozenDictionary{TKey, TElement} that contains the keys and values selected from the input sequence.
        """
        ...

    def try_get_value(self, key: System_Collections_Frozen_FrozenDictionary_TKey, value: typing.Optional[System_Collections_Frozen_FrozenDictionary_TValue]) -> typing.Union[bool, System_Collections_Frozen_FrozenDictionary_TValue]:
        """
        Gets the value associated with the specified key.
        
        :param key: The key of the value to get.
        :param value: When this method returns, contains the value associated with the specified key, if the key is found; otherwise, the default value for the type of the value parameter.
        :returns: true if the dictionary contains an element with the specified key; otherwise, false.
        """
        ...


class AlternateLookup(typing.Generic[System_Collections_Frozen_AlternateLookup_TAlternate]):
    """
    Provides a type that may be used to perform operations on a FrozenSet{T}
    using a TAlternate as a key instead of a T.
    """

    @property
    def set(self) -> System.Collections.Frozen.FrozenSet[T]:
        """Gets the FrozenSet{T} against which this instance performs operations."""
        ...

    @property
    def dictionary(self) -> System.Collections.Frozen.FrozenDictionary[TKey, TValue]:
        """Gets the FrozenDictionary{TKey, TValue} against which this instance performs operations."""
        ...

    def __getitem__(self, key: typing.Any) -> typing.Any:
        """
        Gets or sets the value associated with the specified alternate key.
        
        :param key: The alternate key of the value to get or set.
        """
        ...

    def contains(self, item: System_Collections_Frozen_AlternateLookup_TAlternate) -> bool:
        """
        Determines whether a set contains the specified element.
        
        :param item: The element to locate in the set.
        :returns: true if the set contains the specified element; otherwise, false.
        """
        ...

    def contains_key(self, key: typing.Any) -> bool:
        """
        Determines whether the FrozenDictionary{TKey, TValue} contains the specified alternate key.
        
        :param key: The alternate key to check.
        :returns: true if the key is in the dictionary; otherwise, false.
        """
        ...

    @overload
    def try_get_value(self, equal_value: System_Collections_Frozen_AlternateLookup_TAlternate, actual_value: typing.Optional[typing.Any]) -> typing.Union[bool, typing.Any]:
        """
        Searches the set for a given value and returns the equal value it finds, if any.
        
        :param equal_value: The value to search for.
        :param actual_value: The value from the set that the search found, or the default value of T when the search yielded no match.
        :returns: A value indicating whether the search was successful.
        """
        ...

    @overload
    def try_get_value(self, key: typing.Any, value: typing.Optional[typing.Any]) -> typing.Union[bool, typing.Any]:
        """
        Gets the value associated with the specified alternate key.
        
        :param key: The alternate key of the value to get.
        :param value: When this method returns, contains the value associated with the specified key, if the key is found; otherwise, the default value for the type of the value parameter.
        :returns: true if an entry was found; otherwise, false.
        """
        ...


class FrozenSet(typing.Generic[System_Collections_Frozen_FrozenSet_T], System.Object, System.Collections.Generic.ISet[System_Collections_Frozen_FrozenSet_T], System.Collections.Generic.IReadOnlyCollection[System_Collections_Frozen_FrozenSet_T], typing.Iterable[System_Collections_Frozen_FrozenSet_T], metaclass=abc.ABCMeta):
    """Provides a set of initialization methods for instances of the FrozenSet{T} class."""

    class Enumerator:
        """Enumerates the values of a FrozenSet{T}."""

        @property
        def current(self) -> System_Collections_Frozen_FrozenSet_T:
            ...

        def move_next(self) -> bool:
            ...

    EMPTY: System.Collections.Frozen.FrozenSet[System_Collections_Frozen_FrozenSet_T]
    """Gets an empty FrozenSet{T}."""

    @property
    def comparer(self) -> System.Collections.Generic.IEqualityComparer[System_Collections_Frozen_FrozenSet_T]:
        """Gets the comparer used by this set."""
        ...

    @property
    def items(self) -> System.Collections.Immutable.ImmutableArray[System_Collections_Frozen_FrozenSet_T]:
        """Gets a collection containing the values in the set."""
        ...

    @property
    def count(self) -> int:
        """Gets the number of values contained in the set."""
        ...

    def contains(self, item: System_Collections_Frozen_FrozenSet_T) -> bool:
        """
        Determines whether the set contains the specified element.
        
        :param item: The element to locate.
        :returns: true if the set contains the specified element; otherwise, false.
        """
        ...

    @overload
    def copy_to(self, destination: typing.List[System_Collections_Frozen_FrozenSet_T], destination_index: int) -> None:
        """
        Copies the values in the set to an array, starting at the specified .
        
        :param destination: The array that is the destination of the values copied from the set.
        :param destination_index: The zero-based index in  at which copying begins.
        """
        ...

    @overload
    def copy_to(self, destination: System.Span[System_Collections_Frozen_FrozenSet_T]) -> None:
        """
        Copies the values in the set to a span.
        
        :param destination: The span that is the destination of the values copied from the set.
        """
        ...

    @staticmethod
    @overload
    def create(*source: System_Collections_Frozen_FrozenSet_Create_T) -> System.Collections.Frozen.FrozenSet[System_Collections_Frozen_FrozenSet_Create_T]:
        """
        Creates a FrozenSet{T} with the specified values.
        
        :param source: The values to use to populate the set.
        :returns: A frozen set.
        """
        ...

    @staticmethod
    @overload
    def create(equality_comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Frozen_FrozenSet_Create_T], *source: System_Collections_Frozen_FrozenSet_Create_T) -> System.Collections.Frozen.FrozenSet[System_Collections_Frozen_FrozenSet_Create_T]:
        """
        Creates a FrozenSet{T} with the specified values.
        
        :param equality_comparer: The comparer implementation to use to compare values for equality. If null, EqualityComparer{T}.Default is used.
        :param source: The values to use to populate the set.
        :returns: A frozen set.
        """
        ...

    def get_alternate_lookup(self) -> System.Collections.Frozen.AlternateLookup[System_Collections_Frozen_FrozenSet_GetAlternateLookup_TAlternate]:
        """
        Gets an instance of a type that may be used to perform operations on a FrozenSet{T}
        using a TAlternate instead of a T.
        
        :returns: The created lookup instance.
        """
        ...

    def get_enumerator(self) -> System.Collections.Frozen.FrozenSet.Enumerator:
        """
        Returns an enumerator that iterates through the set.
        
        :returns: An enumerator that iterates through the set.
        """
        ...

    def is_proper_subset_of(self, other: System.Collections.Generic.IEnumerable[System_Collections_Frozen_FrozenSet_T]) -> bool:
        ...

    def is_proper_superset_of(self, other: System.Collections.Generic.IEnumerable[System_Collections_Frozen_FrozenSet_T]) -> bool:
        ...

    def is_subset_of(self, other: System.Collections.Generic.IEnumerable[System_Collections_Frozen_FrozenSet_T]) -> bool:
        ...

    def is_superset_of(self, other: System.Collections.Generic.IEnumerable[System_Collections_Frozen_FrozenSet_T]) -> bool:
        ...

    def overlaps(self, other: System.Collections.Generic.IEnumerable[System_Collections_Frozen_FrozenSet_T]) -> bool:
        ...

    def set_equals(self, other: System.Collections.Generic.IEnumerable[System_Collections_Frozen_FrozenSet_T]) -> bool:
        ...

    @staticmethod
    def to_frozen_set(source: System.Collections.Generic.IEnumerable[System_Collections_Frozen_FrozenSet_ToFrozenSet_T], comparer: System.Collections.Generic.IEqualityComparer[System_Collections_Frozen_FrozenSet_ToFrozenSet_T] = None) -> System.Collections.Frozen.FrozenSet[System_Collections_Frozen_FrozenSet_ToFrozenSet_T]:
        """
        Creates a FrozenSet{T} with the specified values.
        
        :param source: The values to use to populate the set.
        :param comparer: The comparer implementation to use to compare values for equality. If null, EqualityComparer{T}.Default is used.
        :returns: A frozen set.
        """
        ...

    def try_get_value(self, equal_value: System_Collections_Frozen_FrozenSet_T, actual_value: typing.Optional[System_Collections_Frozen_FrozenSet_T]) -> typing.Union[bool, System_Collections_Frozen_FrozenSet_T]:
        """
        Searches the set for a given value and returns the equal value it finds, if any.
        
        :param equal_value: The value to search for.
        :param actual_value: The value from the set that the search found, or the default value of T when the search yielded no match.
        :returns: A value indicating whether the search was successful.
        """
        ...


