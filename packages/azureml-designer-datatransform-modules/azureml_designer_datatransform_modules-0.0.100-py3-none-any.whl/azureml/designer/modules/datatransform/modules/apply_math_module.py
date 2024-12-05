from enum import Enum
import math
import mpmath
import cmath
from decimal import Decimal
from typing import List
import numpy as np
from azureml.studio.core.error import UserError
from azureml.studio.core.utils.column_selection import ColumnSelectionBuilder, ColumnType
from scipy import special, integrate
import pandas as pd
from azureml.designer.modules.datatransform.common.module_base import ModuleBase, ModuleMetaData
from azureml.designer.modules.datatransform.common.module_parameter import InputPortModuleParameter, \
    OutputPortModuleParameter, \
    ValueModuleParameter, ColumnSelectorModuleParameter, ModuleParameters
from azureml.designer.modules.datatransform.common.logger import custom_module_logger as logger
# from azureml.designer.modules.datatransform.common.logger import format_obj
from azureml.designer.modules.datatransform.common.module_spec_node import ModuleSpecNode
from azureml.studio.internal.error import ErrorMapping, BadNumberOfSelectedColumnsError, ParameterParsingError, \
     CouldNotConvertColumnError
from azureml.designer.modules.datatransform.tools.column_selection_utils import convert_column_selection_to_json
from azureml.designer.modules.datatransform.tools.dataframe_utils import is_type
from azureml.studio.core.logger import TimeProfile


class MathCategory(Enum):
    Basic = "Basic"
    Compare = "Compare"
    Operations = "Operations"
    Rounding = "Rounding"
    Special = "Special"
    Trigonometric = "Trigonometric"


class BasicFunc(Enum):
    Abs = "Abs"
    Atan2 = "Atan2"
    Conj = "Conj"
    Cuberoot = "Cuberoot"
    DoubleFactorial = "DoubleFactorial"
    Eps = "Eps"
    Exp = "Exp"
    Exp2 = "Exp2"
    ExpMinus1 = "ExpMinus1"
    Factorial = "Factorial"
    Hypotenuse = "Hypotenuse"
    ImaginaryPart = "ImaginaryPart"
    Ln = "Ln"
    LnPlus1 = "LnPlus1"
    Log = "Log"
    Log10 = "Log10"
    Log2 = "Log2"
    NthRoot = "NthRoot"
    Pow = "Pow"
    RealPart = "RealPart"
    Sqrt = "Sqrt"
    SqrtPi = "SqrtPi"
    Square = "Square"


class CompareFunc(Enum):
    EqualTo = "EqualTo"
    GreaterThan = "GreaterThan"
    GreaterThanOrEqualTo = "GreaterThanOrEqualTo"
    LessThan = "LessThan"
    LessThanOrEqualTo = "LessThanOrEqualTo"
    NotEqualTo = "NotEqualTo"
    PairMax = "PairMax"
    PairMin = "PairMin"


class OperationsFunc(Enum):
    Add = "Add"
    Divide = "Divide"
    Multiply = "Multiply"
    Subtract = "Subtract"


class RoundingFunc(Enum):
    Ceiling = "Ceiling"
    CeilingPower2 = "CeilingPower2"
    Floor = "Floor"
    Mod = "Mod"
    Quotient = "Quotient"
    Remainder = "Remainder"
    RoundDigits = "RoundDigits"
    RoundDown = "RoundDown"
    RoundUp = "RoundUp"
    ToEven = "ToEven"
    ToMultiple = "ToMultiple"
    ToOdd = "ToOdd"
    Truncate = "Truncate"


class SpecialFunc(Enum):
    Beta = "Beta"
    BetaLn = "BetaLn"
    EllipticIntegralE = "EllipticIntegralE"
    EllipticIntegralK = "EllipticIntegralK"
    Erf = "Erf"
    Erfc = "Erfc"
    ErfcScaled = "ErfcScaled"
    ErfInverse = "ErfInverse"
    ExponentialIntegralEin = "ExponentialIntegralEin"
    Gamma = "Gamma"
    GammaLn = "GammaLn"
    GammaRegularizedP = "GammaRegularizedP"
    GammaRegularizedPInverse = "GammaRegularizedPInverse"
    GammaRegularizedQ = "GammaRegularizedQ"
    GammaRegularizedQInverse = "GammaRegularizedQInverse"
    Polygamma = "Polygamma"


