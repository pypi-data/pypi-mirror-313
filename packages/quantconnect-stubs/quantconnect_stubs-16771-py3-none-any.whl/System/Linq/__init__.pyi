from typing import overload
from enum import Enum
import abc
import typing

import System
import System.Collections
import System.Collections.Generic
import System.Collections.Immutable
import System.Linq

System_Linq_ImmutableArrayExtensions_Aggregate_T = typing.TypeVar("System_Linq_ImmutableArrayExtensions_Aggregate_T")
System_Linq_ImmutableArrayExtensions_Aggregate_TAccumulate = typing.TypeVar("System_Linq_ImmutableArrayExtensions_Aggregate_TAccumulate")
System_Linq_ImmutableArrayExtensions_Aggregate_TResult = typing.TypeVar("System_Linq_ImmutableArrayExtensions_Aggregate_TResult")
System_Linq_ImmutableArrayExtensions_ElementAt_T = typing.TypeVar("System_Linq_ImmutableArrayExtensions_ElementAt_T")
System_Linq_ImmutableArrayExtensions_ElementAtOrDefault_T = typing.TypeVar("System_Linq_ImmutableArrayExtensions_ElementAtOrDefault_T")
System_Linq_ImmutableArrayExtensions_First_T = typing.TypeVar("System_Linq_ImmutableArrayExtensions_First_T")
System_Linq_ImmutableArrayExtensions_FirstOrDefault_T = typing.TypeVar("System_Linq_ImmutableArrayExtensions_FirstOrDefault_T")
System_Linq_ImmutableArrayExtensions_Last_T = typing.TypeVar("System_Linq_ImmutableArrayExtensions_Last_T")
System_Linq_ImmutableArrayExtensions_LastOrDefault_T = typing.TypeVar("System_Linq_ImmutableArrayExtensions_LastOrDefault_T")
System_Linq_ImmutableArrayExtensions_Single_T = typing.TypeVar("System_Linq_ImmutableArrayExtensions_Single_T")
System_Linq_ImmutableArrayExtensions_SingleOrDefault_T = typing.TypeVar("System_Linq_ImmutableArrayExtensions_SingleOrDefault_T")
System_Linq_ImmutableArrayExtensions_Select_TResult = typing.TypeVar("System_Linq_ImmutableArrayExtensions_Select_TResult")
System_Linq_ImmutableArrayExtensions_Select_T = typing.TypeVar("System_Linq_ImmutableArrayExtensions_Select_T")
System_Linq_ImmutableArrayExtensions_SelectMany_TResult = typing.TypeVar("System_Linq_ImmutableArrayExtensions_SelectMany_TResult")
System_Linq_ImmutableArrayExtensions_SelectMany_TSource = typing.TypeVar("System_Linq_ImmutableArrayExtensions_SelectMany_TSource")
System_Linq_ImmutableArrayExtensions_SelectMany_TCollection = typing.TypeVar("System_Linq_ImmutableArrayExtensions_SelectMany_TCollection")
System_Linq_ImmutableArrayExtensions_Where_T = typing.TypeVar("System_Linq_ImmutableArrayExtensions_Where_T")
System_Linq_ImmutableArrayExtensions_Any_T = typing.TypeVar("System_Linq_ImmutableArrayExtensions_Any_T")
System_Linq_ImmutableArrayExtensions_All_T = typing.TypeVar("System_Linq_ImmutableArrayExtensions_All_T")
System_Linq_ImmutableArrayExtensions_SequenceEqual_TBase = typing.TypeVar("System_Linq_ImmutableArrayExtensions_SequenceEqual_TBase")
System_Linq_ImmutableArrayExtensions_SequenceEqual_TDerived = typing.TypeVar("System_Linq_ImmutableArrayExtensions_SequenceEqual_TDerived")
System_Linq_ImmutableArrayExtensions_ToDictionary_TKey = typing.TypeVar("System_Linq_ImmutableArrayExtensions_ToDictionary_TKey")
System_Linq_ImmutableArrayExtensions_ToDictionary_T = typing.TypeVar("System_Linq_ImmutableArrayExtensions_ToDictionary_T")
System_Linq_ImmutableArrayExtensions_ToDictionary_TElement = typing.TypeVar("System_Linq_ImmutableArrayExtensions_ToDictionary_TElement")
System_Linq_ImmutableArrayExtensions_ToArray_T = typing.TypeVar("System_Linq_ImmutableArrayExtensions_ToArray_T")
System_Linq_Enumerable_ElementAt_TSource = typing.TypeVar("System_Linq_Enumerable_ElementAt_TSource")
System_Linq_Enumerable_ElementAtOrDefault_TSource = typing.TypeVar("System_Linq_Enumerable_ElementAtOrDefault_TSource")
System_Linq_Enumerable_Last_TSource = typing.TypeVar("System_Linq_Enumerable_Last_TSource")
System_Linq_Enumerable_LastOrDefault_TSource = typing.TypeVar("System_Linq_Enumerable_LastOrDefault_TSource")
System_Linq_Enumerable_DefaultIfEmpty_TSource = typing.TypeVar("System_Linq_Enumerable_DefaultIfEmpty_TSource")
System_Linq_Enumerable_First_TSource = typing.TypeVar("System_Linq_Enumerable_First_TSource")
System_Linq_Enumerable_FirstOrDefault_TSource = typing.TypeVar("System_Linq_Enumerable_FirstOrDefault_TSource")
System_Linq_Enumerable_Append_TSource = typing.TypeVar("System_Linq_Enumerable_Append_TSource")
System_Linq_Enumerable_Prepend_TSource = typing.TypeVar("System_Linq_Enumerable_Prepend_TSource")
System_Linq_Enumerable_Repeat_TResult = typing.TypeVar("System_Linq_Enumerable_Repeat_TResult")
System_Linq_Enumerable_AggregateBy_TAccumulate = typing.TypeVar("System_Linq_Enumerable_AggregateBy_TAccumulate")
System_Linq_Enumerable_Aggregate_TSource = typing.TypeVar("System_Linq_Enumerable_Aggregate_TSource")
System_Linq_Enumerable_Aggregate_TAccumulate = typing.TypeVar("System_Linq_Enumerable_Aggregate_TAccumulate")
System_Linq_Enumerable_Aggregate_TResult = typing.TypeVar("System_Linq_Enumerable_Aggregate_TResult")
System_Linq_Enumerable_Single_TSource = typing.TypeVar("System_Linq_Enumerable_Single_TSource")
System_Linq_Enumerable_SingleOrDefault_TSource = typing.TypeVar("System_Linq_Enumerable_SingleOrDefault_TSource")
System_Linq_Enumerable_Min_TSource = typing.TypeVar("System_Linq_Enumerable_Min_TSource")
System_Linq_Enumerable_MinBy_TSource = typing.TypeVar("System_Linq_Enumerable_MinBy_TSource")
System_Linq_Enumerable_Min_TResult = typing.TypeVar("System_Linq_Enumerable_Min_TResult")
System_Linq_Enumerable_Contains_TSource = typing.TypeVar("System_Linq_Enumerable_Contains_TSource")
System_Linq_Enumerable_Max_TSource = typing.TypeVar("System_Linq_Enumerable_Max_TSource")
System_Linq_Enumerable_MaxBy_TSource = typing.TypeVar("System_Linq_Enumerable_MaxBy_TSource")
System_Linq_Enumerable_Max_TResult = typing.TypeVar("System_Linq_Enumerable_Max_TResult")
System_Linq_Enumerable_Sum_TSource = typing.TypeVar("System_Linq_Enumerable_Sum_TSource")
System_Linq_Enumerable_Count_TSource = typing.TypeVar("System_Linq_Enumerable_Count_TSource")
System_Linq_Enumerable_TryGetNonEnumeratedCount_TSource = typing.TypeVar("System_Linq_Enumerable_TryGetNonEnumeratedCount_TSource")
System_Linq_Enumerable_LongCount_TSource = typing.TypeVar("System_Linq_Enumerable_LongCount_TSource")
System_Linq_Enumerable_Cast_TResult = typing.TypeVar("System_Linq_Enumerable_Cast_TResult")
System_Linq_Enumerable_AsEnumerable_TSource = typing.TypeVar("System_Linq_Enumerable_AsEnumerable_TSource")
System_Linq_Enumerable_Empty_TResult = typing.TypeVar("System_Linq_Enumerable_Empty_TResult")
System_Linq_Enumerable_SelectMany_TResult = typing.TypeVar("System_Linq_Enumerable_SelectMany_TResult")
System_Linq_Enumerable_SelectMany_TSource = typing.TypeVar("System_Linq_Enumerable_SelectMany_TSource")
System_Linq_Enumerable_SelectMany_TCollection = typing.TypeVar("System_Linq_Enumerable_SelectMany_TCollection")
System_Linq_Enumerable_ToArray_TSource = typing.TypeVar("System_Linq_Enumerable_ToArray_TSource")
System_Linq_Enumerable_ToList_TSource = typing.TypeVar("System_Linq_Enumerable_ToList_TSource")
System_Linq_Enumerable_ToDictionary_TKey = typing.TypeVar("System_Linq_Enumerable_ToDictionary_TKey")
System_Linq_Enumerable_ToDictionary_TValue = typing.TypeVar("System_Linq_Enumerable_ToDictionary_TValue")
System_Linq_Enumerable_ToDictionary_TSource = typing.TypeVar("System_Linq_Enumerable_ToDictionary_TSource")
System_Linq_Enumerable_ToDictionary_TElement = typing.TypeVar("System_Linq_Enumerable_ToDictionary_TElement")
System_Linq_Enumerable_ToHashSet_TSource = typing.TypeVar("System_Linq_Enumerable_ToHashSet_TSource")
System_Linq_Enumerable_Intersect_TSource = typing.TypeVar("System_Linq_Enumerable_Intersect_TSource")
System_Linq_Enumerable_IntersectBy_TSource = typing.TypeVar("System_Linq_Enumerable_IntersectBy_TSource")
System_Linq_Enumerable_IntersectBy_TKey = typing.TypeVar("System_Linq_Enumerable_IntersectBy_TKey")
System_Linq_Enumerable_Chunk_TSource = typing.TypeVar("System_Linq_Enumerable_Chunk_TSource")
System_Linq_Enumerable_GroupBy_TSource = typing.TypeVar("System_Linq_Enumerable_GroupBy_TSource")
System_Linq_Enumerable_GroupBy_TKey = typing.TypeVar("System_Linq_Enumerable_GroupBy_TKey")
System_Linq_Enumerable_GroupBy_TElement = typing.TypeVar("System_Linq_Enumerable_GroupBy_TElement")
System_Linq_Enumerable_GroupBy_TResult = typing.TypeVar("System_Linq_Enumerable_GroupBy_TResult")
System_Linq_Enumerable_Concat_TSource = typing.TypeVar("System_Linq_Enumerable_Concat_TSource")
System_Linq_Enumerable_Average_TSource = typing.TypeVar("System_Linq_Enumerable_Average_TSource")
System_Linq_Enumerable_Index_TSource = typing.TypeVar("System_Linq_Enumerable_Index_TSource")
System_Linq_Enumerable_Skip_TSource = typing.TypeVar("System_Linq_Enumerable_Skip_TSource")
System_Linq_Enumerable_SkipWhile_TSource = typing.TypeVar("System_Linq_Enumerable_SkipWhile_TSource")
System_Linq_Enumerable_SkipLast_TSource = typing.TypeVar("System_Linq_Enumerable_SkipLast_TSource")
System_Linq_Enumerable_Zip_TResult = typing.TypeVar("System_Linq_Enumerable_Zip_TResult")
System_Linq_Enumerable_Zip_TFirst = typing.TypeVar("System_Linq_Enumerable_Zip_TFirst")
System_Linq_Enumerable_Zip_TSecond = typing.TypeVar("System_Linq_Enumerable_Zip_TSecond")
System_Linq_Enumerable_Zip_TThird = typing.TypeVar("System_Linq_Enumerable_Zip_TThird")
System_Linq_Enumerable_Union_TSource = typing.TypeVar("System_Linq_Enumerable_Union_TSource")
System_Linq_Enumerable_UnionBy_TSource = typing.TypeVar("System_Linq_Enumerable_UnionBy_TSource")
System_Linq_Enumerable_UnionBy_TKey = typing.TypeVar("System_Linq_Enumerable_UnionBy_TKey")
System_Linq_Enumerable_Reverse_TSource = typing.TypeVar("System_Linq_Enumerable_Reverse_TSource")
System_Linq_Enumerable_Take_TSource = typing.TypeVar("System_Linq_Enumerable_Take_TSource")
System_Linq_Enumerable_TakeWhile_TSource = typing.TypeVar("System_Linq_Enumerable_TakeWhile_TSource")
System_Linq_Enumerable_TakeLast_TSource = typing.TypeVar("System_Linq_Enumerable_TakeLast_TSource")
System_Linq_Enumerable_Select_TResult = typing.TypeVar("System_Linq_Enumerable_Select_TResult")
System_Linq_Enumerable_Select_TSource = typing.TypeVar("System_Linq_Enumerable_Select_TSource")
System_Linq_Enumerable_AggregateBy_TSource = typing.TypeVar("System_Linq_Enumerable_AggregateBy_TSource")
System_Linq_Enumerable_AggregateBy_TKey = typing.TypeVar("System_Linq_Enumerable_AggregateBy_TKey")
System_Linq_Enumerable_ToLookup_TKey = typing.TypeVar("System_Linq_Enumerable_ToLookup_TKey")
System_Linq_Enumerable_ToLookup_TSource = typing.TypeVar("System_Linq_Enumerable_ToLookup_TSource")
System_Linq_Enumerable_ToLookup_TElement = typing.TypeVar("System_Linq_Enumerable_ToLookup_TElement")
System_Linq_Enumerable_Except_TSource = typing.TypeVar("System_Linq_Enumerable_Except_TSource")
System_Linq_Enumerable_ExceptBy_TSource = typing.TypeVar("System_Linq_Enumerable_ExceptBy_TSource")
System_Linq_Enumerable_ExceptBy_TKey = typing.TypeVar("System_Linq_Enumerable_ExceptBy_TKey")
System_Linq_Enumerable_CountBy_TSource = typing.TypeVar("System_Linq_Enumerable_CountBy_TSource")
System_Linq_Enumerable_CountBy_TKey = typing.TypeVar("System_Linq_Enumerable_CountBy_TKey")
System_Linq_Enumerable_Any_TSource = typing.TypeVar("System_Linq_Enumerable_Any_TSource")
System_Linq_Enumerable_All_TSource = typing.TypeVar("System_Linq_Enumerable_All_TSource")
System_Linq_Enumerable_Order_T = typing.TypeVar("System_Linq_Enumerable_Order_T")
System_Linq_Enumerable_OrderBy_TSource = typing.TypeVar("System_Linq_Enumerable_OrderBy_TSource")
System_Linq_Enumerable_OrderBy_TKey = typing.TypeVar("System_Linq_Enumerable_OrderBy_TKey")
System_Linq_Enumerable_OrderDescending_T = typing.TypeVar("System_Linq_Enumerable_OrderDescending_T")
System_Linq_Enumerable_OrderByDescending_TSource = typing.TypeVar("System_Linq_Enumerable_OrderByDescending_TSource")
System_Linq_Enumerable_OrderByDescending_TKey = typing.TypeVar("System_Linq_Enumerable_OrderByDescending_TKey")
System_Linq_Enumerable_ThenBy_TSource = typing.TypeVar("System_Linq_Enumerable_ThenBy_TSource")
System_Linq_Enumerable_ThenBy_TKey = typing.TypeVar("System_Linq_Enumerable_ThenBy_TKey")
System_Linq_Enumerable_ThenByDescending_TSource = typing.TypeVar("System_Linq_Enumerable_ThenByDescending_TSource")
System_Linq_Enumerable_ThenByDescending_TKey = typing.TypeVar("System_Linq_Enumerable_ThenByDescending_TKey")
System_Linq_Enumerable_MinBy_TKey = typing.TypeVar("System_Linq_Enumerable_MinBy_TKey")
System_Linq_Enumerable_Where_TSource = typing.TypeVar("System_Linq_Enumerable_Where_TSource")
System_Linq_Enumerable_Join_TResult = typing.TypeVar("System_Linq_Enumerable_Join_TResult")
System_Linq_Enumerable_Join_TOuter = typing.TypeVar("System_Linq_Enumerable_Join_TOuter")
System_Linq_Enumerable_Join_TInner = typing.TypeVar("System_Linq_Enumerable_Join_TInner")
System_Linq_Enumerable_Join_TKey = typing.TypeVar("System_Linq_Enumerable_Join_TKey")
System_Linq_Enumerable_GroupJoin_TResult = typing.TypeVar("System_Linq_Enumerable_GroupJoin_TResult")
System_Linq_Enumerable_GroupJoin_TOuter = typing.TypeVar("System_Linq_Enumerable_GroupJoin_TOuter")
System_Linq_Enumerable_GroupJoin_TInner = typing.TypeVar("System_Linq_Enumerable_GroupJoin_TInner")
System_Linq_Enumerable_GroupJoin_TKey = typing.TypeVar("System_Linq_Enumerable_GroupJoin_TKey")
System_Linq_Enumerable_SequenceEqual_TSource = typing.TypeVar("System_Linq_Enumerable_SequenceEqual_TSource")
System_Linq_Enumerable_Distinct_TSource = typing.TypeVar("System_Linq_Enumerable_Distinct_TSource")
System_Linq_Enumerable_DistinctBy_TSource = typing.TypeVar("System_Linq_Enumerable_DistinctBy_TSource")
System_Linq_Enumerable_DistinctBy_TKey = typing.TypeVar("System_Linq_Enumerable_DistinctBy_TKey")
System_Linq_Enumerable_OfType_TResult = typing.TypeVar("System_Linq_Enumerable_OfType_TResult")
System_Linq_Enumerable_MaxBy_TKey = typing.TypeVar("System_Linq_Enumerable_MaxBy_TKey")
System_Linq_IGrouping_TKey = typing.TypeVar("System_Linq_IGrouping_TKey")
System_Linq_IGrouping_TElement = typing.TypeVar("System_Linq_IGrouping_TElement")
System_Linq_ILookup_TKey = typing.TypeVar("System_Linq_ILookup_TKey")
System_Linq_ILookup_TElement = typing.TypeVar("System_Linq_ILookup_TElement")
System_Linq_Lookup_TKey = typing.TypeVar("System_Linq_Lookup_TKey")
System_Linq_Lookup_TElement = typing.TypeVar("System_Linq_Lookup_TElement")
System_Linq_Lookup_ApplyResultSelector_TResult = typing.TypeVar("System_Linq_Lookup_ApplyResultSelector_TResult")
System_Linq_IOrderedEnumerable_TElement = typing.TypeVar("System_Linq_IOrderedEnumerable_TElement")
System_Linq_IOrderedEnumerable_CreateOrderedEnumerable_TKey = typing.TypeVar("System_Linq_IOrderedEnumerable_CreateOrderedEnumerable_TKey")


