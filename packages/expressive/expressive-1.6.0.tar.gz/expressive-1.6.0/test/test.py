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

import unittest
import unittest.mock

import contextlib
import re
import time
import warnings
from itertools import zip_longest

import numpy
import sympy

# FIXME ugly hack
import sys
sys.path.append("src")
import expressive


@contextlib.contextmanager
def must_warn(warning_regexes, ordered=False, multimatch=False):
    if isinstance(warning_regexes, str):
        warning_regexes = [warning_regexes]
    if not isinstance(warning_regexes, (list, set, tuple)):  # pragma nocover
        raise ValueError(f"warning_regexes must be one of [str,list,set,tuple], but got {type(warning_regexes)}")
    if ordered and isinstance(warning_regexes, set):  # pragma nocover
        raise ValueError("warning_regexes passed as a set which is unordered, but ordered=True")

    # TODO make exact string vs regex easier/more obvious, assumes re for now
    with warnings.catch_warnings(record=True) as warning_collection:
        yield
        warning_messages = [str(w.message) for w in warning_collection]

    if ordered:  # pragma nocover
        raise NotImplementedError("drop nocover before using")
        for index, warn_re, warn_msg in enumerate(zip_longest(
            warning_regexes,
            warning_messages,
        )):
            if warn_re is None:
                raise AssertionError(f"unmatched warning (warning {index}): '{warn_msg}'")
            if not re.match(warn_re, warn_msg):
                raise AssertionError(f"message doesn't match regex (warning {index}): '{warn_re}' '{warn_msg}'")
        return  # completed ordered path

    # unordered warnings
    count_total_warnings = len(warning_regexes)
    warning_regexes = list(set((warning_regexes)))  # drop duplicates, becomes unordered
    for warn_re in warning_regexes:
        index_matched = []
        for index, warn_msg in enumerate(warning_messages):
            if re.match(warn_re, warn_msg):
                index_matched.append(index)
                if not multimatch:  # only match once message
                    break  # next warn_re
        if not index_matched:  # pragma nocover NOTE can't use else clause due to multimatch
            raise AssertionError(f"failed to match regex to any warning ({count_total_warnings} total): {warn_re}")
        # drop messages backwards by-index so the earlier ones are unaffected by mutation
        for index in index_matched[::-1]:
            del warning_messages[index]

    # in the successful case, every message is deleted
    if warning_messages:  # pragma nocover
        warns_block = "\n".join(warning_messages)
        raise AssertionError(f"failed to match some warnings ({count_total_warnings} total):\n{warns_block}")