class TrigonometricFunc(Enum):
    Acos = "Acos"
    AcosDegrees = "AcosDegrees"
    Acosh = "Acosh"
    Acot = "Acot"
    AcotDegrees = "AcotDegrees"
    Acoth = "Acoth"
    Acsc = "Acsc"
    AcscDegrees = "AcscDegrees"
    Acsch = "Acsch"
    Arg = "Arg"
    Asec = "Asec"
    AsecDegrees = "AsecDegrees"
    Asech = "Asech"
    Asin = "Asin"
    AsinDegrees = "AsinDegrees"
    Asinh = "Asinh"
    Atan = "Atan"
    AtanDegrees = "AtanDegrees"
    Atanh = "Atanh"
    Cis = "Cis"
    Cos = "Cos"
    CosDegrees = "CosDegrees"
    Cosh = "Cosh"
    Cot = "Cot"
    CotDegrees = "CotDegrees"
    Coth = "Coth"
    Csc = "Csc"
    CscDegrees = "CscDegrees"
    Csch = "Csch"
    DegreesToRadians = "DegreesToRadians"
    RadiansToDegrees = "RadiansToDegrees"
    Sec = "Sec"
    SecDegrees = "SecDegrees"
    Sech = "Sech"
    Sign = "Sign"
    Sin = "Sin"
    Sinc = "Sinc"
    SinDegrees = "SinDegrees"
    Sinh = "Sinh"
    Tan = "Tan"
    TanDegrees = "TanDegrees"
    Tanh = "Tanh"


class OutputMode(Enum):
    Append = "Append"
    Inplace = "Inplace"
    ResultOnly = "ResultOnly"
    Inpalce = "Inplace"


class OperationArgumentType(Enum):
    Constant = "Constant"
    ColumnSet = "ColumnSet"


def raise_exception(ex):
    raise ex


def try_math_exp(value):
    try:
        return math.exp(value)
    except OverflowError:
        return np.inf


def try_math_exp2(value1, value2):
    try:
        return np.exp2(value1) * value2
    except OverflowError:
        return np.inf


def try_math_expminus1(value):
    try:
        return math.expm1(value)
    except OverflowError:
        return np.inf


def try_math_factorial(x):
    """
    Ref: https://github.com/mathnet/mathnet-numerics/blob/7e450663689d8555de50caf5d39ec744ccf1c733/src/Numerics
    /SpecialFunctions/Factorial.cs
    for future readers
    """
    if math.isnan(x):
        return np.NaN
    if x < 0:
        return np.NaN
    if not isinstance(x, int):
        x = int(x)
    return math.factorial(x) if x <= 170 else np.inf


def double_factorial(x):
    """
    Ref: https://stackoverflow.com/questions/4740172/how-do-you-a-double-factorial-in-python
    for future readers
    """
    if math.isnan(x):
        return np.NaN
    if x < 0:
        return np.NaN
    if x == 0 or x == 1:
        return 1
    if not isinstance(x, int):
        x = int(x)
    if x > 300:
        return np.inf
    fact = math.factorial
    if x % 2 == 1:
        k = (x + 1) / 2
        return fact(2 * k) / (2 ** k * fact(k))
    else:
        k = x / 2
        return 2 ** k * fact(k)


def try_pow(x, y):
    try:
        if x < 0:
            return np.NaN
        return pow(x, y)
    except OverflowError:
        return np.inf


def try_nthRoot(x, y):
    try:
        if x < 0:
            return np.NaN
        return x ** (1 / float(y))
    except OverflowError:
        return np.inf


def round_digits(x, y):
    if math.isnan(x):
        return np.NaN
    if not isinstance(y, int):
        y = int(y)
    if not (math.isnan(x) or math.isnan(y)):
        return int(x * (10 ** y) + math.copysign(0.5, x)) / (10.0 ** y)
    else:
        raise_exception(CouldNotConvertColumnError(type1=np.NaN, type2=int))


def round_up(x, y=0):
    if math.isnan(x):
        return np.NaN
    if not isinstance(y, int):
        y = int(y)
    if x < 0:
        return -round_up(-x, y)
    return math.ceil(x * (10 ** y)) / (10 ** y)


def round_down(x, y=0):
    if math.isnan(x):
        return np.NaN
    if not isinstance(y, int):
        y = int(y)
    if x < 0:
        return -round_down(-x, y)
    return math.floor(x * (10 ** y)) / (10 ** y)


def truncate(x, y):
    if math.isnan(x):
        return np.NaN
    if not isinstance(y, int):
        y = int(y)
    return int(x * 10 ** y) / 10 ** y


def quotient(x, y):
    if math.isnan(x):
        return np.NaN
    if y == 0:
        if x == 0:
            return np.NaN
        return np.inf
    if isinstance(x, float) or isinstance(y, float):
        return int(x / y)
    else:
        return x // y


