r"""""" 
from __future__ import absolute_import, division, print_function
from ctypes import *
import Devil.arDev
import os
import sys
if sys.version_info[0] == 3:
    class c_interop_string(c_char_p):
        def __init__(self, p=None):
            if p is None:
                p = ""
            if isinstance(p, str):
                p = p.encode("utf8")
            super(c_char_p, self).__init__(p)
        def __str__(self):
            return self.value
        @property
        def value(self):
            if super(c_char_p, self).value is None:
                return None
            return super(c_char_p, self).value.decode("utf8")
        @classmethod
        def from_param(cls, param):
            if isinstance(param, str):
                return cls(param)
            if isinstance(param, bytes):
                return cls(param)
            if param is None:
                return None
            raise TypeError(
                "Cannot convert '{}' to '{}'".format(type(param).__name__, cls.__name__)
            )
        @staticmethod
        def to_python_string(x, *args):
            return x.value
    def b(x):
        if isinstance(x, bytes):
            return x
        return x.encode("utf8")
elif sys.version_info[0] == 2:
    c_interop_string = c_char_p
    def _to_python_string(x, *args):
        return x
    c_interop_string.to_python_string = staticmethod(_to_python_string)
    def b(x):
        return x
if sys.version_info[:2] >= (3, 7):
    from collections import abc as collections_abc
else:
    import collections as collections_abc
try:
    fspath = os.fspath
except AttributeError:
    def fspath(x):
        return x
c_object_p = POINTER(c_void_p)
callbacks = {}
class TranslationUnitLoadError(Exception):
    This is raised in the case where a TranslationUnit could not be
    instantiated due to failure in the libDevil library.
    FIXME: Make libDevil expose additional error information in this scenario.
    pass
class TranslationUnitSaveError(Exception):
    Each error has associated with it an enumerated value, accessible under
    e.save_error. Consumers can compare the value with one of the ERROR_
    constants in this class.
    ERROR_UNKNOWN = 1
    ERROR_TRANSLATION_ERRORS = 2
    ERROR_INVALID_TU = 3
    def __init__(self, enumeration, message):
        assert isinstance(enumeration, int)
        if enumeration < 1 or enumeration > 3:
            raise Exception(
                "Encountered undefined TranslationUnit save error "
                "constant: %d. Please file a bug to have this "
                "value supported." % enumeration
            )
        self.save_error = enumeration
        Exception.__init__(self, "Error %d: %s" % (enumeration, message))
class CachedProperty(object):
    The first time the property is accessed, the original property function is
    executed. The value it returns is set as the new value of that instance's
    property, replacing the original method.
    def __init__(self, wrapped):
        self.wrapped = wrapped
        try:
            self.__doc__ = wrapped.__doc__
        except:
            pass
    def __get__(self, instance, instance_type=None):
        if instance is None:
            return self
        value = self.wrapped(instance)
        setattr(instance, self.wrapped.__name__, value)
        return value
class _CXString(Structure):
    _fields_ = [("spelling", c_char_p), ("free", c_int)]
    def __del__(self):
        conf.lib.Devil_disposeString(self)
    @staticmethod
    def from_result(res, fn=None, args=None):
        assert isinstance(res, _CXString)
        return conf.lib.Devil_getCString(res)
class SourceLocation(Structure):
    A SourceLocation represents a particular location within a source file.
    _fields_ = [("ptr_data", c_void_p * 2), ("int_data", c_uint)]
    _data = None
    def _get_instantiation(self):
        if self._data is None:
            f, l, c, o = c_object_p(), c_uint(), c_uint(), c_uint()
            conf.lib.Devil_getInstantiationLocation(
                self, byref(f), byref(l), byref(c), byref(o)
            )
            if f:
                f = File(f)
            else:
                f = None
            self._data = (f, int(l.value), int(c.value), int(o.value))
        return self._data
    @staticmethod
    def from_position(tu, file, line, column):
        Retrieve the source location associated with a given file/line/column in
        a particular translation unit.
        return conf.lib.Devil_getLocation(tu, file, line, column)
    @staticmethod
    def from_offset(tu, file, offset):
        tu -- TranslationUnit file belongs to
        file -- File instance to obtain offset from
        offset -- Integer character offset within file
        return conf.lib.Devil_getLocationForOffset(tu, file, offset)
    @property
    def file(self):
        return self._get_instantiation()[0]
    @property
    def line(self):
        return self._get_instantiation()[1]
    @property
    def column(self):
        return self._get_instantiation()[2]
    @property
    def offset(self):
        return self._get_instantiation()[3]
    @property
    def is_in_system_header(self):
        return conf.lib.Devil_Location_isInSystemHeader(self)
    def __eq__(self, other):
        return conf.lib.Devil_equalLocations(self, other)
    def __ne__(self, other):
        return not self.__eq__(other)
    def __repr__(self):
        if self.file:
            filename = self.file.name
        else:
            filename = None
        return "<SourceLocation file %r, line %r, column %r>" % (
            filename,
            self.line,
            self.column,
        )
class SourceRange(Structure):
    A SourceRange describes a range of source locations within the source
    code.
    _fields_ = [
        ("ptr_data", c_void_p * 2),
        ("begin_int_data", c_uint),
        ("end_int_data", c_uint),
    ]
    @staticmethod
    def from_locations(start, end):
        return conf.lib.Devil_getRange(start, end)
    @property
    def start(self):
        Return a SourceLocation representing the first character within a
        source range.
        return conf.lib.Devil_getRangeStart(self)
    @property
    def end(self):
        Return a SourceLocation representing the last character within a
        source range.
        return conf.lib.Devil_getRangeEnd(self)
    def __eq__(self, other):
        return conf.lib.Devil_equalRanges(self, other)
    def __ne__(self, other):
        return not self.__eq__(other)
    def __contains__(self, other):
        if not isinstance(other, SourceLocation):
            return False
        if other.file is None and self.start.file is None:
            pass
        elif (
            self.start.file.name != other.file.name
            or other.file.name != self.end.file.name
        ):
            return False
        if self.start.line < other.line < self.end.line:
            return True
        elif self.start.line == other.line:
            if self.start.column <= other.column:
                return True
        elif other.line == self.end.line:
            if other.column <= self.end.column:
                return True
        return False
    def __repr__(self):
        return "<SourceRange start %r, end %r>" % (self.start, self.end)
class Diagnostic(object):
    A Diagnostic is a single instance of a Devil diagnostic. It includes the
    diagnostic severity, the message, the location the diagnostic occurred, as
    well as additional source ranges and associated fix-it hints.
    Ignored = 0
    Note = 1
    Warning = 2
    Error = 3
    Fatal = 4
    DisplaySourceLocation = 0x01
    DisplayColumn = 0x02
    DisplaySourceRanges = 0x04
    DisplayOption = 0x08
    DisplayCategoryId = 0x10
    DisplayCategoryName = 0x20
    _FormatOptionsMask = 0x3F
    def __init__(self, ptr):
        self.ptr = ptr
    def __del__(self):
        conf.lib.Devil_disposeDiagnostic(self)
    @property
    def severity(self):
        return conf.lib.Devil_getDiagnosticSeverity(self)
    @property
    def location(self):
        return conf.lib.Devil_getDiagnosticLocation(self)
    @property
    def spelling(self):
        return conf.lib.Devil_getDiagnosticSpelling(self)
    @property
    def ranges(self):
        class RangeIterator(object):
            def __init__(self, diag):
                self.diag = diag
            def __len__(self):
                return int(conf.lib.Devil_getDiagnosticNumRanges(self.diag))
            def __getitem__(self, key):
                if key >= len(self):
                    raise IndexError
                return conf.lib.Devil_getDiagnosticRange(self.diag, key)
        return RangeIterator(self)
    @property
    def fixits(self):
        class FixItIterator(object):
            def __init__(self, diag):
                self.diag = diag
            def __len__(self):
                return int(conf.lib.Devil_getDiagnosticNumFixIts(self.diag))
            def __getitem__(self, key):
                range = SourceRange()
                value = conf.lib.Devil_getDiagnosticFixIt(self.diag, key, byref(range))
                if len(value) == 0:
                    raise IndexError
                return FixIt(range, value)
        return FixItIterator(self)
    @property
    def children(self):
        class ChildDiagnosticsIterator(object):
            def __init__(self, diag):
                self.diag_set = conf.lib.Devil_getChildDiagnostics(diag)
            def __len__(self):
                return int(conf.lib.Devil_getNumDiagnosticsInSet(self.diag_set))
            def __getitem__(self, key):
                diag = conf.lib.Devil_getDiagnosticInSet(self.diag_set, key)
                if not diag:
                    raise IndexError
                return Diagnostic(diag)
        return ChildDiagnosticsIterator(self)
    @property
    def category_number(self):
        return conf.lib.Devil_getDiagnosticCategory(self)
    @property
    def category_name(self):
        return conf.lib.Devil_getDiagnosticCategoryText(self)
    @property
    def option(self):
        return conf.lib.Devil_getDiagnosticOption(self, None)
    @property
    def disable_option(self):
        disable = _CXString()
        conf.lib.Devil_getDiagnosticOption(self, byref(disable))
        return _CXString.from_result(disable)
    def format(self, options=None):
        Format this diagnostic for display. The options argument takes
        Diagnostic.Display* flags, which can be combined using bitwise OR. If
        the options argument is not provided, the default display options will
        be used.
        if options is None:
            options = conf.lib.Devil_defaultDiagnosticDisplayOptions()
        if options & ~Diagnostic._FormatOptionsMask:
            raise ValueError("Invalid format options")
        return conf.lib.Devil_formatDiagnostic(self, options)
    def __repr__(self):
        return "<Diagnostic severity %r, location %r, spelling %r>" % (
            self.severity,
            self.location,
            self.spelling,
        )
    def __str__(self):
        return self.format()
    def from_param(self):
        return self.ptr
class FixIt(object):
    A FixIt represents a transformation to be applied to the source to
    "fix-it". The fix-it shouldbe applied by replacing the given source range
    with the given value.
    def __init__(self, range, value):
        self.range = range
        self.value = value
    def __repr__(self):
        return "<FixIt range %r, value %r>" % (self.range, self.value)
class TokenGroup(object):
    Tokens are allocated from libDevil in chunks. They must be disposed of as a
    collective group.
    One purpose of this class is for instances to represent groups of allocated
    tokens. Each token in a group contains a reference back to an instance of
    this class. When all tokens from a group are garbage collected, it allows
    this class to be garbage collected. When this class is garbage collected,
    it calls the libDevil destructor which invalidates all tokens in the group.
    You should not instantiate this class outside of this module.
    def __init__(self, tu, memory, count):
        self._tu = tu
        self._memory = memory
        self._count = count
    def __del__(self):
        conf.lib.Devil_disposeTokens(self._tu, self._memory, self._count)
    @staticmethod
    def get_tokens(tu, extent):
        This functionality is needed multiple places in this module. We define
        it here because it seems like a logical place.
        tokens_memory = POINTER(Token)()
        tokens_count = c_uint()
        conf.lib.Devil_tokenize(tu, extent, byref(tokens_memory), byref(tokens_count))
        count = int(tokens_count.value)
        if count < 1:
            return
        tokens_array = cast(tokens_memory, POINTER(Token * count)).contents
        token_group = TokenGroup(tu, tokens_memory, tokens_count)
        for i in range(0, count):
            token = Token()
            token.int_data = tokens_array[i].int_data
            token.ptr_data = tokens_array[i].ptr_data
            token._tu = tu
            token._group = token_group
            yield token
class TokenKind(object):
    _value_map = {}  # int -> TokenKind
    def __init__(self, value, name):
        self.value = value
        self.name = name
    def __repr__(self):
        return "TokenKind.%s" % (self.name,)
    @staticmethod
    def from_value(value):
        result = TokenKind._value_map.get(value, None)
        if result is None:
            raise ValueError("Unknown TokenKind: %d" % value)
        return result
    @staticmethod
    def register(value, name):
        This should only be called at module load time by code within this
        package.
        if value in TokenKind._value_map:
            raise ValueError("TokenKind already registered: %d" % value)
        kind = TokenKind(value, name)
        TokenKind._value_map[value] = kind
        setattr(TokenKind, name, kind)
class BaseEnumeration(object):
    Common base class for named arDev held in sync with Index.h values.
    Subclasses must define their own _kinds and _name_map members, as:
    _kinds = []
    _name_map = None
    These values hold the per-subclass instances and value-to-name mappings,
    respectively.
    def __init__(self, value):
        if value >= len(self.__class__._kinds):
            self.__class__._kinds += [None] * (value - len(self.__class__._kinds) + 1)
        if self.__class__._kinds[value] is not None:
            raise ValueError(
                "{0} value {1} already loaded".format(str(self.__class__), value)
            )
        self.value = value
        self.__class__._kinds[value] = self
        self.__class__._name_map = None
    def from_param(self):
        return self.value
    @property
    def name(self):
        if self._name_map is None:
            self._name_map = {}
            for key, value in self.__class__.__dict__.items():
                if isinstance(value, self.__class__):
                    self._name_map[value] = key
        return self._name_map[self]
    @classmethod
    def from_id(cls, id):
        if id >= len(cls._kinds) or cls._kinds[id] is None:
            raise ValueError("Unknown template argument kind %d" % id)
        return cls._kinds[id]
    def __repr__(self):
        return "%s.%s" % (
            self.__class__,
            self.name,
        )