class TestEqualityExtract(unittest.TestCase):

    def test_equality_extract(self):
        data = {
            "x": numpy.arange(100, dtype="int64"),
        }
        E = expressive.Expressive("r = x**2")
        E.build(data)

        # give it a spin
        data = {
            "x": numpy.arange(1000, dtype="int64"),
        }
        result = E(data)

        self.assertTrue(numpy.array_equal(
            numpy.arange(1000)**2,
            result,
        ))

    def test_pass_name_result(self):
        E = expressive.Expressive("x**2", name_result="some_result")
        self.assertTrue(len(E._results) == 1)
        self.assertTrue("some_result" in E._results)

        # mismatch case
        with self.assertRaisesRegex(ValueError, re.escape("mismatch between name_result (b) and parsed symbol name (a)")):
            E = expressive.Expressive("a = x**2", name_result="b")

    def test_indexed(self):
        data = {
            "x": numpy.arange(1000, dtype="int64"),
        }

        # lhs and rhs are indexed
        E = expressive.Expressive("r[i] = x[i]**2")
        E.build(data)

        # indexed and named everywhere
        E = expressive.Expressive("r[i] = x[i]**2", name_result="r")
        E.build(data)

        self.assertTrue(len(E._results) == 1)
        self.assertTrue("r" in E._results)
        # the symbol should be an IndexedBase
        self.assertTrue(E._results["r"].atoms(sympy.IndexedBase))

        E = expressive.Expressive("r[i] = x**2")
        with self.assertRaisesRegex(ValueError, re.escape("'x' is not indexed, but passed array (ndim=1) value in data")):
            E.build(data)

        # mismatched LHS,RHS indexers
        with self.assertRaisesRegex(ValueError, r"^only a single Idx is supported, but got: \{[ni], [ni]\}$"):
            E = expressive.Expressive("r[i] = a[n]**2")

    def test_indexed_offset(self):

        def idx_range_helper(e):
            indexer, (start, end) = next(iter(e._indexers.items()))
            indexer = str(indexer)
            return indexer, start, end

        for expr_string, offset_values in {
            "r[i] = x[i-1]**2": ("i", -1, 0),
            "r[i] = x[i+1]**2": ("i",  0, 1),
            "r[i+1] = x[i]**2": ("i",  0, 1),
            "r[i-1] = x[i]**2": ("i", -1, 0),
        }.items():
            E = expressive.Expressive(expr_string)
            self.assertEqual(idx_range_helper(E), offset_values)

    def test_bad_equalities(self):
        with self.assertRaisesRegex(ValueError, "multiple possible result values"):
            E = expressive.Expressive("a + b = x")
        with self.assertRaisesRegex(ValueError, "multiple or no possible result values"):
            E = expressive.Expressive("a + b + c = x")
        with self.assertRaisesRegex(ValueError, "multiple or no possible result values"):
            E = expressive.Expressive("a[i] + b = x")
        # FIXME consider this or a similar case of multiple assignment
        #   for example `(a, b) == c` might be a useful construct and be Pythonic, despite
        #   making little sense mathematically
        with self.assertRaisesRegex(ValueError, "multiple or no possible result values"):
            E = expressive.Expressive("a[i] + b[i] = x")

    def test_data_sensible(self):
        data = {
            "a": numpy.arange(1000, dtype="int64"),
        }

        E = expressive.Expressive("r = a**2 + b")

        # passed data doesn't match the signature
        with self.assertRaisesRegex(KeyError, r"b"):
            E.build(data)

        # works when the full data is available
        data["b"] = numpy.arange(1000, dtype="int64")
        E.build(data)
        self.assertEqual(len(E.signatures_mapper), 1)

        # passing r is optional and creates a new signature
        data["r"] = numpy.zeros(1000, dtype="int64")
        E.build(data)
        self.assertEqual(len(E.signatures_mapper), 2)

    def test_name_and_data_only(self):
        E = expressive.Expressive("a**2 + b", name_result="r")

        data = {
            "a": numpy.arange(1000, dtype="int64"),
            "b": numpy.arange(1000, dtype="int64"),
            "r": numpy.zeros(1000, dtype="int64"),
        }
        E.build(data)
        E(data)

    def test_name_and_not_data(self):
        """ fail when missing details about the result array """
        E = expressive.Expressive("a**2 + b", name_result="r")

        data = {
            "a": numpy.arange(1000, dtype="int64"),
            "b": numpy.arange(1000, dtype="int64"),
        }
        E.build(data)
        result = E(data)

        self.assertTrue(numpy.array_equal(
            numpy.arange(1000)**2 + numpy.arange(1000),
            result,
        ))

    def test_mismatched_dtypes(self):
        """ fail when missing details about the result array """
        E = expressive.Expressive("a**2 + b", name_result="r")

        data = {
            "a": numpy.arange(1000, dtype="int64"),
            "b": numpy.arange(1000, dtype="int64"),
            "r": numpy.zeros(1000, dtype="int64"),
        }
        with self.assertRaisesRegex(ValueError, r"mismatched.*int64.*float64"):
            E.build(data, dtype_result="float64")
        with self.assertRaisesRegex(ValueError, r"mismatched.*int64.*int32"):
            E.build(data, dtype_result="int32")

    def test_indxed_rhs(self):
        E = expressive.Expressive("a[i]**2", name_result="r")
        data = {
            "a": numpy.arange(1000, dtype="int64"),
        }
        E.build(data)

    def test_result_array_fill(self):
        """ should fill, not re-create result array """
        E = expressive.Expressive("a[i]**2 + b[i]", name_result="r")
        data = {
            "a": numpy.arange(100, dtype="int64"),
            "b": numpy.arange(100, dtype="int64"),
            "r": numpy.zeros(100, dtype="int64")
        }

        E.build(data)

        # now create new data and build with it, passing result
        data = {
            "a": numpy.arange(1000, dtype="int64"),
            "b": numpy.arange(1000, dtype="int64"),
            "r": numpy.zeros(1000, dtype="int64")
        }
        ref = data["r"]

        result = E(data)
        # reference hasn't been swapped out
        self.assertTrue(ref is result)
        self.assertTrue(data["r"] is ref)
        # check the contents too
        self.assertEqual(data["r"][0], 0)
        self.assertEqual(data["r"][1], 2)
        self.assertEqual(data["r"][2], 6)
        self.assertEqual(data["r"][999], 999**2 + 999)

    def test_self_reference(self):
        """ passing result with data works without explicitly naming it
            however, the user should be warned when they might not mean to do so
        """

        # warn only when the name (symbol) literally 'result' is
        #  - not in LHS, but given in RHS
        #  - not indexed (IndexedBase)
        #  - not named as name_result

        # equivalent instances to compare
        expressive.Expressive("result ** 2", name_result="result")
        expressive.Expressive("result = result ** 2")
        expressive.Expressive("result[i] ** 2")  # functionally equivalent (results), but internally uses the indexed path
        expressive.Expressive("result[i+1] ** 2")  # actually offset by 1 too, but shouldn't raise!
        # ensure warn occurs and then try it!
        with must_warn(r"^symbol 'result' in RHS refers to result array, but not indexed or passed as name_result$"):
            E = expressive.Expressive("result ** 2")

        data = {
            "result": numpy.arange(1000, dtype="int64"),
        }
        ref = data["result"]
        E.build(data)
        result = E(data)

        # reference hasn't been swapped out
        self.assertTrue(ref is result)
        self.assertTrue(data["result"] is ref)
        # check the contents too
        self.assertEqual(data["result"][0], 0)
        self.assertEqual(data["result"][1], 1)
        self.assertEqual(data["result"][2], 4)
        self.assertEqual(data["result"][999], 999**2)

    def test_complex_dtype(self):
        data = {
            "a": numpy.array([1j for _ in range(1000)]),
        }
        E = expressive.Expressive("E**(a * pi)")  # famous e^(i*pi)=-1
        E.build(data)
        result = E(data)
        self.assertTrue(numpy.allclose(result, [-1]*1000))

    # TODO test difference between passing data with and without result array
    #   and whether it should complain about signature mismatch (it should and be clear!)
    #   consider adding to autobuild too


