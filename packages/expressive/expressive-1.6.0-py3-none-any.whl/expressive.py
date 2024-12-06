#!/usr/bin/env python3

""" Copyright 2024 Russell Fordyce

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import re
import time
import warnings
from html import escape as html_escape
from textwrap import dedent as text_dedent

import numba
import numpy
import sympy
from sympy.utilities.lambdify import MODULES as lambdify_modules

__version__ = "1.6.0"  # lazy, see [ISSUE 32]

DTYPES_SUPPORTED = {
    # numpy.dtype("bool"):     1,
    numpy.dtype("uint8"):    8,
    numpy.dtype("uint16"):  16,
    numpy.dtype("uint32"):  32,
    numpy.dtype("uint64"):  64,
    numpy.dtype("int8"):     8,
    numpy.dtype("int16"):   16,
    numpy.dtype("int32"):   32,
    numpy.dtype("int64"):   64,
    numpy.dtype("float32"): 32,
    numpy.dtype("float64"): 64,
    numpy.dtype("complex64"):   64,
    numpy.dtype("complex128"): 128,
}


# helpers for warnings
class ExpressiveWarning(RuntimeWarning):
    pass


def warn(msg):
    warnings.warn(msg, ExpressiveWarning)


def data_cleanup(data):
    """ verify the incoming data can be used

        currently this expects a dict of numpy arrays

        FUTURE optional other numpy-backed arrays support (ie. Pandas, Polars, etc.)
          for now, users can use the relevant .to_numpy() methods
          also consider .to_records()
    """
    if not data:
        raise ValueError("no data provided")
    if not isinstance(data, dict):
        raise TypeError(f"data must be a dict of NumPy arrays, but got {type(data)}")

    result = {}
    vector_length = {}
    for name, ref in data.items():
        # coerce single python values to 0-dim numpy values
        # FIXME makes even small values too wide (int64,float64,complex128)
        # FIXME may not handle very large or very small values
        if isinstance(ref, (int, float, complex)):
            ref = numpy.array(ref)
        if not isinstance(ref, numpy.ndarray):
            raise TypeError(f"data must be a dict of NumPy arrays, but has member ({name}:{type(ref)})")
        if ref.dtype not in DTYPES_SUPPORTED:
            raise TypeError(f"unsupported dtype ({name}:{ref.dtype})")
        # NOTE single (ndim==0) values have shape==() and `len(array)` raises `TypeError: len() of unsized object`
        if ref.ndim == 0:
            vector_length[name] = 0
        elif ref.ndim == 1:
            vector_length[name] = len(ref)
        else:
            raise ValueError(f"only single values or 1-dimensional arrays are allowed, but got {name}:{ref.ndim}")
        result[name] = ref  # pack reference into collection

    # FUTURE support uneven input arrays when indexed [ISSUE 10]
    set_vector_lengths = set(vector_length.values())
    if set_vector_lengths == {0}:
        raise ValueError("only single values passed (ndim=0), no arrays (at least a result array must be passed to determine length)")
    elif len(set_vector_lengths - {0}) != 1:
        raise ValueError(f"uneven data lengths (must be all equal or 0 (non-vector)): {set_vector_lengths}")

    return result


def string_expr_cleanup(expr_string):
    """ a few rounds of basic cleanup to ease usage
        equality is transformed to Eq() form
            `LHS = RHS` -> `LHS==RHS` -> `Eq(LHS,RHS)`
    """
    # FUTURE reconsider if these can use the transformation subsystem
    if not isinstance(expr_string, str):
        raise ValueError("expr must be a string")

    if "<" in expr_string or ">" in expr_string:
        raise ValueError("inequality is not supported")

    # discard all whitespace to ease string processing
    expr_string = re.sub(r"\s+", r"", expr_string)  # expr_string.replace(" ", "")

    # coerce runs of "=" into exactly "=="
    # ideally only (0,1,2) exist, but let users be really excited ==== for now
    expr_string = re.sub(r"=+", "==", expr_string)
    count_equalities = expr_string.count("=") // 2
    if count_equalities == 1:
        lhs, rhs = expr_string.split("==")  # ValueError if doesn't unpack exactly
        # recurse for each half, then rejoin 'em
        lhs = string_expr_cleanup(lhs)
        rhs = string_expr_cleanup(rhs)
        return f"Eq({lhs}, {rhs})"
    elif count_equalities > 1:  # not exactly 0 or 1 (==)
        raise SyntaxError(f"only 1 equivalence (==) can be provided, but parsed {count_equalities}: {expr_string}")

    # user probably meant Pow() not bitwise XOR
    # FIXME add to warning subsystem `if "^" in expr_string:` and allow configuring
    expr_string = expr_string.replace("^", "**")

    # SymPy expects symbols to be separated from Numbers for multiplication
    #   ie. "5x+7" -> "5*x+7"
    # however, care needs to be taken to avoid splitting symbols and functions
    # which contain a number, like `t3`, `log2()`, etc.

    # clean up the case where trailing number isn't multiplied like it should be
    #   ie. "(a+b)2" -> "(a+b)*2"
    # FIXME add to warning subsystem as it feels like an unusual style and could easily be
    # a typo like missing Pow '^' or other operator which would otherwise be silently "fixed"
    # NOTE SymPy might handle this case without the additional '*' after 1.12
    expr_string = re.sub(r"(\))(\d+)", r"\1*\2", expr_string)

    # consider matches where a number appears directly after
    #   start of string | basic operators +-*/ | open parenthesis
    # and directly before a case where
    #   new string starts (symbol or function)
    #   new parentheses block starts "3(a+b)" -> "3*(a+b)"
    # likely this could be better tokenized by Python AST or SymPy itself
    expr_string = re.sub(r"(^|[\+\-\*\/]|\()(\d+)((\w|\())", r"\1\2*\3", expr_string)

    # make sure there's something left
    if not expr_string:
        raise ValueError("no content after cleanup")

    return expr_string


def string_expr_to_sympy(expr_string, name_result=None):
    """ parse string to a SymPy expression
        this is largely support logic to help sympy.parse_expr()
         - support for indexing Symbols via IndexBase[Idx]
         - helps make symbol reference collections consistent before and after parsing
           ie. `reference in e.atoms(IndexedBase)` or `foo is atom` are True

        note that `parse_expr()` creates new symbols for any un-named values

        collections of Symbols are returned as dicts mapping {name:Symbol},
        even if there is only a single Symbol
        while any indexer (Idx) is returned as a mapping of
          {Idx:[low index,high index]}
        so the templated loop won't over or under-run its array indices
    """

    # collection of {name:Symbol} mappings for `sympy.parse_expr()`
    local_dict = {}

    # detect and manage relative offsets
    # FUTURE handle advanced relative indexing logic [ISSUE 11]
    offset_values = {}
    offset_range = [0, 0]  # spread amongst offsets as [min,max]
    for chunk in re.findall(r"(\w+)\[(.+?)\]", expr_string):
        base, indexing_block = chunk
        indexer = str(sympy.parse_expr(indexing_block).free_symbols.pop())
        try:  # extract the offset amount ie. x[i-1] is -1
            offset = sympy.parse_expr(indexing_block).atoms(sympy.Number).pop()
        except KeyError:
            offset = 0  # no offset like x[i]
        offset_range[0] = min(offset_range[0], offset)
        offset_range[1] = max(offset_range[1], offset)
        offset_values[base] = sympy.IndexedBase(base)
        offset_values[indexer] = sympy.Idx(indexer)
    local_dict.update(offset_values)

    # convert forms like `expr_rhs` into `Eq(result_lhs, expr_rhs)`
    verify_literal_result_symbol = False  # avoid NameError in later check
    if not expr_string.startswith("Eq("):
        if "=" in expr_string:
            raise RuntimeError(f"BUG: failed to handle equality during cleanup: {expr_string}")
        if name_result is None:
            verify_literal_result_symbol = True  # enable later warning path checks
            name_result = "result"
        # rewrite `expr_string` to `Eq()` form
        if offset_values:
            syms_result = sympy.IndexedBase(name_result)
            # FIXME indexer smuggled from above loop scope
            expr_string = f"Eq({syms_result}[{indexer}], {expr_string})"
        else:
            syms_result = sympy.Symbol(name_result)
            expr_string = f"Eq({syms_result}, {expr_string})"
        # pack result into locals before parse
        local_dict.update({name_result: syms_result})

    # FUTURE consider transformation system instead of direct regex hackery
    expr_sympy = sympy.parse_expr(expr_string, local_dict=local_dict)

    # assert there is only a single Idx
    # FUTURE multiple Idx can generate deeper loops
    indexers = expr_sympy.atoms(sympy.Idx)  # set of Symbols
    if len(indexers) > 1:
        raise ValueError(f"only a single Idx is supported, but got: {indexers}")

    if not expr_sympy.atoms(sympy.Eq):  # ensures (lhs,rhs) properties, alt: hasattr
        raise RuntimeError(f"BUG: didn't coerce into Eq(LHS, RHS) form: {expr_sympy}")

    # now (re-)extract the result Symbol from LHS
    # NOTE IndexedBase coerced to Symbol [ISSUE 9]
    atoms_lhs = expr_sympy.lhs.atoms(sympy.Symbol)
    # FUTURE opportunity to extract Number from LHS to fail or divide out
    if len(atoms_lhs) == 1:
        pass  # pop later, set of exactly 1 Symbol
    elif len(atoms_lhs) == 2:
        atoms_lhs = expr_sympy.lhs.atoms(sympy.IndexedBase)
        if len(atoms_lhs) != 1:
            raise ValueError(f"multiple possible result values: {atoms_lhs}")
    else:
        raise ValueError(f"multiple or no possible result values from LHS atoms:{atoms_lhs}")
    symbol_result = atoms_lhs.pop()  # now dissolve set: {x} -> x

    if name_result is not None and name_result != symbol_result.name:
        raise ValueError(f"mismatch between name_result ({name_result}) and parsed symbol name ({symbol_result.name})")

    # make dicts of {name: symbol} for caller
    # NOTE `symbol_result` must be last to simplify dropping via slicing in later logic
    # NOTE `.atoms(Symbol)` picks up IndexedBase, but demotes them to new `Symbol` instances [ISSUE 9]
    symbols = {s.name: s for s in expr_sympy.atoms(sympy.Symbol) if s.name != symbol_result.name}

    # rewrite symbols in lexical order
    sym_temp = {}
    for name in sorted(symbols.keys()):  # force lexical symbol ordering for consistency
        try:  # prefer IndexedBase where possible
            sym_temp[name] = local_dict[name]
        except KeyError:
            sym_temp[name] = symbols[name]
    symbols = sym_temp  # clobber name with the new sorted dict

    # make a dict (len==1) of the result symbol
    syms_result = {symbol_result.name: symbol_result}
    # now append it to the symbols dict so it can be an argument
    symbols.update(syms_result)  # always the last symbol

    # hint that user may be misusing "result" name in their RHS
    if verify_literal_result_symbol and (
        name_result in {a.name for a in expr_sympy.rhs.atoms(sympy.Symbol)}) and (
        name_result not in offset_values.keys()
    ):
        warn("symbol 'result' in RHS refers to result array, but not indexed or passed as name_result")

    # extract Idx value (exactly 0 or 1 value)
    syms_idx = {s.name: offset_range for s in indexers}
    if len(syms_idx) > 1:
        raise RuntimeError(f"BUG: too may Idx values: {syms_idx}")

    # FIXME atoms(Symbol) demotes IndexBase and Idx to Symbol in result [ISSUE 9]
    for name_idx in syms_idx.keys():  # expressly remove Idx names
        del symbols[name_idx]
    return expr_sympy, symbols, syms_idx, syms_result


def dtype_result_guess(expr, data):
    """ attempt to automatically determine the resulting dtype given an expr and data

        this is a backup where the user has not provided a result dtype
        possibly it could support warning for likely wrong dtype

        this is not expected to be a general solution as the problem is open-ended
        and likely depends on the real data

        WARNING this logic assumes the highest bit-width is 64
          larger widths will require rewriting some logic!
          intermediately a user should specify the type, assuming
          a (future) numba really has support for it

        FUTURE consider  `numpy.dtype.alignment`
    """
    # set of dtypes from given data
    dtypes_expr = {c.dtype for c in data.values()}  # set of NumPy types

    # throw out some obviously bad cases
    if not dtypes_expr:
        raise ValueError("no data provided")
    dtypes_unsupported = dtypes_expr - set(DTYPES_SUPPORTED.keys())
    if dtypes_unsupported:
        raise TypeError(f"unsupported dtypes: {dtypes_unsupported}")

    max_bitwidth = max(DTYPES_SUPPORTED[dt] for dt in dtypes_expr)

    # always coerce complex types
    if numpy.dtype("complex128") in dtypes_expr:
        return numpy.dtype("complex128")
    if numpy.dtype("complex64") in dtypes_expr:
        return numpy.dtype("complex128")
        # if max_bitwidth _ :  # TODO actually rely on other dtype widths

    # FUTURE support for float128 (does Numba support this?)
    if max_bitwidth > 64:
        raise RuntimeError(f"BUG: max_bitwidth {max_bitwidth}: only complex types exceeding 64 are supported: {dtypes_expr}")

    # now only
    if numpy.dtype("float64") in dtypes_expr:
        return numpy.dtype("float64")
    # promote 32-bit float to 64-bit when greater types are present
    if numpy.dtype("float32") in dtypes_expr:
        if max_bitwidth > 32:
            return numpy.dtype("float64")
        return numpy.dtype("float32")

    # detect structures that make the result logically floating-point
    # TODO perhaps these should be part of a structured attempt to constrain inputs
    #   in addition to being available for guessing resulting type,
    #   even if the constraints are (initially) warns, not hard errors
    # see https://docs.sympy.org/latest/modules/functions/elementary.html
    if (
        expr.atoms(
            # straightforward floats
            sympy.Float,
            # trancendental constants
            sympy.pi,
            sympy.E,
            # FUTURE general scipy.constants support
            # common floating-point functions
            sympy.log,
            sympy.exp,
            # sympy.sqrt,  # NOTE simplifies to Pow(..., Rational(1,2))
            # sympy.cbrt,  #   can be found with expr.match(cbrt(Wild('a')))
            # trig functions
            sympy.sin, sympy.asin, sympy.sinh, sympy.asinh,
            sympy.cos, sympy.acos, sympy.cosh, sympy.acosh,
            sympy.tan, sympy.atan, sympy.tanh, sympy.atanh,
            sympy.cot, sympy.acot, sympy.coth, sympy.acoth,
            sympy.sec, sympy.asec, sympy.sech, sympy.asech,
            sympy.csc, sympy.acsc, sympy.csch, sympy.acsch,
            sympy.sinc,
            sympy.atan2,
            # LambertW?  # TODO is complex support actually extra work?
        ) or (
            # discover simple division
            # direct Integers are Rational, but fractional atoms are not Integer
            # additionally, simple divisions will simplify to Integer
            #   >>> parse_expr("4").atoms(Rational), parse_expr("4").atoms(Integer)
            #   ({4}, {4})
            #   >>> parse_expr("4/2").atoms(Rational), parse_expr("4/2").atoms(Integer)
            #   ({2}, {2})
            #   >>> e = "4/2*x + 1/3*y"
            #   >>> parse_expr(e).atoms(Rational) - parse_expr(e).atoms(Integer)
            #   {1/3}
            expr.atoms(sympy.Rational) - expr.atoms(sympy.Integer)
        ) or (
            # detect N/x constructs
            #   >>> srepr(parse_expr("2/x"))
            #   "Mul(Integer(2), Pow(Symbol('x'), Integer(-1)))"
            expr.match(sympy.Pow(sympy.Wild("", properties=[lambda a: a.is_Symbol or a.is_Function]), sympy.Integer(-1)))
        )
    ):
        if max_bitwidth <= 16:  # TODO is this a good assumption?
            return numpy.dtype("float32")
        return numpy.dtype("float64")

    # now pick the largest useful int
    # NOTE constant coefficients should all be Integer (Rational) if reached here

    w_signed   = 0  # NOTE Falsey
    w_unsigned = 0
    for dtype in dtypes_expr:
        if numpy.issubdtype(dtype, numpy.signedinteger):
            w_signed = max(w_signed, DTYPES_SUPPORTED[dtype])
        elif numpy.issubdtype(dtype, numpy.unsignedinteger):
            w_unsigned = max(w_unsigned, DTYPES_SUPPORTED[dtype])
        else:
            raise RuntimeError(f"BUG: failed to determine if {dtype} is a signed or unsigned int (is it a float?)")
    if w_signed and w_unsigned:
        raise TypeError("won't guess dtype for mixed int and uint, must be provided")
    if w_signed and not w_unsigned:
        return numpy.dtype("int64") if w_signed > 32 else numpy.dtype("int32")  # FUTURE >=
    if not w_signed and w_unsigned:
        return numpy.dtype("uint64") if w_unsigned > 32 else numpy.dtype("uint32")  # FUTURE >=

    raise RuntimeError(f"BUG: couldn't determine a good result dtype for {dtypes_expr}")


def get_result_dtype(expr_sympy, results, data, dtype_result=None):
    """ ensure the result datatype matches what's given if any
        use a reasonable guess when not provided explicitly or via result data array
    """
    if results:
        name_result = next(iter(results.keys()))  # NOTE dict of 1 value
        try:
            dtype_data_result = data[name_result].dtype
        except KeyError:  # name not in in data (not passed: create array later)
            dtype_data_result = None
        else:  # data array contains result for dtype, if expressly provided too, ensure they match
            if dtype_result is None:
                dtype_result = dtype_data_result
            else:
                if dtype_data_result != dtype_result:
                    raise ValueError(f"passed mismatched result array ({dtype_data_result}) and result dtype ({dtype_result})")

    # if dtype_result is still None, guess or raise
    if dtype_result is None:
        dtype_result = dtype_result_guess(expr_sympy, data)

    if dtype_result not in DTYPES_SUPPORTED:
        raise RuntimeError(f"BUG: dtype_result ({dtype_result}) not in DTYPES_SUPPORTED")

    # definitely a supported NumPy type now
    return dtype_result


def signature_generate(symbols, results, data, dtype_result):
    """ generate a signature like
          `Array(int64, 1d, C)(Array(int64, 1d, C))`
        note that Arrays can be named and they begin with the name "array", which
          `repr()` -> `array(int64, 1d, C)`

        refer to Numba types docs and Numba Array(Buffer) classes for more details
          https://numba.readthedocs.io/en/stable/reference/types.html
    """
    # FUTURE support for names (mabye an upstream change to numba)
    #   likely further C-stlye like `void(int32 a[], int64 b)`
    # without names, the dtypes are positional, so ordering must be maintained
    # within logic that could reorder the arguments after fixing the signature!
    # however, when the user calls the Expressive instance,
    # data is passed as kwargs `fn(**data)` to the inner function
    mapper = []

    if len(results) != 1:
        raise RuntimeError("BUG: results symbols should have exactly 1 member: {results}")
    name_result   = next(iter(results.keys()))  # NOTE dict of len==1 if given
    result_passed = bool(name_result in data)  # directly check membership

    names_symbols = list(symbols.keys())
    if not result_passed:
        names_symbols.pop()  # drop the result name (guaranteed to be last symbol in dict)
    for name in names_symbols:  # use symbol ordering, not data ordering
        ref = data[name]
        # make a field like `array(int64, 1d, C)`
        dims   = ref.ndim
        layout = "C"  # FUTURE allow other layouts and use array method [ISSUE 35]
        dtype  = getattr(numba.types, str(ref.dtype))  # FIXME brittle, can `numba.typeof()` be used?
        field  = numba.types.Array(dtype, dims, layout)
        mapper.append(field)

    # TODO warn or raise if not all data names used (+config) [ISSUE 43]
    #   len() is sufficient (KeyError earlier if fewer, but may wrap that too)

    # now build complete signature for Numba to compile
    # FUTURE consider support for additional dimensions in result
    dtype = getattr(numba.types, str(dtype_result))
    return numba.types.Array(dtype, 1, "C")(*mapper), result_passed


def verify_indexed_data_vs_symbols(symbols, result_passed, data):
    """ if this instance is indexed, make sure the data makes sense for it
        for example, with "a + b[i]", `a` must be a single value and `b` must be an array

        TODO consider if this should be merged with `signature_generate()`
    """
    names_symbols = list(symbols.keys())
    if not result_passed:
        names_symbols.pop()  # drop the result name (guaranteed to be last symbol in dict)

    for name in names_symbols:
        symbol = symbols[name]
        dims   = data[name].ndim
        if dims > 1:  # this should have been forced in `data_cleanup()` (for now?)
            raise RuntimeError(f"BUG: no support for higher-dimensional arrays yet {name}:{dims}")
        if isinstance(symbol, sympy.IndexedBase) and dims == 0:
            raise ValueError(f"'{name}' is indexed, but is a single (ndim={dims}) value in data")
        if isinstance(symbol, sympy.Symbol) and dims == 1:
            raise ValueError(f"'{name}' is not indexed, but passed array (ndim={dims}) value in data")


def get_filler_result(dtype_result):
    """ determine a sensible fill value when creating a result array
        only called when
         - using indexing (indexers exists)
         - result array wasn't passed (whatever content it has is used)
    """
    return {
        # numpy.dtype("bool"):,  # FUTURE (probably fail hard and force filling)
        numpy.dtype("uint8"):  0,
        numpy.dtype("uint16"): 0,
        numpy.dtype("uint32"): 0,
        numpy.dtype("uint64"): 0,
        numpy.dtype("int8"):  -1,
        numpy.dtype("int16"): -1,
        numpy.dtype("int32"): -1,
        numpy.dtype("int64"): -1,
        numpy.dtype("float32"): numpy.nan,
        numpy.dtype("float64"): numpy.nan,
        # numpy.dtype("complex64"):,  # TODO [ISSUE 36] complex numbers
        # numpy.dtype("complex128"):,
    }[dtype_result]


def loop_function_template_builder(expr, symbols, indexers, results, result_passed, dtype_result):
    """ generate environment and code to support the function
         - create namespace
         - fill template
         - exec() to generate the code
         - extract new function
    """
    # build namespace with everything needed to support the new callable
    # simplified version of sympy.utilities.lambdify._import
    _, _, translations, import_cmds = lambdify_modules["numpy"]
    expr_namespace = {"I": 1j}  # alt `copy.deepcopy(lambdify_modules["numpy"][1])`
    for import_line in import_cmds:
        exec(import_line, expr_namespace)
    for sympyname, translation in translations.items():
        expr_namespace[sympyname] = expr_namespace[translation]

    # get ready to build the template (note dict of len==1)
    name_result = next(iter(results.keys()))

    # construct further template components
    names_symbols = list(symbols.keys())
    if not result_passed:
        # drop the result from arguments
        names_symbols.pop()

    block_args = ", ".join(names_symbols)

    # prepare values to fill template
    if indexers:
        block_result = ""      # if the result array is passed in, just fill it by-index
        if not result_passed:  # without it, dynamically create an array of discovered length
            result_filler = get_filler_result(dtype_result)
            block_result = f"{name_result} = numpy.full(length, {result_filler}, dtype={dtype_result})"
    else:  # not indexed
        # broadcast when a result array is provided
        # otherwise let LHS be created dynamically
        broadcast_opt = "[:]" if result_passed else ""

    # FUTURE: need to manage this with [ISSUE 10] uneven arrays
    # NOTE assumes the passed array is of an appropriate length, which may not be true
    if result_passed:  # go ahead and use the passed array if possible
        name_size_symbol = name_result
    else:
        atom = sympy.IndexedBase if indexers else sympy.Symbol
        for symbol in expr.rhs.atoms(atom):
            name_symbol = symbol.name
            if name_symbol == name_result:  # result not passed so it can't be used (earlier check)
                continue  # pragma nocover FIXME ordering depends on hash seeding PYTHONHASHSEED
            name_size_symbol = name_symbol
            break
        else:  # this should have been verified in `data_cleanup()` or `verify_indexed_data_vs_symbols()`
            raise ValueError("BUG: couldn't determine size of result array, at least one symbol must be an array or pass a result array to fill")

    # construct template
    # FUTURE consider errno or errno-like arg to retrieve extra information from namespace
    if not indexers:
        T = """
        def expressive_wrapper({block_args}):
            {lhs}{broadcast_opt} = {rhs}
            return {name_result}
        """.format(
            block_args=block_args,
            broadcast_opt=broadcast_opt,
            lhs=expr.lhs,
            rhs=expr.rhs,
            name_result=name_result,
        )
    elif len(indexers) == 1:
        indexer, (start, end) = next(iter(indexers.items()))
        start = -start  # flip start to be positive (no -0 in "normal" Python)
        # FIXME improve accounting for result LHS in range
        #   consider disallowing negative LHS offset, though it could be useful
        T = """
        def expressive_wrapper({block_args}):
            length = len({name_size_symbol})
            {block_result}
            for {indexer} in range({start}, length - {end}):
                {lhs} = {rhs}
            return {name_result}
        """.format(
            block_args=block_args,
            name_size_symbol=name_size_symbol,
            block_result=block_result,
            lhs=expr.lhs,
            rhs=expr.rhs,
            indexer=indexer,
            start=start,
            end=end,
            name_result=name_result,
        )
    else:
        raise RuntimeError(f"BUG: indexers must be len 1 when provided (see string_expr_to_sympy): {indexers}")

    # tidy up template
    T = text_dedent(T)

    # build and extract
    exec(T, expr_namespace)
    fn = expr_namespace["expressive_wrapper"]

    return fn


def verify_cmp(data, expr_sympy, fn_python, fn_compiled, indexers):
    """ check if the compiled and python (pre-jit) functions have the same results
        this helps catch undefined behavior in Numba space, such as log(0)
    """
    # FIXME many magic numbers should be part of config subsystem [ISSUE 29]
    lengths = {k: (len(ref) if ref.ndim == 1 else 1) for k, ref in data.items()}
    lengths_max = max(lengths.values())
    if lengths_max > 2000:
        warn(f"excessive data may be negatively impacting start time: {lengths}")
    data_names_containing_nan = []
    for name, ref in data.items():
        if numpy.isnan(ref).any():
            data_names_containing_nan.append(name)
    if data_names_containing_nan:
        warn(f"some data in {','.join(data_names_containing_nan)} is NaN")

    time_start = time.process_time_ns()
    result_py = fn_python(**data)
    time_py = time.process_time_ns() - time_start

    time_start = time.process_time_ns()
    result_nb = fn_compiled(**data)
    time_nb = time.process_time_ns() - time_start

    # check if either ran more than 10 seconds
    if (time_py // (10**9) >= 10) or (time_nb // (10**9) >= 10):
        warn(f"verify took a long time python:{time_py / (10**9):.2f}s, compiled:{time_nb / (10**9):.2f}s")

    # even very short lists shouldn't be hilariously slower when compiled
    if time_nb / time_py > 50:  # 50x slower
        warn(f"compiled function ({time_nb}ns) may be slower than direct NumPy ({time_py}ns) (data lengths {lengths})")

    # symbolics -> Number -> evalf()
    # FUTURE consider collecting Exceptions into a single warning reporting multiple rows
    result_sp = None
    if not indexers:  # no indexed values, offsetting, etc.
        # NOTE numpy.nan are never equal, while sympy.nan are structurally equal, but not symbolically
        #   >>> numpy.nan == numpy.nan
        #   False
        #   >>> sympy.nan == sympy.nan
        #   True
        #   >>> sympy.Eq(numpy.nan, numpy.nan)
        #   False
        #   >>> sympy.Eq(sympy.nan, sympy.nan)
        #   False
        mapper_incomparable_sympy_results = {
            sympy.oo:   numpy.inf,
            sympy.zoo: -numpy.inf,
            sympy.nan:  numpy.nan,
        }
        result_sp = []
        for ref in data.values():
            if ref.ndim == 1:
                length = len(ref)
                break
        else:  # should have been trapped in `data_cleanup(data)`
            raise RuntimeError("BUG: only single values passed (ndim=0), no arrays")
            # length = 1  # FUTURE if allowing single values
        for index in range(length):
            row = {}
            row_nan = False  # track if the row has nan
            for symbols in data.keys():  # needed to handle single values
                value = data[symbols] if data[symbols].ndim == 0 else data[symbols][index]
                if numpy.isnan(value):
                    row_nan = True
                    break
                row[symbols] = value

            if row_nan:  # row is broken, write nan and continue
                result_sp.append(numpy.nan)  # NOTE sympy.nan are equal
                continue  # next row
            # directly use result as `Eq(LHS,RHS)` when no indexers are passed
            r = expr_sympy.rhs.subs(row).evalf()
            if sympy.I in r.atoms():  # "3 * 1j" -> "3*I" -> "3j"
                r = complex(r)
            else:
                r = mapper_incomparable_sympy_results.get(r) or float(r)  # nan is not Falsey, 0->0.0
            result_sp.append(r)

    if result_sp:
        if indexers:
            raise RuntimeError("BUG: impossible code path, symbolic branch not yet supported with indexers")
        result = []  # collection of bool
        for index in range(length):
            value_np, value_py, value_sp = result_nb[index], result_py[index], result_sp[index]
            r1 = numpy.allclose(value_np, value_py, equal_nan=True)
            r2 = numpy.allclose(value_py, value_sp, equal_nan=True)
            r3 = numpy.allclose(value_sp, value_np, equal_nan=True)
            result.append(r1 and r2 and r3)  # (this is a bool)
        result = all(result)  # compact collection into single bool
    else:
        indexer, (start, end) = next(iter(indexers.items()))
        start = -start
        end   = -end or None  # `1` to `-1`, `0` to `None`
        result = numpy.allclose(result_py[start:end], result_nb[start:end], equal_nan=True)

    if not result:  # FUTURE opportunity to hard fail here (via from config?) [ISSUE 29]
        raise RuntimeError(f"not allclose({result}) when comparing between NumPy and compiled function")
    results = {
        "nb": result_nb,
        "py": result_py,
        "sp": result_sp,
    }
    return result, results


class Expressive:

    def __init__(self, expr, name_result=None, *, config=None, allow_autobuild=False):
        # FUTURE make cleanup optional (arg or config)
        # FUTURE support passing SymPy expr [ISSUE 42]
        self._expr_source_string = string_expr_cleanup(expr)
        self._expr_sympy, self._symbols, self._indexers, self._results = string_expr_to_sympy(self._expr_source_string, name_result)

        # TODO config subsystem [ISSUE 29]
        "config hoopla"
        self.allow_autobuild = allow_autobuild

        self._verifications = {}  # FIXME unstable contents for now
        self.signatures_mapper = {}

    def __str__(self):
        # NOTE unstable result for now
        return f"{type(self).__name__}({self._expr_sympy})"

    def __repr__(self):
        # NOTE unstable result for now
        # FUTURE display some major config settings (but most in a dedicated output)
        # FUTURE consider how to support or use `sympy.srepr()`
        content = [
            f"build_signatures={len(self.signatures_mapper)}",
            f"allow_autobuild={self.allow_autobuild}",
        ]
        return f"{str(self)} <{','.join(content)}>"

    def _repr_html_(self):
        """ dedicated Jupyter/IPython notebook pretty printer method
            this is loaded into an iframe, so mathjax is dynamically acquired too
            in order to render the LaTeX output from SymPy
        """
        # NOTE unstable result for now

        expr_latex = self._expr_sympy._repr_latex_()

        # ensure expr can be displayed properly
        # output wrapped by $$ is the normal output, however, it causes the result to be centered
        # instead, \(expr\) form is preferred which makes the result "inline" and aligned as parent
        expr_latex = re.sub(r"^\$\$?([^\$]+)\$\$?$", r"\(\1\)", expr_latex)
        if not (expr_latex.startswith(r"\(") and expr_latex.endswith(r"\)") and len(expr_latex) >= 5):
            warn(rf"unexpected expr format (should be wrapped in $ -> \(\)): {expr_latex}")
            return repr(self)

        # TODO improved templating (though I want to keep deps low)
        #   consider some template engine when available
        # generated as-suggested on mozilla https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity
        #   `cat src/tex-chtml.js | openssl dgst -sha384 -binary | openssl base64 -A`
        # https://github.com/mathjax/MathJax 3.2.2@227c4fecc0037cef1866d03c64c3af10b685916d
        # see also https://github.com/mathjax/MathJax-src
        template = """
        <!DOCTYPE html>
        <html>
        <head>
        <script type="text/javascript" id="MathJax-script"
            src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-chtml.js"
            integrity="sha348-AHAnt9ZhGeHIrydA1Kp1L7FN+2UosbF7RQg6C+9Is/a7kDpQ1684C2iH2VWil6r4"
            crossorigin="anonymous"></script>
        </head>
        <body>
        <ul style="list-style-type:none;padding-left:0;">
        {html_list}
        </ul>
        </body>
        </html>
        """

        # stack entries in unordered list
        collected_values = [
            expr_latex,  # advanced representation
            repr(self),  # FIXME unstable
        ]
        html_list = "\n        ".join(f"<li>{html_escape(a)}</li>" for a in collected_values)

        # fill template
        content = text_dedent(template.format(
            html_list=html_list,
        ))

        return content

    def _prepare(self, data, dtype_result):
        """ prepare before build or __call__ """
        data = data_cleanup(data)
        dtype_result = get_result_dtype(self._expr_sympy, self._results, data, dtype_result)
        signature, result_passed = signature_generate(self._symbols, self._results, data, dtype_result)
        if self._indexers:  # when indexed, the data shape (array vs single values) matter much more
            verify_indexed_data_vs_symbols(self._symbols, result_passed, data)
        return data, dtype_result, signature, result_passed

    def build(self, data, *, dtype_result=None, verify=None):  # arch target?
        """ compile function and collect it in signatures_mapper """
        data, dtype_result, signature, result_passed = self._prepare(data, dtype_result)

        # automatically set to verify when the array is small
        # only happens for pre-builds as __call__ sets `verify=False` when autobuilding
        if verify is None:
            # approximate max array length (ignores offsets)
            lengths_max = max((len(ref) if ref.ndim == 1 else 1) for ref in data.values())
            if lengths_max <= 50:  # FIXME magic numbers to config subsystem [ISSUE 29]
                verify = True

        # generate Python function
        expr_fn = loop_function_template_builder(
            self._expr_sympy,
            self._symbols,
            self._indexers,
            self._results,
            result_passed,
            dtype_result
        )

        # pre-compile function as the signature is given
        # FUTURE collect into a class with additional properties (just build time?)
        built_function = numba.jit(
            signature,
            nopython=True,  # now the default
            # fastmath=True,  # FUTURE config setting [ISSUE 29]
            parallel=True,  # FUTURE config setting [ISSUE 29]
        )(expr_fn)

        if verify:
            result, results = verify_cmp(data, self._expr_sympy, expr_fn, built_function, self._indexers)
            # self._verifications[signature] = result, results  # unstable contents for now

        self.signatures_mapper[signature] = built_function

        # FUTURE does it make sense to return the result(s) from verify?
        #   return self, {"py": result_py, "nb": result_nb, "sp": result_sp}
        # no: probably better to make the result(s) a new property
        return self  # enable dot chaining

    def __call__(self, data, dtype_result=None):
        """ call the relevant compiled function for a particular data collection on it
            if signatures_mapper doesn't have the signature, allow_autobuild can be used
            to create it dynamically, though this loses a lot of the runtime execution speed
            benefits available to users who are able to pre-build for all the data
            signatures they have
        """
        data, dtype_result, signature, result_passed = self._prepare(data, dtype_result)

        try:
            fn = self.signatures_mapper[signature]
        except KeyError:
            if not self.allow_autobuild:
                raise KeyError("no matching signature for data: use .build() with representative sample data (or set allow_autobuild=True)")
            # FUTURE improve warning subsystem (never, once, each, some callback, etc.)
            #   further opportunity for dedicated config features
            # really it's important to alert users to a potential error, but not nanny 'em
            time_start = time.process_time()
            self.build(data, dtype_result=dtype_result, verify=False)
            time_build = time.process_time() - time_start
            warn(f"autobuild took {time_build:.2f}s of process time, prefer .build(sample_data) in advance if possible")
            try:
                fn = self.signatures_mapper[signature]
            except KeyError:  # pragma nocover - bug path
                raise RuntimeError("BUG: failed to match signature after autobuild")

        return fn(**data)