def ceiling(x, y):
    if math.isnan(x):
        return np.NaN
    if (x > 0) and (y < 0):
        return np.NaN

    if math.isinf(x):
        return np.inf

    return math.ceil(x / y) * y if y != 0 else 0


def floor(x, y):
    if math.isnan(x):
        return np.NaN
    if (x > 0) and (y < 0):
        return np.NaN
    return math.floor(x / y) * y if y != 0 else np.NaN


def round_to_multiple(x, y):
    if y < 0:
        return np.NaN
    if y == 0:
        return 0
    r = x % y
    return x + y - r if r + r >= y else x - r


def log(x, y):
    if x < 0 or y <= 0 or y == 1:
        return np.NaN
    if x == 0:
        return np.inf
    return math.log(x, y)


def beta(x, y):
    if x < 0.0 or y < 0.0:
        return np.NaN
    if x == 0 or y == 0:
        return np.inf
    return special.beta(x, y)


def betaLn(x, y):
    if x < 0.0 or y < 0.0:
        return np.NaN
    if x == 0 or y == 0:
        return np.inf
    return special.betaln(x, y)


def ellipticIntegralE(x):
    if x < 0:
        return np.NaN
    return special.ellipe(x)


def ellipticIntegralK(x):
    if x < 0:
        return np.NaN
    return special.ellipk(x)


def exponentialIntegralEin(x):
    """
    Modified exponential integral Ein(z). For real x, the modified exponential integral is defined as
       Ein(x) = \\int_{0}^{x}\\frac{1-exp(-t)}{t}{\\mathrm{d} t}
    """
    if x == 0:
        return 0
    if np.isinf(x):
        return np.inf
    olderr = np.seterr(over='ignore')
    y = integrate.quad(lambda t: (1 - np.exp(-t)) / t, 0, x, maxp1=100, limit=100)[0]
    np.seterr(**olderr)

    if np.isinf(y):
        return np.NaN
    else:
        return y


def digamma(x):
    if x < 0:
        return np.NaN
    if x == 0:
        return np.inf
    return special.digamma(x)


def atanh(x):
    if x == 1 or x == -1:
        return np.inf
    try:
        # atanh domain: -1 < x < 1:
        return math.atanh(x)
    except ValueError:
        return np.NaN


def mpf2float(x):
    """
    Convert an mpf to the nearest floating point number. Just using
    float directly doesn't work because of results like this:
    with mp.workdps(50):
        float(mpf("0.99999999999999999")) = 0.9999999999999999
    """
    try:
        res = float(mpmath.nstr(x, 17, min_fixed=0, max_fixed=0))
        return res
    except ValueError:
        # do not support complex data type
        return np.NaN


def sign(x):
    if math.isnan(x):
        return np.NaN
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def sinc(x):
    """
    The sinc function is defined as:
    \\sin(\\pi x)/(\\pi x)
    """
    if np.isinf(x):
        return 1/x
    if not x:
        return x+1
    return math.sin(math.pi * x)/(math.pi * x)