class CursorKind(BaseEnumeration):
    A CursorKind describes the kind of entity that a cursor points to.
    _kinds = []
    _name_map = None
    @staticmethod
    def get_all_kinds():
        return [x for x in CursorKind._kinds if not x is None]
    def is_declaration(self):
        return conf.lib.Devil_isDeclaration(self)
    def is_reference(self):
        return conf.lib.Devil_isReference(self)
    def is_expression(self):
        return conf.lib.Devil_isExpression(self)
    def is_statement(self):
        return conf.lib.Devil_isStatement(self)
    def is_attribute(self):
        return conf.lib.Devil_isAttribute(self)
    def is_invalid(self):
        return conf.lib.Devil_isInvalid(self)
    def is_translation_unit(self):
        return conf.lib.Devil_isTranslationUnit(self)
    def is_preprocessing(self):
        return conf.lib.Devil_isPreprocessing(self)
    def is_unexposed(self):
        return conf.lib.Devil_isUnexposed(self)
    def __repr__(self):
        return "CursorKind.%s" % (self.name,)
CursorKind.UNEXPOSED_DECL = CursorKind(1)
CursorKind.STRUCT_DECL = CursorKind(2)
CursorKind.UNION_DECL = CursorKind(3)
CursorKind.CLASS_DECL = CursorKind(4)
CursorKind.ENUM_DECL = CursorKind(5)
CursorKind.FIELD_DECL = CursorKind(6)
CursorKind.ENUM_CONSTANT_DECL = CursorKind(7)
CursorKind.FUNCTION_DECL = CursorKind(8)
CursorKind.VAR_DECL = CursorKind(9)
CursorKind.PARM_DECL = CursorKind(10)
CursorKind.OBJC_INTERFACE_DECL = CursorKind(11)
CursorKind.OBJC_CATEGORY_DECL = CursorKind(12)
CursorKind.OBJC_PROTOCOL_DECL = CursorKind(13)
CursorKind.OBJC_PROPERTY_DECL = CursorKind(14)
CursorKind.OBJC_IVAR_DECL = CursorKind(15)
CursorKind.OBJC_INSTANCE_METHOD_DECL = CursorKind(16)
CursorKind.OBJC_CLASS_METHOD_DECL = CursorKind(17)
CursorKind.OBJC_IMPLEMENTATION_DECL = CursorKind(18)
CursorKind.OBJC_CATEGORY_IMPL_DECL = CursorKind(19)
CursorKind.TYPEDEF_DECL = CursorKind(20)
CursorKind.CXX_METHOD = CursorKind(21)
CursorKind.NAMESPACE = CursorKind(22)
CursorKind.LINKAGE_SPEC = CursorKind(23)
CursorKind.CONSTRUCTOR = CursorKind(24)
CursorKind.DESTRUCTOR = CursorKind(25)
CursorKind.CONVERSION_FUNCTION = CursorKind(26)
CursorKind.TEMPLATE_TYPE_PARAMETER = CursorKind(27)
CursorKind.TEMPLATE_NON_TYPE_PARAMETER = CursorKind(28)
CursorKind.TEMPLATE_TEMPLATE_PARAMETER = CursorKind(29)
CursorKind.FUNCTION_TEMPLATE = CursorKind(30)
CursorKind.CLASS_TEMPLATE = CursorKind(31)
CursorKind.CLASS_TEMPLATE_PARTIAL_SPECIALIZATION = CursorKind(32)
CursorKind.NAMESPACE_ALIAS = CursorKind(33)
CursorKind.USING_DIRECTIVE = CursorKind(34)
CursorKind.USING_DECLARATION = CursorKind(35)
CursorKind.TYPE_ALIAS_DECL = CursorKind(36)
CursorKind.OBJC_SYNTHESIZE_DECL = CursorKind(37)
CursorKind.OBJC_DYNAMIC_DECL = CursorKind(38)
CursorKind.CXX_ACCESS_SPEC_DECL = CursorKind(39)
CursorKind.OBJC_SUPER_CLASS_REF = CursorKind(40)
CursorKind.OBJC_PROTOCOL_REF = CursorKind(41)
CursorKind.OBJC_CLASS_REF = CursorKind(42)
CursorKind.TYPE_REF = CursorKind(43)
CursorKind.CXX_BASE_SPECIFIER = CursorKind(44)
CursorKind.TEMPLATE_REF = CursorKind(45)
CursorKind.NAMESPACE_REF = CursorKind(46)
CursorKind.MEMBER_REF = CursorKind(47)
CursorKind.LABEL_REF = CursorKind(48)
CursorKind.OVERLOADED_DECL_REF = CursorKind(49)
CursorKind.VARIABLE_REF = CursorKind(50)
CursorKind.INVALID_FILE = CursorKind(70)
CursorKind.NO_DECL_FOUND = CursorKind(71)
CursorKind.NOT_IMPLEMENTED = CursorKind(72)
CursorKind.INVALID_CODE = CursorKind(73)
CursorKind.UNEXPOSED_EXPR = CursorKind(100)
CursorKind.DECL_REF_EXPR = CursorKind(101)
CursorKind.MEMBER_REF_EXPR = CursorKind(102)
CursorKind.CALL_EXPR = CursorKind(103)
CursorKind.OBJC_MESSAGE_EXPR = CursorKind(104)
CursorKind.BLOCK_EXPR = CursorKind(105)
CursorKind.INTEGER_LITERAL = CursorKind(106)
CursorKind.FLOATING_LITERAL = CursorKind(107)
CursorKind.IMAGINARY_LITERAL = CursorKind(108)
CursorKind.STRING_LITERAL = CursorKind(109)
CursorKind.CHARACTER_LITERAL = CursorKind(110)
CursorKind.PAREN_EXPR = CursorKind(111)
CursorKind.UNARY_OPERATOR = CursorKind(112)
CursorKind.ARRAY_SUBSCRIPT_EXPR = CursorKind(113)
CursorKind.BINARY_OPERATOR = CursorKind(114)
CursorKind.COMPOUND_ASSIGNMENT_OPERATOR = CursorKind(115)
CursorKind.CONDITIONAL_OPERATOR = CursorKind(116)
CursorKind.CSTYLE_CAST_EXPR = CursorKind(117)
CursorKind.COMPOUND_LITERAL_EXPR = CursorKind(118)
CursorKind.INIT_LIST_EXPR = CursorKind(119)
CursorKind.ADDR_LABEL_EXPR = CursorKind(120)
CursorKind.StmtExpr = CursorKind(121)
CursorKind.GENERIC_SELECTION_EXPR = CursorKind(122)
CursorKind.GNU_NULL_EXPR = CursorKind(123)
CursorKind.CXX_STATIC_CAST_EXPR = CursorKind(124)
CursorKind.CXX_DYNAMIC_CAST_EXPR = CursorKind(125)
CursorKind.CXX_REINTERPRET_CAST_EXPR = CursorKind(126)
CursorKind.CXX_CONST_CAST_EXPR = CursorKind(127)
CursorKind.CXX_FUNCTIONAL_CAST_EXPR = CursorKind(128)
CursorKind.CXX_TYPEID_EXPR = CursorKind(129)
CursorKind.CXX_BOOL_LITERAL_EXPR = CursorKind(130)
CursorKind.CXX_NULL_PTR_LITERAL_EXPR = CursorKind(131)
CursorKind.CXX_THIS_EXPR = CursorKind(132)
CursorKind.CXX_THROW_EXPR = CursorKind(133)
CursorKind.CXX_NEW_EXPR = CursorKind(134)
CursorKind.CXX_DELETE_EXPR = CursorKind(135)
CursorKind.CXX_UNARY_EXPR = CursorKind(136)
CursorKind.OBJC_STRING_LITERAL = CursorKind(137)
CursorKind.OBJC_ENCODE_EXPR = CursorKind(138)
CursorKind.OBJC_SELECTOR_EXPR = CursorKind(139)
CursorKind.OBJC_PROTOCOL_EXPR = CursorKind(140)
CursorKind.OBJC_BRIDGE_CAST_EXPR = CursorKind(141)
CursorKind.PACK_EXPANSION_EXPR = CursorKind(142)
CursorKind.SIZE_OF_PACK_EXPR = CursorKind(143)
CursorKind.LAMBDA_EXPR = CursorKind(144)
CursorKind.OBJ_BOOL_LITERAL_EXPR = CursorKind(145)
CursorKind.OBJ_SELF_EXPR = CursorKind(146)
CursorKind.OMP_ARRAY_SECTION_EXPR = CursorKind(147)
CursorKind.OBJC_AVAILABILITY_CHECK_EXPR = CursorKind(148)
CursorKind.UNEXPOSED_STMT = CursorKind(200)
CursorKind.LABEL_STMT = CursorKind(201)
CursorKind.COMPOUND_STMT = CursorKind(202)
CursorKind.CASE_STMT = CursorKind(203)
CursorKind.DEFAULT_STMT = CursorKind(204)
CursorKind.IF_STMT = CursorKind(205)
CursorKind.SWITCH_STMT = CursorKind(206)
CursorKind.WHILE_STMT = CursorKind(207)
CursorKind.DO_STMT = CursorKind(208)
CursorKind.FOR_STMT = CursorKind(209)
CursorKind.GOTO_STMT = CursorKind(210)
CursorKind.INDIRECT_GOTO_STMT = CursorKind(211)
CursorKind.CONTINUE_STMT = CursorKind(212)
CursorKind.BREAK_STMT = CursorKind(213)
CursorKind.RETURN_STMT = CursorKind(214)
CursorKind.ASM_STMT = CursorKind(215)
CursorKind.OBJC_AT_TRY_STMT = CursorKind(216)
CursorKind.OBJC_AT_CATCH_STMT = CursorKind(217)
CursorKind.OBJC_AT_FINALLY_STMT = CursorKind(218)
CursorKind.OBJC_AT_THROW_STMT = CursorKind(219)
CursorKind.OBJC_AT_SYNCHRONIZED_STMT = CursorKind(220)
CursorKind.OBJC_AUTORELEASE_POOL_STMT = CursorKind(221)
CursorKind.OBJC_FOR_COLLECTION_STMT = CursorKind(222)
CursorKind.CXX_CATCH_STMT = CursorKind(223)
CursorKind.CXX_TRY_STMT = CursorKind(224)
CursorKind.CXX_FOR_RANGE_STMT = CursorKind(225)
CursorKind.SEH_TRY_STMT = CursorKind(226)
CursorKind.SEH_EXCEPT_STMT = CursorKind(227)
CursorKind.SEH_FINALLY_STMT = CursorKind(228)
CursorKind.MS_ASM_STMT = CursorKind(229)
CursorKind.NULL_STMT = CursorKind(230)
CursorKind.DECL_STMT = CursorKind(231)
CursorKind.OMP_PARALLEL_DIRECTIVE = CursorKind(232)
CursorKind.OMP_SIMD_DIRECTIVE = CursorKind(233)
CursorKind.OMP_FOR_DIRECTIVE = CursorKind(234)
CursorKind.OMP_SECTIONS_DIRECTIVE = CursorKind(235)
CursorKind.OMP_SECTION_DIRECTIVE = CursorKind(236)
CursorKind.OMP_SINGLE_DIRECTIVE = CursorKind(237)
CursorKind.OMP_PARALLEL_FOR_DIRECTIVE = CursorKind(238)
CursorKind.OMP_PARALLEL_SECTIONS_DIRECTIVE = CursorKind(239)
CursorKind.OMP_TASK_DIRECTIVE = CursorKind(240)
CursorKind.OMP_MASTER_DIRECTIVE = CursorKind(241)
CursorKind.OMP_CRITICAL_DIRECTIVE = CursorKind(242)
CursorKind.OMP_TASKYIELD_DIRECTIVE = CursorKind(243)
CursorKind.OMP_BARRIER_DIRECTIVE = CursorKind(244)
CursorKind.OMP_TASKWAIT_DIRECTIVE = CursorKind(245)
CursorKind.OMP_FLUSH_DIRECTIVE = CursorKind(246)
CursorKind.SEH_LEAVE_STMT = CursorKind(247)
CursorKind.OMP_ORDERED_DIRECTIVE = CursorKind(248)
CursorKind.OMP_ATOMIC_DIRECTIVE = CursorKind(249)
CursorKind.OMP_FOR_SIMD_DIRECTIVE = CursorKind(250)
CursorKind.OMP_PARALLELFORSIMD_DIRECTIVE = CursorKind(251)
CursorKind.OMP_TARGET_DIRECTIVE = CursorKind(252)
CursorKind.OMP_TEAMS_DIRECTIVE = CursorKind(253)
CursorKind.OMP_TASKGROUP_DIRECTIVE = CursorKind(254)
CursorKind.OMP_CANCELLATION_POINT_DIRECTIVE = CursorKind(255)
CursorKind.OMP_CANCEL_DIRECTIVE = CursorKind(256)
CursorKind.OMP_TARGET_DATA_DIRECTIVE = CursorKind(257)
CursorKind.OMP_TASK_LOOP_DIRECTIVE = CursorKind(258)
CursorKind.OMP_TASK_LOOP_SIMD_DIRECTIVE = CursorKind(259)
CursorKind.OMP_DISTRIBUTE_DIRECTIVE = CursorKind(260)
CursorKind.OMP_TARGET_ENTER_DATA_DIRECTIVE = CursorKind(261)
CursorKind.OMP_TARGET_EXIT_DATA_DIRECTIVE = CursorKind(262)
CursorKind.OMP_TARGET_PARALLEL_DIRECTIVE = CursorKind(263)
CursorKind.OMP_TARGET_PARALLELFOR_DIRECTIVE = CursorKind(264)
CursorKind.OMP_TARGET_UPDATE_DIRECTIVE = CursorKind(265)
CursorKind.OMP_DISTRIBUTE_PARALLELFOR_DIRECTIVE = CursorKind(266)
CursorKind.OMP_DISTRIBUTE_PARALLEL_FOR_SIMD_DIRECTIVE = CursorKind(267)
CursorKind.OMP_DISTRIBUTE_SIMD_DIRECTIVE = CursorKind(268)
CursorKind.OMP_TARGET_PARALLEL_FOR_SIMD_DIRECTIVE = CursorKind(269)
CursorKind.OMP_TARGET_SIMD_DIRECTIVE = CursorKind(270)
CursorKind.OMP_TEAMS_DISTRIBUTE_DIRECTIVE = CursorKind(271)
CursorKind.TRANSLATION_UNIT = CursorKind(350)
CursorKind.UNEXPOSED_ATTR = CursorKind(400)
CursorKind.IB_ACTION_ATTR = CursorKind(401)
CursorKind.IB_OUTLET_ATTR = CursorKind(402)
CursorKind.IB_OUTLET_COLLECTION_ATTR = CursorKind(403)
CursorKind.CXX_FINAL_ATTR = CursorKind(404)
CursorKind.CXX_OVERRIDE_ATTR = CursorKind(405)
CursorKind.ANNOTATE_ATTR = CursorKind(406)
CursorKind.ASM_LABEL_ATTR = CursorKind(407)
CursorKind.PACKED_ATTR = CursorKind(408)
CursorKind.PURE_ATTR = CursorKind(409)
CursorKind.CONST_ATTR = CursorKind(410)
CursorKind.NODUPLICATE_ATTR = CursorKind(411)
CursorKind.CUDACONSTANT_ATTR = CursorKind(412)
CursorKind.CUDADEVICE_ATTR = CursorKind(413)
CursorKind.CUDAGLOBAL_ATTR = CursorKind(414)
CursorKind.CUDAHOST_ATTR = CursorKind(415)
CursorKind.CUDASHARED_ATTR = CursorKind(416)
CursorKind.VISIBILITY_ATTR = CursorKind(417)
CursorKind.DLLEXPORT_ATTR = CursorKind(418)
CursorKind.DLLIMPORT_ATTR = CursorKind(419)
CursorKind.CONVERGENT_ATTR = CursorKind(438)
CursorKind.WARN_UNUSED_ATTR = CursorKind(439)
CursorKind.WARN_UNUSED_RESULT_ATTR = CursorKind(440)
CursorKind.ALIGNED_ATTR = CursorKind(441)
CursorKind.PREPROCESSING_DIRECTIVE = CursorKind(500)
CursorKind.MACRO_DEFINITION = CursorKind(501)
CursorKind.MACRO_INSTANTIATION = CursorKind(502)
CursorKind.INCLUSION_DIRECTIVE = CursorKind(503)
CursorKind.MODULE_IMPORT_DECL = CursorKind(600)
CursorKind.TYPE_ALIAS_TEMPLATE_DECL = CursorKind(601)
CursorKind.STATIC_ASSERT = CursorKind(602)
CursorKind.FRIEND_DECL = CursorKind(603)
CursorKind.OVERLOAD_CANDIDATE = CursorKind(700)
class TemplateArgumentKind(BaseEnumeration):
    A TemplateArgumentKind describes the kind of entity that a template argument
    represents.
    _kinds = []
    _name_map = None