class ImmutableArrayExtensions(System.Object):
    """LINQ extension method overrides that offer greater efficiency for ImmutableArray{T} than the standard LINQ methods"""

    @staticmethod
    @overload
    def aggregate(immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_Aggregate_T], func: typing.Callable[[System_Linq_ImmutableArrayExtensions_Aggregate_T, System_Linq_ImmutableArrayExtensions_Aggregate_T], System_Linq_ImmutableArrayExtensions_Aggregate_T]) -> System_Linq_ImmutableArrayExtensions_Aggregate_T:
        """Applies an accumulator function over a sequence."""
        ...

    @staticmethod
    @overload
    def aggregate(immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_Aggregate_T], seed: System_Linq_ImmutableArrayExtensions_Aggregate_TAccumulate, func: typing.Callable[[System_Linq_ImmutableArrayExtensions_Aggregate_TAccumulate, System_Linq_ImmutableArrayExtensions_Aggregate_T], System_Linq_ImmutableArrayExtensions_Aggregate_TAccumulate]) -> System_Linq_ImmutableArrayExtensions_Aggregate_TAccumulate:
        """Applies an accumulator function over a sequence."""
        ...

    @staticmethod
    @overload
    def aggregate(immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_Aggregate_T], seed: System_Linq_ImmutableArrayExtensions_Aggregate_TAccumulate, func: typing.Callable[[System_Linq_ImmutableArrayExtensions_Aggregate_TAccumulate, System_Linq_ImmutableArrayExtensions_Aggregate_T], System_Linq_ImmutableArrayExtensions_Aggregate_TAccumulate], result_selector: typing.Callable[[System_Linq_ImmutableArrayExtensions_Aggregate_TAccumulate], System_Linq_ImmutableArrayExtensions_Aggregate_TResult]) -> System_Linq_ImmutableArrayExtensions_Aggregate_TResult:
        """
        Applies an accumulator function over a sequence.
        
        :param immutable_array: An immutable array to aggregate over.
        :param seed: The initial accumulator value.
        :param func: An accumulator function to be invoked on each element.
        :param result_selector: A function to transform the final accumulator value into the result type.
        """
        ...

    @staticmethod
    def all(immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_All_T], predicate: typing.Callable[[System_Linq_ImmutableArrayExtensions_All_T], bool]) -> bool:
        """
        Gets a value indicating whether all elements in this collection
        match a given condition.
        
        :param predicate: The predicate.
        :returns: true if every element of the source sequence passes the test in the specified predicate, or if the sequence is empty; otherwise, false.
        """
        ...

    @staticmethod
    @overload
    def any(immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_Any_T]) -> bool:
        """Gets a value indicating whether any elements are in this collection."""
        ...

    @staticmethod
    @overload
    def any(immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_Any_T], predicate: typing.Callable[[System_Linq_ImmutableArrayExtensions_Any_T], bool]) -> bool:
        """
        Gets a value indicating whether any elements are in this collection
        that match a given condition.
        
        :param predicate: The predicate.
        """
        ...

    @staticmethod
    @overload
    def any(builder: System.Collections.Immutable.ImmutableArray.Builder) -> bool:
        """Returns a value indicating whether this collection contains any elements."""
        ...

    @staticmethod
    def element_at(immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_ElementAt_T], index: int) -> System_Linq_ImmutableArrayExtensions_ElementAt_T:
        """Returns the element at a specified index in a sequence."""
        ...

    @staticmethod
    def element_at_or_default(immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_ElementAtOrDefault_T], index: int) -> System_Linq_ImmutableArrayExtensions_ElementAtOrDefault_T:
        """Returns the element at a specified index in a sequence or a default value if the index is out of range."""
        ...

    @staticmethod
    @overload
    def first(immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_First_T], predicate: typing.Callable[[System_Linq_ImmutableArrayExtensions_First_T], bool]) -> System_Linq_ImmutableArrayExtensions_First_T:
        """Returns the first element in a sequence that satisfies a specified condition."""
        ...

    @staticmethod
    @overload
    def first(immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_First_T]) -> System_Linq_ImmutableArrayExtensions_First_T:
        """Returns the first element in a sequence that satisfies a specified condition."""
        ...

    @staticmethod
    @overload
    def first(builder: System.Collections.Immutable.ImmutableArray.Builder) -> System_Linq_ImmutableArrayExtensions_First_T:
        """Returns the first element in the collection."""
        ...

    @staticmethod
    @overload
    def first_or_default(immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_FirstOrDefault_T]) -> System_Linq_ImmutableArrayExtensions_FirstOrDefault_T:
        """Returns the first element of a sequence, or a default value if the sequence contains no elements."""
        ...

    @staticmethod
    @overload
    def first_or_default(immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_FirstOrDefault_T], predicate: typing.Callable[[System_Linq_ImmutableArrayExtensions_FirstOrDefault_T], bool]) -> System_Linq_ImmutableArrayExtensions_FirstOrDefault_T:
        """Returns the first element of the sequence that satisfies a condition or a default value if no such element is found."""
        ...

    @staticmethod
    @overload
    def first_or_default(builder: System.Collections.Immutable.ImmutableArray.Builder) -> System_Linq_ImmutableArrayExtensions_FirstOrDefault_T:
        """Returns the first element in the collection, or the default value if the collection is empty."""
        ...

    @staticmethod
    @overload
    def last(immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_Last_T]) -> System_Linq_ImmutableArrayExtensions_Last_T:
        """Returns the last element of a sequence."""
        ...

    @staticmethod
    @overload
    def last(immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_Last_T], predicate: typing.Callable[[System_Linq_ImmutableArrayExtensions_Last_T], bool]) -> System_Linq_ImmutableArrayExtensions_Last_T:
        """Returns the last element of a sequence that satisfies a specified condition."""
        ...

    @staticmethod
    @overload
    def last(builder: System.Collections.Immutable.ImmutableArray.Builder) -> System_Linq_ImmutableArrayExtensions_Last_T:
        """Returns the last element in the collection."""
        ...

    @staticmethod
    @overload
    def last_or_default(immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_LastOrDefault_T]) -> System_Linq_ImmutableArrayExtensions_LastOrDefault_T:
        """Returns the last element of a sequence, or a default value if the sequence contains no elements."""
        ...

    @staticmethod
    @overload
    def last_or_default(immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_LastOrDefault_T], predicate: typing.Callable[[System_Linq_ImmutableArrayExtensions_LastOrDefault_T], bool]) -> System_Linq_ImmutableArrayExtensions_LastOrDefault_T:
        """Returns the last element of a sequence that satisfies a condition or a default value if no such element is found."""
        ...

    @staticmethod
    @overload
    def last_or_default(builder: System.Collections.Immutable.ImmutableArray.Builder) -> System_Linq_ImmutableArrayExtensions_LastOrDefault_T:
        """Returns the last element in the collection, or the default value if the collection is empty."""
        ...

    @staticmethod
    def select(immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_Select_T], selector: typing.Callable[[System_Linq_ImmutableArrayExtensions_Select_T], System_Linq_ImmutableArrayExtensions_Select_TResult]) -> System.Collections.Generic.IEnumerable[System_Linq_ImmutableArrayExtensions_Select_TResult]:
        """
        Projects each element of a sequence into a new form.
        
        :param immutable_array: The immutable array.
        :param selector: The selector.
        """
        ...

    @staticmethod
    def select_many(immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_SelectMany_TSource], collection_selector: typing.Callable[[System_Linq_ImmutableArrayExtensions_SelectMany_TSource], System.Collections.Generic.IEnumerable[System_Linq_ImmutableArrayExtensions_SelectMany_TCollection]], result_selector: typing.Callable[[System_Linq_ImmutableArrayExtensions_SelectMany_TSource, System_Linq_ImmutableArrayExtensions_SelectMany_TCollection], System_Linq_ImmutableArrayExtensions_SelectMany_TResult]) -> System.Collections.Generic.IEnumerable[System_Linq_ImmutableArrayExtensions_SelectMany_TResult]:
        """
        Projects each element of a sequence to an IEnumerable{T},
        flattens the resulting sequences into one sequence, and invokes a result
        selector function on each element therein.
        
        :param immutable_array: The immutable array.
        :param collection_selector: A transform function to apply to each element of the input sequence.
        :param result_selector: A transform function to apply to each element of the intermediate sequence.
        :returns: An IEnumerable{T} whose elements are the result of invoking the one-to-many transform function  on each element of  and then mapping each of those sequence elements and their corresponding source element to a result element.
        """
        ...

    @staticmethod
    @overload
    def sequence_equal(immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_SequenceEqual_TBase], items: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_SequenceEqual_TDerived], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_ImmutableArrayExtensions_SequenceEqual_TBase] = None) -> bool:
        """Determines whether two sequences are equal according to an equality comparer."""
        ...

    @staticmethod
    @overload
    def sequence_equal(immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_SequenceEqual_TBase], items: System.Collections.Generic.IEnumerable[System_Linq_ImmutableArrayExtensions_SequenceEqual_TDerived], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_ImmutableArrayExtensions_SequenceEqual_TBase] = None) -> bool:
        """Determines whether two sequences are equal according to an equality comparer."""
        ...

    @staticmethod
    @overload
    def sequence_equal(immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_SequenceEqual_TBase], items: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_SequenceEqual_TDerived], predicate: typing.Callable[[System_Linq_ImmutableArrayExtensions_SequenceEqual_TBase, System_Linq_ImmutableArrayExtensions_SequenceEqual_TBase], bool]) -> bool:
        """Determines whether two sequences are equal according to an equality comparer."""
        ...

    @staticmethod
    @overload
    def single(immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_Single_T]) -> System_Linq_ImmutableArrayExtensions_Single_T:
        """Returns the only element of a sequence, and throws an exception if there is not exactly one element in the sequence."""
        ...

    @staticmethod
    @overload
    def single(immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_Single_T], predicate: typing.Callable[[System_Linq_ImmutableArrayExtensions_Single_T], bool]) -> System_Linq_ImmutableArrayExtensions_Single_T:
        """
        Returns the only element of a sequence that satisfies a specified condition, and throws an exception if more than one such element exists.
        
        :param immutable_array: The immutable array to return a single element from.
        :param predicate: The function to test whether an element should be returned.
        """
        ...

    @staticmethod
    @overload
    def single_or_default(immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_SingleOrDefault_T]) -> System_Linq_ImmutableArrayExtensions_SingleOrDefault_T:
        """Returns the only element of a sequence, or a default value if the sequence is empty; this method throws an exception if there is more than one element in the sequence."""
        ...

    @staticmethod
    @overload
    def single_or_default(immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_SingleOrDefault_T], predicate: typing.Callable[[System_Linq_ImmutableArrayExtensions_SingleOrDefault_T], bool]) -> System_Linq_ImmutableArrayExtensions_SingleOrDefault_T:
        """Returns the only element of a sequence that satisfies a specified condition or a default value if no such element exists; this method throws an exception if more than one element satisfies the condition."""
        ...

    @staticmethod
    def to_array(immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_ToArray_T]) -> typing.List[System_Linq_ImmutableArrayExtensions_ToArray_T]:
        """
        Copies the contents of this array to a mutable array.
        
        :param immutable_array: The immutable array to copy into a mutable one.
        :returns: The newly instantiated array.
        """
        ...

    @staticmethod
    @overload
    def to_dictionary(immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_ToDictionary_T], key_selector: typing.Callable[[System_Linq_ImmutableArrayExtensions_ToDictionary_T], System_Linq_ImmutableArrayExtensions_ToDictionary_TKey]) -> System.Collections.Generic.Dictionary[System_Linq_ImmutableArrayExtensions_ToDictionary_TKey, System_Linq_ImmutableArrayExtensions_ToDictionary_T]:
        """
        Creates a dictionary based on the contents of this array.
        
        :param key_selector: The key selector.
        :returns: The newly initialized dictionary.
        """
        ...

    @staticmethod
    @overload
    def to_dictionary(immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_ToDictionary_T], key_selector: typing.Callable[[System_Linq_ImmutableArrayExtensions_ToDictionary_T], System_Linq_ImmutableArrayExtensions_ToDictionary_TKey], element_selector: typing.Callable[[System_Linq_ImmutableArrayExtensions_ToDictionary_T], System_Linq_ImmutableArrayExtensions_ToDictionary_TElement]) -> System.Collections.Generic.Dictionary[System_Linq_ImmutableArrayExtensions_ToDictionary_TKey, System_Linq_ImmutableArrayExtensions_ToDictionary_TElement]:
        """
        Creates a dictionary based on the contents of this array.
        
        :param key_selector: The key selector.
        :param element_selector: The element selector.
        :returns: The newly initialized dictionary.
        """
        ...

    @staticmethod
    @overload
    def to_dictionary(immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_ToDictionary_T], key_selector: typing.Callable[[System_Linq_ImmutableArrayExtensions_ToDictionary_T], System_Linq_ImmutableArrayExtensions_ToDictionary_TKey], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_ImmutableArrayExtensions_ToDictionary_TKey]) -> System.Collections.Generic.Dictionary[System_Linq_ImmutableArrayExtensions_ToDictionary_TKey, System_Linq_ImmutableArrayExtensions_ToDictionary_T]:
        """
        Creates a dictionary based on the contents of this array.
        
        :param key_selector: The key selector.
        :param comparer: The comparer to initialize the dictionary with.
        :returns: The newly initialized dictionary.
        """
        ...

    @staticmethod
    @overload
    def to_dictionary(immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_ToDictionary_T], key_selector: typing.Callable[[System_Linq_ImmutableArrayExtensions_ToDictionary_T], System_Linq_ImmutableArrayExtensions_ToDictionary_TKey], element_selector: typing.Callable[[System_Linq_ImmutableArrayExtensions_ToDictionary_T], System_Linq_ImmutableArrayExtensions_ToDictionary_TElement], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_ImmutableArrayExtensions_ToDictionary_TKey]) -> System.Collections.Generic.Dictionary[System_Linq_ImmutableArrayExtensions_ToDictionary_TKey, System_Linq_ImmutableArrayExtensions_ToDictionary_TElement]:
        """
        Creates a dictionary based on the contents of this array.
        
        :param key_selector: The key selector.
        :param element_selector: The element selector.
        :param comparer: The comparer to initialize the dictionary with.
        :returns: The newly initialized dictionary.
        """
        ...

    @staticmethod
    def where(immutable_array: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_Where_T], predicate: typing.Callable[[System_Linq_ImmutableArrayExtensions_Where_T], bool]) -> System.Collections.Generic.IEnumerable[System_Linq_ImmutableArrayExtensions_Where_T]:
        """Filters a sequence of values based on a predicate."""
        ...