class ApplyMathModule(ModuleBase):
    # Customize functions plus special handling for edge cases
    _OPS_FUNC_MAPPING = {
        BasicFunc.Abs: abs,
        BasicFunc.Atan2: lambda x, y: math.atan2(y, x),
        BasicFunc.Conj: lambda x: np.conj(x),  # meaningless for real number
        BasicFunc.Cuberoot: lambda x: np.cbrt(x),
        BasicFunc.DoubleFactorial: lambda x: double_factorial(x),
        BasicFunc.Eps: lambda x: np.spacing(x),
        BasicFunc.Exp: lambda x: try_math_exp(x),
        BasicFunc.Exp2: lambda x, y: try_math_exp2(x, y),
        BasicFunc.ExpMinus1: lambda x: try_math_expminus1(x),
        BasicFunc.Factorial: lambda x: try_math_factorial(x),
        BasicFunc.Hypotenuse: lambda x, y: math.hypot(x, y),
        BasicFunc.ImaginaryPart: np.imag,  # meaningless for real number
        BasicFunc.Ln: lambda x: math.log(x) if x > 0 else np.NaN,
        BasicFunc.LnPlus1: lambda x: math.log(x + 1) if x + 1 > 0 else np.NaN,
        BasicFunc.Log: lambda x, y: log(x, y),
        BasicFunc.Log10: lambda x: math.log10(x) if x > 0 else np.NaN,
        BasicFunc.Log2: lambda x: math.log2(x) if x > 0 else np.NaN,
        BasicFunc.NthRoot: lambda x, y: try_nthRoot(x, y),
        BasicFunc.Pow: lambda x, y: try_pow(x, y),
        BasicFunc.RealPart: np.real,  # meaningless for real number
        BasicFunc.Sqrt: lambda x: np.sqrt(x) if x > 0 else np.NaN,
        BasicFunc.SqrtPi: lambda x: np.sqrt(x * math.pi) if x > 0 else np.NaN,
        BasicFunc.Square: lambda x: np.square(x),
        CompareFunc.EqualTo: lambda x, y: x == y,
        CompareFunc.GreaterThan: lambda x, y: x > y,
        CompareFunc.GreaterThanOrEqualTo: lambda x, y: x >= y,
        CompareFunc.LessThan: lambda x, y: x < y,
        CompareFunc.LessThanOrEqualTo: lambda x, y: x <= y,
        CompareFunc.NotEqualTo: lambda x, y: x != y,
        CompareFunc.PairMax: lambda x, y: np.amax([x, y]),
        CompareFunc.PairMin: lambda x, y: np.amin([x, y]),
        OperationsFunc.Add: lambda x, y: np.add(x, y),
        OperationsFunc.Divide: lambda x, y: np.divide(x, y) if y != 0 else np.inf,
        OperationsFunc.Multiply: lambda x, y: np.multiply(x, y),
        OperationsFunc.Subtract: lambda x, y: np.subtract(x, y),
        RoundingFunc.Ceiling: lambda x, y: ceiling(x, y),
        RoundingFunc.CeilingPower2: lambda x: math.ceil(x) ** 2,
        RoundingFunc.Floor: lambda x, y: floor(x, y),
        RoundingFunc.Mod: lambda x, y: x % y if y != 0 else np.NaN,
        RoundingFunc.Quotient: lambda x, y: quotient(x, y) if y != 0 else np.inf,
        RoundingFunc.Remainder: lambda x, y: float(Decimal(x) % Decimal(y)) if y != 0 else np.NaN,
        RoundingFunc.RoundDigits: lambda x, y: round_digits(x, y),
        RoundingFunc.RoundDown: lambda x, y: round_down(x, y),
        RoundingFunc.RoundUp: lambda x, y: round_up(x, y),
        RoundingFunc.ToEven: lambda x: round(x / 2.) * 2,
        RoundingFunc.ToMultiple: lambda x, y: round_to_multiple(x, y),
        RoundingFunc.ToOdd: lambda x: x // 2 * 2 + 1,
        RoundingFunc.Truncate: lambda x, y: truncate(x, y),
        SpecialFunc.Beta: lambda x, y: beta(x, y),
        SpecialFunc.BetaLn: lambda x, y: betaLn(x, y),
        SpecialFunc.EllipticIntegralE: lambda x: ellipticIntegralE(x),
        SpecialFunc.EllipticIntegralK: lambda x: ellipticIntegralK(x),
        SpecialFunc.Erf: lambda x: special.erf(x),
        SpecialFunc.Erfc: lambda x: special.erfc(x),
        SpecialFunc.ErfcScaled: lambda x: special.erfcx(x),
        SpecialFunc.ErfInverse: lambda x: special.erfinv(x) if -1 <= x <= 1 else np.NaN,
        SpecialFunc.ExponentialIntegralEin: lambda x: exponentialIntegralEin(x),
        SpecialFunc.Gamma: lambda x: special.gamma(x),
        SpecialFunc.GammaLn: lambda x: special.gammaln(x) if x >= 0 else np.NaN,
        SpecialFunc.GammaRegularizedP: lambda x, y: special.gammainc(x, y),
        SpecialFunc.GammaRegularizedPInverse: lambda x, y: special.gammaincinv(x, y),
        SpecialFunc.GammaRegularizedQ: lambda x, y: special.gammaincc(x, y),
        SpecialFunc.GammaRegularizedQInverse: lambda x, y: special.gammainccinv(x, y),
        SpecialFunc.Polygamma: lambda x, y: digamma(x),
        TrigonometricFunc.Atanh: lambda x: atanh(x),
        TrigonometricFunc.Cis: lambda x: cmath.rect(1, x),
        TrigonometricFunc.DegreesToRadians: lambda x: math.radians(x),
        TrigonometricFunc.RadiansToDegrees: lambda x: math.degrees(x),
        TrigonometricFunc.Acsc: lambda x: mpf2float(mpmath.acsc(x)) if x != 0 else np.NaN,
        TrigonometricFunc.AcscDegrees: lambda x: math.degrees(mpf2float(mpmath.acsc(x))) if x != 0 else np.NaN,
        TrigonometricFunc.Acsch: lambda x: mpf2float(mpmath.acsch(x)) if x != 0 else np.inf,
        TrigonometricFunc.Asec: lambda x: mpf2float(mpmath.asec(x)) if x != 0 else np.NaN,
        TrigonometricFunc.AsecDegrees: lambda x: math.degrees(mpf2float(mpmath.asec(x))) if x != 0 else np.NaN,
        TrigonometricFunc.Asech: lambda x: mpf2float(mpmath.asech(x)) if x != 0 else np.inf,
        TrigonometricFunc.Cot: lambda x: mpf2float(mpmath.cot(x)) if x != 0 else np.inf,
        TrigonometricFunc.CotDegrees: lambda x: mpf2float(mpmath.cot(math.radians(x))) if x != 0 else np.inf,
        TrigonometricFunc.Coth: lambda x: mpf2float(mpmath.coth(x)) if x != 0 else np.inf,
        TrigonometricFunc.Csc: lambda x: mpf2float(mpmath.csc(x)) if x != 0 else np.inf,
        TrigonometricFunc.CscDegrees: lambda x: mpf2float(mpmath.csc(math.radians(x))) if x != 0 else np.inf,
        TrigonometricFunc.Csch: lambda x: mpf2float(mpmath.csch(x)) if x != 0 else np.inf,
        TrigonometricFunc.SecDegrees: lambda x: mpf2float(mpmath.sec(math.radians(x))),
        TrigonometricFunc.Sign: lambda x: sign(x),
        TrigonometricFunc.Sinc: lambda x: sinc(x),
    }

    _EXTRA_ARG_OP_MAPPING = {
        MathCategory.Basic: [
            BasicFunc.Log,
            BasicFunc.NthRoot,
            BasicFunc.Pow,
            BasicFunc.Atan2,
            BasicFunc.Exp2,
            BasicFunc.Hypotenuse],
        MathCategory.Compare: list(CompareFunc),
        MathCategory.Operations: list(OperationsFunc),
        MathCategory.Rounding: [
            RoundingFunc.Ceiling,
            RoundingFunc.Floor,
            RoundingFunc.Mod,
            RoundingFunc.Quotient,
            RoundingFunc.Remainder,
            RoundingFunc.RoundDigits,
            RoundingFunc.RoundDown,
            RoundingFunc.RoundUp,
            RoundingFunc.ToMultiple,
            RoundingFunc.Truncate],
        MathCategory.Special: [
            SpecialFunc.Beta,
            SpecialFunc.BetaLn,
            SpecialFunc.GammaRegularizedP,
            SpecialFunc.GammaRegularizedQ,
            SpecialFunc.GammaRegularizedP,
            SpecialFunc.GammaRegularizedPInverse,
            SpecialFunc.GammaRegularizedQInverse,
            SpecialFunc.Polygamma]}

    _MPMATH_TRIGONOMETRIC = (
        TrigonometricFunc.Acot,
        TrigonometricFunc.AcotDegrees,
        TrigonometricFunc.Acoth,
        TrigonometricFunc.Arg,
        TrigonometricFunc.Sec,
        TrigonometricFunc.Sech,
    )

    _MATH_TRIGONOMETRIC = (
        TrigonometricFunc.Acos,
        TrigonometricFunc.AcosDegrees,
        TrigonometricFunc.Acosh,
        TrigonometricFunc.Asin,
        TrigonometricFunc.AsinDegrees,
        TrigonometricFunc.Asinh,
        TrigonometricFunc.Atan,
        TrigonometricFunc.AtanDegrees,
        TrigonometricFunc.Cos,
        TrigonometricFunc.CosDegrees,
        TrigonometricFunc.Cosh,
        TrigonometricFunc.Sin,
        TrigonometricFunc.SinDegrees,
        TrigonometricFunc.Sinh,
        TrigonometricFunc.Tan,
        TrigonometricFunc.TanDegrees,
        TrigonometricFunc.Tanh,
    )

    @staticmethod
    def _call_math_by_name(func_name: str, x):
        """
        Dynamically call trigonometric methods from math module
        """
        try:
            if func_name in ["AsinDegrees", "AcosDegrees", "AtanDegrees"]:
                method_to_call = getattr(math, func_name[:-7].lower())
                return math.degrees(method_to_call(x))
            elif func_name in ["SinDegrees", "CosDegrees", "TanDegrees"]:
                method_to_call = getattr(math, func_name[:-7].lower())
                return method_to_call(math.radians(x))
            else:
                method_to_call = getattr(math, func_name.lower())
                return method_to_call(x)
        except ValueError:
            return np.NaN
        except OverflowError:
            return np.inf

    @staticmethod
    def _call_mpmath_by_name(func_name: str, x):
        """
        Dynamically call trigonometric methods from mpmath module
        """
        try:
            if func_name.endswith("Degrees"):
                method_to_call = getattr(mpmath, func_name[:-7].lower())(x)
            else:
                method_to_call = getattr(mpmath, func_name.lower())(x)

            res = mpf2float(method_to_call)
            if func_name.endswith("Degrees"):
                return math.degrees(res)
            return res
        except ValueError:
            return np.NaN

    def __init__(self):
        meta_data = ModuleMetaData(
            id="6bd12c13-d9c3-4522-94d3-4aa44513af57",
            name="Apply Math Operation",
            category="Data Transformation",
            description="Applies a mathematical operation to column values.")
        parameter_list = [
            InputPortModuleParameter(
                name="input",
                friendly_name="Input"),
            ColumnSelectorModuleParameter(
                name="column_selector",
                friendly_name="Column set",
                default_value=convert_column_selection_to_json(
                    ColumnSelectionBuilder().include_col_types(
                        ColumnType.NUMERIC))),
            ValueModuleParameter(
                name="category",
                friendly_name="Category",
                data_type=MathCategory,
                default_value=MathCategory.Basic),
            ValueModuleParameter(
                name="basic_func",
                friendly_name="Basic math function",
                data_type=BasicFunc,
                default_value=BasicFunc.Abs),
            ValueModuleParameter(
                name="operations_func",
                friendly_name="Arithmetic operation",
                data_type=OperationsFunc,
                default_value=OperationsFunc.Add),
            ValueModuleParameter(
                name="compare_func",
                friendly_name="Comparison function",
                data_type=CompareFunc,
                default_value=CompareFunc.EqualTo),
            ValueModuleParameter(
                name="rounding_func",
                friendly_name="Rounding operation",
                data_type=RoundingFunc,
                default_value=RoundingFunc.Ceiling),
            ValueModuleParameter(
                name="special_func",
                friendly_name="Special function",
                data_type=SpecialFunc,
                default_value=SpecialFunc.Beta),
            ValueModuleParameter(
                name="trigonometric_func",
                friendly_name="Trigonometric Function",
                data_type=TrigonometricFunc,
                default_value=TrigonometricFunc.Acos),
            OutputPortModuleParameter(
                name="dataset",
                friendly_name="Result_dataset",
                is_optional=False)]
        for category in MathCategory:
            if category == MathCategory.Trigonometric:
                continue
            category_string = category.value.lower()
            second_argument_type_name = "Second argument type"
            second_argument_name = "Second argument"  # noqa: F841
            if category == MathCategory.Compare:
                second_argument_type_name = "Value to compare type"
                second_argument_name = "Value to compare"  # noqa: F841
            elif category == MathCategory.Rounding:
                second_argument_type_name = "Precision type"
                second_argument_name = "Precision"  # noqa: F841
            parameter_list.extend([
                ValueModuleParameter(
                    name=f"{category_string}_arg_type", friendly_name=second_argument_type_name,
                    data_type=OperationArgumentType, default_value=OperationArgumentType.Constant),
                ColumnSelectorModuleParameter(
                    name=f"{category_string}_column_selector", friendly_name=f"Second argument",
                    default_value=convert_column_selection_to_json(
                        ColumnSelectionBuilder().include_col_types(ColumnType.NUMERIC))),
                ValueModuleParameter(
                    name=f"{category_string}_constant", friendly_name=f"Second argument",
                    data_type=float, default_value=0),
            ])
        parameter_list.append(
            ValueModuleParameter(
                name="output_mode",
                friendly_name="Output mode",
                data_type=OutputMode,
                default_value=OutputMode.Append))
        parameters = ModuleParameters(parameter_list)
        # Bind input port
        parameters["column_selector"].bind_input(parameters["input"])
        for category in MathCategory:
            if category == MathCategory.Trigonometric:
                continue
            category_string = category.value.lower()
            parameters[f"{category_string}_column_selector"].bind_input(
                parameters["input"])
        # Construct module node & dependency
        module_node_category = ModuleSpecNode.from_module_parameter(
            parameters["category"])
        for category in MathCategory:
            category_string = category.value.lower()
            module_node_func = ModuleSpecNode.from_module_parameter(
                parameters[f"{category_string}_func"],
                parent_node=module_node_category,
                options=[category])
            if category == MathCategory.Trigonometric:
                continue
            module_node_arg_type = ModuleSpecNode.from_module_parameter(
                parameters[f"{category_string}_arg_type"],
                parent_node=module_node_category if category in [
                    MathCategory.Compare,
                    MathCategory.Operations] else module_node_func,
                options=[category] if category in [
                    MathCategory.Compare,
                    MathCategory.Operations] else self._EXTRA_ARG_OP_MAPPING[category])

            module_node_column_selector = ModuleSpecNode.from_module_parameter(  # noqa: F841
                parameters[f"{category_string}_column_selector"],
                parent_node=module_node_arg_type,
                options=[
                    OperationArgumentType.ColumnSet])

            module_node_constant = ModuleSpecNode.from_module_parameter(  # noqa: F841
                parameters[f"{category_string}_constant"],
                parent_node=module_node_arg_type,
                options=[
                    OperationArgumentType.Constant])
        module_nodes = [
            ModuleSpecNode.from_module_parameter(parameters["input"]),
            module_node_category,
            ModuleSpecNode.from_module_parameter(parameters["column_selector"]),
            ModuleSpecNode.from_module_parameter(parameters["dataset"]),
            ModuleSpecNode.from_module_parameter(parameters["output_mode"])
        ]
        conda_config_file = './azureml/designer/modules/datatransform/modules/conda_config/apply_math_module.yml'
        super().__init__(
            meta_data=meta_data,
            parameters=parameters,
            module_nodes=module_nodes,
            conda_config_file=conda_config_file)

    def run(self):
        input_data = self._get_input("input")
        try:
            data_df = self._get_input("column_selector")
            self._validate_dataframe(data_df, "column_selector")
            with TimeProfile("Applying math operations on input dataset"):
                output = self._run_op(input_data=input_data, data_df=data_df)

            with TimeProfile("Prepare result for output"):
                result = self._prepare_result(
                    input_data=input_data,
                    output=output,
                    op_columns=data_df.columns)
            # logger.info(format_obj("output", result))
            self._handle_output("dataset", result)
        except Exception as err:
            raise err

    @property
    def _output_mode(self):
        return self.parameters["output_mode"].value

    def _run_op(self, input_data: pd.DataFrame,
                data_df: pd.DataFrame) -> pd.DataFrame:
        operation_type = self.parameters["category"].value
        operation_name = self.parameters[f"{operation_type.value.lower()}_func"].value
        logger.info(f'Operation type is {operation_type.value}, operation name is {operation_name.value}')
        operation_arg_type = None if operation_type == MathCategory.Trigonometric \
            else self.parameters[f"{operation_type.value.lower()}_arg_type"].value
        if operation_arg_type is None:
            logger.info('Apply operations without a constant or percentile')
            output = self._no_arg_op(data_df=data_df, op_name=operation_name)
        elif operation_arg_type == OperationArgumentType.Constant:
            extra_arg = self.parameters[f"{operation_type.value.lower()}_constant"].value
            logger.info('Apply operations on Constant type')
            output = self._const_arg_op(
                data_df=data_df, op_name=operation_name, const=extra_arg)
        else:
            arg_df = self._get_input(
                f"{operation_type.value.lower()}_column_selector")
            self._validate_dataframe(
                arg_df, f"{operation_type.value.lower()}_column_selector")
            logger.info('Apply operations on column selection')
            output = self._column_select_arg_op(
                data_df=data_df,
                op_name=operation_name,
                arg_df=arg_df,
                output_mode=self._output_mode)
        return output

    def _validate_dataframe(self, data: pd.DataFrame, arg_name: str):
        for column_name in data.columns:
            selected_column = data[column_name]
            if not pd.api.types.is_numeric_dtype(selected_column) and not is_type(
                    selected_column, bool) and not selected_column.dropna().count() == 0:
                error_message = f"Specified column \"{selected_column.name}\" dtype is " \
                                f"{selected_column.dtype} which is non-numeric. " \
                                f"This type is not supported by the module."
                ErrorMapping.throw(UserError(error_message))

    def _prepare_result(
            self,
            input_data: pd.DataFrame,
            op_columns: List[str],
            output: pd.DataFrame) -> pd.DataFrame:
        output_mode = self._output_mode
        if output_mode == OutputMode.Append:
            logger.info('Append output to input data')
            _rename_dataframe_to_avoid_duplicated_names(output, input_data.columns.tolist())
            return pd.concat([input_data, output], axis=1)
        if output_mode == OutputMode.ResultOnly:
            logger.info('Generate output without appending to input data')
            return output
        input_data[op_columns] = output
        return input_data

    def _operator(self, op_name, *args):
        if None in args:
            return None
        if op_name in self._MPMATH_TRIGONOMETRIC:
            return ApplyMathModule._call_mpmath_by_name(op_name.value, *args)
        if op_name in self._MATH_TRIGONOMETRIC:
            return ApplyMathModule._call_math_by_name(op_name.value, *args)
        if op_name in self._OPS_FUNC_MAPPING.keys():
            return self._OPS_FUNC_MAPPING[op_name](*args)
        ErrorMapping.throw(ParameterParsingError(op_name))

    def _no_arg_op(self, data_df: pd.DataFrame, op_name) -> pd.DataFrame:
        result = data_df.applymap(lambda x: self._operator(op_name, x))
        result = result.rename(
            columns={
                column: f"{op_name.value}({column})" for column in result})
        return result

    def _const_arg_op(
            self,
            data_df: pd.DataFrame,
            op_name,
            const: float) -> pd.DataFrame:
        result = data_df.applymap(lambda x: self._operator(op_name, x, const))
        result = result.rename(
            columns={
                column: f"{op_name.value}({column}_${const})" for column in result})
        return result

    def _column_select_arg_op(
            self,
            data_df: pd.DataFrame,
            op_name,
            arg_df: pd.DataFrame,
            output_mode: OutputMode) -> pd.DataFrame:
        arg_column_count = len(arg_df.columns)
        data_column_count = len(data_df.columns)
        if len(data_df.columns) != 1 and len(arg_df.columns) != 1 and len(data_df.columns) != len(arg_df.columns):
            ErrorMapping.throw(
                BadNumberOfSelectedColumnsError(
                    self._parameters["column_selector"].friendly_name,
                    expected_col_count=len(arg_df.columns),
                    selected_col_count=len(data_df.columns)))
        elif len(data_df.columns) == 1 and len(arg_df.columns) != 1 and output_mode == OutputMode.Inplace:
            ErrorMapping.throw(
                BadNumberOfSelectedColumnsError(
                    self._parameters["column_selector"].friendly_name,
                    expected_col_count=len(arg_df.columns),
                    selected_col_count=len(data_df.columns)))
        output_df = pd.DataFrame()
        if arg_column_count == 1 or data_column_count == 1:
            for data_column_name in data_df:
                data_column = data_df[data_column_name]
                for arg_column_name in arg_df:
                    arg_column = arg_df[arg_column_name]
                    result_ds = self._op_2_columns(
                        data_column, arg_column, op_name)
                    output_df[result_ds.name] = result_ds
        else:
            for column_index in range(0, data_column_count):
                data_column = data_df.iloc[:, column_index]
                arg_column = arg_df.iloc[:, column_index]
                result_ds = self._op_2_columns(
                    data_column, arg_column, op_name)
                output_df[result_ds.name] = result_ds
        return output_df

    def _op_2_columns(
            self,
            data1: pd.Series,
            data2: pd.Series,
            op_name) -> pd.Series:
        return pd.Series(
            data=[
                self._operator(
                    op_name,
                    v1,
                    v2) for v1, v2 in zip(
                    data1.values.tolist(),
                    data2.values.tolist())],
            name=op_name.value + "(" + data1.name + "_" + data2.name + ")")

    def _check_column_element_type(self, df: pd.DataFrame):
        pass


def _rename_dataframe_to_avoid_duplicated_names(df_to_rename: pd.DataFrame, col_name_list: list):
    """Rename dataframe to avoid duplicated names with a given column name list.

    >>> df = pd.DataFrame({"col0": [1, 2, 3]})
    >>> _rename_dataframe_to_avoid_duplicated_names(df, ["col0", "col1"])
    >>> df.columns.tolist()
    ['col0(2)']

    :param df_to_rename: pd.DataFrame
    :param col_name_list: list
    :return: None
    """
    col_name_mapper = dict()
    column_name_set = set(col_name_list)
    for col_name in df_to_rename.columns:
        if col_name in column_name_set:
            i = 2
            # Append (2) as column name suffix to align with the renaming behavior in V1 Apply Math Operation module..
            new_name = f"{col_name}({i})"
            while new_name in col_name_list:
                i += 1
                new_name = f"{col_name}({i})"

            logger.warning(f"Rename column {col_name} to {new_name}.")
            column_name_set.add(new_name)
            col_name_mapper.update({col_name: new_name})

    df_to_rename.rename(columns=col_name_mapper, inplace=True)