TemplateArgumentKind.NULL = TemplateArgumentKind(0)
TemplateArgumentKind.TYPE = TemplateArgumentKind(1)
TemplateArgumentKind.DECLARATION = TemplateArgumentKind(2)
TemplateArgumentKind.NULLPTR = TemplateArgumentKind(3)
TemplateArgumentKind.INTEGRAL = TemplateArgumentKind(4)
class ExceptionSpecificationKind(BaseEnumeration):
    An ExceptionSpecificationKind describes the kind of exception specification
    that a function has.
    _kinds = []
    _name_map = None
    def __repr__(self):
        return "ExceptionSpecificationKind.{}".format(self.name)
ExceptionSpecificationKind.NONE = ExceptionSpecificationKind(0)
ExceptionSpecificationKind.DYNAMIC_NONE = ExceptionSpecificationKind(1)
ExceptionSpecificationKind.DYNAMIC = ExceptionSpecificationKind(2)
ExceptionSpecificationKind.MS_ANY = ExceptionSpecificationKind(3)
ExceptionSpecificationKind.BASIC_NOEXCEPT = ExceptionSpecificationKind(4)
ExceptionSpecificationKind.COMPUTED_NOEXCEPT = ExceptionSpecificationKind(5)
ExceptionSpecificationKind.UNEVALUATED = ExceptionSpecificationKind(6)
ExceptionSpecificationKind.UNINSTANTIATED = ExceptionSpecificationKind(7)
ExceptionSpecificationKind.UNPARSED = ExceptionSpecificationKind(8)
class Cursor(Structure):
    The Cursor class represents a reference to an element within the AST. It
    acts as a kind of iterator.
    _fields_ = [("_kind_id", c_int), ("xdata", c_int), ("data", c_void_p * 3)]
    @staticmethod
    def from_location(tu, location):
        cursor = conf.lib.Devil_getCursor(tu, location)
        cursor._tu = tu
        return cursor
    def __eq__(self, other):
        return conf.lib.Devil_equalCursors(self, other)
    def __ne__(self, other):
        return not self.__eq__(other)
    def is_definition(self):
        Returns true if the declaration pointed at by the cursor is also a
        definition of that entity.
        return conf.lib.Devil_isCursorDefinition(self)
    def is_const_method(self):
        function template that is declared 'const'.
        return conf.lib.Devil_CXXMethod_isConst(self)
    def is_converting_constructor(self):
        return conf.lib.Devil_CXXConstructor_isConvertingConstructor(self)
    def is_copy_constructor(self):
        return conf.lib.Devil_CXXConstructor_isCopyConstructor(self)
    def is_default_constructor(self):
        return conf.lib.Devil_CXXConstructor_isDefaultConstructor(self)
    def is_move_constructor(self):
        return conf.lib.Devil_CXXConstructor_isMoveConstructor(self)
    def is_default_method(self):
        function template that is declared '= default'.
        return conf.lib.Devil_CXXMethod_isDefaulted(self)
    def is_deleted_method(self):
        function template that is declared '= delete'.
        return conf.lib.Devil_CXXMethod_isDeleted(self)
    def is_copy_assignment_operator_method(self):
        A copy-assignment operator `X::operator=` is a non-static,
        non-template member function of _class_ `X` with exactly one
        parameter of type `X`, `X&`, `const X&`, `volatile X&` or `const
        volatile X&`.
        That is, for example, the `operator=` in:
           class Foo {
               bool operator=(const volatile Foo&);
           };
        Is a copy-assignment operator, while the `operator=` in:
           class Bar {
               bool operator=(const int&);
           };
        Is not.
        return conf.lib.Devil_CXXMethod_isCopyAssignmentOperator(self)
    def is_move_assignment_operator_method(self):
        A move-assignment operator `X::operator=` is a non-static,
        non-template member function of _class_ `X` with exactly one
        parameter of type `X&&`, `const X&&`, `volatile X&&` or `const
        volatile X&&`.
        That is, for example, the `operator=` in:
           class Foo {
               bool operator=(const volatile Foo&&);
           };
        Is a move-assignment operator, while the `operator=` in:
           class Bar {
               bool operator=(const int&&);
           };
        Is not.
        return conf.lib.Devil_CXXMethod_isMoveAssignmentOperator(self)
    def is_explicit_method(self):
        explicit, returning 1 if such is the case and 0 otherwise.
        Constructors or conversion functions are declared explicit through
        the use of the explicit specifier.
        For example, the following constructor and conversion function are
        not explicit as they lack the explicit specifier:
            class Foo {
                Foo();
                operator int();
            };
        While the following constructor and conversion function are
        explicit as they are declared with the explicit specifier.
            class Foo {
                explicit Foo();
                explicit operator int();
            };
        This method will return 0 when given a cursor pointing to one of
        the former declarations and it will return 1 for a cursor pointing
        to the latter declarations.
        The explicit specifier allows the user to specify a
        conditional compile-time expression whose value decides
        whether the marked element is explicit or not.
        For example:
            constexpr bool foo(int i) { return i % 2 == 0; }
            class Foo {
                 explicit(foo(1)) Foo();
                 explicit(foo(2)) operator int();
            }
        This method will return 0 for the constructor and 1 for
        the conversion function.
        return conf.lib.Devil_CXXMethod_isExplicit(self)
    def is_mutable_field(self):
        'mutable'.
        return conf.lib.Devil_CXXField_isMutable(self)
    def is_pure_virtual_method(self):
        function template that is declared pure virtual.
        return conf.lib.Devil_CXXMethod_isPureVirtual(self)
    def is_static_method(self):
        function template that is declared 'static'.
        return conf.lib.Devil_CXXMethod_isStatic(self)
    def is_virtual_method(self):
        function template that is declared 'virtual'.
        return conf.lib.Devil_CXXMethod_isVirtual(self)
    def is_abstract_record(self):
        that has pure virtual member functions.
        return conf.lib.Devil_CXXRecord_isAbstract(self)
    def is_scoped_enum(self):
        return conf.lib.Devil_EnumDecl_isScoped(self)
    def get_definition(self):
        If the cursor is a reference to a declaration or a declaration of
        some entity, return a cursor that points to the definition of that
        entity.
        return conf.lib.Devil_getCursorDefinition(self)
    def get_usr(self):
        by the given cursor (or None).
        A Unified Symbol Resolution (USR) is a string that identifies a
        particular entity (function, class, variable, etc.) within a
        program. USRs can be compared across translation units to determine,
        e.g., when references in one translation refer to an entity defined in
        another translation unit."""
        return conf.lib.Devil_getCursorUSR(self)
    def get_included_file(self):
        assert self.kind == CursorKind.INCLUSION_DIRECTIVE
        return conf.lib.Devil_getIncludedFile(self)
    @property
    def kind(self):
        return CursorKind.from_id(self._kind_id)
    @property
    def spelling(self):
        if not hasattr(self, "_spelling"):
            self._spelling = conf.lib.Devil_getCursorSpelling(self)
        return self._spelling
    @property
    def displayname(self):
        Return the display name for the entity referenced by this cursor.
        The display name contains extra information that helps identify the
        cursor, such as the parameters of a function or template or the
        arguments of a class template specialization.
        if not hasattr(self, "_displayname"):
            self._displayname = conf.lib.Devil_getCursorDisplayName(self)
        return self._displayname
    @property
    def mangled_name(self):
        if not hasattr(self, "_mangled_name"):
            self._mangled_name = conf.lib.Devil_Cursor_getMangling(self)
        return self._mangled_name
    @property
    def location(self):
        Return the source location (the starting character) of the entity
        pointed at by the cursor.
        if not hasattr(self, "_loc"):
            self._loc = conf.lib.Devil_getCursorLocation(self)
        return self._loc
    @property
    def linkage(self):
        if not hasattr(self, "_linkage"):
            self._linkage = conf.lib.Devil_getCursorLinkage(self)
        return LinkageKind.from_id(self._linkage)
    @property
    def tls_kind(self):
        if not hasattr(self, "_tls_kind"):
            self._tls_kind = conf.lib.Devil_getCursorTLSKind(self)
        return TLSKind.from_id(self._tls_kind)
    @property
    def extent(self):
        Return the source range (the range of text) occupied by the entity
        pointed at by the cursor.
        if not hasattr(self, "_extent"):
            self._extent = conf.lib.Devil_getCursorExtent(self)
        return self._extent
    @property
    def storage_class(self):
        Retrieves the storage class (if any) of the entity pointed at by the
        cursor.
        if not hasattr(self, "_storage_class"):
            self._storage_class = conf.lib.Devil_Cursor_getStorageClass(self)
        return StorageClass.from_id(self._storage_class)
    @property
    def availability(self):
        Retrieves the availability of the entity pointed at by the cursor.
        if not hasattr(self, "_availability"):
            self._availability = conf.lib.Devil_getCursorAvailability(self)
        return AvailabilityKind.from_id(self._availability)
    @property
    def access_specifier(self):
        Retrieves the access specifier (if any) of the entity pointed at by the
        cursor.
        if not hasattr(self, "_access_specifier"):
            self._access_specifier = conf.lib.Devil_getCXXAccessSpecifier(self)
        return AccessSpecifier.from_id(self._access_specifier)
    @property
    def type(self):
        Retrieve the Type (if any) of the entity pointed at by the cursor.
        if not hasattr(self, "_type"):
            self._type = conf.lib.Devil_getCursorType(self)
        return self._type
    @property
    def canonical(self):
        The canonical cursor is the cursor which is representative for the
        underlying entity. For example, if you have multiple forward
        declarations for the same class, the canonical cursor for the forward
        declarations will be identical.
        if not hasattr(self, "_canonical"):
            self._canonical = conf.lib.Devil_getCanonicalCursor(self)
        return self._canonical
    @property
    def result_type(self):
        if not hasattr(self, "_result_type"):
            self._result_type = conf.lib.Devil_getCursorResultType(self)
        return self._result_type
    @property
    def exception_specification_kind(self):
        Retrieve the exception specification kind, which is one of the values
        from the ExceptionSpecificationKind enumeration.
        if not hasattr(self, "_exception_specification_kind"):
            exc_kind = conf.lib.Devil_getCursorExceptionSpecificationType(self)
            self._exception_specification_kind = ExceptionSpecificationKind.from_id(
                exc_kind
            )
        return self._exception_specification_kind
    @property
    def underlying_typedef_type(self):
        Returns a Type for the typedef this cursor is a declaration for. If
        the current cursor is not a typedef, this raises.
        if not hasattr(self, "_underlying_type"):
            assert self.kind.is_declaration()
            self._underlying_type = conf.lib.Devil_getTypedefDeclUnderlyingType(self)
        return self._underlying_type
    @property
    def enum_type(self):
        Returns a Type corresponding to an integer. If the cursor is not for an
        enum, this raises.
        if not hasattr(self, "_enum_type"):
            assert self.kind == CursorKind.ENUM_DECL
            self._enum_type = conf.lib.Devil_getEnumDeclIntegerType(self)
        return self._enum_type
    @property
    def enum_value(self):
        if not hasattr(self, "_enum_value"):
            assert self.kind == CursorKind.ENUM_CONSTANT_DECL
            underlying_type = self.type
            if underlying_type.kind == TypeKind.ENUM:
                underlying_type = underlying_type.get_declaration().enum_type
            if underlying_type.kind in (
                TypeKind.CHAR_U,
                TypeKind.UCHAR,
                TypeKind.CHAR16,
                TypeKind.CHAR32,
                TypeKind.USHORT,
                TypeKind.UINT,
                TypeKind.ULONG,
                TypeKind.ULONGLONG,
                TypeKind.UINT128,
            ):
                self._enum_value = conf.lib.Devil_getEnumConstantDeclUnsignedValue(self)
            else:
                self._enum_value = conf.lib.Devil_getEnumConstantDeclValue(self)
        return self._enum_value
    @property
    def objc_type_encoding(self):
        if not hasattr(self, "_objc_type_encoding"):
            self._objc_type_encoding = conf.lib.Devil_getDeclObjCTypeEncoding(self)
        return self._objc_type_encoding
    @property
    def hash(self):
        if not hasattr(self, "_hash"):
            self._hash = conf.lib.Devil_hashCursor(self)
        return self._hash
    @property
    def semantic_parent(self):
        if not hasattr(self, "_semantic_parent"):
            self._semantic_parent = conf.lib.Devil_getCursorSemanticParent(self)
        return self._semantic_parent
    @property
    def lexical_parent(self):
        if not hasattr(self, "_lexical_parent"):
            self._lexical_parent = conf.lib.Devil_getCursorLexicalParent(self)
        return self._lexical_parent
    @property
    def translation_unit(self):
        return self._tu
    @property
    def referenced(self):
        For a cursor that is a reference, returns a cursor
        representing the entity that it references.
        if not hasattr(self, "_referenced"):
            self._referenced = conf.lib.Devil_getCursorReferenced(self)
        return self._referenced
    @property
    def brief_comment(self):
        return conf.lib.Devil_Cursor_getBriefCommentText(self)
    @property
    def raw_comment(self):
        return conf.lib.Devil_Cursor_getRawCommentText(self)
    def get_arguments(self):
        num_args = conf.lib.Devil_Cursor_getNumArguments(self)
        for i in range(0, num_args):
            yield conf.lib.Devil_Cursor_getArgument(self, i)
    def get_num_template_arguments(self):
        return conf.lib.Devil_Cursor_getNumTemplateArguments(self)
    def get_template_argument_kind(self, num):
        argument."""
        return conf.lib.Devil_Cursor_getTemplateArgumentKind(self, num)
    def get_template_argument_type(self, num):
        return conf.lib.Devil_Cursor_getTemplateArgumentType(self, num)
    def get_template_argument_value(self, num):
        return conf.lib.Devil_Cursor_getTemplateArgumentValue(self, num)
    def get_template_argument_unsigned_value(self, num):
        return conf.lib.Devil_Cursor_getTemplateArgumentUnsignedValue(self, num)
    def get_children(self):
        def visitor(child, parent, children):
            assert child != conf.lib.Devil_getNullCursor()
            child._tu = self._tu
            children.append(child)
            return 1  # continue
        children = []
        conf.lib.Devil_visitChildren(self, callbacks["cursor_visit"](visitor), children)
        return iter(children)
    def walk_preorder(self):
        Yields cursors.
        yield self
        for child in self.get_children():
            for descendant in child.walk_preorder():
                yield descendant
    def get_tokens(self):
        This is a generator for Token instances. It returns all tokens which
        occupy the extent this cursor occupies.
        return TokenGroup.get_tokens(self._tu, self.extent)
    def get_field_offsetof(self):
        return conf.lib.Devil_Cursor_getOffsetOfField(self)
    def is_anonymous(self):
        Check if the record is anonymous.
        if self.kind == CursorKind.FIELD_DECL:
            return self.type.get_declaration().is_anonymous()
        return conf.lib.Devil_Cursor_isAnonymous(self)
    def is_bitfield(self):
        Check if the field is a bitfield.
        return conf.lib.Devil_Cursor_isBitField(self)
    def get_bitfield_width(self):
        Retrieve the width of a bitfield.
        return conf.lib.Devil_getFieldDeclBitWidth(self)
    @staticmethod
    def from_result(res, fn, args):
        assert isinstance(res, Cursor)
        if res == conf.lib.Devil_getNullCursor():
            return None
        tu = None
        for arg in args:
            if isinstance(arg, TranslationUnit):
                tu = arg
                break
            if hasattr(arg, "translation_unit"):
                tu = arg.translation_unit
                break
        assert tu is not None
        res._tu = tu
        return res
    @staticmethod
    def from_cursor_result(res, fn, args):
        assert isinstance(res, Cursor)
        if res == conf.lib.Devil_getNullCursor():
            return None
        res._tu = args[0]._tu
        return res