class ILookup(typing.Generic[System_Linq_ILookup_TKey, System_Linq_ILookup_TElement], metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def count(self) -> int:
        ...

    def __getitem__(self, key: System_Linq_ILookup_TKey) -> System.Collections.Generic.IEnumerable[System_Linq_ILookup_TElement]:
        ...

    def contains(self, key: System_Linq_ILookup_TKey) -> bool:
        ...


class IOrderedEnumerable(typing.Generic[System_Linq_IOrderedEnumerable_TElement], metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def create_ordered_enumerable(self, key_selector: typing.Callable[[System_Linq_IOrderedEnumerable_TElement], System_Linq_IOrderedEnumerable_CreateOrderedEnumerable_TKey], comparer: System.Collections.Generic.IComparer[System_Linq_IOrderedEnumerable_CreateOrderedEnumerable_TKey], descending: bool) -> System.Linq.IOrderedEnumerable[System_Linq_IOrderedEnumerable_TElement]:
        ...


class IGrouping(typing.Generic[System_Linq_IGrouping_TKey, System_Linq_IGrouping_TElement], metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def key(self) -> System_Linq_IGrouping_TKey:
        ...


class Enumerable(System.Object):
    """This class has no documentation."""

    @staticmethod
    @overload
    def aggregate(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Aggregate_TSource], func: typing.Callable[[System_Linq_Enumerable_Aggregate_TSource, System_Linq_Enumerable_Aggregate_TSource], System_Linq_Enumerable_Aggregate_TSource]) -> System_Linq_Enumerable_Aggregate_TSource:
        ...

    @staticmethod
    @overload
    def aggregate(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Aggregate_TSource], seed: System_Linq_Enumerable_Aggregate_TAccumulate, func: typing.Callable[[System_Linq_Enumerable_Aggregate_TAccumulate, System_Linq_Enumerable_Aggregate_TSource], System_Linq_Enumerable_Aggregate_TAccumulate]) -> System_Linq_Enumerable_Aggregate_TAccumulate:
        ...

    @staticmethod
    @overload
    def aggregate(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Aggregate_TSource], seed: System_Linq_Enumerable_Aggregate_TAccumulate, func: typing.Callable[[System_Linq_Enumerable_Aggregate_TAccumulate, System_Linq_Enumerable_Aggregate_TSource], System_Linq_Enumerable_Aggregate_TAccumulate], result_selector: typing.Callable[[System_Linq_Enumerable_Aggregate_TAccumulate], System_Linq_Enumerable_Aggregate_TResult]) -> System_Linq_Enumerable_Aggregate_TResult:
        ...

    @staticmethod
    @overload
    def aggregate_by(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_AggregateBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_AggregateBy_TSource], System_Linq_Enumerable_AggregateBy_TKey], seed: System_Linq_Enumerable_AggregateBy_TAccumulate, func: typing.Callable[[System_Linq_Enumerable_AggregateBy_TAccumulate, System_Linq_Enumerable_AggregateBy_TSource], System_Linq_Enumerable_AggregateBy_TAccumulate], key_comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_AggregateBy_TKey] = None) -> System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Linq_Enumerable_AggregateBy_TKey, System_Linq_Enumerable_AggregateBy_TAccumulate]]:
        """
        Applies an accumulator function over a sequence, grouping results by key.
        
        :param source: An IEnumerable{T} to aggregate over.
        :param key_selector: A function to extract the key for each element.
        :param seed: The initial accumulator value.
        :param func: An accumulator function to be invoked on each element.
        :param key_comparer: An IEqualityComparer{T} to compare keys with.
        :returns: An enumerable containing the aggregates corresponding to each key deriving from .
        """
        ...

    @staticmethod
    @overload
    def aggregate_by(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_AggregateBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_AggregateBy_TSource], System_Linq_Enumerable_AggregateBy_TKey], seed_selector: typing.Callable[[System_Linq_Enumerable_AggregateBy_TKey], System_Linq_Enumerable_AggregateBy_TAccumulate], func: typing.Callable[[System_Linq_Enumerable_AggregateBy_TAccumulate, System_Linq_Enumerable_AggregateBy_TSource], System_Linq_Enumerable_AggregateBy_TAccumulate], key_comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_AggregateBy_TKey] = None) -> System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Linq_Enumerable_AggregateBy_TKey, System_Linq_Enumerable_AggregateBy_TAccumulate]]:
        """
        Applies an accumulator function over a sequence, grouping results by key.
        
        :param source: An IEnumerable{T} to aggregate over.
        :param key_selector: A function to extract the key for each element.
        :param seed_selector: A factory for the initial accumulator value.
        :param func: An accumulator function to be invoked on each element.
        :param key_comparer: An IEqualityComparer{T} to compare keys with.
        :returns: An enumerable containing the aggregates corresponding to each key deriving from .
        """
        ...

    @staticmethod
    def all(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_All_TSource], predicate: typing.Callable[[System_Linq_Enumerable_All_TSource], bool]) -> bool:
        ...

    @staticmethod
    @overload
    def any(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Any_TSource]) -> bool:
        ...

    @staticmethod
    @overload
    def any(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Any_TSource], predicate: typing.Callable[[System_Linq_Enumerable_Any_TSource], bool]) -> bool:
        ...

    @staticmethod
    def append(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Append_TSource], element: System_Linq_Enumerable_Append_TSource) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Append_TSource]:
        ...

    @staticmethod
    def as_enumerable(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_AsEnumerable_TSource]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_AsEnumerable_TSource]:
        ...

    @staticmethod
    @overload
    def average(source: System.Collections.Generic.IEnumerable[int]) -> float:
        ...

    @staticmethod
    @overload
    def average(source: System.Collections.Generic.IEnumerable[int]) -> float:
        ...

    @staticmethod
    @overload
    def average(source: System.Collections.Generic.IEnumerable[float]) -> float:
        ...

    @staticmethod
    @overload
    def average(source: System.Collections.Generic.IEnumerable[float]) -> float:
        ...

    @staticmethod
    @overload
    def average(source: System.Collections.Generic.IEnumerable[float]) -> float:
        ...

    @staticmethod
    @overload
    def average(source: System.Collections.Generic.IEnumerable[typing.Optional[int]]) -> typing.Optional[float]:
        ...

    @staticmethod
    @overload
    def average(source: System.Collections.Generic.IEnumerable[typing.Optional[int]]) -> typing.Optional[float]:
        ...

    @staticmethod
    @overload
    def average(source: System.Collections.Generic.IEnumerable[typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @staticmethod
    @overload
    def average(source: System.Collections.Generic.IEnumerable[typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @staticmethod
    @overload
    def average(source: System.Collections.Generic.IEnumerable[typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @staticmethod
    @overload
    def average(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Average_TSource], selector: typing.Callable[[System_Linq_Enumerable_Average_TSource], int]) -> float:
        ...

    @staticmethod
    @overload
    def average(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Average_TSource], selector: typing.Callable[[System_Linq_Enumerable_Average_TSource], int]) -> float:
        ...

    @staticmethod
    @overload
    def average(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Average_TSource], selector: typing.Callable[[System_Linq_Enumerable_Average_TSource], float]) -> float:
        ...

    @staticmethod
    @overload
    def average(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Average_TSource], selector: typing.Callable[[System_Linq_Enumerable_Average_TSource], float]) -> float:
        ...

    @staticmethod
    @overload
    def average(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Average_TSource], selector: typing.Callable[[System_Linq_Enumerable_Average_TSource], float]) -> float:
        ...

    @staticmethod
    @overload
    def average(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Average_TSource], selector: typing.Callable[[System_Linq_Enumerable_Average_TSource], typing.Optional[int]]) -> typing.Optional[float]:
        ...

    @staticmethod
    @overload
    def average(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Average_TSource], selector: typing.Callable[[System_Linq_Enumerable_Average_TSource], typing.Optional[int]]) -> typing.Optional[float]:
        ...

    @staticmethod
    @overload
    def average(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Average_TSource], selector: typing.Callable[[System_Linq_Enumerable_Average_TSource], typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @staticmethod
    @overload
    def average(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Average_TSource], selector: typing.Callable[[System_Linq_Enumerable_Average_TSource], typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @staticmethod
    @overload
    def average(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Average_TSource], selector: typing.Callable[[System_Linq_Enumerable_Average_TSource], typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @staticmethod
    def cast(source: System.Collections.IEnumerable) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Cast_TResult]:
        ...

    @staticmethod
    def chunk(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Chunk_TSource], size: int) -> System.Collections.Generic.IEnumerable[typing.List[System_Linq_Enumerable_Chunk_TSource]]:
        """
        Split the elements of a sequence into chunks of size at most .
        
        :param source: An IEnumerable{T} whose elements to chunk.
        :param size: Maximum size of each chunk.
        :returns: An IEnumerable{T} that contains the elements of the input sequence split into chunks of size .
        """
        ...

    @staticmethod
    def concat(first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Concat_TSource], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Concat_TSource]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Concat_TSource]:
        ...

    @staticmethod
    @overload
    def contains(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Contains_TSource], value: System_Linq_Enumerable_Contains_TSource) -> bool:
        ...

    @staticmethod
    @overload
    def contains(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Contains_TSource], value: System_Linq_Enumerable_Contains_TSource, comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_Contains_TSource]) -> bool:
        ...

    @staticmethod
    @overload
    def count(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Count_TSource]) -> int:
        ...

    @staticmethod
    @overload
    def count(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Count_TSource], predicate: typing.Callable[[System_Linq_Enumerable_Count_TSource], bool]) -> int:
        ...

    @staticmethod
    def count_by(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_CountBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_CountBy_TSource], System_Linq_Enumerable_CountBy_TKey], key_comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_CountBy_TKey] = None) -> System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Linq_Enumerable_CountBy_TKey, int]]:
        """
        Returns the count of elements in the source sequence grouped by key.
        
        :param source: A sequence that contains elements to be counted.
        :param key_selector: A function to extract the key for each element.
        :param key_comparer: An IEqualityComparer{T} to compare keys with.
        :returns: An enumerable containing the frequencies of each key occurrence in .
        """
        ...

    @staticmethod
    @overload
    def default_if_empty(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_DefaultIfEmpty_TSource]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_DefaultIfEmpty_TSource]:
        ...

    @staticmethod
    @overload
    def default_if_empty(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_DefaultIfEmpty_TSource], default_value: System_Linq_Enumerable_DefaultIfEmpty_TSource) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_DefaultIfEmpty_TSource]:
        ...

    @staticmethod
    @overload
    def distinct(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Distinct_TSource]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Distinct_TSource]:
        ...

    @staticmethod
    @overload
    def distinct(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Distinct_TSource], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_Distinct_TSource]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Distinct_TSource]:
        ...

    @staticmethod
    @overload
    def distinct_by(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_DistinctBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_DistinctBy_TSource], System_Linq_Enumerable_DistinctBy_TKey]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_DistinctBy_TSource]:
        """
        Returns distinct elements from a sequence according to a specified key selector function.
        
        :param source: The sequence to remove duplicate elements from.
        :param key_selector: A function to extract the key for each element.
        :returns: An IEnumerable{T} that contains distinct elements from the source sequence.
        """
        ...

    @staticmethod
    @overload
    def distinct_by(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_DistinctBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_DistinctBy_TSource], System_Linq_Enumerable_DistinctBy_TKey], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_DistinctBy_TKey]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_DistinctBy_TSource]:
        """
        Returns distinct elements from a sequence according to a specified key selector function.
        
        :param source: The sequence to remove duplicate elements from.
        :param key_selector: A function to extract the key for each element.
        :param comparer: An IEqualityComparer{TKey} to compare keys.
        :returns: An IEnumerable{T} that contains distinct elements from the source sequence.
        """
        ...

    @staticmethod
    @overload
    def element_at(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ElementAt_TSource], index: int) -> System_Linq_Enumerable_ElementAt_TSource:
        ...

    @staticmethod
    @overload
    def element_at(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ElementAt_TSource], index: System.Index) -> System_Linq_Enumerable_ElementAt_TSource:
        """
        Returns the element at a specified index in a sequence.
        
        :param source: An IEnumerable{T} to return an element from.
        :param index: The index of the element to retrieve, which is either from the start or the end.
        :returns: The element at the specified position in the  sequence.
        """
        ...

    @staticmethod
    @overload
    def element_at_or_default(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ElementAtOrDefault_TSource], index: int) -> System_Linq_Enumerable_ElementAtOrDefault_TSource:
        ...

    @staticmethod
    @overload
    def element_at_or_default(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ElementAtOrDefault_TSource], index: System.Index) -> System_Linq_Enumerable_ElementAtOrDefault_TSource:
        """
        Returns the element at a specified index in a sequence or a default value if the index is out of range.
        
        :param source: An IEnumerable{T} to return an element from.
        :param index: The index of the element to retrieve, which is either from the start or the end.
        :returns: default if  is outside the bounds of the  sequence; otherwise, the element at the specified position in the  sequence.
        """
        ...

    @staticmethod
    def empty() -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Empty_TResult]:
        """Returns an empty IEnumerable{TResult}."""
        ...

    @staticmethod
    @overload
    def Except(first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Except_TSource], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Except_TSource]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Except_TSource]:
        ...

    @staticmethod
    @overload
    def Except(first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Except_TSource], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Except_TSource], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_Except_TSource]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Except_TSource]:
        ...

    @staticmethod
    @overload
    def except_by(first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ExceptBy_TSource], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ExceptBy_TKey], key_selector: typing.Callable[[System_Linq_Enumerable_ExceptBy_TSource], System_Linq_Enumerable_ExceptBy_TKey]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ExceptBy_TSource]:
        """
        Produces the set difference of two sequences according to a specified key selector function.
        
        :param first: An IEnumerable{TSource} whose keys that are not also in  will be returned.
        :param second: An IEnumerable{TKey} whose keys that also occur in the first sequence will cause those elements to be removed from the returned sequence.
        :param key_selector: A function to extract the key for each element.
        :returns: A sequence that contains the set difference of the elements of two sequences.
        """
        ...

    @staticmethod
    @overload
    def except_by(first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ExceptBy_TSource], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ExceptBy_TKey], key_selector: typing.Callable[[System_Linq_Enumerable_ExceptBy_TSource], System_Linq_Enumerable_ExceptBy_TKey], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_ExceptBy_TKey]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ExceptBy_TSource]:
        """
        Produces the set difference of two sequences according to a specified key selector function.
        
        :param first: An IEnumerable{TSource} whose keys that are not also in  will be returned.
        :param second: An IEnumerable{TKey} whose keys that also occur in the first sequence will cause those elements to be removed from the returned sequence.
        :param key_selector: A function to extract the key for each element.
        :param comparer: The IEqualityComparer{TKey} to compare values.
        :returns: A sequence that contains the set difference of the elements of two sequences.
        """
        ...

    @staticmethod
    @overload
    def first(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_First_TSource]) -> System_Linq_Enumerable_First_TSource:
        ...

    @staticmethod
    @overload
    def first(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_First_TSource], predicate: typing.Callable[[System_Linq_Enumerable_First_TSource], bool]) -> System_Linq_Enumerable_First_TSource:
        ...

    @staticmethod
    @overload
    def first_or_default(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_FirstOrDefault_TSource]) -> System_Linq_Enumerable_FirstOrDefault_TSource:
        ...

    @staticmethod
    @overload
    def first_or_default(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_FirstOrDefault_TSource], default_value: System_Linq_Enumerable_FirstOrDefault_TSource) -> System_Linq_Enumerable_FirstOrDefault_TSource:
        """
        Returns the first element of a sequence, or a default value if the sequence contains no elements.
        
        :param source: The IEnumerable{T} to return the first element of.
        :param default_value: The default value to return if the sequence is empty.
        :returns: if  is empty; otherwise, the first element in .
        """
        ...

    @staticmethod
    @overload
    def first_or_default(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_FirstOrDefault_TSource], predicate: typing.Callable[[System_Linq_Enumerable_FirstOrDefault_TSource], bool]) -> System_Linq_Enumerable_FirstOrDefault_TSource:
        ...

    @staticmethod
    @overload
    def first_or_default(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_FirstOrDefault_TSource], predicate: typing.Callable[[System_Linq_Enumerable_FirstOrDefault_TSource], bool], default_value: System_Linq_Enumerable_FirstOrDefault_TSource) -> System_Linq_Enumerable_FirstOrDefault_TSource:
        """
        Returns the first element of the sequence that satisfies a condition or a default value if no such element is found.
        
        :param source: An IEnumerable{T} to return an element from.
        :param predicate: A function to test each element for a condition.
        :param default_value: The default value to return if the sequence is empty.
        :returns: if  is empty or if no element passes the test specified by ; otherwise, the first element in  that passes the test specified by .
        """
        ...

    @staticmethod
    @overload
    def group_by(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_GroupBy_TSource], System_Linq_Enumerable_GroupBy_TKey]) -> System.Collections.Generic.IEnumerable[System.Linq.IGrouping[System_Linq_Enumerable_GroupBy_TKey, System_Linq_Enumerable_GroupBy_TSource]]:
        ...

    @staticmethod
    @overload
    def group_by(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_GroupBy_TSource], System_Linq_Enumerable_GroupBy_TKey], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_GroupBy_TKey]) -> System.Collections.Generic.IEnumerable[System.Linq.IGrouping[System_Linq_Enumerable_GroupBy_TKey, System_Linq_Enumerable_GroupBy_TSource]]:
        ...

    @staticmethod
    @overload
    def group_by(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_GroupBy_TSource], System_Linq_Enumerable_GroupBy_TKey], element_selector: typing.Callable[[System_Linq_Enumerable_GroupBy_TSource], System_Linq_Enumerable_GroupBy_TElement]) -> System.Collections.Generic.IEnumerable[System.Linq.IGrouping[System_Linq_Enumerable_GroupBy_TKey, System_Linq_Enumerable_GroupBy_TElement]]:
        ...

    @staticmethod
    @overload
    def group_by(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_GroupBy_TSource], System_Linq_Enumerable_GroupBy_TKey], element_selector: typing.Callable[[System_Linq_Enumerable_GroupBy_TSource], System_Linq_Enumerable_GroupBy_TElement], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_GroupBy_TKey]) -> System.Collections.Generic.IEnumerable[System.Linq.IGrouping[System_Linq_Enumerable_GroupBy_TKey, System_Linq_Enumerable_GroupBy_TElement]]:
        ...

    @staticmethod
    @overload
    def group_by(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_GroupBy_TSource], System_Linq_Enumerable_GroupBy_TKey], result_selector: typing.Callable[[System_Linq_Enumerable_GroupBy_TKey, System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupBy_TSource]], System_Linq_Enumerable_GroupBy_TResult]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupBy_TResult]:
        ...

    @staticmethod
    @overload
    def group_by(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_GroupBy_TSource], System_Linq_Enumerable_GroupBy_TKey], result_selector: typing.Callable[[System_Linq_Enumerable_GroupBy_TKey, System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupBy_TSource]], System_Linq_Enumerable_GroupBy_TResult], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_GroupBy_TKey]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupBy_TResult]:
        ...

    @staticmethod
    @overload
    def group_by(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_GroupBy_TSource], System_Linq_Enumerable_GroupBy_TKey], element_selector: typing.Callable[[System_Linq_Enumerable_GroupBy_TSource], System_Linq_Enumerable_GroupBy_TElement], result_selector: typing.Callable[[System_Linq_Enumerable_GroupBy_TKey, System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupBy_TElement]], System_Linq_Enumerable_GroupBy_TResult]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupBy_TResult]:
        ...

    @staticmethod
    @overload
    def group_by(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_GroupBy_TSource], System_Linq_Enumerable_GroupBy_TKey], element_selector: typing.Callable[[System_Linq_Enumerable_GroupBy_TSource], System_Linq_Enumerable_GroupBy_TElement], result_selector: typing.Callable[[System_Linq_Enumerable_GroupBy_TKey, System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupBy_TElement]], System_Linq_Enumerable_GroupBy_TResult], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_GroupBy_TKey]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupBy_TResult]:
        ...

    @staticmethod
    @overload
    def group_join(outer: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupJoin_TOuter], inner: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupJoin_TInner], outer_key_selector: typing.Callable[[System_Linq_Enumerable_GroupJoin_TOuter], System_Linq_Enumerable_GroupJoin_TKey], inner_key_selector: typing.Callable[[System_Linq_Enumerable_GroupJoin_TInner], System_Linq_Enumerable_GroupJoin_TKey], result_selector: typing.Callable[[System_Linq_Enumerable_GroupJoin_TOuter, System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupJoin_TInner]], System_Linq_Enumerable_GroupJoin_TResult]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupJoin_TResult]:
        ...

    @staticmethod
    @overload
    def group_join(outer: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupJoin_TOuter], inner: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupJoin_TInner], outer_key_selector: typing.Callable[[System_Linq_Enumerable_GroupJoin_TOuter], System_Linq_Enumerable_GroupJoin_TKey], inner_key_selector: typing.Callable[[System_Linq_Enumerable_GroupJoin_TInner], System_Linq_Enumerable_GroupJoin_TKey], result_selector: typing.Callable[[System_Linq_Enumerable_GroupJoin_TOuter, System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupJoin_TInner]], System_Linq_Enumerable_GroupJoin_TResult], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_GroupJoin_TKey]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_GroupJoin_TResult]:
        ...

    @staticmethod
    def index(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Index_TSource]) -> System.Collections.Generic.IEnumerable[System.ValueTuple[int, System_Linq_Enumerable_Index_TSource]]:
        """
        Returns an enumerable that incorporates the element's index into a tuple.
        
        :param source: The source enumerable providing the elements.
        :returns: An enumerable that incorporates each element index into a tuple.
        """
        ...

    @staticmethod
    @overload
    def intersect(first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Intersect_TSource], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Intersect_TSource]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Intersect_TSource]:
        ...

    @staticmethod
    @overload
    def intersect(first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Intersect_TSource], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Intersect_TSource], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_Intersect_TSource]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Intersect_TSource]:
        ...

    @staticmethod
    @overload
    def intersect_by(first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_IntersectBy_TSource], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_IntersectBy_TKey], key_selector: typing.Callable[[System_Linq_Enumerable_IntersectBy_TSource], System_Linq_Enumerable_IntersectBy_TKey]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_IntersectBy_TSource]:
        """
        Produces the set intersection of two sequences according to a specified key selector function.
        
        :param first: An IEnumerable{T} whose distinct elements that also appear in  will be returned.
        :param second: An IEnumerable{T} whose distinct elements that also appear in the first sequence will be returned.
        :param key_selector: A function to extract the key for each element.
        :returns: A sequence that contains the elements that form the set intersection of two sequences.
        """
        ...

    @staticmethod
    @overload
    def intersect_by(first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_IntersectBy_TSource], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_IntersectBy_TKey], key_selector: typing.Callable[[System_Linq_Enumerable_IntersectBy_TSource], System_Linq_Enumerable_IntersectBy_TKey], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_IntersectBy_TKey]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_IntersectBy_TSource]:
        """
        Produces the set intersection of two sequences according to a specified key selector function.
        
        :param first: An IEnumerable{T} whose distinct elements that also appear in  will be returned.
        :param second: An IEnumerable{T} whose distinct elements that also appear in the first sequence will be returned.
        :param key_selector: A function to extract the key for each element.
        :param comparer: An IEqualityComparer{TKey} to compare keys.
        :returns: A sequence that contains the elements that form the set intersection of two sequences.
        """
        ...

    @staticmethod
    @overload
    def join(outer: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Join_TOuter], inner: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Join_TInner], outer_key_selector: typing.Callable[[System_Linq_Enumerable_Join_TOuter], System_Linq_Enumerable_Join_TKey], inner_key_selector: typing.Callable[[System_Linq_Enumerable_Join_TInner], System_Linq_Enumerable_Join_TKey], result_selector: typing.Callable[[System_Linq_Enumerable_Join_TOuter, System_Linq_Enumerable_Join_TInner], System_Linq_Enumerable_Join_TResult]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Join_TResult]:
        ...

    @staticmethod
    @overload
    def join(outer: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Join_TOuter], inner: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Join_TInner], outer_key_selector: typing.Callable[[System_Linq_Enumerable_Join_TOuter], System_Linq_Enumerable_Join_TKey], inner_key_selector: typing.Callable[[System_Linq_Enumerable_Join_TInner], System_Linq_Enumerable_Join_TKey], result_selector: typing.Callable[[System_Linq_Enumerable_Join_TOuter, System_Linq_Enumerable_Join_TInner], System_Linq_Enumerable_Join_TResult], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_Join_TKey]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Join_TResult]:
        ...

    @staticmethod
    @overload
    def last(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Last_TSource]) -> System_Linq_Enumerable_Last_TSource:
        ...

    @staticmethod
    @overload
    def last(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Last_TSource], predicate: typing.Callable[[System_Linq_Enumerable_Last_TSource], bool]) -> System_Linq_Enumerable_Last_TSource:
        ...

    @staticmethod
    @overload
    def last_or_default(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_LastOrDefault_TSource]) -> System_Linq_Enumerable_LastOrDefault_TSource:
        ...

    @staticmethod
    @overload
    def last_or_default(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_LastOrDefault_TSource], default_value: System_Linq_Enumerable_LastOrDefault_TSource) -> System_Linq_Enumerable_LastOrDefault_TSource:
        """
        Returns the last element of a sequence, or a default value if the sequence contains no elements.
        
        :param source: An IEnumerable{T} to return the last element of.
        :param default_value: The default value to return if the sequence is empty.
        :returns: if the source sequence is empty; otherwise, the last element in the IEnumerable{T}.
        """
        ...

    @staticmethod
    @overload
    def last_or_default(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_LastOrDefault_TSource], predicate: typing.Callable[[System_Linq_Enumerable_LastOrDefault_TSource], bool]) -> System_Linq_Enumerable_LastOrDefault_TSource:
        ...

    @staticmethod
    @overload
    def last_or_default(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_LastOrDefault_TSource], predicate: typing.Callable[[System_Linq_Enumerable_LastOrDefault_TSource], bool], default_value: System_Linq_Enumerable_LastOrDefault_TSource) -> System_Linq_Enumerable_LastOrDefault_TSource:
        """
        Returns the last element of a sequence that satisfies a condition or a default value if no such element is found.
        
        :param source: An IEnumerable{T} to return an element from.
        :param predicate: A function to test each element for a condition.
        :param default_value: The default value to return if the sequence is empty.
        :returns: if the sequence is empty or if no elements pass the test in the predicate function; otherwise, the last element that passes the test in the predicate function.
        """
        ...

    @staticmethod
    @overload
    def long_count(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_LongCount_TSource]) -> int:
        ...

    @staticmethod
    @overload
    def long_count(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_LongCount_TSource], predicate: typing.Callable[[System_Linq_Enumerable_LongCount_TSource], bool]) -> int:
        ...

    @staticmethod
    @overload
    def max(source: System.Collections.Generic.IEnumerable[int]) -> int:
        ...

    @staticmethod
    @overload
    def max(source: System.Collections.Generic.IEnumerable[int]) -> int:
        ...

    @staticmethod
    @overload
    def max(source: System.Collections.Generic.IEnumerable[typing.Optional[int]]) -> typing.Optional[int]:
        ...

    @staticmethod
    @overload
    def max(source: System.Collections.Generic.IEnumerable[typing.Optional[int]]) -> typing.Optional[int]:
        ...

    @staticmethod
    @overload
    def max(source: System.Collections.Generic.IEnumerable[float]) -> float:
        ...

    @staticmethod
    @overload
    def max(source: System.Collections.Generic.IEnumerable[typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @staticmethod
    @overload
    def max(source: System.Collections.Generic.IEnumerable[float]) -> float:
        ...

    @staticmethod
    @overload
    def max(source: System.Collections.Generic.IEnumerable[typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @staticmethod
    @overload
    def max(source: System.Collections.Generic.IEnumerable[float]) -> float:
        ...

    @staticmethod
    @overload
    def max(source: System.Collections.Generic.IEnumerable[typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @staticmethod
    @overload
    def max(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Max_TSource]) -> System_Linq_Enumerable_Max_TSource:
        ...

    @staticmethod
    @overload
    def max(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Max_TSource], comparer: System.Collections.Generic.IComparer[System_Linq_Enumerable_Max_TSource]) -> System_Linq_Enumerable_Max_TSource:
        """
        Returns the maximum value in a generic sequence.
        
        :param source: A sequence of values to determine the maximum value of.
        :param comparer: The IComparer{T} to compare values.
        :returns: The maximum value in the sequence.
        """
        ...

    @staticmethod
    @overload
    def max(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Max_TSource], selector: typing.Callable[[System_Linq_Enumerable_Max_TSource], int]) -> int:
        ...

    @staticmethod
    @overload
    def max(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Max_TSource], selector: typing.Callable[[System_Linq_Enumerable_Max_TSource], typing.Optional[int]]) -> typing.Optional[int]:
        ...

    @staticmethod
    @overload
    def max(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Max_TSource], selector: typing.Callable[[System_Linq_Enumerable_Max_TSource], int]) -> int:
        ...

    @staticmethod
    @overload
    def max(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Max_TSource], selector: typing.Callable[[System_Linq_Enumerable_Max_TSource], typing.Optional[int]]) -> typing.Optional[int]:
        ...

    @staticmethod
    @overload
    def max(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Max_TSource], selector: typing.Callable[[System_Linq_Enumerable_Max_TSource], float]) -> float:
        ...

    @staticmethod
    @overload
    def max(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Max_TSource], selector: typing.Callable[[System_Linq_Enumerable_Max_TSource], typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @staticmethod
    @overload
    def max(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Max_TSource], selector: typing.Callable[[System_Linq_Enumerable_Max_TSource], float]) -> float:
        ...

    @staticmethod
    @overload
    def max(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Max_TSource], selector: typing.Callable[[System_Linq_Enumerable_Max_TSource], typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @staticmethod
    @overload
    def max(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Max_TSource], selector: typing.Callable[[System_Linq_Enumerable_Max_TSource], float]) -> float:
        ...

    @staticmethod
    @overload
    def max(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Max_TSource], selector: typing.Callable[[System_Linq_Enumerable_Max_TSource], typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @staticmethod
    @overload
    def max(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Max_TSource], selector: typing.Callable[[System_Linq_Enumerable_Max_TSource], System_Linq_Enumerable_Max_TResult]) -> System_Linq_Enumerable_Max_TResult:
        ...

    @staticmethod
    @overload
    def max_by(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_MaxBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_MaxBy_TSource], System_Linq_Enumerable_MaxBy_TKey]) -> System_Linq_Enumerable_MaxBy_TSource:
        """
        Returns the maximum value in a generic sequence according to a specified key selector function.
        
        :param source: A sequence of values to determine the maximum value of.
        :param key_selector: A function to extract the key for each element.
        :returns: The value with the maximum key in the sequence.
        """
        ...

    @staticmethod
    @overload
    def max_by(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_MaxBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_MaxBy_TSource], System_Linq_Enumerable_MaxBy_TKey], comparer: System.Collections.Generic.IComparer[System_Linq_Enumerable_MaxBy_TKey]) -> System_Linq_Enumerable_MaxBy_TSource:
        """
        Returns the maximum value in a generic sequence according to a specified key selector function.
        
        :param source: A sequence of values to determine the maximum value of.
        :param key_selector: A function to extract the key for each element.
        :param comparer: The IComparer{TKey} to compare keys.
        :returns: The value with the maximum key in the sequence.
        """
        ...

    @staticmethod
    @overload
    def min(source: System.Collections.Generic.IEnumerable[int]) -> int:
        ...

    @staticmethod
    @overload
    def min(source: System.Collections.Generic.IEnumerable[int]) -> int:
        ...

    @staticmethod
    @overload
    def min(source: System.Collections.Generic.IEnumerable[typing.Optional[int]]) -> typing.Optional[int]:
        ...

    @staticmethod
    @overload
    def min(source: System.Collections.Generic.IEnumerable[typing.Optional[int]]) -> typing.Optional[int]:
        ...

    @staticmethod
    @overload
    def min(source: System.Collections.Generic.IEnumerable[float]) -> float:
        ...

    @staticmethod
    @overload
    def min(source: System.Collections.Generic.IEnumerable[typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @staticmethod
    @overload
    def min(source: System.Collections.Generic.IEnumerable[float]) -> float:
        ...

    @staticmethod
    @overload
    def min(source: System.Collections.Generic.IEnumerable[typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @staticmethod
    @overload
    def min(source: System.Collections.Generic.IEnumerable[float]) -> float:
        ...

    @staticmethod
    @overload
    def min(source: System.Collections.Generic.IEnumerable[typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @staticmethod
    @overload
    def min(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Min_TSource]) -> System_Linq_Enumerable_Min_TSource:
        ...

    @staticmethod
    @overload
    def min(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Min_TSource], comparer: System.Collections.Generic.IComparer[System_Linq_Enumerable_Min_TSource]) -> System_Linq_Enumerable_Min_TSource:
        """
        Returns the minimum value in a generic sequence.
        
        :param source: A sequence of values to determine the minimum value of.
        :param comparer: The IComparer{T} to compare values.
        :returns: The minimum value in the sequence.
        """
        ...

    @staticmethod
    @overload
    def min(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Min_TSource], selector: typing.Callable[[System_Linq_Enumerable_Min_TSource], int]) -> int:
        ...

    @staticmethod
    @overload
    def min(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Min_TSource], selector: typing.Callable[[System_Linq_Enumerable_Min_TSource], typing.Optional[int]]) -> typing.Optional[int]:
        ...

    @staticmethod
    @overload
    def min(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Min_TSource], selector: typing.Callable[[System_Linq_Enumerable_Min_TSource], int]) -> int:
        ...

    @staticmethod
    @overload
    def min(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Min_TSource], selector: typing.Callable[[System_Linq_Enumerable_Min_TSource], typing.Optional[int]]) -> typing.Optional[int]:
        ...

    @staticmethod
    @overload
    def min(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Min_TSource], selector: typing.Callable[[System_Linq_Enumerable_Min_TSource], float]) -> float:
        ...

    @staticmethod
    @overload
    def min(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Min_TSource], selector: typing.Callable[[System_Linq_Enumerable_Min_TSource], typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @staticmethod
    @overload
    def min(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Min_TSource], selector: typing.Callable[[System_Linq_Enumerable_Min_TSource], float]) -> float:
        ...

    @staticmethod
    @overload
    def min(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Min_TSource], selector: typing.Callable[[System_Linq_Enumerable_Min_TSource], typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @staticmethod
    @overload
    def min(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Min_TSource], selector: typing.Callable[[System_Linq_Enumerable_Min_TSource], float]) -> float:
        ...

    @staticmethod
    @overload
    def min(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Min_TSource], selector: typing.Callable[[System_Linq_Enumerable_Min_TSource], typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @staticmethod
    @overload
    def min(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Min_TSource], selector: typing.Callable[[System_Linq_Enumerable_Min_TSource], System_Linq_Enumerable_Min_TResult]) -> System_Linq_Enumerable_Min_TResult:
        ...

    @staticmethod
    @overload
    def min_by(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_MinBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_MinBy_TSource], System_Linq_Enumerable_MinBy_TKey]) -> System_Linq_Enumerable_MinBy_TSource:
        """
        Returns the minimum value in a generic sequence according to a specified key selector function.
        
        :param source: A sequence of values to determine the minimum value of.
        :param key_selector: A function to extract the key for each element.
        :returns: The value with the minimum key in the sequence.
        """
        ...

    @staticmethod
    @overload
    def min_by(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_MinBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_MinBy_TSource], System_Linq_Enumerable_MinBy_TKey], comparer: System.Collections.Generic.IComparer[System_Linq_Enumerable_MinBy_TKey]) -> System_Linq_Enumerable_MinBy_TSource:
        """
        Returns the minimum value in a generic sequence according to a specified key selector function.
        
        :param source: A sequence of values to determine the minimum value of.
        :param key_selector: A function to extract the key for each element.
        :param comparer: The IComparer{TKey} to compare keys.
        :returns: The value with the minimum key in the sequence.
        """
        ...

    @staticmethod
    def of_type(source: System.Collections.IEnumerable) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_OfType_TResult]:
        ...

    @staticmethod
    @overload
    def order(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Order_T]) -> System.Linq.IOrderedEnumerable[System_Linq_Enumerable_Order_T]:
        """
        Sorts the elements of a sequence in ascending order.
        
        :param source: A sequence of values to order.
        :returns: An IOrderedEnumerable{TElement} whose elements are sorted.
        """
        ...

    @staticmethod
    @overload
    def order(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Order_T], comparer: System.Collections.Generic.IComparer[System_Linq_Enumerable_Order_T]) -> System.Linq.IOrderedEnumerable[System_Linq_Enumerable_Order_T]:
        """
        Sorts the elements of a sequence in ascending order.
        
        :param source: A sequence of values to order.
        :param comparer: An IComparer{T} to compare keys.
        :returns: An IOrderedEnumerable{TElement} whose elements are sorted.
        """
        ...

    @staticmethod
    @overload
    def order_by(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_OrderBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_OrderBy_TSource], System_Linq_Enumerable_OrderBy_TKey]) -> System.Linq.IOrderedEnumerable[System_Linq_Enumerable_OrderBy_TSource]:
        ...

    @staticmethod
    @overload
    def order_by(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_OrderBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_OrderBy_TSource], System_Linq_Enumerable_OrderBy_TKey], comparer: System.Collections.Generic.IComparer[System_Linq_Enumerable_OrderBy_TKey]) -> System.Linq.IOrderedEnumerable[System_Linq_Enumerable_OrderBy_TSource]:
        ...

    @staticmethod
    @overload
    def order_by_descending(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_OrderByDescending_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_OrderByDescending_TSource], System_Linq_Enumerable_OrderByDescending_TKey]) -> System.Linq.IOrderedEnumerable[System_Linq_Enumerable_OrderByDescending_TSource]:
        ...

    @staticmethod
    @overload
    def order_by_descending(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_OrderByDescending_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_OrderByDescending_TSource], System_Linq_Enumerable_OrderByDescending_TKey], comparer: System.Collections.Generic.IComparer[System_Linq_Enumerable_OrderByDescending_TKey]) -> System.Linq.IOrderedEnumerable[System_Linq_Enumerable_OrderByDescending_TSource]:
        ...

    @staticmethod
    @overload
    def order_descending(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_OrderDescending_T]) -> System.Linq.IOrderedEnumerable[System_Linq_Enumerable_OrderDescending_T]:
        """
        Sorts the elements of a sequence in descending order.
        
        :param source: A sequence of values to order.
        :returns: An IOrderedEnumerable{TElement} whose elements are sorted.
        """
        ...

    @staticmethod
    @overload
    def order_descending(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_OrderDescending_T], comparer: System.Collections.Generic.IComparer[System_Linq_Enumerable_OrderDescending_T]) -> System.Linq.IOrderedEnumerable[System_Linq_Enumerable_OrderDescending_T]:
        """
        Sorts the elements of a sequence in descending order.
        
        :param source: A sequence of values to order.
        :param comparer: An IComparer{T} to compare keys.
        :returns: An IOrderedEnumerable{TElement} whose elements are sorted.
        """
        ...

    @staticmethod
    def prepend(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Prepend_TSource], element: System_Linq_Enumerable_Prepend_TSource) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Prepend_TSource]:
        ...

    @staticmethod
    def range(start: int, count: int) -> System.Collections.Generic.IEnumerable[int]:
        ...

    @staticmethod
    def repeat(element: System_Linq_Enumerable_Repeat_TResult, count: int) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Repeat_TResult]:
        ...

    @staticmethod
    @overload
    def reverse(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Reverse_TSource]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Reverse_TSource]:
        ...

    @staticmethod
    @overload
    def reverse(source: typing.List[System_Linq_Enumerable_Reverse_TSource]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Reverse_TSource]:
        ...

    @staticmethod
    @overload
    def select(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Select_TSource], selector: typing.Callable[[System_Linq_Enumerable_Select_TSource], System_Linq_Enumerable_Select_TResult]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Select_TResult]:
        ...

    @staticmethod
    @overload
    def select(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Select_TSource], selector: typing.Callable[[System_Linq_Enumerable_Select_TSource, int], System_Linq_Enumerable_Select_TResult]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Select_TResult]:
        ...

    @staticmethod
    @overload
    def select_many(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SelectMany_TSource], selector: typing.Callable[[System_Linq_Enumerable_SelectMany_TSource], System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SelectMany_TResult]]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SelectMany_TResult]:
        ...

    @staticmethod
    @overload
    def select_many(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SelectMany_TSource], selector: typing.Callable[[System_Linq_Enumerable_SelectMany_TSource, int], System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SelectMany_TResult]]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SelectMany_TResult]:
        ...

    @staticmethod
    @overload
    def select_many(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SelectMany_TSource], collection_selector: typing.Callable[[System_Linq_Enumerable_SelectMany_TSource, int], System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SelectMany_TCollection]], result_selector: typing.Callable[[System_Linq_Enumerable_SelectMany_TSource, System_Linq_Enumerable_SelectMany_TCollection], System_Linq_Enumerable_SelectMany_TResult]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SelectMany_TResult]:
        ...

    @staticmethod
    @overload
    def select_many(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SelectMany_TSource], collection_selector: typing.Callable[[System_Linq_Enumerable_SelectMany_TSource], System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SelectMany_TCollection]], result_selector: typing.Callable[[System_Linq_Enumerable_SelectMany_TSource, System_Linq_Enumerable_SelectMany_TCollection], System_Linq_Enumerable_SelectMany_TResult]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SelectMany_TResult]:
        ...

    @staticmethod
    @overload
    def sequence_equal(first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SequenceEqual_TSource], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SequenceEqual_TSource]) -> bool:
        ...

    @staticmethod
    @overload
    def sequence_equal(first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SequenceEqual_TSource], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SequenceEqual_TSource], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_SequenceEqual_TSource]) -> bool:
        ...

    @staticmethod
    @overload
    def single(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Single_TSource]) -> System_Linq_Enumerable_Single_TSource:
        ...

    @staticmethod
    @overload
    def single(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Single_TSource], predicate: typing.Callable[[System_Linq_Enumerable_Single_TSource], bool]) -> System_Linq_Enumerable_Single_TSource:
        ...

    @staticmethod
    @overload
    def single_or_default(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SingleOrDefault_TSource]) -> System_Linq_Enumerable_SingleOrDefault_TSource:
        ...

    @staticmethod
    @overload
    def single_or_default(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SingleOrDefault_TSource], default_value: System_Linq_Enumerable_SingleOrDefault_TSource) -> System_Linq_Enumerable_SingleOrDefault_TSource:
        """
        Returns the only element of a sequence, or a default value if the sequence is empty; this method throws an exception if there is more than one element in the sequence.
        
        :param source: An IEnumerable{T} to return the single element of.
        :param default_value: The default value to return if the sequence is empty.
        :returns: The single element of the input sequence, or  if the sequence contains no elements.
        """
        ...

    @staticmethod
    @overload
    def single_or_default(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SingleOrDefault_TSource], predicate: typing.Callable[[System_Linq_Enumerable_SingleOrDefault_TSource], bool]) -> System_Linq_Enumerable_SingleOrDefault_TSource:
        ...

    @staticmethod
    @overload
    def single_or_default(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SingleOrDefault_TSource], predicate: typing.Callable[[System_Linq_Enumerable_SingleOrDefault_TSource], bool], default_value: System_Linq_Enumerable_SingleOrDefault_TSource) -> System_Linq_Enumerable_SingleOrDefault_TSource:
        """
        Returns the only element of a sequence that satisfies a specified condition or a default value if no such element exists; this method throws an exception if more than one element satisfies the condition.
        
        :param source: An IEnumerable{T} to return a single element from.
        :param predicate: A function to test an element for a condition.
        :param default_value: The default value to return if the sequence is empty.
        :returns: The single element of the input sequence that satisfies the condition, or  if no such element is found.
        """
        ...

    @staticmethod
    def skip(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Skip_TSource], count: int) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Skip_TSource]:
        ...

    @staticmethod
    def skip_last(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SkipLast_TSource], count: int) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SkipLast_TSource]:
        ...

    @staticmethod
    @overload
    def skip_while(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SkipWhile_TSource], predicate: typing.Callable[[System_Linq_Enumerable_SkipWhile_TSource], bool]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SkipWhile_TSource]:
        ...

    @staticmethod
    @overload
    def skip_while(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SkipWhile_TSource], predicate: typing.Callable[[System_Linq_Enumerable_SkipWhile_TSource, int], bool]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_SkipWhile_TSource]:
        ...

    @staticmethod
    @overload
    def sum(source: System.Collections.Generic.IEnumerable[int]) -> int:
        ...

    @staticmethod
    @overload
    def sum(source: System.Collections.Generic.IEnumerable[int]) -> int:
        ...

    @staticmethod
    @overload
    def sum(source: System.Collections.Generic.IEnumerable[float]) -> float:
        ...

    @staticmethod
    @overload
    def sum(source: System.Collections.Generic.IEnumerable[float]) -> float:
        ...

    @staticmethod
    @overload
    def sum(source: System.Collections.Generic.IEnumerable[float]) -> float:
        ...

    @staticmethod
    @overload
    def sum(source: System.Collections.Generic.IEnumerable[typing.Optional[int]]) -> typing.Optional[int]:
        ...

    @staticmethod
    @overload
    def sum(source: System.Collections.Generic.IEnumerable[typing.Optional[int]]) -> typing.Optional[int]:
        ...

    @staticmethod
    @overload
    def sum(source: System.Collections.Generic.IEnumerable[typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @staticmethod
    @overload
    def sum(source: System.Collections.Generic.IEnumerable[typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @staticmethod
    @overload
    def sum(source: System.Collections.Generic.IEnumerable[typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @staticmethod
    @overload
    def sum(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Sum_TSource], selector: typing.Callable[[System_Linq_Enumerable_Sum_TSource], int]) -> int:
        ...

    @staticmethod
    @overload
    def sum(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Sum_TSource], selector: typing.Callable[[System_Linq_Enumerable_Sum_TSource], int]) -> int:
        ...

    @staticmethod
    @overload
    def sum(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Sum_TSource], selector: typing.Callable[[System_Linq_Enumerable_Sum_TSource], float]) -> float:
        ...

    @staticmethod
    @overload
    def sum(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Sum_TSource], selector: typing.Callable[[System_Linq_Enumerable_Sum_TSource], float]) -> float:
        ...

    @staticmethod
    @overload
    def sum(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Sum_TSource], selector: typing.Callable[[System_Linq_Enumerable_Sum_TSource], float]) -> float:
        ...

    @staticmethod
    @overload
    def sum(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Sum_TSource], selector: typing.Callable[[System_Linq_Enumerable_Sum_TSource], typing.Optional[int]]) -> typing.Optional[int]:
        ...

    @staticmethod
    @overload
    def sum(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Sum_TSource], selector: typing.Callable[[System_Linq_Enumerable_Sum_TSource], typing.Optional[int]]) -> typing.Optional[int]:
        ...

    @staticmethod
    @overload
    def sum(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Sum_TSource], selector: typing.Callable[[System_Linq_Enumerable_Sum_TSource], typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @staticmethod
    @overload
    def sum(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Sum_TSource], selector: typing.Callable[[System_Linq_Enumerable_Sum_TSource], typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @staticmethod
    @overload
    def sum(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Sum_TSource], selector: typing.Callable[[System_Linq_Enumerable_Sum_TSource], typing.Optional[float]]) -> typing.Optional[float]:
        ...

    @staticmethod
    @overload
    def take(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Take_TSource], count: int) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Take_TSource]:
        ...

    @staticmethod
    @overload
    def take(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Take_TSource], range: System.Range) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Take_TSource]:
        """
        Returns a specified range of contiguous elements from a sequence.
        
        :param source: The sequence to return elements from.
        :param range: The range of elements to return, which has start and end indexes either from the start or the end.
        :returns: An IEnumerable{T} that contains the specified  of elements from the  sequence.
        """
        ...

    @staticmethod
    def take_last(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_TakeLast_TSource], count: int) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_TakeLast_TSource]:
        ...

    @staticmethod
    @overload
    def take_while(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_TakeWhile_TSource], predicate: typing.Callable[[System_Linq_Enumerable_TakeWhile_TSource], bool]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_TakeWhile_TSource]:
        ...

    @staticmethod
    @overload
    def take_while(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_TakeWhile_TSource], predicate: typing.Callable[[System_Linq_Enumerable_TakeWhile_TSource, int], bool]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_TakeWhile_TSource]:
        ...

    @staticmethod
    @overload
    def then_by(source: System.Linq.IOrderedEnumerable[System_Linq_Enumerable_ThenBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_ThenBy_TSource], System_Linq_Enumerable_ThenBy_TKey]) -> System.Linq.IOrderedEnumerable[System_Linq_Enumerable_ThenBy_TSource]:
        ...

    @staticmethod
    @overload
    def then_by(source: System.Linq.IOrderedEnumerable[System_Linq_Enumerable_ThenBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_ThenBy_TSource], System_Linq_Enumerable_ThenBy_TKey], comparer: System.Collections.Generic.IComparer[System_Linq_Enumerable_ThenBy_TKey]) -> System.Linq.IOrderedEnumerable[System_Linq_Enumerable_ThenBy_TSource]:
        ...

    @staticmethod
    @overload
    def then_by_descending(source: System.Linq.IOrderedEnumerable[System_Linq_Enumerable_ThenByDescending_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_ThenByDescending_TSource], System_Linq_Enumerable_ThenByDescending_TKey]) -> System.Linq.IOrderedEnumerable[System_Linq_Enumerable_ThenByDescending_TSource]:
        ...

    @staticmethod
    @overload
    def then_by_descending(source: System.Linq.IOrderedEnumerable[System_Linq_Enumerable_ThenByDescending_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_ThenByDescending_TSource], System_Linq_Enumerable_ThenByDescending_TKey], comparer: System.Collections.Generic.IComparer[System_Linq_Enumerable_ThenByDescending_TKey]) -> System.Linq.IOrderedEnumerable[System_Linq_Enumerable_ThenByDescending_TSource]:
        ...

    @staticmethod
    def to_array(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ToArray_TSource]) -> typing.List[System_Linq_Enumerable_ToArray_TSource]:
        ...

    @staticmethod
    @overload
    def to_dictionary(source: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Linq_Enumerable_ToDictionary_TKey, System_Linq_Enumerable_ToDictionary_TValue]]) -> System.Collections.Generic.Dictionary[System_Linq_Enumerable_ToDictionary_TKey, System_Linq_Enumerable_ToDictionary_TValue]:
        """
        Creates a Dictionary{TKey,TValue} from an IEnumerable{T} according to the default comparer for the key type.
        
        :param source: The IEnumerable{T} to create a Dictionary{TKey,TValue} from.
        :returns: A Dictionary{TKey,TValue} that contains keys and values from  and uses default comparer for the key type.
        """
        ...

    @staticmethod
    @overload
    def to_dictionary(source: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[System_Linq_Enumerable_ToDictionary_TKey, System_Linq_Enumerable_ToDictionary_TValue]], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_ToDictionary_TKey]) -> System.Collections.Generic.Dictionary[System_Linq_Enumerable_ToDictionary_TKey, System_Linq_Enumerable_ToDictionary_TValue]:
        """
        Creates a Dictionary{TKey,TValue} from an IEnumerable{T} according to specified key comparer.
        
        :param source: The IEnumerable{T} to create a Dictionary{TKey,TValue} from.
        :param comparer: An IEqualityComparer{TKey} to compare keys.
        :returns: A Dictionary{TKey,TValue} that contains keys and values from .
        """
        ...

    @staticmethod
    @overload
    def to_dictionary(source: System.Collections.Generic.IEnumerable[System.ValueTuple[System_Linq_Enumerable_ToDictionary_TKey, System_Linq_Enumerable_ToDictionary_TValue]]) -> System.Collections.Generic.Dictionary[System_Linq_Enumerable_ToDictionary_TKey, System_Linq_Enumerable_ToDictionary_TValue]:
        """
        Creates a Dictionary{TKey,TValue} from an IEnumerable{T} according to the default comparer for the key type.
        
        :param source: The IEnumerable{T} to create a Dictionary{TKey,TValue} from.
        :returns: A Dictionary{TKey,TValue} that contains keys and values from  and uses default comparer for the key type.
        """
        ...

    @staticmethod
    @overload
    def to_dictionary(source: System.Collections.Generic.IEnumerable[System.ValueTuple[System_Linq_Enumerable_ToDictionary_TKey, System_Linq_Enumerable_ToDictionary_TValue]], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_ToDictionary_TKey]) -> System.Collections.Generic.Dictionary[System_Linq_Enumerable_ToDictionary_TKey, System_Linq_Enumerable_ToDictionary_TValue]:
        """
        Creates a Dictionary{TKey,TValue} from an IEnumerable{T} according to specified key comparer.
        
        :param source: The IEnumerable{T} to create a Dictionary{TKey,TValue} from.
        :param comparer: An IEqualityComparer{TKey} to compare keys.
        :returns: A Dictionary{TKey,TValue} that contains keys and values from .
        """
        ...

    @staticmethod
    @overload
    def to_dictionary(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ToDictionary_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_ToDictionary_TSource], System_Linq_Enumerable_ToDictionary_TKey]) -> System.Collections.Generic.Dictionary[System_Linq_Enumerable_ToDictionary_TKey, System_Linq_Enumerable_ToDictionary_TSource]:
        ...

    @staticmethod
    @overload
    def to_dictionary(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ToDictionary_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_ToDictionary_TSource], System_Linq_Enumerable_ToDictionary_TKey], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_ToDictionary_TKey]) -> System.Collections.Generic.Dictionary[System_Linq_Enumerable_ToDictionary_TKey, System_Linq_Enumerable_ToDictionary_TSource]:
        ...

    @staticmethod
    @overload
    def to_dictionary(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ToDictionary_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_ToDictionary_TSource], System_Linq_Enumerable_ToDictionary_TKey], element_selector: typing.Callable[[System_Linq_Enumerable_ToDictionary_TSource], System_Linq_Enumerable_ToDictionary_TElement]) -> System.Collections.Generic.Dictionary[System_Linq_Enumerable_ToDictionary_TKey, System_Linq_Enumerable_ToDictionary_TElement]:
        ...

    @staticmethod
    @overload
    def to_dictionary(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ToDictionary_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_ToDictionary_TSource], System_Linq_Enumerable_ToDictionary_TKey], element_selector: typing.Callable[[System_Linq_Enumerable_ToDictionary_TSource], System_Linq_Enumerable_ToDictionary_TElement], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_ToDictionary_TKey]) -> System.Collections.Generic.Dictionary[System_Linq_Enumerable_ToDictionary_TKey, System_Linq_Enumerable_ToDictionary_TElement]:
        ...

    @staticmethod
    @overload
    def to_hash_set(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ToHashSet_TSource]) -> System.Collections.Generic.HashSet[System_Linq_Enumerable_ToHashSet_TSource]:
        ...

    @staticmethod
    @overload
    def to_hash_set(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ToHashSet_TSource], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_ToHashSet_TSource]) -> System.Collections.Generic.HashSet[System_Linq_Enumerable_ToHashSet_TSource]:
        ...

    @staticmethod
    def to_list(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ToList_TSource]) -> System.Collections.Generic.List[System_Linq_Enumerable_ToList_TSource]:
        ...

    @staticmethod
    @overload
    def to_lookup(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ToLookup_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_ToLookup_TSource], System_Linq_Enumerable_ToLookup_TKey]) -> System.Linq.ILookup[System_Linq_Enumerable_ToLookup_TKey, System_Linq_Enumerable_ToLookup_TSource]:
        ...

    @staticmethod
    @overload
    def to_lookup(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ToLookup_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_ToLookup_TSource], System_Linq_Enumerable_ToLookup_TKey], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_ToLookup_TKey]) -> System.Linq.ILookup[System_Linq_Enumerable_ToLookup_TKey, System_Linq_Enumerable_ToLookup_TSource]:
        ...

    @staticmethod
    @overload
    def to_lookup(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ToLookup_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_ToLookup_TSource], System_Linq_Enumerable_ToLookup_TKey], element_selector: typing.Callable[[System_Linq_Enumerable_ToLookup_TSource], System_Linq_Enumerable_ToLookup_TElement]) -> System.Linq.ILookup[System_Linq_Enumerable_ToLookup_TKey, System_Linq_Enumerable_ToLookup_TElement]:
        ...

    @staticmethod
    @overload
    def to_lookup(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_ToLookup_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_ToLookup_TSource], System_Linq_Enumerable_ToLookup_TKey], element_selector: typing.Callable[[System_Linq_Enumerable_ToLookup_TSource], System_Linq_Enumerable_ToLookup_TElement], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_ToLookup_TKey]) -> System.Linq.ILookup[System_Linq_Enumerable_ToLookup_TKey, System_Linq_Enumerable_ToLookup_TElement]:
        ...

    @staticmethod
    def try_get_non_enumerated_count(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_TryGetNonEnumeratedCount_TSource], count: typing.Optional[int]) -> typing.Union[bool, int]:
        """
        Attempts to determine the number of elements in a sequence without forcing an enumeration.
        
        :param source: A sequence that contains elements to be counted.
        :param count: When this method returns, contains the count of  if successful,     or zero if the method failed to determine the count.
        :returns: true if the count of  can be determined without enumeration;   otherwise, false.
        """
        ...

    @staticmethod
    @overload
    def union(first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Union_TSource], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Union_TSource]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Union_TSource]:
        ...

    @staticmethod
    @overload
    def union(first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Union_TSource], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Union_TSource], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_Union_TSource]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Union_TSource]:
        ...

    @staticmethod
    @overload
    def union_by(first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_UnionBy_TSource], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_UnionBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_UnionBy_TSource], System_Linq_Enumerable_UnionBy_TKey]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_UnionBy_TSource]:
        """
        Produces the set union of two sequences according to a specified key selector function.
        
        :param first: An IEnumerable{T} whose distinct elements form the first set for the union.
        :param second: An IEnumerable{T} whose distinct elements form the second set for the union.
        :param key_selector: A function to extract the key for each element.
        :returns: An IEnumerable{T} that contains the elements from both input sequences, excluding duplicates.
        """
        ...

    @staticmethod
    @overload
    def union_by(first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_UnionBy_TSource], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_UnionBy_TSource], key_selector: typing.Callable[[System_Linq_Enumerable_UnionBy_TSource], System_Linq_Enumerable_UnionBy_TKey], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_Enumerable_UnionBy_TKey]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_UnionBy_TSource]:
        """
        Produces the set union of two sequences according to a specified key selector function.
        
        :param first: An IEnumerable{T} whose distinct elements form the first set for the union.
        :param second: An IEnumerable{T} whose distinct elements form the second set for the union.
        :param key_selector: A function to extract the key for each element.
        :param comparer: The IEqualityComparer{T} to compare values.
        :returns: An IEnumerable{T} that contains the elements from both input sequences, excluding duplicates.
        """
        ...

    @staticmethod
    @overload
    def where(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Where_TSource], predicate: typing.Callable[[System_Linq_Enumerable_Where_TSource], bool]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Where_TSource]:
        ...

    @staticmethod
    @overload
    def where(source: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Where_TSource], predicate: typing.Callable[[System_Linq_Enumerable_Where_TSource, int], bool]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Where_TSource]:
        ...

    @staticmethod
    @overload
    def zip(first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Zip_TFirst], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Zip_TSecond], result_selector: typing.Callable[[System_Linq_Enumerable_Zip_TFirst, System_Linq_Enumerable_Zip_TSecond], System_Linq_Enumerable_Zip_TResult]) -> System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Zip_TResult]:
        ...

    @staticmethod
    @overload
    def zip(first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Zip_TFirst], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Zip_TSecond]) -> System.Collections.Generic.IEnumerable[System.ValueTuple[System_Linq_Enumerable_Zip_TFirst, System_Linq_Enumerable_Zip_TSecond]]:
        ...

    @staticmethod
    @overload
    def zip(first: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Zip_TFirst], second: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Zip_TSecond], third: System.Collections.Generic.IEnumerable[System_Linq_Enumerable_Zip_TThird]) -> System.Collections.Generic.IEnumerable[System.ValueTuple[System_Linq_Enumerable_Zip_TFirst, System_Linq_Enumerable_Zip_TSecond, System_Linq_Enumerable_Zip_TThird]]:
        """
        Produces a sequence of tuples with elements from the three specified sequences.
        
        :param first: The first sequence to merge.
        :param second: The second sequence to merge.
        :param third: The third sequence to merge.
        :returns: A sequence of tuples with elements taken from the first, second, and third sequences, in that order.
        """
        ...


class Lookup(typing.Generic[System_Linq_Lookup_TKey, System_Linq_Lookup_TElement], System.Object, System.Linq.ILookup[System_Linq_Lookup_TKey, System_Linq_Lookup_TElement], typing.Iterable[System.Linq.IGrouping[System_Linq_Lookup_TKey, System_Linq_Lookup_TElement]]):
    """This class has no documentation."""

    @property
    def count(self) -> int:
        ...

    def __getitem__(self, key: System_Linq_Lookup_TKey) -> System.Collections.Generic.IEnumerable[System_Linq_Lookup_TElement]:
        ...

    def apply_result_selector(self, result_selector: typing.Callable[[System_Linq_Lookup_TKey, System.Collections.Generic.IEnumerable[System_Linq_Lookup_TElement]], System_Linq_Lookup_ApplyResultSelector_TResult]) -> System.Collections.Generic.IEnumerable[System_Linq_Lookup_ApplyResultSelector_TResult]:
        ...

    def contains(self, key: System_Linq_Lookup_TKey) -> bool:
        ...

    def get_enumerator(self) -> System.Collections.Generic.IEnumerator[System.Linq.IGrouping[System_Linq_Lookup_TKey, System_Linq_Lookup_TElement]]:
        ...