class TestGuess_dtype(unittest.TestCase):

    def test_simple(self):
        data = {
            "a": numpy.array([1,2,3], dtype="uint8"),
        }
        E = expressive.Expressive("2*a")
        dt = expressive.dtype_result_guess(E._expr_sympy, data)
        self.assertEqual(dt, "uint32")

        # exclusively float32
        data = {
            "a": numpy.array([1,2,3], dtype="float32"),
            "b": numpy.array([1,2,3], dtype="float32"),
        }
        E = expressive.Expressive("a * b")
        dt = expressive.dtype_result_guess(E._expr_sympy, data)
        self.assertEqual(dt, "float32")

        # choose wider when present
        data = {
            "a": numpy.array([1,2,3], dtype="float32"),
            "b": numpy.array([1,2,3], dtype="float64"),
        }
        E = expressive.Expressive("a * b")
        dt = expressive.dtype_result_guess(E._expr_sympy, data)
        self.assertEqual(dt, "float64")

    def test_empty_inputs(self):
        E = expressive.Expressive("2*a")
        with self.assertRaisesRegex(ValueError, r"no data"):
            expressive.dtype_result_guess(E._expr_sympy, data={})

    def test_floating_point_operators(self):
        # most floating point math results in float64
        data = {
            "a": numpy.array([1,2,3], dtype="int32"),
        }
        E = expressive.Expressive("log(a)")
        dt = expressive.dtype_result_guess(E._expr_sympy, data)
        self.assertEqual(dt, "float64")

    def test_float_promote(self):
        # presence of a wider value causes promotion to float64
        data = {
            "a": numpy.array([1,2,3], dtype="int64"),
            "b": numpy.array([1,2,3], dtype="float32"),
        }
        E = expressive.Expressive("a * b")
        dt = expressive.dtype_result_guess(E._expr_sympy, data)
        self.assertEqual(dt, "float64")

        # most values are promoted to float64 regardless of width
        data = {
            "a": numpy.array([1,2,3], dtype="int32"),
        }
        E = expressive.Expressive("log(a)")
        dt = expressive.dtype_result_guess(E._expr_sympy, data)
        self.assertEqual(dt, "float64")

        # while small values are promoted to float32
        data = {
            "a": numpy.array([1,2,3], dtype="int8"),
            "b": numpy.array([1,2,3], dtype="int8"),
        }
        E = expressive.Expressive("log(a) + b")
        dt = expressive.dtype_result_guess(E._expr_sympy, data)
        self.assertEqual(dt, "float32")

    def test_bad(self):
        # boolean is currently unsupported
        data = {
            "a": numpy.array([1,2,3], dtype="bool"),
            "b": numpy.array([1,2,3], dtype="bool"),
        }
        E = expressive.Expressive("a * b")
        with self.assertRaisesRegex(TypeError, r"unsupported.*bool"):
            expressive.dtype_result_guess(E._expr_sympy, data=data)

        # mixed integer signs
        data = {
            "a": numpy.array([1,2,3], dtype="int32"),
            "b": numpy.array([1,2,3], dtype="uint32"),
        }
        E = expressive.Expressive("a * b")
        with self.assertRaisesRegex(TypeError, r"mixed int and uint"):
            expressive.dtype_result_guess(E._expr_sympy, data=data)

    def test_complex_dtype(self):
        data = {
            "a": numpy.array([1,2,3], dtype="complex64"),
            "b": numpy.array([1,2,3], dtype="float32"),
        }
        E = expressive.Expressive("a * b")
        dt = expressive.dtype_result_guess(E._expr_sympy, data)
        self.assertEqual(dt, "complex128")

    def test_complex_dtype_mixed(self):

        data = {
            "a": numpy.array([1,2,3], dtype="complex64"),
            "b": numpy.array([1,2,3], dtype="float64"),
            "c": numpy.array([1,2,3], dtype="complex128"),
        }
        E = expressive.Expressive("a * b * c")
        dt = expressive.dtype_result_guess(E._expr_sympy, data)
        # self.assertEqual(dt, "complex64")  # FUTURE support more narrow type
        self.assertEqual(dt, "complex128")

    # FUTURE overflowing test(s) [ISSUE 46]