class StorageClass(object):
    Describes the storage class of a declaration
    _kinds = []
    _name_map = None
    def __init__(self, value):
        if value >= len(StorageClass._kinds):
            StorageClass._kinds += [None] * (value - len(StorageClass._kinds) + 1)
        if StorageClass._kinds[value] is not None:
            raise ValueError("StorageClass already loaded")
        self.value = value
        StorageClass._kinds[value] = self
        StorageClass._name_map = None
    def from_param(self):
        return self.value
    @property
    def name(self):
        if self._name_map is None:
            self._name_map = {}
            for key, value in StorageClass.__dict__.items():
                if isinstance(value, StorageClass):
                    self._name_map[value] = key
        return self._name_map[self]
    @staticmethod
    def from_id(id):
        if id >= len(StorageClass._kinds) or not StorageClass._kinds[id]:
            raise ValueError("Unknown storage class %d" % id)
        return StorageClass._kinds[id]
    def __repr__(self):
        return "StorageClass.%s" % (self.name,)
StorageClass.INVALID = StorageClass(0)
StorageClass.NONE = StorageClass(1)
StorageClass.EXTERN = StorageClass(2)
StorageClass.STATIC = StorageClass(3)
StorageClass.PRIVATEEXTERN = StorageClass(4)
StorageClass.OPENCLWORKGROUPLOCAL = StorageClass(5)
StorageClass.AUTO = StorageClass(6)
StorageClass.REGISTER = StorageClass(7)
class AvailabilityKind(BaseEnumeration):
    Describes the availability of an entity.
    _kinds = []
    _name_map = None
    def __repr__(self):
        return "AvailabilityKind.%s" % (self.name,)
AvailabilityKind.AVAILABLE = AvailabilityKind(0)
AvailabilityKind.DEPRECATED = AvailabilityKind(1)
AvailabilityKind.NOT_AVAILABLE = AvailabilityKind(2)
AvailabilityKind.NOT_ACCESSIBLE = AvailabilityKind(3)
class AccessSpecifier(BaseEnumeration):
    Describes the access of a C++ class member
    _kinds = []
    _name_map = None
    def from_param(self):
        return self.value
    def __repr__(self):
        return "AccessSpecifier.%s" % (self.name,)
AccessSpecifier.INVALID = AccessSpecifier(0)
AccessSpecifier.PUBLIC = AccessSpecifier(1)
AccessSpecifier.PROTECTED = AccessSpecifier(2)
AccessSpecifier.PRIVATE = AccessSpecifier(3)
AccessSpecifier.NONE = AccessSpecifier(4)
class TypeKind(BaseEnumeration):
    Describes the kind of type.
    _kinds = []
    _name_map = None
    @property
    def spelling(self):
        return conf.lib.Devil_getTypeKindSpelling(self.value)
    def __repr__(self):
        return "TypeKind.%s" % (self.name,)
TypeKind.INVALID = TypeKind(0)
TypeKind.UNEXPOSED = TypeKind(1)
TypeKind.VOID = TypeKind(2)
TypeKind.BOOL = TypeKind(3)
TypeKind.CHAR_U = TypeKind(4)
TypeKind.UCHAR = TypeKind(5)
TypeKind.CHAR16 = TypeKind(6)
TypeKind.CHAR32 = TypeKind(7)
TypeKind.USHORT = TypeKind(8)
TypeKind.UINT = TypeKind(9)
TypeKind.ULONG = TypeKind(10)
TypeKind.ULONGLONG = TypeKind(11)
TypeKind.UINT128 = TypeKind(12)
TypeKind.CHAR_S = TypeKind(13)
TypeKind.SCHAR = TypeKind(14)
TypeKind.WCHAR = TypeKind(15)
TypeKind.SHORT = TypeKind(16)
TypeKind.INT = TypeKind(17)
TypeKind.LONG = TypeKind(18)
TypeKind.LONGLONG = TypeKind(19)
TypeKind.INT128 = TypeKind(20)
TypeKind.FLOAT = TypeKind(21)
TypeKind.DOUBLE = TypeKind(22)
TypeKind.LONGDOUBLE = TypeKind(23)
TypeKind.NULLPTR = TypeKind(24)
TypeKind.OVERLOAD = TypeKind(25)
TypeKind.DEPENDENT = TypeKind(26)
TypeKind.OBJCID = TypeKind(27)
TypeKind.OBJCCLASS = TypeKind(28)
TypeKind.OBJCSEL = TypeKind(29)
TypeKind.FLOAT128 = TypeKind(30)
TypeKind.HALF = TypeKind(31)
TypeKind.IBM128 = TypeKind(40)
TypeKind.COMPLEX = TypeKind(100)
TypeKind.POINTER = TypeKind(101)
TypeKind.BLOCKPOINTER = TypeKind(102)
TypeKind.LVALUEREFERENCE = TypeKind(103)
TypeKind.RVALUEREFERENCE = TypeKind(104)
TypeKind.RECORD = TypeKind(105)
TypeKind.ENUM = TypeKind(106)
TypeKind.TYPEDEF = TypeKind(107)
TypeKind.OBJCINTERFACE = TypeKind(108)
TypeKind.OBJCOBJECTPOINTER = TypeKind(109)
TypeKind.FUNCTIONNOPROTO = TypeKind(110)
TypeKind.FUNCTIONPROTO = TypeKind(111)
TypeKind.CONSTANTARRAY = TypeKind(112)
TypeKind.VECTOR = TypeKind(113)
TypeKind.INCOMPLETEARRAY = TypeKind(114)
TypeKind.VARIABLEARRAY = TypeKind(115)
TypeKind.DEPENDENTSIZEDARRAY = TypeKind(116)
TypeKind.MEMBERPOINTER = TypeKind(117)
TypeKind.AUTO = TypeKind(118)
TypeKind.ELABORATED = TypeKind(119)
TypeKind.PIPE = TypeKind(120)
TypeKind.OCLIMAGE1DRO = TypeKind(121)
TypeKind.OCLIMAGE1DARRAYRO = TypeKind(122)
TypeKind.OCLIMAGE1DBUFFERRO = TypeKind(123)
TypeKind.OCLIMAGE2DRO = TypeKind(124)
TypeKind.OCLIMAGE2DARRAYRO = TypeKind(125)
TypeKind.OCLIMAGE2DDEPTHRO = TypeKind(126)
TypeKind.OCLIMAGE2DARRAYDEPTHRO = TypeKind(127)
TypeKind.OCLIMAGE2DMSAARO = TypeKind(128)
TypeKind.OCLIMAGE2DARRAYMSAARO = TypeKind(129)
TypeKind.OCLIMAGE2DMSAADEPTHRO = TypeKind(130)
TypeKind.OCLIMAGE2DARRAYMSAADEPTHRO = TypeKind(131)
TypeKind.OCLIMAGE3DRO = TypeKind(132)
TypeKind.OCLIMAGE1DWO = TypeKind(133)
TypeKind.OCLIMAGE1DARRAYWO = TypeKind(134)
TypeKind.OCLIMAGE1DBUFFERWO = TypeKind(135)
TypeKind.OCLIMAGE2DWO = TypeKind(136)
TypeKind.OCLIMAGE2DARRAYWO = TypeKind(137)
TypeKind.OCLIMAGE2DDEPTHWO = TypeKind(138)
TypeKind.OCLIMAGE2DARRAYDEPTHWO = TypeKind(139)
TypeKind.OCLIMAGE2DMSAAWO = TypeKind(140)
TypeKind.OCLIMAGE2DARRAYMSAAWO = TypeKind(141)
TypeKind.OCLIMAGE2DMSAADEPTHWO = TypeKind(142)
TypeKind.OCLIMAGE2DARRAYMSAADEPTHWO = TypeKind(143)
TypeKind.OCLIMAGE3DWO = TypeKind(144)
TypeKind.OCLIMAGE1DRW = TypeKind(145)
TypeKind.OCLIMAGE1DARRAYRW = TypeKind(146)
TypeKind.OCLIMAGE1DBUFFERRW = TypeKind(147)
TypeKind.OCLIMAGE2DRW = TypeKind(148)
TypeKind.OCLIMAGE2DARRAYRW = TypeKind(149)
TypeKind.OCLIMAGE2DDEPTHRW = TypeKind(150)
TypeKind.OCLIMAGE2DARRAYDEPTHRW = TypeKind(151)
TypeKind.OCLIMAGE2DMSAARW = TypeKind(152)
TypeKind.OCLIMAGE2DARRAYMSAARW = TypeKind(153)
TypeKind.OCLIMAGE2DMSAADEPTHRW = TypeKind(154)
TypeKind.OCLIMAGE2DARRAYMSAADEPTHRW = TypeKind(155)
TypeKind.OCLIMAGE3DRW = TypeKind(156)
TypeKind.OCLSAMPLER = TypeKind(157)
TypeKind.OCLEVENT = TypeKind(158)
TypeKind.OCLQUEUE = TypeKind(159)
TypeKind.OCLRESERVEID = TypeKind(160)
TypeKind.EXTVECTOR = TypeKind(176)
TypeKind.ATOMIC = TypeKind(177)
class RefQualifierKind(BaseEnumeration):
    _kinds = []
    _name_map = None
    def from_param(self):
        return self.value
    def __repr__(self):
        return "RefQualifierKind.%s" % (self.name,)
