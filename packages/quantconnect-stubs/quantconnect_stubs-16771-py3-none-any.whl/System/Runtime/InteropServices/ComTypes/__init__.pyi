from typing import overload
from enum import Enum
import abc
import typing

import System
import System.Runtime.InteropServices.ComTypes


class CONNECTDATA:
    """This class has no documentation."""

    @property
    def p_unk(self) -> System.Object:
        ...

    @property
    def dw_cookie(self) -> int:
        ...


class IEnumConnections(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def clone(self, ppenum: typing.Optional[System.Runtime.InteropServices.ComTypes.IEnumConnections]) -> typing.Union[None, System.Runtime.InteropServices.ComTypes.IEnumConnections]:
        ...

    def next(self, celt: int, rgelt: typing.List[System.Runtime.InteropServices.ComTypes.CONNECTDATA], pcelt_fetched: System.IntPtr) -> int:
        ...

    def reset(self) -> None:
        ...

    def skip(self, celt: int) -> int:
        ...


class IConnectionPoint(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def advise(self, p_unk_sink: typing.Any, pdw_cookie: typing.Optional[int]) -> typing.Union[None, int]:
        ...

    def enum_connections(self, pp_enum: typing.Optional[System.Runtime.InteropServices.ComTypes.IEnumConnections]) -> typing.Union[None, System.Runtime.InteropServices.ComTypes.IEnumConnections]:
        ...

    def get_connection_interface(self, p_iid: typing.Optional[System.Guid]) -> typing.Union[None, System.Guid]:
        ...

    def get_connection_point_container(self, pp_cpc: typing.Optional[System.Runtime.InteropServices.ComTypes.IConnectionPointContainer]) -> typing.Union[None, System.Runtime.InteropServices.ComTypes.IConnectionPointContainer]:
        ...

    def unadvise(self, dw_cookie: int) -> None:
        ...


class IEnumConnectionPoints(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def clone(self, ppenum: typing.Optional[System.Runtime.InteropServices.ComTypes.IEnumConnectionPoints]) -> typing.Union[None, System.Runtime.InteropServices.ComTypes.IEnumConnectionPoints]:
        ...

    def next(self, celt: int, rgelt: typing.List[System.Runtime.InteropServices.ComTypes.IConnectionPoint], pcelt_fetched: System.IntPtr) -> int:
        ...

    def reset(self) -> None:
        ...

    def skip(self, celt: int) -> int:
        ...


class TYPEKIND(Enum):
    """This class has no documentation."""

    TKIND_ENUM = 0

    TKIND_RECORD = ...

    TKIND_MODULE = ...

    TKIND_INTERFACE = ...

    TKIND_DISPATCH = ...

    TKIND_COCLASS = ...

    TKIND_ALIAS = ...

    TKIND_UNION = ...

    TKIND_MAX = ...


class ITypeLib(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def find_name(self, sz_name_buf: str, l_hash_val: int, pp_t_info: typing.List[System.Runtime.InteropServices.ComTypes.ITypeInfo], rg_mem_id: typing.List[int], pc_found: int) -> None:
        ...

    def get_documentation(self, index: int, str_name: typing.Optional[str], str_doc_string: typing.Optional[str], dw_help_context: typing.Optional[int], str_help_file: typing.Optional[str]) -> typing.Union[None, str, str, int, str]:
        ...

    def get_lib_attr(self, pp_t_lib_attr: typing.Optional[System.IntPtr]) -> typing.Union[None, System.IntPtr]:
        ...

    def get_type_comp(self, pp_t_comp: typing.Optional[System.Runtime.InteropServices.ComTypes.ITypeComp]) -> typing.Union[None, System.Runtime.InteropServices.ComTypes.ITypeComp]:
        ...

    def get_type_info(self, index: int, pp_ti: typing.Optional[System.Runtime.InteropServices.ComTypes.ITypeInfo]) -> typing.Union[None, System.Runtime.InteropServices.ComTypes.ITypeInfo]:
        ...

    def get_type_info_count(self) -> int:
        ...

    def get_type_info_of_guid(self, guid: System.Guid, pp_t_info: typing.Optional[System.Runtime.InteropServices.ComTypes.ITypeInfo]) -> typing.Union[None, System.Runtime.InteropServices.ComTypes.ITypeInfo]:
        ...

    def get_type_info_type(self, index: int, p_t_kind: typing.Optional[System.Runtime.InteropServices.ComTypes.TYPEKIND]) -> typing.Union[None, System.Runtime.InteropServices.ComTypes.TYPEKIND]:
        ...

    def is_name(self, sz_name_buf: str, l_hash_val: int) -> bool:
        ...

    def release_t_lib_attr(self, p_t_lib_attr: System.IntPtr) -> None:
        ...


class ITypeLib2(System.Runtime.InteropServices.ComTypes.ITypeLib, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def get_all_cust_data(self, p_cust_data: System.IntPtr) -> None:
        ...

    def get_cust_data(self, guid: System.Guid, p_var_val: typing.Optional[typing.Any]) -> typing.Union[None, typing.Any]:
        ...

    def get_documentation_2(self, index: int, pbstr_help_string: typing.Optional[str], pdw_help_string_context: typing.Optional[int], pbstr_help_string_dll: typing.Optional[str]) -> typing.Union[None, str, int, str]:
        ...

    def get_lib_statistics(self, pc_unique_names: System.IntPtr, pcch_unique_names: typing.Optional[int]) -> typing.Union[None, int]:
        ...


class IEnumVARIANT(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def clone(self) -> System.Runtime.InteropServices.ComTypes.IEnumVARIANT:
        ...

    def next(self, celt: int, rg_var: typing.List[System.Object], pcelt_fetched: System.IntPtr) -> int:
        ...

    def reset(self) -> int:
        ...

    def skip(self, celt: int) -> int:
        ...


class FILETIME:
    """This class has no documentation."""

    @property
    def dw_low_date_time(self) -> int:
        ...

    @property
    def dw_high_date_time(self) -> int:
        ...


class STATSTG:
    """This class has no documentation."""

    @property
    def pwcs_name(self) -> str:
        ...

    @property
    def type(self) -> int:
        ...

    @property
    def cb_size(self) -> int:
        ...

    @property
    def mtime(self) -> System.Runtime.InteropServices.ComTypes.FILETIME:
        ...

    @property
    def ctime(self) -> System.Runtime.InteropServices.ComTypes.FILETIME:
        ...

    @property
    def atime(self) -> System.Runtime.InteropServices.ComTypes.FILETIME:
        ...

    @property
    def grf_mode(self) -> int:
        ...

    @property
    def grf_locks_supported(self) -> int:
        ...

    @property
    def clsid(self) -> System.Guid:
        ...

    @property
    def grf_state_bits(self) -> int:
        ...

    @property
    def reserved(self) -> int:
        ...


class IStream(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def clone(self, ppstm: typing.Optional[System.Runtime.InteropServices.ComTypes.IStream]) -> typing.Union[None, System.Runtime.InteropServices.ComTypes.IStream]:
        ...

    def commit(self, grf_commit_flags: int) -> None:
        ...

    def copy_to(self, pstm: System.Runtime.InteropServices.ComTypes.IStream, cb: int, pcb_read: System.IntPtr, pcb_written: System.IntPtr) -> None:
        ...

    def lock_region(self, lib_offset: int, cb: int, dw_lock_type: int) -> None:
        ...

    def read(self, pv: typing.List[int], cb: int, pcb_read: System.IntPtr) -> None:
        ...

    def revert(self) -> None:
        ...

    def seek(self, dlib_move: int, dw_origin: int, plib_new_position: System.IntPtr) -> None:
        ...

    def set_size(self, lib_new_size: int) -> None:
        ...

    def stat(self, pstatstg: typing.Optional[System.Runtime.InteropServices.ComTypes.STATSTG], grf_stat_flag: int) -> typing.Union[None, System.Runtime.InteropServices.ComTypes.STATSTG]:
        ...

    def unlock_region(self, lib_offset: int, cb: int, dw_lock_type: int) -> None:
        ...

    def write(self, pv: typing.List[int], cb: int, pcb_written: System.IntPtr) -> None:
        ...


class IEnumMoniker(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def clone(self, ppenum: typing.Optional[System.Runtime.InteropServices.ComTypes.IEnumMoniker]) -> typing.Union[None, System.Runtime.InteropServices.ComTypes.IEnumMoniker]:
        ...

    def next(self, celt: int, rgelt: typing.List[System.Runtime.InteropServices.ComTypes.IMoniker], pcelt_fetched: System.IntPtr) -> int:
        ...

    def reset(self) -> None:
        ...

    def skip(self, celt: int) -> int:
        ...


class IMoniker(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def bind_to_object(self, pbc: System.Runtime.InteropServices.ComTypes.IBindCtx, pmk_to_left: System.Runtime.InteropServices.ComTypes.IMoniker, riid_result: System.Guid, ppv_result: typing.Optional[typing.Any]) -> typing.Union[None, typing.Any]:
        ...

    def bind_to_storage(self, pbc: System.Runtime.InteropServices.ComTypes.IBindCtx, pmk_to_left: System.Runtime.InteropServices.ComTypes.IMoniker, riid: System.Guid, ppv_obj: typing.Optional[typing.Any]) -> typing.Union[None, typing.Any]:
        ...

    def common_prefix_with(self, pmk_other: System.Runtime.InteropServices.ComTypes.IMoniker, ppmk_prefix: typing.Optional[System.Runtime.InteropServices.ComTypes.IMoniker]) -> typing.Union[None, System.Runtime.InteropServices.ComTypes.IMoniker]:
        ...

    def compose_with(self, pmk_right: System.Runtime.InteropServices.ComTypes.IMoniker, f_only_if_not_generic: bool, ppmk_composite: typing.Optional[System.Runtime.InteropServices.ComTypes.IMoniker]) -> typing.Union[None, System.Runtime.InteropServices.ComTypes.IMoniker]:
        ...

    def enum(self, f_forward: bool, ppenum_moniker: typing.Optional[System.Runtime.InteropServices.ComTypes.IEnumMoniker]) -> typing.Union[None, System.Runtime.InteropServices.ComTypes.IEnumMoniker]:
        ...

    def get_class_id(self, p_class_id: typing.Optional[System.Guid]) -> typing.Union[None, System.Guid]:
        ...

    def get_display_name(self, pbc: System.Runtime.InteropServices.ComTypes.IBindCtx, pmk_to_left: System.Runtime.InteropServices.ComTypes.IMoniker, ppsz_display_name: typing.Optional[str]) -> typing.Union[None, str]:
        ...

    def get_size_max(self, pcb_size: typing.Optional[int]) -> typing.Union[None, int]:
        ...

    def get_time_of_last_change(self, pbc: System.Runtime.InteropServices.ComTypes.IBindCtx, pmk_to_left: System.Runtime.InteropServices.ComTypes.IMoniker, p_file_time: typing.Optional[System.Runtime.InteropServices.ComTypes.FILETIME]) -> typing.Union[None, System.Runtime.InteropServices.ComTypes.FILETIME]:
        ...

    def hash(self, pdw_hash: typing.Optional[int]) -> typing.Union[None, int]:
        ...

    def inverse(self, ppmk: typing.Optional[System.Runtime.InteropServices.ComTypes.IMoniker]) -> typing.Union[None, System.Runtime.InteropServices.ComTypes.IMoniker]:
        ...

    def is_dirty(self) -> int:
        ...

    def is_equal(self, pmk_other_moniker: System.Runtime.InteropServices.ComTypes.IMoniker) -> int:
        ...

    def is_running(self, pbc: System.Runtime.InteropServices.ComTypes.IBindCtx, pmk_to_left: System.Runtime.InteropServices.ComTypes.IMoniker, pmk_newly_running: System.Runtime.InteropServices.ComTypes.IMoniker) -> int:
        ...

    def is_system_moniker(self, pdw_mksys: typing.Optional[int]) -> typing.Union[int, int]:
        ...

    def load(self, p_stm: System.Runtime.InteropServices.ComTypes.IStream) -> None:
        ...

    def parse_display_name(self, pbc: System.Runtime.InteropServices.ComTypes.IBindCtx, pmk_to_left: System.Runtime.InteropServices.ComTypes.IMoniker, psz_display_name: str, pch_eaten: typing.Optional[int], ppmk_out: typing.Optional[System.Runtime.InteropServices.ComTypes.IMoniker]) -> typing.Union[None, int, System.Runtime.InteropServices.ComTypes.IMoniker]:
        ...

    def reduce(self, pbc: System.Runtime.InteropServices.ComTypes.IBindCtx, dw_reduce_how_far: int, ppmk_to_left: System.Runtime.InteropServices.ComTypes.IMoniker, ppmk_reduced: typing.Optional[System.Runtime.InteropServices.ComTypes.IMoniker]) -> typing.Union[None, System.Runtime.InteropServices.ComTypes.IMoniker]:
        ...

    def relative_path_to(self, pmk_other: System.Runtime.InteropServices.ComTypes.IMoniker, ppmk_rel_path: typing.Optional[System.Runtime.InteropServices.ComTypes.IMoniker]) -> typing.Union[None, System.Runtime.InteropServices.ComTypes.IMoniker]:
        ...

    def save(self, p_stm: System.Runtime.InteropServices.ComTypes.IStream, f_clear_dirty: bool) -> None:
        ...


class IRunningObjectTable(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def enum_running(self, ppenum_moniker: typing.Optional[System.Runtime.InteropServices.ComTypes.IEnumMoniker]) -> typing.Union[None, System.Runtime.InteropServices.ComTypes.IEnumMoniker]:
        ...

    def get_object(self, pmk_object_name: System.Runtime.InteropServices.ComTypes.IMoniker, ppunk_object: typing.Optional[typing.Any]) -> typing.Union[int, typing.Any]:
        ...

    def get_time_of_last_change(self, pmk_object_name: System.Runtime.InteropServices.ComTypes.IMoniker, pfiletime: typing.Optional[System.Runtime.InteropServices.ComTypes.FILETIME]) -> typing.Union[int, System.Runtime.InteropServices.ComTypes.FILETIME]:
        ...

    def is_running(self, pmk_object_name: System.Runtime.InteropServices.ComTypes.IMoniker) -> int:
        ...

    def note_change_time(self, dw_register: int, pfiletime: System.Runtime.InteropServices.ComTypes.FILETIME) -> None:
        ...

    def register(self, grf_flags: int, punk_object: typing.Any, pmk_object_name: System.Runtime.InteropServices.ComTypes.IMoniker) -> int:
        ...

    def revoke(self, dw_register: int) -> None:
        ...


class IPersistFile(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def get_class_id(self, p_class_id: typing.Optional[System.Guid]) -> typing.Union[None, System.Guid]:
        ...

    def get_cur_file(self, ppsz_file_name: typing.Optional[str]) -> typing.Union[None, str]:
        ...

    def is_dirty(self) -> int:
        ...

    def load(self, psz_file_name: str, dw_mode: int) -> None:
        ...

    def save(self, psz_file_name: str, f_remember: bool) -> None:
        ...

    def save_completed(self, psz_file_name: str) -> None:
        ...


class IConnectionPointContainer(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def enum_connection_points(self, pp_enum: typing.Optional[System.Runtime.InteropServices.ComTypes.IEnumConnectionPoints]) -> typing.Union[None, System.Runtime.InteropServices.ComTypes.IEnumConnectionPoints]:
        ...

    def find_connection_point(self, riid: System.Guid, pp_cp: typing.Optional[System.Runtime.InteropServices.ComTypes.IConnectionPoint]) -> typing.Union[None, System.Runtime.InteropServices.ComTypes.IConnectionPoint]:
        ...


class DESCKIND(Enum):
    """This class has no documentation."""

    DESCKIND_NONE = 0

    DESCKIND_FUNCDESC = ...

    DESCKIND_VARDESC = ...

    DESCKIND_TYPECOMP = ...

    DESCKIND_IMPLICITAPPOBJ = ...

    DESCKIND_MAX = ...


class BINDPTR:
    """This class has no documentation."""

    @property
    def lpfuncdesc(self) -> System.IntPtr:
        ...

    @property
    def lpvardesc(self) -> System.IntPtr:
        ...

    @property
    def lptcomp(self) -> System.IntPtr:
        ...


class DISPPARAMS:
    """This class has no documentation."""

    @property
    def rgvarg(self) -> System.IntPtr:
        ...

    @property
    def rgdispid_named_args(self) -> System.IntPtr:
        ...

    @property
    def c_args(self) -> int:
        ...

    @property
    def c_named_args(self) -> int:
        ...


class INVOKEKIND(Enum):
    """This class has no documentation."""

    INVOKE_FUNC = ...

    INVOKE_PROPERTYGET = ...

    INVOKE_PROPERTYPUT = ...

    INVOKE_PROPERTYPUTREF = ...


class IMPLTYPEFLAGS(Enum):
    """This class has no documentation."""

    IMPLTYPEFLAG_FDEFAULT = ...

    IMPLTYPEFLAG_FSOURCE = ...

    IMPLTYPEFLAG_FRESTRICTED = ...

    IMPLTYPEFLAG_FDEFAULTVTABLE = ...


class ITypeInfo(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def address_of_member(self, memid: int, inv_kind: System.Runtime.InteropServices.ComTypes.INVOKEKIND, ppv: typing.Optional[System.IntPtr]) -> typing.Union[None, System.IntPtr]:
        ...

    def create_instance(self, p_unk_outer: typing.Any, riid: System.Guid, ppv_obj: typing.Optional[typing.Any]) -> typing.Union[None, typing.Any]:
        ...

    def get_containing_type_lib(self, pp_tlb: typing.Optional[System.Runtime.InteropServices.ComTypes.ITypeLib], p_index: typing.Optional[int]) -> typing.Union[None, System.Runtime.InteropServices.ComTypes.ITypeLib, int]:
        ...

    def get_dll_entry(self, memid: int, inv_kind: System.Runtime.InteropServices.ComTypes.INVOKEKIND, p_bstr_dll_name: System.IntPtr, p_bstr_name: System.IntPtr, pw_ordinal: System.IntPtr) -> None:
        ...

    def get_documentation(self, index: int, str_name: typing.Optional[str], str_doc_string: typing.Optional[str], dw_help_context: typing.Optional[int], str_help_file: typing.Optional[str]) -> typing.Union[None, str, str, int, str]:
        ...

    def get_func_desc(self, index: int, pp_func_desc: typing.Optional[System.IntPtr]) -> typing.Union[None, System.IntPtr]:
        ...

    def get_i_ds_of_names(self, rgsz_names: typing.List[str], c_names: int, p_mem_id: typing.List[int]) -> None:
        ...

    def get_impl_type_flags(self, index: int, p_impl_type_flags: typing.Optional[System.Runtime.InteropServices.ComTypes.IMPLTYPEFLAGS]) -> typing.Union[None, System.Runtime.InteropServices.ComTypes.IMPLTYPEFLAGS]:
        ...

    def get_mops(self, memid: int, p_bstr_mops: typing.Optional[str]) -> typing.Union[None, str]:
        ...

    def get_names(self, memid: int, rg_bstr_names: typing.List[str], c_max_names: int, pc_names: typing.Optional[int]) -> typing.Union[None, int]:
        ...

    def get_ref_type_info(self, h_ref: int, pp_ti: typing.Optional[System.Runtime.InteropServices.ComTypes.ITypeInfo]) -> typing.Union[None, System.Runtime.InteropServices.ComTypes.ITypeInfo]:
        ...

    def get_ref_type_of_impl_type(self, index: int, href: typing.Optional[int]) -> typing.Union[None, int]:
        ...

    def get_type_attr(self, pp_type_attr: typing.Optional[System.IntPtr]) -> typing.Union[None, System.IntPtr]:
        ...

    def get_type_comp(self, pp_t_comp: typing.Optional[System.Runtime.InteropServices.ComTypes.ITypeComp]) -> typing.Union[None, System.Runtime.InteropServices.ComTypes.ITypeComp]:
        ...

    def get_var_desc(self, index: int, pp_var_desc: typing.Optional[System.IntPtr]) -> typing.Union[None, System.IntPtr]:
        ...

    def invoke(self, pv_instance: typing.Any, memid: int, w_flags: int, p_disp_params: System.Runtime.InteropServices.ComTypes.DISPPARAMS, p_var_result: System.IntPtr, p_excep_info: System.IntPtr, pu_arg_err: typing.Optional[int]) -> typing.Union[None, int]:
        ...

    def release_func_desc(self, p_func_desc: System.IntPtr) -> None:
        ...

    def release_type_attr(self, p_type_attr: System.IntPtr) -> None:
        ...

    def release_var_desc(self, p_var_desc: System.IntPtr) -> None:
        ...


class ITypeComp(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def bind(self, sz_name: str, l_hash_val: int, w_flags: int, pp_t_info: typing.Optional[System.Runtime.InteropServices.ComTypes.ITypeInfo], p_desc_kind: typing.Optional[System.Runtime.InteropServices.ComTypes.DESCKIND], p_bind_ptr: typing.Optional[System.Runtime.InteropServices.ComTypes.BINDPTR]) -> typing.Union[None, System.Runtime.InteropServices.ComTypes.ITypeInfo, System.Runtime.InteropServices.ComTypes.DESCKIND, System.Runtime.InteropServices.ComTypes.BINDPTR]:
        ...

    def bind_type(self, sz_name: str, l_hash_val: int, pp_t_info: typing.Optional[System.Runtime.InteropServices.ComTypes.ITypeInfo], pp_t_comp: typing.Optional[System.Runtime.InteropServices.ComTypes.ITypeComp]) -> typing.Union[None, System.Runtime.InteropServices.ComTypes.ITypeInfo, System.Runtime.InteropServices.ComTypes.ITypeComp]:
        ...


class BIND_OPTS:
    """This class has no documentation."""

    @property
    def cb_struct(self) -> int:
        ...

    @property
    def grf_flags(self) -> int:
        ...

    @property
    def grf_mode(self) -> int:
        ...

    @property
    def dw_tick_count_deadline(self) -> int:
        ...


class IEnumString(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def clone(self, ppenum: typing.Optional[System.Runtime.InteropServices.ComTypes.IEnumString]) -> typing.Union[None, System.Runtime.InteropServices.ComTypes.IEnumString]:
        ...

    def next(self, celt: int, rgelt: typing.List[str], pcelt_fetched: System.IntPtr) -> int:
        ...

    def reset(self) -> None:
        ...

    def skip(self, celt: int) -> int:
        ...


class IBindCtx(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def enum_object_param(self, ppenum: typing.Optional[System.Runtime.InteropServices.ComTypes.IEnumString]) -> typing.Union[None, System.Runtime.InteropServices.ComTypes.IEnumString]:
        ...

    def get_bind_options(self, pbindopts: System.Runtime.InteropServices.ComTypes.BIND_OPTS) -> None:
        ...

    def get_object_param(self, psz_key: str, ppunk: typing.Optional[typing.Any]) -> typing.Union[None, typing.Any]:
        ...

    def get_running_object_table(self, pprot: typing.Optional[System.Runtime.InteropServices.ComTypes.IRunningObjectTable]) -> typing.Union[None, System.Runtime.InteropServices.ComTypes.IRunningObjectTable]:
        ...

    def register_object_bound(self, punk: typing.Any) -> None:
        ...

    def register_object_param(self, psz_key: str, punk: typing.Any) -> None:
        ...

    def release_bound_objects(self) -> None:
        ...

    def revoke_object_bound(self, punk: typing.Any) -> None:
        ...

    def revoke_object_param(self, psz_key: str) -> int:
        ...

    def set_bind_options(self, pbindopts: System.Runtime.InteropServices.ComTypes.BIND_OPTS) -> None:
        ...


class TYPEFLAGS(Enum):
    """This class has no documentation."""

    TYPEFLAG_FAPPOBJECT = ...

    TYPEFLAG_FCANCREATE = ...

    TYPEFLAG_FLICENSED = ...

    TYPEFLAG_FPREDECLID = ...

    TYPEFLAG_FHIDDEN = ...

    TYPEFLAG_FCONTROL = ...

    TYPEFLAG_FDUAL = ...

    TYPEFLAG_FNONEXTENSIBLE = ...

    TYPEFLAG_FOLEAUTOMATION = ...

    TYPEFLAG_FRESTRICTED = ...

    TYPEFLAG_FAGGREGATABLE = ...

    TYPEFLAG_FREPLACEABLE = ...

    TYPEFLAG_FDISPATCHABLE = ...

    TYPEFLAG_FREVERSEBIND = ...

    TYPEFLAG_FPROXY = ...


class TYPEDESC:
    """This class has no documentation."""

    @property
    def lp_value(self) -> System.IntPtr:
        ...

    @property
    def vt(self) -> int:
        ...


class IDLFLAG(Enum):
    """This class has no documentation."""

    IDLFLAG_NONE = ...

    IDLFLAG_FIN = ...

    IDLFLAG_FOUT = ...

    IDLFLAG_FLCID = ...

    IDLFLAG_FRETVAL = ...


class IDLDESC:
    """This class has no documentation."""

    @property
    def dw_reserved(self) -> System.IntPtr:
        ...

    @property
    def w_idl_flags(self) -> System.Runtime.InteropServices.ComTypes.IDLFLAG:
        ...


class TYPEATTR:
    """This class has no documentation."""

    MEMBER_ID_NIL: int = ...

    @property
    def guid(self) -> System.Guid:
        ...

    @property
    def lcid(self) -> int:
        ...

    @property
    def dw_reserved(self) -> int:
        ...

    @property
    def memid_constructor(self) -> int:
        ...

    @property
    def memid_destructor(self) -> int:
        ...

    @property
    def lpstr_schema(self) -> System.IntPtr:
        ...

    @property
    def cb_size_instance(self) -> int:
        ...

    @property
    def typekind(self) -> System.Runtime.InteropServices.ComTypes.TYPEKIND:
        ...

    @property
    def c_funcs(self) -> int:
        ...

    @property
    def c_vars(self) -> int:
        ...

    @property
    def c_impl_types(self) -> int:
        ...

    @property
    def cb_size_vft(self) -> int:
        ...

    @property
    def cb_alignment(self) -> int:
        ...

    @property
    def w_type_flags(self) -> System.Runtime.InteropServices.ComTypes.TYPEFLAGS:
        ...

    @property
    def w_major_ver_num(self) -> int:
        ...

    @property
    def w_minor_ver_num(self) -> int:
        ...

    @property
    def tdesc_alias(self) -> System.Runtime.InteropServices.ComTypes.TYPEDESC:
        ...

    @property
    def idldesc_type(self) -> System.Runtime.InteropServices.ComTypes.IDLDESC:
        ...


class FUNCKIND(Enum):
    """This class has no documentation."""

    FUNC_VIRTUAL = 0

    FUNC_PUREVIRTUAL = 1

    FUNC_NONVIRTUAL = 2

    FUNC_STATIC = 3

    FUNC_DISPATCH = 4


class CALLCONV(Enum):
    """This class has no documentation."""

    CC_CDECL = 1

    CC_MSCPASCAL = 2

    CC_PASCAL = ...

    CC_MACPASCAL = 3

    CC_STDCALL = 4

    CC_RESERVED = 5

    CC_SYSCALL = 6

    CC_MPWCDECL = 7

    CC_MPWPASCAL = 8

    CC_MAX = 9


class PARAMFLAG(Enum):
    """This class has no documentation."""

    PARAMFLAG_NONE = 0

    PARAMFLAG_FIN = ...

    PARAMFLAG_FOUT = ...

    PARAMFLAG_FLCID = ...

    PARAMFLAG_FRETVAL = ...

    PARAMFLAG_FOPT = ...

    PARAMFLAG_FHASDEFAULT = ...

    PARAMFLAG_FHASCUSTDATA = ...


class PARAMDESC:
    """This class has no documentation."""

    @property
    def lp_var_value(self) -> System.IntPtr:
        ...

    @property
    def w_param_flags(self) -> System.Runtime.InteropServices.ComTypes.PARAMFLAG:
        ...


class ELEMDESC:
    """This class has no documentation."""

    class DESCUNION:
        """This class has no documentation."""

        @property
        def idldesc(self) -> System.Runtime.InteropServices.ComTypes.IDLDESC:
            ...

        @property
        def paramdesc(self) -> System.Runtime.InteropServices.ComTypes.PARAMDESC:
            ...

    @property
    def tdesc(self) -> System.Runtime.InteropServices.ComTypes.TYPEDESC:
        ...

    @property
    def desc(self) -> System.Runtime.InteropServices.ComTypes.ELEMDESC.DESCUNION:
        ...


class FUNCDESC:
    """This class has no documentation."""

    @property
    def memid(self) -> int:
        ...

    @property
    def lprgscode(self) -> System.IntPtr:
        ...

    @property
    def lprgelemdesc_param(self) -> System.IntPtr:
        ...

    @property
    def funckind(self) -> System.Runtime.InteropServices.ComTypes.FUNCKIND:
        ...

    @property
    def invkind(self) -> System.Runtime.InteropServices.ComTypes.INVOKEKIND:
        ...

    @property
    def callconv(self) -> System.Runtime.InteropServices.ComTypes.CALLCONV:
        ...

    @property
    def c_params(self) -> int:
        ...

    @property
    def c_params_opt(self) -> int:
        ...

    @property
    def o_vft(self) -> int:
        ...

    @property
    def c_scodes(self) -> int:
        ...

    @property
    def elemdesc_func(self) -> System.Runtime.InteropServices.ComTypes.ELEMDESC:
        ...

    @property
    def w_func_flags(self) -> int:
        ...


class VARKIND(Enum):
    """This class has no documentation."""

    VAR_PERINSTANCE = ...

    VAR_STATIC = ...

    VAR_CONST = ...

    VAR_DISPATCH = ...


class VARDESC:
    """This class has no documentation."""

    class DESCUNION:
        """This class has no documentation."""

        @property
        def o_inst(self) -> int:
            ...

        @property
        def lpvar_value(self) -> System.IntPtr:
            ...

    @property
    def memid(self) -> int:
        ...

    @property
    def lpstr_schema(self) -> str:
        ...

    @property
    def desc(self) -> System.Runtime.InteropServices.ComTypes.VARDESC.DESCUNION:
        ...

    @property
    def elemdesc_var(self) -> System.Runtime.InteropServices.ComTypes.ELEMDESC:
        ...

    @property
    def w_var_flags(self) -> int:
        ...

    @property
    def varkind(self) -> System.Runtime.InteropServices.ComTypes.VARKIND:
        ...


class EXCEPINFO:
    """This class has no documentation."""

    @property
    def w_code(self) -> int:
        ...

    @property
    def w_reserved(self) -> int:
        ...

    @property
    def bstr_source(self) -> str:
        ...

    @property
    def bstr_description(self) -> str:
        ...

    @property
    def bstr_help_file(self) -> str:
        ...

    @property
    def dw_help_context(self) -> int:
        ...

    @property
    def pv_reserved(self) -> System.IntPtr:
        ...

    @property
    def pfn_deferred_fill_in(self) -> System.IntPtr:
        ...

    @property
    def scode(self) -> int:
        ...


class FUNCFLAGS(Enum):
    """This class has no documentation."""

    FUNCFLAG_FRESTRICTED = ...

    FUNCFLAG_FSOURCE = ...

    FUNCFLAG_FBINDABLE = ...

    FUNCFLAG_FREQUESTEDIT = ...

    FUNCFLAG_FDISPLAYBIND = ...

    FUNCFLAG_FDEFAULTBIND = ...

    FUNCFLAG_FHIDDEN = ...

    FUNCFLAG_FUSESGETLASTERROR = ...

    FUNCFLAG_FDEFAULTCOLLELEM = ...

    FUNCFLAG_FUIDEFAULT = ...

    FUNCFLAG_FNONBROWSABLE = ...

    FUNCFLAG_FREPLACEABLE = ...

    FUNCFLAG_FIMMEDIATEBIND = ...


class VARFLAGS(Enum):
    """This class has no documentation."""

    VARFLAG_FREADONLY = ...

    VARFLAG_FSOURCE = ...

    VARFLAG_FBINDABLE = ...

    VARFLAG_FREQUESTEDIT = ...

    VARFLAG_FDISPLAYBIND = ...

    VARFLAG_FDEFAULTBIND = ...

    VARFLAG_FHIDDEN = ...

    VARFLAG_FRESTRICTED = ...

    VARFLAG_FDEFAULTCOLLELEM = ...

    VARFLAG_FUIDEFAULT = ...

    VARFLAG_FNONBROWSABLE = ...

    VARFLAG_FREPLACEABLE = ...

    VARFLAG_FIMMEDIATEBIND = ...


class SYSKIND(Enum):
    """This class has no documentation."""

    SYS_WIN_16 = 0

    SYS_WIN_32 = ...

    SYS_MAC = ...

    SYS_WIN_64 = ...


class LIBFLAGS(Enum):
    """This class has no documentation."""

    LIBFLAG_FRESTRICTED = ...

    LIBFLAG_FCONTROL = ...

    LIBFLAG_FHIDDEN = ...

    LIBFLAG_FHASDISKIMAGE = ...


class TYPELIBATTR:
    """This class has no documentation."""

    @property
    def guid(self) -> System.Guid:
        ...

    @property
    def lcid(self) -> int:
        ...

    @property
    def syskind(self) -> System.Runtime.InteropServices.ComTypes.SYSKIND:
        ...

    @property
    def w_major_ver_num(self) -> int:
        ...

    @property
    def w_minor_ver_num(self) -> int:
        ...

    @property
    def w_lib_flags(self) -> System.Runtime.InteropServices.ComTypes.LIBFLAGS:
        ...


class ITypeInfo2(System.Runtime.InteropServices.ComTypes.ITypeInfo, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def get_all_cust_data(self, p_cust_data: System.IntPtr) -> None:
        ...

    def get_all_func_cust_data(self, index: int, p_cust_data: System.IntPtr) -> None:
        ...

    def get_all_impl_type_cust_data(self, index: int, p_cust_data: System.IntPtr) -> None:
        ...

    def get_all_param_cust_data(self, index_func: int, index_param: int, p_cust_data: System.IntPtr) -> None:
        ...

    def get_all_var_cust_data(self, index: int, p_cust_data: System.IntPtr) -> None:
        ...

    def get_cust_data(self, guid: System.Guid, p_var_val: typing.Optional[typing.Any]) -> typing.Union[None, typing.Any]:
        ...

    def get_documentation_2(self, memid: int, pbstr_help_string: typing.Optional[str], pdw_help_string_context: typing.Optional[int], pbstr_help_string_dll: typing.Optional[str]) -> typing.Union[None, str, int, str]:
        ...

    def get_func_cust_data(self, index: int, guid: System.Guid, p_var_val: typing.Optional[typing.Any]) -> typing.Union[None, typing.Any]:
        ...

    def get_func_index_of_mem_id(self, memid: int, inv_kind: System.Runtime.InteropServices.ComTypes.INVOKEKIND, p_func_index: typing.Optional[int]) -> typing.Union[None, int]:
        ...

    def get_impl_type_cust_data(self, index: int, guid: System.Guid, p_var_val: typing.Optional[typing.Any]) -> typing.Union[None, typing.Any]:
        ...

    def get_param_cust_data(self, index_func: int, index_param: int, guid: System.Guid, p_var_val: typing.Optional[typing.Any]) -> typing.Union[None, typing.Any]:
        ...

    def get_type_flags(self, p_type_flags: typing.Optional[int]) -> typing.Union[None, int]:
        ...

    def get_type_kind(self, p_type_kind: typing.Optional[System.Runtime.InteropServices.ComTypes.TYPEKIND]) -> typing.Union[None, System.Runtime.InteropServices.ComTypes.TYPEKIND]:
        ...

    def get_var_cust_data(self, index: int, guid: System.Guid, p_var_val: typing.Optional[typing.Any]) -> typing.Union[None, typing.Any]:
        ...

    def get_var_index_of_mem_id(self, memid: int, p_var_index: typing.Optional[int]) -> typing.Union[None, int]:
        ...