class Testdata_cleanup(unittest.TestCase):

    def test_simple(self):
        with self.assertRaisesRegex(ValueError, r"no data"):
            expressive.data_cleanup({})

        data = ["a"]
        with self.assertRaisesRegex(TypeError, r"dict of NumPy arrays, .*list"):
            expressive.data_cleanup(data)

        data = {"a": [1]}
        with self.assertRaisesRegex(TypeError, r"dict of NumPy arrays, .*list"):
            expressive.data_cleanup(data)

        data = {"a": numpy.array([1,2,3], dtype="bool")}
        with self.assertRaisesRegex(TypeError, r"unsupported dtype .*bool"):
            expressive.data_cleanup(data)

    def test_uneven_arrays(self):
        # see also TestSingleValues for non-vector data
        data = {
            "a": numpy.arange(100, dtype="int64"),
            "b": numpy.arange( 99, dtype="int64"),
        }
        with self.assertRaisesRegex(ValueError, r"uneven data lengths .*99"):
            expressive.data_cleanup(data)

    def test_ndims_parse(self):
        # see also TestSingleValues for non-vector data
        data = {
            "a": numpy.array([[1, 2], [3, 4]], dtype="int64"),
        }
        with self.assertRaisesRegex(ValueError, r"^only single values or 1-dimensional arrays are allowed, but got a:2$"):
            expressive.data_cleanup(data)

    def test_complex_dtype(self):
        data = {
            "aj": numpy.array([1j for _ in range(1000)], dtype="complex64"),
        }
        data = expressive.data_cleanup(data)
        self.assertEqual(data["aj"].dtype, numpy.dtype("complex64"))  # no change

        data = {
            "a": 1j,
            "b": numpy.arange(1000, dtype="complex64"),
            "c": numpy.arange(1000),
        }
        data = expressive.data_cleanup(data)
        self.assertEqual(data["a"].dtype, numpy.dtype("complex128"))  # automatic coerce
        self.assertEqual(data["b"].dtype, numpy.dtype("complex64"))


class TestSingleValues(unittest.TestCase):

    def test_simple(self):
        data = {
            "a": numpy.arange(100, dtype="int64"),
            "b": 5,
        }

        result_expected = numpy.arange(100) + 5
        E = expressive.Expressive("a + b")
        E.build(data)
        result = E(data)
        self.assertTrue(numpy.array_equal(result_expected, result))

    def test_indexed_mixed(self):
        data = {
            "a": numpy.arange(100, dtype="int64"),
            "b": 5,
        }

        result_expected = numpy.arange(100) + 5
        E = expressive.Expressive("a[i] + b")
        E.build(data)
        result = E(data)
        self.assertTrue(numpy.array_equal(result_expected, result))

    def test_all_single_values(self):
        data = {
            "a": 1,
            "b": 2,
        }
        E = expressive.Expressive("a + b")

        # returning a single (ndim==0) value is possible, but I'm not it's useful to implement
        # for now the result length can't be determined, so raise
        msg = re.escape("only single values passed (ndim=0), no arrays (at least a result array must be passed to determine length)")
        with self.assertRaisesRegex(ValueError, "^" + msg + r".*$"):
            E.build(data)

        # however, passing an array works
        data["result"] = numpy.zeros(100)

        # build and get the result
        E.build(data)
        result = E(data)
        self.assertTrue(len(result) == 100)
        self.assertTrue(set(result) == {3})  # all 3

    def test_lhs_indexed_all_single(self):
        data = {
            "a": 1,
            "b": 2,
            "r": numpy.zeros(100),  # avoids ValueError, see TestEqualityExtract.test_indexed
        }
        # only LHS is indexed, so the indexed template is used
        E = expressive.Expressive("r[i] = a + b")

        E.build(data)
        result = E(data)
        self.assertTrue(len(result) == 100)
        self.assertTrue(set(result) == {3})  # all 3

    def test_lhs_indexed_all_single_advanced(self):
        data = {
            "a": 10,
            "b": 5,
            "r": numpy.zeros(100),  # avoids ValueError, see TestEqualityExtract.test_indexed
        }
        #
        E = expressive.Expressive("r[i] = a ** 2 + a ** b")
        E.build(data)
        result = E(data)
        self.assertTrue(len(result) == 100)
        self.assertTrue(set(result) == {10**2 + 10**5})  # all 10^5

    def test_lhs_indexed_mixed_single_array(self):
        data = {
            "a": numpy.full(100, 1, dtype="int64"),
            "b": 2,
            "r": numpy.zeros(100),
        }

        # when nothing is indexed, mixing single values and arrays is fine
        E = expressive.Expressive("r = a + b")
        E.build(data)
        result = E(data)
        self.assertTrue(len(result) == 100)
        self.assertTrue(set(result) == {3})  # all 3

        # however, when LHS is indexed, unindexed symbols are treated as single values
        E = expressive.Expressive("r[i] = a + b")
        with self.assertRaisesRegex(ValueError, re.escape("'a' is not indexed, but passed array (ndim=1) value in data")):
            E.build(data)
        # or simply when the data doesn't match up
        E = expressive.Expressive("a[i] + b[i]")
        with self.assertRaisesRegex(ValueError, re.escape("'b' is indexed, but is a single (ndim=0) value in data")):
            E.build(data)  # data doesn't match indexing in instance