RefQualifierKind.NONE = RefQualifierKind(0)
RefQualifierKind.LVALUE = RefQualifierKind(1)
RefQualifierKind.RVALUE = RefQualifierKind(2)
class LinkageKind(BaseEnumeration):
    _kinds = []
    _name_map = None
    def from_param(self):
        return self.value
    def __repr__(self):
        return "LinkageKind.%s" % (self.name,)
LinkageKind.INVALID = LinkageKind(0)
LinkageKind.NO_LINKAGE = LinkageKind(1)
LinkageKind.INTERNAL = LinkageKind(2)
LinkageKind.UNIQUE_EXTERNAL = LinkageKind(3)
LinkageKind.EXTERNAL = LinkageKind(4)
class TLSKind(BaseEnumeration):
    _kinds = []
    _name_map = None
    def from_param(self):
        return self.value
    def __repr__(self):
        return "TLSKind.%s" % (self.name,)
TLSKind.NONE = TLSKind(0)
TLSKind.DYNAMIC = TLSKind(1)
TLSKind.STATIC = TLSKind(2)
class Type(Structure):
    The type of an element in the abstract syntax tree.
    _fields_ = [("_kind_id", c_int), ("data", c_void_p * 2)]
    @property
    def kind(self):
        return TypeKind.from_id(self._kind_id)
    def argument_types(self):
        The returned object is iterable and indexable. Each item in the
        container is a Type instance.
        class ArgumentsIterator(collections_abc.Sequence):
            def __init__(self, parent):
                self.parent = parent
                self.length = None
            def __len__(self):
                if self.length is None:
                    self.length = conf.lib.Devil_getNumArgTypes(self.parent)
                return self.length
            def __getitem__(self, key):
                if not isinstance(key, int):
                    raise TypeError("Must supply a non-negative int.")
                if key < 0:
                    raise IndexError("Only non-negative indexes are accepted.")
                if key >= len(self):
                    raise IndexError(
                        "Index greater than container length: "
                        "%d > %d" % (key, len(self))
                    )
                result = conf.lib.Devil_getArgType(self.parent, key)
                if result.kind == TypeKind.INVALID:
                    raise IndexError("Argument could not be retrieved.")
                return result
        assert self.kind == TypeKind.FUNCTIONPROTO
        return ArgumentsIterator(self)
    @property
    def element_type(self):
        If accessed on a type that is not an array, complex, or vector type, an
        exception will be raised.
        result = conf.lib.Devil_getElementType(self)
        if result.kind == TypeKind.INVALID:
            raise Exception("Element type not available on this type.")
        return result
    @property
    def element_count(self):
        Returns an int.
        If the Type is not an array or vector, this raises.
        result = conf.lib.Devil_getNumElements(self)
        if result < 0:
            raise Exception("Type does not have elements.")
        return result
    @property
    def translation_unit(self):
        return self._tu
    @staticmethod
    def from_result(res, fn, args):
        assert isinstance(res, Type)
        tu = None
        for arg in args:
            if hasattr(arg, "translation_unit"):
                tu = arg.translation_unit
                break
        assert tu is not None
        res._tu = tu
        return res
    def get_num_template_arguments(self):
        return conf.lib.Devil_Type_getNumTemplateArguments(self)
    def get_template_argument_type(self, num):
        return conf.lib.Devil_Type_getTemplateArgumentAsType(self, num)
    def get_canonical(self):
        Return the canonical type for a Type.
        Devil's type system explicitly models typedefs and all the
        ways a specific type can be represented.  The canonical type
        is the underlying type with all the "sugar" removed.  For
        example, if 'T' is a typedef for 'int', the canonical type for
        'T' would be 'int'.
        return conf.lib.Devil_getCanonicalType(self)
    def is_const_qualified(self):
        This does not look through typedefs that may have added "const"
        at a different level.
        return conf.lib.Devil_isConstQualifiedType(self)
    def is_volatile_qualified(self):
        This does not look through typedefs that may have added "volatile"
        at a different level.
        return conf.lib.Devil_isVolatileQualifiedType(self)
    def is_restrict_qualified(self):
        This does not look through typedefs that may have added "restrict" at
        a different level.
        return conf.lib.Devil_isRestrictQualifiedType(self)
    def is_function_variadic(self):
        assert self.kind == TypeKind.FUNCTIONPROTO
        return conf.lib.Devil_isFunctionTypeVariadic(self)
    def get_address_space(self):
        return conf.lib.Devil_getAddressSpace(self)
    def get_typedef_name(self):
        return conf.lib.Devil_getTypedefName(self)
    def is_pod(self):
        return conf.lib.Devil_isPODType(self)
    def get_pointee(self):
        For pointer types, returns the type of the pointee.
        return conf.lib.Devil_getPointeeType(self)
    def get_declaration(self):
        Return the cursor for the declaration of the given type.
        return conf.lib.Devil_getTypeDeclaration(self)
    def get_result(self):
        Retrieve the result type associated with a function type.
        return conf.lib.Devil_getResultType(self)
    def get_array_element_type(self):
        Retrieve the type of the elements of the array type.
        return conf.lib.Devil_getArrayElementType(self)
    def get_array_size(self):
        Retrieve the size of the constant array.
        return conf.lib.Devil_getArraySize(self)
    def get_class_type(self):
        Retrieve the class type of the member pointer type.
        return conf.lib.Devil_Type_getClassType(self)
    def get_named_type(self):
        Retrieve the type named by the qualified-id.
        return conf.lib.Devil_Type_getNamedType(self)
    def get_align(self):
        Retrieve the alignment of the record.
        return conf.lib.Devil_Type_getAlignOf(self)
    def get_size(self):
        Retrieve the size of the record.
        return conf.lib.Devil_Type_getSizeOf(self)
    def get_offset(self, fieldname):
        Retrieve the offset of a field in the record.
        return conf.lib.Devil_Type_getOffsetOf(self, fieldname)
    def get_ref_qualifier(self):
        Retrieve the ref-qualifier of the type.
        return RefQualifierKind.from_id(conf.lib.Devil_Type_getCXXRefQualifier(self))
    def get_fields(self):
        def visitor(field, children):
            assert field != conf.lib.Devil_getNullCursor()
            field._tu = self._tu
            fields.append(field)
            return 1  # continue
        fields = []
        conf.lib.Devil_Type_visitFields(
            self, callbacks["fields_visit"](visitor), fields
        )
        return iter(fields)
    def get_exception_specification_kind(self):
        Return the kind of the exception specification; a value from
        the ExceptionSpecificationKind enumeration.
        return ExceptionSpecificationKind.from_id(
            conf.lib.Devil.getExceptionSpecificationType(self)
        )
    @property
    def spelling(self):
        return conf.lib.Devil_getTypeSpelling(self)
    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return conf.lib.Devil_equalTypes(self, other)
    def __ne__(self, other):
        return not self.__eq__(other)
class DevilObject(object):
    A helper for Devil objects. This class helps act as an intermediary for
    the ctypes library and the Devil DevilTop library.
    def __init__(self, obj):
        assert isinstance(obj, c_object_p) and obj
        self.obj = self._as_parameter_ = obj
    def from_param(self):
        return self._as_parameter_
class _CXUnsavedFile(Structure):
    _fields_ = [("name", c_char_p), ("contents", c_char_p), ("length", c_ulong)]
SpellingCache = {
    6: "(",  # CompletionChunk.Kind("LeftParen"),
    7: ")",  # CompletionChunk.Kind("RightParen"),
    8: "[",  # CompletionChunk.Kind("LeftBracket"),
    9: "]",  # CompletionChunk.Kind("RightBracket"),
    10: "{",  # CompletionChunk.Kind("LeftBrace"),
    11: "}",  # CompletionChunk.Kind("RightBrace"),
    12: "<",  # CompletionChunk.Kind("LeftAngle"),
    13: ">",  # CompletionChunk.Kind("RightAngle"),
    14: ", ",  # CompletionChunk.Kind("Comma"),
    16: ":",  # CompletionChunk.Kind("Colon"),
    17: ";",  # CompletionChunk.Kind("SemiColon"),
    18: "=",  # CompletionChunk.Kind("Equal"),
    19: " ",  # CompletionChunk.Kind("HorizontalSpace"),
}
class CompletionChunk(object):
    class Kind(object):
        def __init__(self, name):
            self.name = name
        def __str__(self):
            return self.name
        def __repr__(self):
            return "<ChunkKind: %s>" % self
    def __init__(self, completionString, key):
        self.cs = completionString
        self.key = key
        self.__kindNumberCache = -1
    def __repr__(self):
        return "{'" + self.spelling + "', " + str(self.kind) + "}"
    @CachedProperty
    def spelling(self):
        if self.__kindNumber in SpellingCache:
            return SpellingCache[self.__kindNumber]
        return conf.lib.Devil_getCompletionChunkText(self.cs, self.key)
    @property
    def __kindNumber(self):
        if self.__kindNumberCache == -1:
            self.__kindNumberCache = conf.lib.Devil_getCompletionChunkKind(
                self.cs, self.key
            )
        return self.__kindNumberCache
    @CachedProperty
    def kind(self):
        return completionChunkKindMap[self.__kindNumber]
    @CachedProperty
    def string(self):
        res = conf.lib.Devil_getCompletionChunkCompletionString(self.cs, self.key)
        if res:
            return CompletionString(res)
        else:
            None
    def isKindOptional(self):
        return self.__kindNumber == 0
    def isKindTypedText(self):
        return self.__kindNumber == 1
    def isKindPlaceHolder(self):
        return self.__kindNumber == 3
    def isKindInformative(self):
        return self.__kindNumber == 4
    def isKindResultType(self):
        return self.__kindNumber == 15