class Test_input_cleanup(unittest.TestCase):

    def test_simple(self):
        # whitespace removal
        expr_string = expressive.string_expr_cleanup("a * b")
        self.assertEqual(expr_string, "a*b")

    def test_bad(self):
        # junk inputs
        with self.assertRaisesRegex(ValueError, "string"):
            expressive.string_expr_cleanup(None)
        with self.assertRaisesRegex(ValueError, "string"):
            expressive.string_expr_cleanup(3)

        # empty string
        with self.assertRaisesRegex(ValueError, "no content"):
            expressive.string_expr_cleanup("")
        with self.assertRaisesRegex(ValueError, "no content"):
            expressive.string_expr_cleanup(" ")

        # SymPy expr doesn't need these cleanups (already parsed)
        E = expressive.Expressive("a*b")
        expr = E._expr_sympy
        with self.assertRaisesRegex(ValueError, "string"):
            expressive.string_expr_cleanup(expr)

    def test_adjacent_to_mul(self):
        # simple coefficient
        expr_string = expressive.string_expr_cleanup("2x")
        self.assertEqual(expr_string, "2*x")

        # directly adjacent to the parenthesis
        expr_string = expressive.string_expr_cleanup("2(x+1)")
        self.assertEqual(expr_string, "2*(x+1)")

        # FIXME should this warn? (see notes in expressive.py)
        expr_string = expressive.string_expr_cleanup("(x+1)2")
        self.assertEqual(expr_string, "(x+1)*2")

        expr_string = expressive.string_expr_cleanup("(a+1)2 - 3(b+2)")
        self.assertEqual(expr_string, "(a+1)*2-3*(b+2)")

        # multiple cleanups
        expr_string = expressive.string_expr_cleanup("1 + 2x - 7y")
        self.assertEqual(expr_string, "1+2*x-7*y")

        # handle function or symbol
        expr_string = expressive.string_expr_cleanup("3cos(2x + pi)")
        self.assertEqual(expr_string, "3*cos(2*x+pi)")

        # function with number in name
        expr_string = expressive.string_expr_cleanup("2x + 3 - log2(n)")
        self.assertEqual(expr_string, "2*x+3-log2(n)")

        # symbol with a number in the name
        expr_string = expressive.string_expr_cleanup("t0 + t2")
        self.assertEqual(expr_string, "t0+t2")

        # more complicated parses
        # FIXME consider detecting and raise/warn for very confusing parses

        expr_string = expressive.string_expr_cleanup("log2(2value3)")
        self.assertEqual(expr_string, "log2(2*value3)")

        expr_string = expressive.string_expr_cleanup("log2(a)3(b+2)4atan(c)")
        self.assertEqual(expr_string, "log2(a)*3*(b+2)*4*atan(c)")

    def test_pow_xor(self):
        expr_string = expressive.string_expr_cleanup("2^x")
        self.assertEqual(expr_string, "2**x")

    def test_fraction(self):
        expr_string = "1/2x"

        # fails without cleanup
        with self.assertRaises(SyntaxError):
            expressive.string_expr_to_sympy(expr_string)

        # division (actually Mul internally)
        expr_string = expressive.string_expr_cleanup(expr_string)
        self.assertEqual(expr_string, "1/2*x")

        # parsed result should be consistent across inputs
        self.assertEqual(
            expressive.string_expr_to_sympy(expr_string),
            expressive.string_expr_to_sympy("""Mul(Rational(1, 2), Symbol("x"))"""),
            expressive.string_expr_to_sympy("x/2"),
        )

    def test_equality_rewrite(self):
        """ test equality parsing to Eq
            basic workflow
                A = B
                A == B
                Eq(A, B)
        """
        # basic parse
        expr_string = expressive.string_expr_cleanup("r = x**2")
        self.assertEqual(expr_string, "Eq(r, x**2)")

        # more advanced parse
        expr_string = expressive.string_expr_cleanup("r[i] = 3^5b")
        self.assertEqual(expr_string, "Eq(r[i], 3**5*b)")

        # trivial single vs double equality
        expr_string = expressive.string_expr_cleanup("foo = bar")
        self.assertEqual(expr_string, "Eq(foo, bar)")
        expr_string = expressive.string_expr_cleanup("foo == bar")
        self.assertEqual(expr_string, "Eq(foo, bar)")

        # fail for multiple equalities
        with self.assertRaisesRegex(SyntaxError, re.escape("only 1 equivalence (==) can be provided, but parsed 2")):
            expressive.string_expr_cleanup("foo = bar = baz")

        # fail for inequalities
        with self.assertRaisesRegex(ValueError, r"inequality is not supported"):
            expressive.string_expr_cleanup("x <= y")

    def test_complex_types_parse(self):
        # TODO consider if case like `a4I` or `a4j` should parse `a*4` out with imaginary constant hint
        # expr_string = expressive.string_expr_cleanup("a4I + 2b")  # [ISSUE 69]
        expr_string = expressive.string_expr_cleanup("4a*I + 2b")
        self.assertEqual(expr_string, "4*a*I+2*b")

        expr_sympy, symbols, syms_idx, syms_result = expressive.string_expr_to_sympy(expr_string)

        # ensure it really read SymPy's imaginary `I`
        self.assertTrue(sympy.I in expr_sympy.atoms())

        # extract symbols and compare to constructed expr
        a, b = symbols["a"], symbols["b"]
        self.assertEqual(
            expr_sympy.rhs,
            4 * a * sympy.I + 2 * b,
        )