completionChunkKindMap = {
    0: CompletionChunk.Kind("Optional"),
    1: CompletionChunk.Kind("TypedText"),
    2: CompletionChunk.Kind("Text"),
    3: CompletionChunk.Kind("Placeholder"),
    4: CompletionChunk.Kind("Informative"),
    5: CompletionChunk.Kind("CurrentParameter"),
    6: CompletionChunk.Kind("LeftParen"),
    7: CompletionChunk.Kind("RightParen"),
    8: CompletionChunk.Kind("LeftBracket"),
    9: CompletionChunk.Kind("RightBracket"),
    10: CompletionChunk.Kind("LeftBrace"),
    11: CompletionChunk.Kind("RightBrace"),
    12: CompletionChunk.Kind("LeftAngle"),
    13: CompletionChunk.Kind("RightAngle"),
    14: CompletionChunk.Kind("Comma"),
    15: CompletionChunk.Kind("ResultType"),
    16: CompletionChunk.Kind("Colon"),
    17: CompletionChunk.Kind("SemiColon"),
    18: CompletionChunk.Kind("Equal"),
    19: CompletionChunk.Kind("HorizontalSpace"),
    20: CompletionChunk.Kind("VerticalSpace"),
}
class CompletionString(DevilObject):
    class Availability(object):
        def __init__(self, name):
            self.name = name
        def __str__(self):
            return self.name
        def __repr__(self):
            return "<Availability: %s>" % self
    def __len__(self):
        return self.num_chunks
    @CachedProperty
    def num_chunks(self):
        return conf.lib.Devil_getNumCompletionChunks(self.obj)
    def __getitem__(self, key):
        if self.num_chunks <= key:
            raise IndexError
        return CompletionChunk(self.obj, key)
    @property
    def priority(self):
        return conf.lib.Devil_getCompletionPriority(self.obj)
    @property
    def availability(self):
        res = conf.lib.Devil_getCompletionAvailability(self.obj)
        return availabilityKinds[res]
    @property
    def briefComment(self):
        if conf.function_exists("Devil_getCompletionBriefComment"):
            return conf.lib.Devil_getCompletionBriefComment(self.obj)
        return _CXString()
    def __repr__(self):
        return (
            " | ".join([str(a) for a in self])
            + " || Priority: "
            + str(self.priority)
            + " || Availability: "
            + str(self.availability)
            + " || Brief comment: "
            + str(self.briefComment)
        )
availabilityKinds = {
    0: CompletionChunk.Kind("Available"),
    1: CompletionChunk.Kind("Deprecated"),
    2: CompletionChunk.Kind("NotAvailable"),
    3: CompletionChunk.Kind("NotAccessible"),
}
class CodeCompletionResult(Structure):
    _fields_ = [("cursorKind", c_int), ("completionString", c_object_p)]
    def __repr__(self):
        return str(CompletionString(self.completionString))
    @property
    def kind(self):
        return CursorKind.from_id(self.cursorKind)
    @property
    def string(self):
        return CompletionString(self.completionString)
class CCRStructure(Structure):
    _fields_ = [("results", POINTER(CodeCompletionResult)), ("numResults", c_int)]
    def __len__(self):
        return self.numResults
    def __getitem__(self, key):
        if len(self) <= key:
            raise IndexError
        return self.results[key]
class CodeCompletionResults(DevilObject):
    def __init__(self, ptr):
        assert isinstance(ptr, POINTER(CCRStructure)) and ptr
        self.ptr = self._as_parameter_ = ptr
    def from_param(self):
        return self._as_parameter_
    def __del__(self):
        conf.lib.Devil_disposeCodeCompleteResults(self)
    @property
    def results(self):
        return self.ptr.contents
    @property
    def diagnostics(self):
        class DiagnosticsItr(object):
            def __init__(self, ccr):
                self.ccr = ccr
            def __len__(self):
                return int(conf.lib.Devil_codeCompleteGetNumDiagnostics(self.ccr))
            def __getitem__(self, key):
                return conf.lib.Devil_codeCompleteGetDiagnostic(self.ccr, key)
        return DiagnosticsItr(self)
class Index(DevilObject):
    The Index type provides the primary interface to the Devil DevilTop library,
    primarily by providing an interface for reading and parsing translation
    units.
    @staticmethod
    def create(excludeDecls=False):
        Create a new Index.
        Parameters:
        excludeDecls -- Exclude local declarations from translation units.
        return Index(conf.lib.Devil_createIndex(excludeDecls, 0))
    def __del__(self):
        conf.lib.Devil_disposeIndex(self)
    def read(self, path):
        return TranslationUnit.from_ast_file(path, self)
    def parse(self, path, args=None, unsaved_files=None, options=0):
        Devil and generating the AST before loading. Additional command line
        parameters can be passed to Devil via the args parameter.
        In-memory contents for files can be provided by passing a list of pairs
        to as unsaved_files, the first item should be the filenames to be mapped
        and the second should be the contents to be substituted for the
        file. The contents may be passed as strings or file objects.
        If an error was encountered during parsing, a TranslationUnitLoadError
        will be raised.
        return TranslationUnit.from_source(path, args, unsaved_files, options, self)
class TranslationUnit(DevilObject):
    This is one of the main types in the API. Any time you wish to interact
    with Devil's representation of a source file, you typically start with a
    translation unit.
    PARSE_NONE = 0
    PARSE_DETAILED_PROCESSING_RECORD = 1
    PARSE_INCOMPLETE = 2
    PARSE_PRECOMPILED_PREAMBLE = 4
    PARSE_CACHE_COMPLETION_RESULTS = 8
    PARSE_SKIP_FUNCTION_BODIES = 64
    PARSE_INCLUDE_BRIEF_COMMENTS_IN_CODE_COMPLETION = 128
    @classmethod
    def from_source(
        cls, filename, args=None, unsaved_files=None, options=0, index=None
    ):
        This is capable of processing source code both from files on the
        filesystem as well as in-memory contents.
        Command-line arguments that would be passed to Devil are specified as
        a list via args. These can be used to specify include paths, warnings,
        etc. e.g. ["-Wall", "-I/path/to/include"].
        In-memory file content can be provided via unsaved_files. This is an
        iterable of 2-tuples. The first element is the filename (str or
        PathLike). The second element defines the content. Content can be
        provided as str source code or as file objects (anything with a read()
        method). If a file object is being used, content will be read until EOF
        and the read cursor will not be reset to its original position.
        options is a bitwise or of TranslationUnit.PARSE_XXX flags which will
        control parsing behavior.
        index is an Index instance to utilize. If not provided, a new Index
        will be created for this TranslationUnit.
        To parse source from the filesystem, the filename of the file to parse
        is specified by the filename argument. Or, filename could be None and
        the args list would contain the filename(s) to parse.
        To parse source from an in-memory buffer, set filename to the virtual
        filename you wish to associate with this source (e.g. "test.c"). The
        contents of that file are then provided in unsaved_files.
        If an error occurs, a TranslationUnitLoadError is raised.
        Please note that a TranslationUnit with parser errors may be returned.
        It is the caller's responsibility to check tu.diagnostics for errors.
        Also note that Devil infers the source language from the extension of
        the input filename. If you pass in source code containing a C++ class
        declaration with the filename "test.c" parsing will fail.
        if args is None:
            args = []
        if unsaved_files is None:
            unsaved_files = []
        if index is None:
            index = Index.create()
        args_array = None
        if len(args) > 0:
            args_array = (c_char_p * len(args))(*[b(x) for x in args])
        unsaved_array = None
        if len(unsaved_files) > 0:
            unsaved_array = (_CXUnsavedFile * len(unsaved_files))()
            for i, (name, contents) in enumerate(unsaved_files):
                if hasattr(contents, "read"):
                    contents = contents.read()
                contents = b(contents)
                unsaved_array[i].name = b(fspath(name))
                unsaved_array[i].contents = contents
                unsaved_array[i].length = len(contents)
        ptr = conf.lib.Devil_parseTranslationUnit(
            index,
            fspath(filename) if filename is not None else None,
            args_array,
            len(args),
            unsaved_array,
            len(unsaved_files),
            options,
        )
        if not ptr:
            raise TranslationUnitLoadError("Error parsing translation unit.")
        return cls(ptr, index=index)
    @classmethod
    def from_ast_file(cls, filename, index=None):
        A previously-saved AST file (provided with -emit-ast or
        TranslationUnit.save()) is loaded from the filename specified.
        If the file cannot be loaded, a TranslationUnitLoadError will be
        raised.
        index is optional and is the Index instance to use. If not provided,
        a default Index will be created.
        filename can be str or PathLike.
        if index is None:
            index = Index.create()
        ptr = conf.lib.Devil_createTranslationUnit(index, fspath(filename))
        if not ptr:
            raise TranslationUnitLoadError(filename)
        return cls(ptr=ptr, index=index)
    def __init__(self, ptr, index):
        TranslationUnits should be created using one of the from_* @classmethod
        functions above. __init__ is only called internally.
        assert isinstance(index, Index)
        self.index = index
        DevilObject.__init__(self, ptr)
    def __del__(self):
        conf.lib.Devil_disposeTranslationUnit(self)
    @property
    def cursor(self):
        return conf.lib.Devil_getTranslationUnitCursor(self)
    @property
    def spelling(self):
        return conf.lib.Devil_getTranslationUnitSpelling(self)
    def get_includes(self):
        Return an iterable sequence of FileInclusion objects that describe the
        sequence of inclusions in a translation unit. The first object in
        this sequence is always the input file. Note that this method will not
        recursively iterate over header files included through precompiled
        headers.
        def visitor(fobj, lptr, depth, includes):
            if depth > 0:
                loc = lptr.contents
                includes.append(FileInclusion(loc.file, File(fobj), loc, depth))
        includes = []
        conf.lib.Devil_getInclusions(
            self, callbacks["translation_unit_includes"](visitor), includes
        )
        return iter(includes)
    def get_file(self, filename):
        return File.from_name(self, filename)
    def get_location(self, filename, position):
        The position can be specified by passing:
          - Integer file offset. Initial file offset is 0.
          - 2-tuple of (line number, column number). Initial file position is
            (0, 0)
        f = self.get_file(filename)
        if isinstance(position, int):
            return SourceLocation.from_offset(self, f, position)
        return SourceLocation.from_position(self, f, position[0], position[1])
    def get_extent(self, filename, locations):
        The bounds of the SourceRange must ultimately be defined by a start and
        end SourceLocation. For the locations argument, you can pass:
          - 2 SourceLocation instances in a 2-tuple or list.
          - 2 int file offsets via a 2-tuple or list.
          - 2 2-tuple or lists of (line, column) pairs in a 2-tuple or list.
        e.g.
        get_extent('foo.c', (5, 10))
        get_extent('foo.c', ((1, 1), (1, 15)))
        f = self.get_file(filename)
        if len(locations) < 2:
            raise Exception("Must pass object with at least 2 elements")
        start_location, end_location = locations
        if hasattr(start_location, "__len__"):
            start_location = SourceLocation.from_position(
                self, f, start_location[0], start_location[1]
            )
        elif isinstance(start_location, int):
            start_location = SourceLocation.from_offset(self, f, start_location)
        if hasattr(end_location, "__len__"):
            end_location = SourceLocation.from_position(
                self, f, end_location[0], end_location[1]
            )
        elif isinstance(end_location, int):
            end_location = SourceLocation.from_offset(self, f, end_location)
        assert isinstance(start_location, SourceLocation)
        assert isinstance(end_location, SourceLocation)
        return SourceRange.from_locations(start_location, end_location)
    @property
    def diagnostics(self):
        Return an iterable (and indexable) object containing the diagnostics.
        class DiagIterator(object):
            def __init__(self, tu):
                self.tu = tu
            def __len__(self):
                return int(conf.lib.Devil_getNumDiagnostics(self.tu))
            def __getitem__(self, key):
                diag = conf.lib.Devil_getDiagnostic(self.tu, key)
                if not diag:
                    raise IndexError
                return Diagnostic(diag)
        return DiagIterator(self)
    def reparse(self, unsaved_files=None, options=0):
        Reparse an already parsed translation unit.
        In-memory contents for files can be provided by passing a list of pairs
        as unsaved_files, the first items should be the filenames to be mapped
        and the second should be the contents to be substituted for the
        file. The contents may be passed as strings or file objects.
        if unsaved_files is None:
            unsaved_files = []
        unsaved_files_array = 0
        if len(unsaved_files):
            unsaved_files_array = (_CXUnsavedFile * len(unsaved_files))()
            for i, (name, contents) in enumerate(unsaved_files):
                if hasattr(contents, "read"):
                    contents = contents.read()
                contents = b(contents)
                unsaved_files_array[i].name = b(fspath(name))
                unsaved_files_array[i].contents = contents
                unsaved_files_array[i].length = len(contents)
        ptr = conf.lib.Devil_reparseTranslationUnit(
            self, len(unsaved_files), unsaved_files_array, options
        )
    def save(self, filename):
        This is equivalent to passing -emit-ast to the Devil frontend. The
        saved file can be loaded back into a TranslationUnit. Or, if it
        corresponds to a header, it can be used as a pre-compiled header file.
        If an error occurs while saving, a TranslationUnitSaveError is raised.
        If the error was TranslationUnitSaveError.ERROR_INVALID_TU, this means
        the constructed TranslationUnit was not valid at time of save. In this
        case, the reason(s) why should be available via
        TranslationUnit.diagnostics().
        filename -- The path to save the translation unit to (str or PathLike).
        options = conf.lib.Devil_defaultSaveOptions(self)
        result = int(
            conf.lib.Devil_saveTranslationUnit(self, fspath(filename), options)
        )
        if result != 0:
            raise TranslationUnitSaveError(result, "Error saving TranslationUnit.")
    def codeComplete(
        self,
        path,
        line,
        column,
        unsaved_files=None,
        include_macros=False,
        include_code_patterns=False,
        include_brief_comments=False,
    ):
        Code complete in this translation unit.
        In-memory contents for files can be provided by passing a list of pairs
        as unsaved_files, the first items should be the filenames to be mapped
        and the second should be the contents to be substituted for the
        file. The contents may be passed as strings or file objects.
        options = 0
        if include_macros:
            options += 1
        if include_code_patterns:
            options += 2
        if include_brief_comments:
            options += 4
        if unsaved_files is None:
            unsaved_files = []
        unsaved_files_array = 0
        if len(unsaved_files):
            unsaved_files_array = (_CXUnsavedFile * len(unsaved_files))()
            for i, (name, contents) in enumerate(unsaved_files):
                if hasattr(contents, "read"):
                    contents = contents.read()
                contents = b(contents)
                unsaved_files_array[i].name = b(fspath(name))
                unsaved_files_array[i].contents = contents
                unsaved_files_array[i].length = len(contents)
        ptr = conf.lib.Devil_codeCompleteAt(
            self,
            fspath(path),
            line,
            column,
            unsaved_files_array,
            len(unsaved_files),
            options,
        )
        if ptr:
            return CodeCompletionResults(ptr)
        return None
    def get_tokens(self, locations=None, extent=None):
        This is a generator for Token instances. The caller specifies a range
        of source code to obtain tokens for. The range can be specified as a
        2-tuple of SourceLocation or as a SourceRange. If both are defined,
        behavior is undefined.
        if locations is not None:
            extent = SourceRange(start=locations[0], end=locations[1])
        return TokenGroup.get_tokens(self, extent)
class File(DevilObject):
    The File class represents a particular source file that is part of a
    translation unit.
    @staticmethod
    def from_name(translation_unit, file_name):
        return File(conf.lib.Devil_getFile(translation_unit, fspath(file_name)))
    @property
    def name(self):
        return conf.lib.Devil_getFileName(self)
    @property
    def time(self):
        return conf.lib.Devil_getFileTime(self)
    def __str__(self):
        return self.name
    def __repr__(self):
        return "<File: %s>" % (self.name)
    @staticmethod
    def from_result(res, fn, args):
        assert isinstance(res, c_object_p)
        res = File(res)
        res._tu = args[0]._tu
        return res
class FileInclusion(object):
    The FileInclusion class represents the inclusion of one source file by
    another via a '#include' directive or as the input file for the translation
    unit. This class provides information about the included file, the including
    file, the location of the '#include' directive and the depth of the included
    file in the stack. Note that the input file has depth 0.
    def __init__(self, src, tgt, loc, depth):
        self.source = src
        self.include = tgt
        self.location = loc
        self.depth = depth
    @property
    def is_input_file(self):
        return self.depth == 0
class CompilationDatabaseError(Exception):
    Each error is associated to an enumerated value, accessible under
    e.cdb_error. Consumers can compare the value with one of the ERROR_
    constants in this class.
    ERROR_UNKNOWN = 0
    ERROR_CANNOTLOADDATABASE = 1
    def __init__(self, enumeration, message):
        assert isinstance(enumeration, int)
        if enumeration > 1:
            raise Exception(
                "Encountered undefined CompilationDatabase error "
                "constant: %d. Please file a bug to have this "
                "value supported." % enumeration
            )
        self.cdb_error = enumeration
        Exception.__init__(self, "Error %d: %s" % (enumeration, message))
class CompileCommand(object):
    def __init__(self, cmd, ccmds):
        self.cmd = cmd
        self.ccmds = ccmds
    @property
    def directory(self):
        return conf.lib.Devil_CompileCommand_getDirectory(self.cmd)
    @property
    def filename(self):
        return conf.lib.Devil_CompileCommand_getFilename(self.cmd)
    @property
    def arguments(self):
        Get an iterable object providing each argument in the
        command line for the compiler invocation as a _CXString.
        Invariant : the first argument is the compiler executable
        length = conf.lib.Devil_CompileCommand_getNumArgs(self.cmd)
        for i in range(length):
            yield conf.lib.Devil_CompileCommand_getArg(self.cmd, i)
class CompileCommands(object):
    CompileCommands is an iterable object containing all CompileCommand
    that can be used for building a specific file.
    def __init__(self, ccmds):
        self.ccmds = ccmds
    def __del__(self):
        conf.lib.Devil_CompileCommands_dispose(self.ccmds)
    def __len__(self):
        return int(conf.lib.Devil_CompileCommands_getSize(self.ccmds))
    def __getitem__(self, i):
        cc = conf.lib.Devil_CompileCommands_getCommand(self.ccmds, i)
        if not cc:
            raise IndexError
        return CompileCommand(cc, self)
    @staticmethod
    def from_result(res, fn, args):
        if not res:
            return None
        return CompileCommands(res)
class CompilationDatabase(DevilObject):
    The CompilationDatabase is a wrapper class around
    Devil::tooling::CompilationDatabase
    It enables querying how a specific source file can be built.
    def __del__(self):
        conf.lib.Devil_CompilationDatabase_dispose(self)
    @staticmethod
    def from_result(res, fn, args):
        if not res:
            raise CompilationDatabaseError(0, "CompilationDatabase loading failed")
        return CompilationDatabase(res)
    @staticmethod
    def fromDirectory(buildDir):
        errorCode = c_uint()
        try:
            cdb = conf.lib.Devil_CompilationDatabase_fromDirectory(
                fspath(buildDir), byref(errorCode)
            )
        except CompilationDatabaseError as e:
            raise CompilationDatabaseError(
                int(errorCode.value), "CompilationDatabase loading failed"
            )
        return cdb
    def getCompileCommands(self, filename):
        Get an iterable object providing all the CompileCommands available to
        build filename. Returns None if filename is not found in the database.
        return conf.lib.Devil_CompilationDatabase_getCompileCommands(
            self, fspath(filename)
        )
    def getAllCompileCommands(self):
        Get an iterable object providing all the CompileCommands available from
        the database.
        return conf.lib.Devil_CompilationDatabase_getAllCompileCommands(self)
class Token(Structure):
    Tokens are effectively segments of source code. Source code is first parsed
    into tokens before being converted into the AST and Cursors.
    Tokens are obtained from parsed TranslationUnit instances. You currently
    can't create tokens manually.
    _fields_ = [("int_data", c_uint * 4), ("ptr_data", c_void_p)]
    @property
    def spelling(self):
        This is the textual representation of the token in source.
        return conf.lib.Devil_getTokenSpelling(self._tu, self)
    @property
    def kind(self):
        return TokenKind.from_value(conf.lib.Devil_getTokenKind(self))
    @property
    def location(self):
        return conf.lib.Devil_getTokenLocation(self._tu, self)
    @property
    def extent(self):
        return conf.lib.Devil_getTokenExtent(self._tu, self)
    @property
    def cursor(self):
        cursor = Cursor()
        cursor._tu = self._tu
        conf.lib.Devil_annotateTokens(self._tu, byref(self), 1, byref(cursor))
        return cursor