class TestRelativeOffsets(unittest.TestCase):

    def test_paired(self):
        data = {
            "a": numpy.arange(100, dtype="int64"),
            "b": numpy.arange(100, dtype="int64"),
            "c": numpy.arange(100, dtype="int64"),
        }
        E = expressive.Expressive("a[i+1] + b[i-1] + c[i]")
        E.build(data)

        # give it a spin
        data = {
            "a": numpy.arange(10000, dtype="int64"),
            "b": numpy.arange(10000, dtype="int64"),
            "c": numpy.arange(10000, dtype="int64"),
        }
        result = E(data)

        # cherry-pick test cases
        self.assertEqual(result[   1],    0 +    2 +    1)
        self.assertEqual(result[5000], 4999 + 5000 + 5001)
        self.assertEqual(result[9000], 8999 + 9000 + 9001)
        # slice and verify whole array
        self.assertTrue(numpy.array_equal(
            result[1:-1],
            (numpy.arange(10000) * 3)[1:-1],
        ))

    def test_bad(self):
        # multiple indexers
        with self.assertRaisesRegex(ValueError, r"only a single Idx is supported, but got:"):
            E = expressive.Expressive("a[i] + b[n]")


class TestAutoBuilding(unittest.TestCase):

    def test_autobuild_basic(self):
        data = {
            "a": numpy.array(range(100_000), dtype="int32"),
            "b": numpy.array(range(100_000), dtype="int32"),
        }

        result_expected = numpy.array(range(100_000), dtype="int32") * 2

        E = expressive.Expressive("a + b", allow_autobuild=True)
        self.assertTrue(len(E.signatures_mapper) == 0)  # no cached builds

        with must_warn(r"autobuild took [\d\.]+s .*prefer \.build\("):
            result = E(data)

        self.assertTrue(numpy.array_equal(result_expected, result))
        self.assertTrue(len(E.signatures_mapper) == 1)  # exactly one build

    def test_autobuild_error(self):
        data = {
            "a": numpy.arange(100, dtype="int32"),
        }
        E = expressive.Expressive("a**2")
        with self.assertRaisesRegex(KeyError, r"no matching signature for data: use .build"):
            result = E(data)


class TestExprDisplay(unittest.TestCase):

    def test_version(self):
        """ version property must be available and sensible """
        self.assertTrue(re.match(r"\d+\.\d+\.\d+", expressive.__version__))

    def test_display_basic(self):
        E = expressive.Expressive("a + b")
        self.assertTrue("a + b" in str(E))
        self.assertTrue("build_signatures=0" in repr(E))
        self.assertTrue("allow_autobuild=False" in repr(E))


class TestVerify(unittest.TestCase):

    def test_verify(self):
        data = {
            "a": numpy.array([1, 2, 3, 4], dtype="int64"),
            "b": numpy.array([5, 6, 7, 8], dtype="int64"),
        }
        E = expressive.Expressive("a + b")
        E.build(data, verify=True)

    def test_verify_indexed(self):
        # skips the SymPy .subs() branch
        data = {
            "a": numpy.array([1, 2, 3, 4], dtype="int64"),
            "b": numpy.array([5, 6, 7, 8], dtype="int64"),
        }
        E = expressive.Expressive("a[i] + b[i+1]")
        self.assertEqual(len(E._indexers), 1)
        self.assertEqual(E._indexers["i"], [0, 1])
        E.build(data, verify=True)

    # FUTURE test for exclusively single values (no arrays), raises `data_cleanup({'a':1,'b':1})` for now [ISSUE 53]

    def test_log0(self):
        """ generally a big reason to implement this functionality """
        data = {
            "a": numpy.arange(10, dtype="int64"),  # NOTE begins with 0
        }
        E = expressive.Expressive("log(a)")        # not valid at 0
        # make it rain
        with must_warn(r"^divide by zero encountered in log$"):   # Python(NumPy)
            E.build(data, verify=True)

    def test_too_much_data(self):
        data = {
            "a": numpy.arange(5000, dtype="int64"),
            "b": numpy.arange(5000, dtype="int64"),
        }
        E = expressive.Expressive("a + b")
        with must_warn(r"^excessive data may be negatively impacting start time: {'a': 5000, 'b': 5000}$"):
            E.build(data, verify=True)

    def test_NaN(self):
        data = {
            "a": numpy.array([0, 1, 2, 3, numpy.nan, 4, 5], dtype="float32"),  # NOTE begins with 0
        }
        E = expressive.Expressive("log(a)")        # not valid at 0
        # make it rain
        # FIXME this should also warn about nan in general [ISSUE 59]
        with must_warn([
            "some data in a is NaN",
            r"^divide by zero encountered in log$"  # Python(NumPy)
        ]):
            E.build(data, verify=True)

        # sympy.nan are expressly rejected because object isn't a valid dtype
        # FUTURE consider making this error clearer, though `dtypdtype=object` can actually be anything
        data = {
            "a": numpy.array([0, 1, 2, 3, sympy.nan, 4, 5])
        }
        with self.assertRaisesRegex(TypeError, re.escape("unsupported dtype (a:object)")):
            E.build(data, verify=True)


    def test_None(self):
        data = {
            "a": numpy.array([0, 1, 2, 3, None, 4, 5], dtype="float32"),  # NOTE begins with 0
        }
        E = expressive.Expressive("log(a)")        # not valid at 0
        # make it rain
        with must_warn([
            "some data in a is NaN",
            r"^divide by zero encountered in log$"  # Python(NumPy)
        ]):
            E.build(data, verify=True)

    def test_warnings(self):
        data = {
            "a": numpy.array([1, 2, 3, 4], dtype="int32"),
        }

        # extremely simple functions which will act as if they return an array
        def fn_python(a):
            return [1, 2, 3, 4]

        def fn_compiled(a):  # still behaves like the compiled function for this purpose
            return [1, 2, 3, 1]

        # TODO is it better to mock warnings.warn?
        with must_warn([
            re.escape("verify took a long time python:0.00s, compiled:20.00s"),
            re.escape("compiled function (20000000000ns) may be slower than direct NumPy (10000ns) (data lengths {'a': 4})"),
        ]):
            with unittest.mock.patch("expressive.time") as mock:
                m = unittest.mock.Mock()
                m.side_effect = [0, 10_000, 0, 20 * 1_000_000_000]  # 20s in nanoseconds
                mock.process_time_ns = m
                with self.assertRaisesRegex(RuntimeError, re.escape("not allclose(False) when comparing between NumPy and compiled function")):
                    result = expressive.verify_cmp(
                        data,
                        None,  # ignored when indexers are present
                        fn_python,
                        fn_compiled,
                        {None: [0, 0]},  # impossible, but contentful indexers to skip SymPy expr
                    )

    def test_auto_verify(self):
        """ test if verify_cmp() is called automatically for varying lengths of data """
        E = expressive.Expressive("a + b")

        for datalen, verify_expected in (
            (10,  True),
            (100, False),
        ):
            with unittest.mock.patch("expressive.verify_cmp") as mock:
                mock.side_effect = [(None, None)]  # just needs to be unpackable
                data = {
                    "a": numpy.arange(datalen, dtype="int64"),
                    "b": numpy.arange(datalen, dtype="int64"),
                }
                E.build(data)
                self.assertEqual(mock.called, verify_expected)

    def test_complex_result(self):
        data = {
            "a": 1j,  # possibly better in TestSingleValues
            "b": numpy.arange(100),
        }
        E = expressive.Expressive("(a + b)*3")
        E.build(data, verify=True)  # shouldn't raise

        data = {
            "a": 1j,
            "b": numpy.arange(10000),
        }
        result = E(data)

        self.assertEqual(result.dtype, numpy.dtype("complex128"))
        self.assertEqual(result[1], 3+3j)
        self.assertEqual(result[2], 6+3j)
        self.assertEqual(result[-1], (9999*3)+3j)