callbacks["translation_unit_includes"] = CFUNCTYPE(
    None, c_object_p, POINTER(SourceLocation), c_uint, py_object
)
callbacks["cursor_visit"] = CFUNCTYPE(c_int, Cursor, Cursor, py_object)
callbacks["fields_visit"] = CFUNCTYPE(c_int, Cursor, py_object)
functionList = [
    (
        "Devil_annotateTokens",
        [TranslationUnit, POINTER(Token), c_uint, POINTER(Cursor)],
    ),
    ("Devil_CompilationDatabase_dispose", [c_object_p]),
    (
        "Devil_CompilationDatabase_fromDirectory",
        [c_interop_string, POINTER(c_uint)],
        c_object_p,
        CompilationDatabase.from_result,
    ),
    (
        "Devil_CompilationDatabase_getAllCompileCommands",
        [c_object_p],
        c_object_p,
        CompileCommands.from_result,
    ),
    (
        "Devil_CompilationDatabase_getCompileCommands",
        [c_object_p, c_interop_string],
        c_object_p,
        CompileCommands.from_result,
    ),
    ("Devil_CompileCommands_dispose", [c_object_p]),
    ("Devil_CompileCommands_getCommand", [c_object_p, c_uint], c_object_p),
    ("Devil_CompileCommands_getSize", [c_object_p], c_uint),
    (
        "Devil_CompileCommand_getArg",
        [c_object_p, c_uint],
        _CXString,
        _CXString.from_result,
    ),
    (
        "Devil_CompileCommand_getDirectory",
        [c_object_p],
        _CXString,
        _CXString.from_result,
    ),
    (
        "Devil_CompileCommand_getFilename",
        [c_object_p],
        _CXString,
        _CXString.from_result,
    ),
    ("Devil_CompileCommand_getNumArgs", [c_object_p], c_uint),
    (
        "Devil_codeCompleteAt",
        [TranslationUnit, c_interop_string, c_int, c_int, c_void_p, c_int, c_int],
        POINTER(CCRStructure),
    ),
    ("Devil_codeCompleteGetDiagnostic", [CodeCompletionResults, c_int], Diagnostic),
    ("Devil_codeCompleteGetNumDiagnostics", [CodeCompletionResults], c_int),
    ("Devil_createIndex", [c_int, c_int], c_object_p),
    ("Devil_createTranslationUnit", [Index, c_interop_string], c_object_p),
    ("Devil_CXXConstructor_isConvertingConstructor", [Cursor], bool),
    ("Devil_CXXConstructor_isCopyConstructor", [Cursor], bool),
    ("Devil_CXXConstructor_isDefaultConstructor", [Cursor], bool),
    ("Devil_CXXConstructor_isMoveConstructor", [Cursor], bool),
    ("Devil_CXXField_isMutable", [Cursor], bool),
    ("Devil_CXXMethod_isConst", [Cursor], bool),
    ("Devil_CXXMethod_isDefaulted", [Cursor], bool),
    ("Devil_CXXMethod_isDeleted", [Cursor], bool),
    ("Devil_CXXMethod_isCopyAssignmentOperator", [Cursor], bool),
    ("Devil_CXXMethod_isMoveAssignmentOperator", [Cursor], bool),
    ("Devil_CXXMethod_isExplicit", [Cursor], bool),
    ("Devil_CXXMethod_isPureVirtual", [Cursor], bool),
    ("Devil_CXXMethod_isStatic", [Cursor], bool),
    ("Devil_CXXMethod_isVirtual", [Cursor], bool),
    ("Devil_CXXRecord_isAbstract", [Cursor], bool),
    ("Devil_EnumDecl_isScoped", [Cursor], bool),
    ("Devil_defaultDiagnosticDisplayOptions", [], c_uint),
    ("Devil_defaultSaveOptions", [TranslationUnit], c_uint),
    ("Devil_disposeCodeCompleteResults", [CodeCompletionResults]),
    ("Devil_disposeDiagnostic", [Diagnostic]),
    ("Devil_disposeIndex", [Index]),
    ("Devil_disposeString", [_CXString]),
    ("Devil_disposeTokens", [TranslationUnit, POINTER(Token), c_uint]),
    ("Devil_disposeTranslationUnit", [TranslationUnit]),
    ("Devil_equalCursors", [Cursor, Cursor], bool),
    ("Devil_equalLocations", [SourceLocation, SourceLocation], bool),
    ("Devil_equalRanges", [SourceRange, SourceRange], bool),
    ("Devil_equalTypes", [Type, Type], bool),
    ("Devil_formatDiagnostic", [Diagnostic, c_uint], _CXString, _CXString.from_result),
    ("Devil_getArgType", [Type, c_uint], Type, Type.from_result),
    ("Devil_getArrayElementType", [Type], Type, Type.from_result),
    ("Devil_getArraySize", [Type], c_longlong),
    ("Devil_getFieldDeclBitWidth", [Cursor], c_int),
    ("Devil_getCanonicalCursor", [Cursor], Cursor, Cursor.from_cursor_result),
    ("Devil_getCanonicalType", [Type], Type, Type.from_result),
    ("Devil_getChildDiagnostics", [Diagnostic], c_object_p),
    ("Devil_getCompletionAvailability", [c_void_p], c_int),
    ("Devil_getCompletionBriefComment", [c_void_p], _CXString, _CXString.from_result),
    ("Devil_getCompletionChunkCompletionString", [c_void_p, c_int], c_object_p),
    ("Devil_getCompletionChunkKind", [c_void_p, c_int], c_int),
    (
        "Devil_getCompletionChunkText",
        [c_void_p, c_int],
        _CXString,
        _CXString.from_result,
    ),
    ("Devil_getCompletionPriority", [c_void_p], c_int),
    (
        "Devil_getCString",
        [_CXString],
        c_interop_string,
        c_interop_string.to_python_string,
    ),
    ("Devil_getCursor", [TranslationUnit, SourceLocation], Cursor),
    ("Devil_getCursorAvailability", [Cursor], c_int),
    ("Devil_getCursorDefinition", [Cursor], Cursor, Cursor.from_result),
    ("Devil_getCursorDisplayName", [Cursor], _CXString, _CXString.from_result),
    ("Devil_getCursorExtent", [Cursor], SourceRange),
    ("Devil_getCursorLexicalParent", [Cursor], Cursor, Cursor.from_cursor_result),
    ("Devil_getCursorLocation", [Cursor], SourceLocation),
    ("Devil_getCursorReferenced", [Cursor], Cursor, Cursor.from_result),
    ("Devil_getCursorReferenceNameRange", [Cursor, c_uint, c_uint], SourceRange),
    ("Devil_getCursorResultType", [Cursor], Type, Type.from_result),
    ("Devil_getCursorSemanticParent", [Cursor], Cursor, Cursor.from_cursor_result),
    ("Devil_getCursorSpelling", [Cursor], _CXString, _CXString.from_result),
    ("Devil_getCursorType", [Cursor], Type, Type.from_result),
    ("Devil_getCursorUSR", [Cursor], _CXString, _CXString.from_result),
    ("Devil_Cursor_getMangling", [Cursor], _CXString, _CXString.from_result),
    ("Devil_getCXXAccessSpecifier", [Cursor], c_uint),
    ("Devil_getDeclObjCTypeEncoding", [Cursor], _CXString, _CXString.from_result),
    ("Devil_getDiagnostic", [c_object_p, c_uint], c_object_p),
    ("Devil_getDiagnosticCategory", [Diagnostic], c_uint),
    ("Devil_getDiagnosticCategoryText", [Diagnostic], _CXString, _CXString.from_result),
    (
        "Devil_getDiagnosticFixIt",
        [Diagnostic, c_uint, POINTER(SourceRange)],
        _CXString,
        _CXString.from_result,
    ),
    ("Devil_getDiagnosticInSet", [c_object_p, c_uint], c_object_p),
    ("Devil_getDiagnosticLocation", [Diagnostic], SourceLocation),
    ("Devil_getDiagnosticNumFixIts", [Diagnostic], c_uint),
    ("Devil_getDiagnosticNumRanges", [Diagnostic], c_uint),
    (
        "Devil_getDiagnosticOption",
        [Diagnostic, POINTER(_CXString)],
        _CXString,
        _CXString.from_result,
    ),
    ("Devil_getDiagnosticRange", [Diagnostic, c_uint], SourceRange),
    ("Devil_getDiagnosticSeverity", [Diagnostic], c_int),
    ("Devil_getDiagnosticSpelling", [Diagnostic], _CXString, _CXString.from_result),
    ("Devil_getElementType", [Type], Type, Type.from_result),
    ("Devil_getEnumConstantDeclUnsignedValue", [Cursor], c_ulonglong),
    ("Devil_getEnumConstantDeclValue", [Cursor], c_longlong),
    ("Devil_getEnumDeclIntegerType", [Cursor], Type, Type.from_result),
    ("Devil_getFile", [TranslationUnit, c_interop_string], c_object_p),
    ("Devil_getFileName", [File], _CXString, _CXString.from_result),
    ("Devil_getFileTime", [File], c_uint),
    ("Devil_getIBOutletCollectionType", [Cursor], Type, Type.from_result),
    ("Devil_getIncludedFile", [Cursor], c_object_p, File.from_result),
    (
        "Devil_getInclusions",
        [TranslationUnit, callbacks["translation_unit_includes"], py_object],
    ),
    (
        "Devil_getInstantiationLocation",
        [
            SourceLocation,
            POINTER(c_object_p),
            POINTER(c_uint),
            POINTER(c_uint),
            POINTER(c_uint),
        ],
    ),
    ("Devil_getLocation", [TranslationUnit, File, c_uint, c_uint], SourceLocation),
    ("Devil_getLocationForOffset", [TranslationUnit, File, c_uint], SourceLocation),
    ("Devil_getNullCursor", None, Cursor),
    ("Devil_getNumArgTypes", [Type], c_uint),
    ("Devil_getNumCompletionChunks", [c_void_p], c_int),
    ("Devil_getNumDiagnostics", [c_object_p], c_uint),
    ("Devil_getNumDiagnosticsInSet", [c_object_p], c_uint),
    ("Devil_getNumElements", [Type], c_longlong),
    ("Devil_getNumOverloadedDecls", [Cursor], c_uint),
    ("Devil_getOverloadedDecl", [Cursor, c_uint], Cursor, Cursor.from_cursor_result),
    ("Devil_getPointeeType", [Type], Type, Type.from_result),
    ("Devil_getRange", [SourceLocation, SourceLocation], SourceRange),
    ("Devil_getRangeEnd", [SourceRange], SourceLocation),
    ("Devil_getRangeStart", [SourceRange], SourceLocation),
    ("Devil_getResultType", [Type], Type, Type.from_result),
    ("Devil_getSpecializedCursorTemplate", [Cursor], Cursor, Cursor.from_cursor_result),
    ("Devil_getTemplateCursorKind", [Cursor], c_uint),
    ("Devil_getTokenExtent", [TranslationUnit, Token], SourceRange),
    ("Devil_getTokenKind", [Token], c_uint),
    ("Devil_getTokenLocation", [TranslationUnit, Token], SourceLocation),
    (
        "Devil_getTokenSpelling",
        [TranslationUnit, Token],
        _CXString,
        _CXString.from_result,
    ),
    ("Devil_getTranslationUnitCursor", [TranslationUnit], Cursor, Cursor.from_result),
    (
        "Devil_getTranslationUnitSpelling",
        [TranslationUnit],
        _CXString,
        _CXString.from_result,
    ),
    (
        "Devil_getTUResourceUsageName",
        [c_uint],
        c_interop_string,
        c_interop_string.to_python_string,
    ),
    ("Devil_getTypeDeclaration", [Type], Cursor, Cursor.from_result),
    ("Devil_getTypedefDeclUnderlyingType", [Cursor], Type, Type.from_result),
    ("Devil_getTypedefName", [Type], _CXString, _CXString.from_result),
    ("Devil_getTypeKindSpelling", [c_uint], _CXString, _CXString.from_result),
    ("Devil_getTypeSpelling", [Type], _CXString, _CXString.from_result),
    ("Devil_hashCursor", [Cursor], c_uint),
    ("Devil_isAttribute", [CursorKind], bool),
    ("Devil_isConstQualifiedType", [Type], bool),
    ("Devil_isCursorDefinition", [Cursor], bool),
    ("Devil_isDeclaration", [CursorKind], bool),
    ("Devil_isExpression", [CursorKind], bool),
    ("Devil_isFileMultipleIncludeGuarded", [TranslationUnit, File], bool),
    ("Devil_isFunctionTypeVariadic", [Type], bool),
    ("Devil_isInvalid", [CursorKind], bool),
    ("Devil_isPODType", [Type], bool),
    ("Devil_isPreprocessing", [CursorKind], bool),
    ("Devil_isReference", [CursorKind], bool),
    ("Devil_isRestrictQualifiedType", [Type], bool),
    ("Devil_isStatement", [CursorKind], bool),
    ("Devil_isTranslationUnit", [CursorKind], bool),
    ("Devil_isUnexposed", [CursorKind], bool),
    ("Devil_isVirtualBase", [Cursor], bool),
    ("Devil_isVolatileQualifiedType", [Type], bool),
    (
        "Devil_parseTranslationUnit",
        [Index, c_interop_string, c_void_p, c_int, c_void_p, c_int, c_int],
        c_object_p,
    ),
    ("Devil_reparseTranslationUnit", [TranslationUnit, c_int, c_void_p, c_int], c_int),
    ("Devil_saveTranslationUnit", [TranslationUnit, c_interop_string, c_uint], c_int),
    (
        "Devil_tokenize",
        [TranslationUnit, SourceRange, POINTER(POINTER(Token)), POINTER(c_uint)],
    ),
    ("Devil_visitChildren", [Cursor, callbacks["cursor_visit"], py_object], c_uint),
    ("Devil_Cursor_getNumArguments", [Cursor], c_int),
    ("Devil_Cursor_getArgument", [Cursor, c_uint], Cursor, Cursor.from_result),
    ("Devil_Cursor_getNumTemplateArguments", [Cursor], c_int),
    (
        "Devil_Cursor_getTemplateArgumentKind",
        [Cursor, c_uint],
        TemplateArgumentKind.from_id,
    ),
    ("Devil_Cursor_getTemplateArgumentType", [Cursor, c_uint], Type, Type.from_result),
    ("Devil_Cursor_getTemplateArgumentValue", [Cursor, c_uint], c_longlong),
    ("Devil_Cursor_getTemplateArgumentUnsignedValue", [Cursor, c_uint], c_ulonglong),
    ("Devil_Cursor_isAnonymous", [Cursor], bool),
    ("Devil_Cursor_isBitField", [Cursor], bool),
    ("Devil_Cursor_getBriefCommentText", [Cursor], _CXString, _CXString.from_result),
    ("Devil_Cursor_getRawCommentText", [Cursor], _CXString, _CXString.from_result),
    ("Devil_Cursor_getOffsetOfField", [Cursor], c_longlong),
    ("Devil_Location_isInSystemHeader", [SourceLocation], bool),
    ("Devil_Type_getAlignOf", [Type], c_longlong),
    ("Devil_Type_getClassType", [Type], Type, Type.from_result),
    ("Devil_Type_getNumTemplateArguments", [Type], c_int),
    ("Devil_Type_getTemplateArgumentAsType", [Type, c_uint], Type, Type.from_result),
    ("Devil_Type_getOffsetOf", [Type, c_interop_string], c_longlong),
    ("Devil_Type_getSizeOf", [Type], c_longlong),
    ("Devil_Type_getCXXRefQualifier", [Type], c_uint),
    ("Devil_Type_getNamedType", [Type], Type, Type.from_result),
    ("Devil_Type_visitFields", [Type, callbacks["fields_visit"], py_object], c_uint),
]
class LibDevilError(Exception):
    def __init__(self, message):
        self.m = message
    def __str__(self):
        return self.m
def register_function(lib, item, ignore_errors):
    try:
        func = getattr(lib, item[0])
    except AttributeError as e:
        msg = (
            str(e) + ". Please ensure that your python bindings are "
            "compatible with your libDevil.so version."
        )
        if ignore_errors:
            return
        raise LibDevilError(msg)
    if len(item) >= 2:
        func.argtypes = item[1]
    if len(item) >= 3:
        func.restype = item[2]
    if len(item) == 4:
        func.errcheck = item[3]
def register_functions(lib, ignore_errors):
    This must be called as part of library instantiation so Python knows how
    to call out to the shared library.
    def register(item):
        return register_function(lib, item, ignore_errors)
    for f in functionList:
        register(f)
class Config(object):
    library_path = None
    library_file = None
    compatibility_check = True
    loaded = False
    @staticmethod
    def set_library_path(path):
        if Config.loaded:
            raise Exception(
                "library path must be set before before using "
                "any other functionalities in libDevil."
            )
        Config.library_path = fspath(path)
    @staticmethod
    def set_library_file(filename):
        if Config.loaded:
            raise Exception(
                "library file must be set before before using "
                "any other functionalities in libDevil."
            )
        Config.library_file = fspath(filename)
    @staticmethod
    def set_compatibility_check(check_status):
        The python bindings are only tested and evaluated with the version of
        libDevil they are provided with. To ensure correct behavior a (limited)
        compatibility check is performed when loading the bindings. This check
        will throw an exception, as soon as it fails.
        In case these bindings are used with an older version of libDevil, parts
        that have been stable between releases may still work. Users of the
        python bindings can disable the compatibility check. This will cause
        the python bindings to load, even though they are written for a newer
        version of libDevil. Failures now arise if unsupported or incompatible
        features are accessed. The user is required to test themselves if the
        features they are using are available and compatible between different
        libDevil versions.
        if Config.loaded:
            raise Exception(
                "compatibility_check must be set before before "
                "using any other functionalities in libDevil."
            )
        Config.compatibility_check = check_status
    @CachedProperty
    def lib(self):
        lib = self.get_DevilTop_library()
        register_functions(lib, not Config.compatibility_check)
        Config.loaded = True
        return lib
    def get_filename(self):
        if Config.library_file:
            return Config.library_file
        import platform
        name = platform.system()
        if name == "Darwin":
            file = "libDevil.dylib"
        elif name == "Windows":
            file = "libDevil.dll"
        else:
            file = "libDevil-17.so"
        if Config.library_path:
            file = Config.library_path + "/" + file
        return file
    def get_DevilTop_library(self):
        try:
            library = cdll.LoadLibrary(self.get_filename())
        except OSError as e:
            msg = (
                str(e) + ". To provide a path to libDevil use "
                "Config.set_library_path() or "
                "Config.set_library_file()."
            )
            raise LibDevilError(msg)
        return library
    def function_exists(self, name):
        try:
            getattr(self.lib, name)
        except AttributeError:
            return False
        return True
def register_arDev():
    for name, value in Devil.arDev.TokenKinds:
        TokenKind.register(value, name)
conf = Config()
register_arDev()
__all__ = [
    "AvailabilityKind",
    "Config",
    "CodeCompletionResults",
    "CompilationDatabase",
    "CompileCommands",
    "CompileCommand",
    "CursorKind",
    "Cursor",
    "Diagnostic",
    "File",
    "FixIt",
    "Index",
    "LinkageKind",
    "SourceLocation",
    "SourceRange",
    "TLSKind",
    "TokenKind",
    "Token",
    "TranslationUnitLoadError",
    "TranslationUnit",
    "TypeKind",
    "Type",
]