class TestIPythonREPR(unittest.TestCase):
    """ unit tests for special IPython display method(s)
        currently only _repr_html_() is supported

        refer to Notes block of `IPython.display.display` docs
        https://ipython.readthedocs.io/en/latest/api/generated/IPython.display.html#IPython.display.display
    """

    def test_repr_basic(self):
        """ html output is as-expected """
        E = expressive.Expressive("x**3 - 2y")
        block = E._repr_html_()
        self.assertTrue("Expressive(Eq(result, x**3 - 2*y))" in block)
        self.assertTrue(r"\(\displaystyle result = x^{3} - 2 y\)" in block)  # transformed by mathjax client-side
        self.assertTrue("&lt;build_signatures=0,allow_autobuild=False&gt;</li>" in block)  # NOTE repr unstable

    def test_demote_warn(self):
        """ patch SymPy LaTeX repr to trigger warning path """
        E = expressive.Expressive("x**3 - 2y")
        with must_warn(r"^unexpected expr format .*: mocked LaTeX repr result$"):
            with unittest.mock.patch("sympy.Eq._repr_latex_") as mock:  # outer atom is always Eq
                mock.side_effect = ["mocked LaTeX repr result"]
                block = E._repr_html_()  # triggers warn path as not wrapped "$expr$" or "$$expr$$" (transformed to "\(expr\)")
                self.assertTrue("html" not in block)  # returns basic repr instead of html
                self.assertEqual(block, repr(E))

    # FUTURE render javascript
    # FUTURE ensure integrity check works (assures .js from jsdelivr)


class TestMany(unittest.TestCase):
    # integration test, not a unittest packed in here
    # maybe move to examples
    # generally this sort of test is bad because it provides too much coverage
    # for too little test
    # also it can take a long time (and quite long if generating really big arrays)

    def test_many(self):
        # size = 2**(32-1) - 1  # fill int32
        size = 10**7
        data = {              # lots of data created
            "a": numpy.arange(size, dtype="int32"),
            "b": numpy.arange(size, dtype="int64"),
            "c": 5,                                  # single value to be coerced
            "r": numpy.arange(size, dtype="int32"),  # force type and content
        }

        # indexed function
        # chain from .build()
        # 3log is converted to 3*log
        E = expressive.Expressive("r[i-2] = c*r[i+5] + a[i-3]**1.1 + 3log(b[i-2])", allow_autobuild=True).build(data)
        # print(data["r"][:10])

        # doesn't generate a warning (already built above)
        time_start = time.time()  # should be fast!
        result = E(data)
        runtime = time.time() - time_start
        self.assertTrue(runtime < 5)

        # the first and last 5 values remained the same
        self.assertEqual(data["r"][0], 0)
        self.assertEqual(data["r"][-1], size-1)
        self.assertEqual(data["r"][-2], size-2)
        self.assertEqual(data["r"][-3], size-3)
        self.assertEqual(data["r"][-4], size-4)
        self.assertEqual(data["r"][-5], size-5)
        # self.assertEqual(data["r"][-6], size-6)

        # inner values are filled       c   r     a     b
        self.assertEqual(data["r"][ 1], 5 * (8) + (0) + int(3 * numpy.log(1)))  # written at `i=3`
        self.assertEqual(data["r"][ 2], 5 * (9) + (1) + int(3 * numpy.log(2)))  # written at `i=4`
        # self.assertEqual(data["r"][-8], 5 * (size-6+5) + int((size-6+3)**1.1) + int(3 * numpy.log(size-7)))  # written at `i=size-6`
        # self.assertEqual(data["r"][-8], 5 * (size-6+5) + int((size-6-3)**1.1) + int(3 * numpy.log(size-6+2)))  # written at `i=size-6`
        a = data["r"][-8]
        b = 5 * (size-6+5) + int((size-6-3)**1.1) + 3 * int(numpy.log(size-6+2))  # written at `i=size-6`
        c = 5 * (size-6+5) +    ((size-6-3)**1.1) + 3 *    (numpy.log(size-6+2))  # floating-point version
        # print(f"a: {a}, b: {b}, c: {c}")
        self.assertTrue(numpy.isclose(a, b, c))

        # result and data["r"] really are the same
        self.assertTrue(data["r"] is result)  # they are really the same array
        self.assertEqual(data["r"][10], result[10])

        # generates a new build and promotes the resulting type
        self.assertEqual(result.dtype, numpy.dtype("int32"))  # from data["r"] forces int32
        del data["r"]  # drop r from data to force detect and create
        E.build(data)
        result = E(data)
        self.assertEqual(result.dtype, numpy.dtype("float64"))  # discovered dtype


if __name__ == "__main__":
     r = unittest.main(exit=False)
     if not r.result.wasSuccessful():
        sys.exit("some tests failed")  # pragma nocover
