"""
Benchmarking tools.
"""
from __future__ import annotations

# Python Modules
import logging
import time

from inspect import signature
from itertools import product
from typing import Any, Callable, Iterable, Literal, Optional, TypeVar, cast, get_args

# 3rd Party Modules
import numpy as np
import pandas as pd
import plotnine as pn

from icontract import require
from numpy.typing import ArrayLike
from scipy.stats import ttest_ind
from tqdm.auto import tqdm  # This works better in Jupyter notebooks than 'from tqdm import tqdm'

from rwskit.collections_ import is_generator, is_iterable

# Project Modules

log = logging.getLogger(__name__)


__all__ = [
    "TimeUnit",
    "AggregationFunctionName",
    "AggregationFunction",
    "BenchmarkSortValue",
    "BenchmarkResult",
    "BenchmarkRunner",
    "change_time_unit",
    "get_time_unit_abbreviation",
    "validate_call_signature",
]

T = TypeVar("T", bool, int, float, str)
I = TypeVar("I")

TimeUnit = Literal[
    "seconds", "s",
    "milliseconds", "ms",
    "microseconds", "us", "µs",
    "nanoseconds", "ns"
]
"""
The supported units of time.
"""

AggregationFunctionName = Literal["min", "max", "mean", "median", "sum"]
"""
The names of the supported aggregation functions.
"""

AggregationFunction = Callable[[ArrayLike], float]
"""
An aggregation function is a callable that takes an array-like object and
returns a single float.
"""

BenchmarkSortValue = Literal["min", "mean", "function"]
"""
The supported values for sorting the ``BenchmarkResults`` when represented
as a string.
"""

PlotTheme = Literal[
    "theme_538",
    "theme_bw",
    "theme_classic",
    "theme_dark",
    "theme_gray",
    "theme_grey",
    "theme_light",
    "theme_linedraw",
    "theme_matplotlib",
    "theme_minimal",
    "theme_seaborn",
    "theme_tufte",
    "theme_void",
    "theme_xkcd"
]

_time_conversion_factors = {
    "seconds"       : 1   ,
    "milliseconds"  : 1e-3,
    "microseconds"  : 1e-6,
    "nanoseconds"   : 1e-9,
}

_time_unit_abbreviation_to_name: dict[TimeUnit, TimeUnit] = {
    "s": "seconds",
    "ms": "milliseconds",
    "us": "microseconds",
    "µs": "microseconds",
    "ns": "nanoseconds",
    "seconds": "seconds",
    "milliseconds": "milliseconds",
    "microseconds": "microseconds",
    "nanoseconds": "nanoseconds"
}

_time_unit_name_to_abbreviation = {
    "seconds": "s",
    "milliseconds": "ms",
    "microseconds": "µs",
    "nanoseconds": "ns",
}

_valid_themes = {
    pn.theme_538,
    pn.theme_bw,
    pn.theme_classic,
    pn.theme_dark,
    pn.theme_gray,
    pn.theme_grey,
    pn.theme_light,
    pn.theme_linedraw,
    pn.theme_matplotlib,
    pn.theme_minimal,
    pn.theme_seaborn,
    pn.theme_tufte,
    pn.theme_void,
    pn.theme_xkcd,
}

_theme_name_to_theme = {theme.__name__: theme for theme in _valid_themes}


@require(
    lambda name: name in _time_unit_abbreviation_to_name.keys(),
    f"Unsupported time unit. Must be one of: {_time_unit_abbreviation_to_name.keys()}"
)
def get_time_unit_abbreviation(name: TimeUnit) -> TimeUnit:
    """
    Get the time unit abbreviation from the given string.

    Parameters
    ----------
    name : str
        The name or abbreviation of a supported time unit.

    Returns
    -------
    str
        The abbreviation of the time unit specified by ``name``.

    Raises
    ------
    icontract.errors.ViolationError
        If the ``name`` is not a supported :data:`TimeUnit`.

    """
    return _time_unit_abbreviation_to_name.get(name, name)


@require(lambda from_unit: from_unit in get_args(TimeUnit), "Invalid time unit")
@require(lambda to_unit: to_unit in get_args(TimeUnit), "Invalid time unit")
def change_time_unit(value: int | float, from_unit: TimeUnit, to_unit: TimeUnit) -> float:
    """
    Change the unit of time of a given ``value`` currently in the ``from_unit``
    unit to a value in the ``to_unit`` unit.

    Parameters
    ----------
    value : int or float
        The current time value.
    from_unit : TimeUnit
        The unit of the current value.
    to_unit : TimeUnit
        The unit to change the value into.

    Returns
    -------
    float
        Return the equivalent value in the new time unit ``to_unit``
    """
    seconds = value * _time_conversion_factors[from_unit]

    return seconds / _time_conversion_factors[to_unit]


def validate_call_signature(
        fn1: Callable[..., Any],
        fn2: Callable[..., Any],
        strict: bool = False
) -> bool:
    """
    Check that the two functions take the same parameters.

    Parameters
    ----------
    fn1 : Callable[..., Any]
        The first function to compare.
    fn2 : Callable[..., Any]
        The second function to compare.
    strict : bool, default = False
        If ``True`` the signatures must match exactly, including whether
        defaults are present and their values. Otherwise, they are considered
        equal if the number and types of all parameters are the same.

    Returns
    -------
    bool
        True if the functions take the same number and type of parameters.
    """
    params1 = signature(fn1).parameters.values()
    params2 = signature(fn2).parameters.values()

    if len(params1) != len(params2):
        return False

    if strict:
        return all(p1 == p2 for p1, p2 in zip(params1, params2))

    return all(
        p1.name == p2.name and p1.annotation == p2.annotation
        for p1, p2 in zip(params1, params2)
    )


# region BenchmarkRunner Input Validation
def _are_setup_fn_and_functions_compatible(
        benchmark_space: dict[str, list[T]],
        setup_fn: Optional[Callable],
        functions: Iterable[Callable]
) -> bool:
    if setup_fn is None:
        return True

    functions = list(functions.values()) if isinstance(functions, dict) else list(functions)
    kwargs = {k: v[0] for k, v in benchmark_space.items()}
    setup_fn_output = setup_fn(**kwargs)

    if not isinstance(setup_fn_output, dict):
        return False

    parameter_names = [p.name for p in signature(functions[0]).parameters.values()]

    if len(parameter_names) != len(setup_fn_output):
        return False

    return all(k in parameter_names for k in setup_fn_output.keys())


def _are_benchmark_space_and_functions_compatible(
        setup_fn: Optional[Callable],
        benchmark_space: dict[str, list[T]],
        functions: Iterable[callable]
) -> bool:
    if setup_fn is not None:
        return True

    functions = list(functions.values()) if isinstance(functions, dict) else list(functions)

    if not bool(functions):
        # We shouldn't get here if the decorators are ordered properly
        return False

    parameter_names = [p.name for p in signature(functions[0]).parameters.values()]

    if len(parameter_names) != len(benchmark_space):
        return False

    return all(k in parameter_names for k in benchmark_space)


def _is_space_distinct_from_run_label(benchmark_space: dict[str, list[T]], run_label: str) -> bool:
    return not any(k == run_label for k in benchmark_space.keys())


def _functions_have_same_call_signatures(functions: Iterable[callable]) -> bool:
    functions = list(functions.values()) if isinstance(functions, dict) else list(functions)
    if len(functions) < 1:
        return False

    fn1 = functions[0]

    return all(validate_call_signature(fn1, fn2) for fn2 in functions[1:])


def _functions_have_proper_type(functions: Iterable[callable]) -> bool:
    if isinstance(functions, dict):
        return all(isinstance(k, str) and callable(v) for k, v in functions.items())

    return all(callable(f) for f in functions)


def _are_benchmark_space_and_setup_fn_compatible(
        benchmark_space: dict[str, list[T]],
        setup_fn: Optional[Callable]
) -> bool:
    # There's nothing to check
    if setup_fn is None:
        return True

    parameter_names = [p.name for p in signature(setup_fn).parameters.values()]

    # They need the same number of arguments
    if len(parameter_names) != len(benchmark_space):
        return False

    return all(k in parameter_names for k in benchmark_space)


def _benchmark_space_has_valid_keys(benchmark_space: dict[str, list[T]]) -> bool:
    return not any(k in ("min", "max", "mean", "std") for k in benchmark_space)


def _benchmark_space_is_dict_of_lists(benchmark_space: dict[str, list[T]]) -> bool:
    is_dict_of_lists = all(
        isinstance(k, str) and isinstance(v, list)
        for k, v in benchmark_space.items()
    )
    is_non_empty = bool(benchmark_space) and any(bool(v) for v in benchmark_space.values())
    has_valid_values = all(
        isinstance(v, (bool, int, float, str))
        for lov in benchmark_space.values()
        for v in lov
    )

    return is_dict_of_lists and is_non_empty and has_valid_values


def _is_valid_float_format(float_fmt: str) -> bool:
    try:
        format(123.45, float_fmt)
    except (ValueError, TypeError):
        return False
    else:
        return True
# endregion BenchmarkRunner Input Validation


class BenchmarkRunner:
    """
    A class for comparing the execution time of multiple functions
    """

    _aggregate_function_lookup = {
        "min": np.min,
        "max": np.max,
        "mean": np.mean,
        "median": np.median,
        "sum": np.sum
    }

    # Decorators are evaluated from bottom to top. So more complex contracts,
    # especially ones that depend on previous checks being performed, must be
    # defined first even though it is more intuitive to have the contracts
    # provided in the same order as the __init__ arguments.
    @require(
        _are_setup_fn_and_functions_compatible,
        "'setup_fn' should return a dict suitable to use as **kwargs for the test functions."
    )
    @require(
        _are_benchmark_space_and_functions_compatible,
        "The 'benchmark_space' keys must match the 'functions' params when 'setup_fn' is None."
    )
    @require(
        _is_space_distinct_from_run_label,
        "The 'benchmark_space' can't have a key that is equal to the 'run_label'."
    )
    @require(
        _functions_have_same_call_signatures,
        "All the functions must have the same call signature."
    )
    @require(
        _functions_have_proper_type,
        "'functions' must be a dict[str, callable] or an iterable of callables."
    )
    @require(
        lambda functions: bool(list(functions)),
        "'functions' must be non-empty."
    )
    @require(
        lambda functions: not is_generator(functions),
        "'functions' cannot be a generator."
    )
    @require(
        lambda functions: is_iterable(functions),
        "'functions' must be iterable."
    )
    @require(
        _are_benchmark_space_and_setup_fn_compatible,
        "The 'benchmark_space' keys must match the 'setup_fn' params if 'setup_fn' is given."
    )
    @require(
        lambda setup_fn: callable(setup_fn) if setup_fn is not None else True,
        "'setup_fn' must be callable."
    )
    @require(
        _benchmark_space_has_valid_keys,
        f"'benchmark_space' cannot contain the keys: [min, max, mean, std]"
    )
    @require(
        _benchmark_space_is_dict_of_lists,
        "'benchmark_space' must be a non-empty dict[str, list[bool, int, float, str]]."
    )
    @require(
        lambda n_runs: n_runs > 0,
        "There must be at least one run."
    )
    @require(
        lambda n_tests: n_tests > 0,
        "There must be at least one test")
    @require(
        lambda n_warm_ups: n_warm_ups >= 0,
        "There can't be negative warm ups.")
    @require(
        lambda time_unit: time_unit in get_args(TimeUnit),
        f"Invalid 'time_unit' must be one of: {get_args(TimeUnit)}"
    )
    @require(
        lambda test_agg_fn: test_agg_fn in get_args(AggregationFunctionName),
        f"Invalid 'test_agg_fn' function name. It must be one of: {get_args(AggregationFunctionName)}"
    )
    @require(
        _is_valid_float_format,
        "Invalid 'float_fmt'"
    )
    @require(
        lambda sort_by: sort_by in get_args(BenchmarkSortValue),
        f"Invalid 'sort_by' value. It must be one of: {get_args(BenchmarkSortValue)}."
    )
    def __init__(
            self,
            functions: Iterable[Callable] | dict[str, Callable],
            benchmark_space: dict[str, list[T]],
            setup_fn: Optional[Callable] = None,
            use_single_setup: bool = True,
            n_runs: int = 10,
            n_tests: int = 2,
            n_warm_ups: int = 1,
            time_unit: TimeUnit = cast(TimeUnit, "s"),
            test_agg_fn: AggregationFunctionName = "min",
            run_label: str = "run",
            show_progress: bool = False,
            verbose: bool = True,
            float_fmt: str = "0.4e",
            sort_by: BenchmarkSortValue = "min",
            test_significance: bool = True
    ):
        """
        A class for profiling a set of functions based on one or mor criteria.

        The high level view of the benchmarking process is as follows.
        For every combination of parameters in the ``benchmark_space`` a
        sub-benchmark will be run.
        There are 2 nested execution loops for each sub-benchmark.
        The innermost loop runs each function on the current data ``n_tests``
        number of times and aggregates the results using the ``test_agg_fn``.
        The same data is always used for this loop no matter what. The outer
        loop will run this process ``n_runs`` times. If ``use_single_setup``
        is ``True`` then the setup function will only be called once and
        will be used for all the runs. If it is ``False`` the setup
        function will be called for every run. The execution times for all
        runs will be stored in a Pandas DataFrame that can be retrieved after
        calling the benchmark.

        .. note::
            ``min``, ``max``, ``mean``, ``std`` cannot be used as keys in
            the ``benchmark_space``.

        .. note::
            ``functions`` must be an iterable, but cannot be a generator.

        .. note::
            The first parameter in the ``benchmark_space`` is always used
            as the x-axis for :meth:`BenchmarkResult.plot`.

        Parameters
        ----------
        functions : list[BenchmarkFunction]
            A list of functions to benchmark or a dictionary that maps a label
            to a benchmark function.
        benchmark_space : dict[str, list[T]]
            The space of values to benchmark over. A benchmark will be
            executed for each combination of values obtained from the
            dictionary. The combinations are formed by taking the Cartesian
            product taking one value from each list in the dictionary.
            The names of the keys of this dictionary must either be the names
            of keyword arguments of the ``setup_fn``, or keyword arguments of
            the benchmark functions if no ``setup_fn`` is provided. Only
            ``bool``, ``int``, ``float``, and ``str`` values are supported.
        setup_fn : SetupFunction
            A function that initializes data to be passed to the benchmark
            ``functions``. If ``None``, the values from ``setup_args`` will
            be passed directly to each function in ``functions``.
        use_single_setup : bool, default = True
            For functions that are guaranteed to be deterministic no matter
            what the input is, this should be ``True``. However, if the
            function is non-deterministic or the performance might depend
            on how the data is initialized, this should be ``False``.
        n_runs : int
            The number of execution tests to run.
        n_tests : int
            The number times to run each function in a single test.
        n_warm_ups : int
            The number of tests to run before recording the timing data.
        test_agg_fn : {'min', 'max', 'mean', 'median', 'sum'}
            The function to use for aggregating individual test results within
            a run.
        run_label : str
            The column label in the resulting Pandas ``DataFrame`` that
            indicates the run number for the given execution times.
        show_progress : bool = False
            Show progress bars while running the benchmark.
        verbose : bool, default = True
            Print the full results and summary statistics to ``stdout``
            when complete.
        float_fmt : str
            The format used to print floating point values to a string.
        sort_by : str {min, mean, function}
            When ``verbose=True`` this will determine how the results are
            sorted (either by the min run time, max run time or by the
            function name).
        test_significance: bool, default = False
            If ``True``, test if the difference in run times are different
            between all pairs of models.

        Notes
        -----

        **Deterministic Function and Deterministic Data**

        If your algorithm is deterministic and is not influenced at all
        by the content of the data, only its size, then I would suggest the
        following parameters:

        * ``use_single_setup = True``: Use the same data for all the runs
          on the current setup parameters.
        * ``n_runs > 1``: Run it at least a few times per parameter set
          to make sure there weren't any anomalies biasing the results.
        * ``n_tests = 1``: You should not need to run multiple tests here.

        **Deterministic Function and Non-Deterministic Data**

        If your function is deterministic (the sequence of execution is always
        the same), but could be influenced by the content of the data I would
        suggest the following parameters:

        * ``setup_fn != None``: The setup function should return different
          data each run (of the same size)
        * ``use_single_setup = False``: Run the setup function to generate
          new data on each run.
        * ``n_tests > 1``: Run the function on the same data a few times
          in case there was an anomaly, which could bias the result.
        * ``n_runs > 1``: Run the function on multiple different data
          sets to estimate how much variability is expected due to the
          makeup of the data.
        * ``test_agg_fn = 'min'``: Since the function should execute
          the same way on the same data, the `min` should be the most
          informative.

        **Non-Deterministic Function**

        If the function itself is non-deterministic you probably want something
        similar to the deterministic case with non-deterministic data. In
        this case however, it is probably pointless to set ``n_tests > 1``
        and you should just increase ``n_runs`` to get better overall estimates.

        Examples
        --------

        .. code-block:: python

            >>> import time
            >>> sort_setup_fn = (
            ...    lambda array_size, dtype, unique_values:
            ...        np.random.randint(unique_values, size=array_size).astype(dtype)
            ... )

            >>> b = BenchmarkRunner(functions={"fn1": lambda a: time.sleep(0.01),
            ...                                "fn2": lambda a: time.sleep(0.02)},
            ...                     benchmark_space={"array_size": [100, 10000],
            ...                                      "dtype": ["U", "int"],
            ...                                      "unique_values": [10, 100, 1000]},
            ...                     setup_fn=sort_setup_fn
            ...                     time_unit="ms"
            ...                     float_fmt="0.3f")

            >>> b()
            function  array_size  unique_values    min   mean    std
            --------------------------------------------------------
                 fn1         100             10  1.040  1.053  0.008
                 fn2         100             10  5.057  5.058  0.001
            --------------------------------------------------------
                 fn1         100            100  1.053  1.056  0.002
                 fn2         100            100  5.057  5.058  0.001
            --------------------------------------------------------
                 fn1         100           1000  1.056  1.057  0.000
                 fn2         100           1000  5.058  5.058  0.000
            --------------------------------------------------------
                 fn1       10000             10  1.056  1.057  0.000
                 fn2       10000             10  5.058  5.059  0.000
            --------------------------------------------------------
                 fn1       10000            100  1.056  1.057  0.000
                 fn2       10000            100  5.058  5.064  0.009
            --------------------------------------------------------
                 fn1       10000           1000  1.056  1.057  0.001
                 fn2       10000           1000  5.063  5.066  0.002



    """
        self._check_for_configuration_problems(use_single_setup, setup_fn, n_runs)

        self.functions = self._normalize_functions(functions)
        self.benchmark_space = benchmark_space
        self.setup_fn = setup_fn or self._passthrough_setup_args
        self.use_single_setup = use_single_setup
        self.n_runs = n_runs
        self.n_tests = n_tests
        self.n_warm_ups = n_warm_ups
        self.test_agg_fn = self._aggregate_function_lookup[test_agg_fn]
        self.run_label = run_label
        self.show_progress = show_progress
        self.verbose = verbose
        self.time_unit: TimeUnit = cast(TimeUnit, get_time_unit_abbreviation(time_unit))
        self.float_fmt = float_fmt
        self.sort_by = sort_by
        self.test_significance = test_significance

    def __call__(self) -> BenchmarkResult:
        """Runs the benchmark.

        Returns
        -------
        BenchmarkResult

        """
        return self.run()

    def run(self) -> BenchmarkResult:
        """Runs the benchmark.

        Returns
        -------
        BenchmarkResult
        """
        # Create the DataFrame to store the results
        results = self._initialize_data_frame()

        # Create a generator to iterate through all possible combinations of
        # the benchmark space.
        parameter_values = product(*self.benchmark_space.values())

        # Set up the parameter space loop with optional progress indicators
        parameter_progress = self._progress(
            parameter_values,
            total=np.prod([len(x) for x in self.benchmark_space.values()]),
            position=0,
            unit="parameters"
        )

        # Loop through all combinations
        for parameter_values in parameter_progress:
            # Create the setup_fn kwargs
            setup_kwargs = {k: v for k, v in zip(self.benchmark_space.keys(), parameter_values)}

            # Get the function arguments here if we only want to generate
            # them once for all runs of this parameter set (i.e., pure deterministic functions).
            function_args = self.setup_fn(**setup_kwargs) if self.use_single_setup else None

            # Set up the run loop with optional progress indicators
            run_progress = self._progress(
                range(1, self.n_runs + 1),
                position=1,
                leave=False,
                unit="runs"
            )

            for run_num in run_progress:
                self._do_run(results, run_num, setup_kwargs, function_args)

        significance_results = self._run_ttest(results) if self.test_significance else None

        result = BenchmarkResult(
            results,
            significance_results,
            self.benchmark_space,
            self.float_fmt,
            self.sort_by,
            self.run_label,
            self.time_unit,
        )

        if self.verbose:
            print(result)

        return result

    @staticmethod
    def _check_for_configuration_problems(
            use_single_setup: bool,
            setup_fn: Optional[Callable],
            n_runs: int
    ):
        if not use_single_setup and not setup_fn:
            log.warning(
                f"Setting 'single_setup' to 'False' implies the performance of the functions "
                f"may be non-deterministic. However, no 'setup_fn' was defined so be sure that "
                f"the only non-determinism is coming from the functions themselves."
            )
        if not use_single_setup and n_runs == 1:
            log.warning(
                f"Setting 'single_setup' to 'False' implies the performance of the functions "
                f"may be non-deterministic. However, 'n_runs' is set to 1, which will not."
            )

    @staticmethod
    def _normalize_functions(
            functions: list[Callable] | dict[str, Callable]
    ) -> dict[str, Callable]:
        return functions if isinstance(functions, dict) else {f.__name__: f for f in functions}

    @staticmethod
    def _passthrough_setup_args(**kwargs: T) -> dict[str, T]:
        return kwargs

    @staticmethod
    def _identity(x: Any) -> Any:
        return x

    def _set_default_run_agg_fn(self) -> AggregationFunction:
        if self.use_single_setup:
            return self._aggregate_function_lookup["min"]

        return self._aggregate_function_lookup["mean"]

    def _progress(self, values: Iterable[I], **tqdm_kwargs):
        return tqdm(values, disable=not self.show_progress, **tqdm_kwargs)

    def _initialize_data_frame(self) -> pd.DataFrame:
        index_map = {self.run_label: list(range(1, self.n_runs + 1))} | self.benchmark_space

        multi_index = pd.MultiIndex.from_product(
            list(index_map.values()),
            names=index_map.keys()
        )

        return pd.DataFrame(
            index=multi_index,
            columns=list(self.functions.keys()),
            dtype=np.float64
        )

    def _do_run(
            self,
            results: pd.DataFrame,
            run_num: int,
            setup_args: dict[str, T],
            function_args: Optional[dict[str, T]],
    ):
        # If we didn't set the function arguments already (i.e., use_single_setup=False)
        # we need to set them here.
        function_args = function_args or self.setup_fn(**setup_args)

        for function_name, function in self.functions.items():
            row_index = (run_num,) + tuple(setup_args.values())
            column_name = function_name
            results.loc[row_index, column_name] = self._do_test(function, function_args)

    def _do_test(self, function: Callable, function_args: dict[str, Any]) -> float:
        test_times = [
            self._time_function(function, function_args)
            for _ in range(self.n_warm_ups + self.n_tests)
        ]

        return self.test_agg_fn(test_times[self.n_warm_ups:])

    def _time_function(self, function: Callable, function_args: list[Any] | dict[str, Any]) -> float:
        start = time.perf_counter_ns()
        function(**function_args)
        return change_time_unit(time.perf_counter_ns() - start, "nanoseconds", self.time_unit)

    def _run_ttest(self, df: pd.DataFrame) -> pd.DataFrame:
        benchmark_space = list(self.benchmark_space)
        functions = list(self.functions.keys())

        def _pairwise_ttest(group):
            tt_df = pd.DataFrame({
                f1: {f2: ttest_ind(group[f1], group[f2]).pvalue for f2 in functions}
                for f1 in functions
            })
            tt_df.index.name = "function"
            return tt_df

        return df.groupby(benchmark_space).apply(_pairwise_ttest).reset_index()


class BenchmarkResult:
    """A class for managing the results output by a :class:`BenchmarkRunner`.
    """

    def __init__(
            self,
            results: pd.DataFrame,
            significance_results: Optional[pd.DataFrame],
            benchmark_space: dict[str, list[T]],
            float_fmt: str = "0.4e",
            sort_by: BenchmarkSortValue = "min",
            run_label: str = "run",
            time_unit: TimeUnit = "s"
    ):
        """A class for managing the results output by a :class:`BenchmarkRunner`.

        .. note::
            This class is not intended to be instantiated directly.

        Parameters
        ----------
        results : DataFrame
            The results DataFrame obtained by a :class:`BenchmarkRunner`.
        significance_results : DataFrame
            Pairwise t-test results.
        benchmark_space : dict[string, list[T]]
            The parameters used to benchmark the functions.
        float_fmt : str
            A valid format string to use for floating point numbers.
        sort_by : str {min, mean}
            The summary statistic to sort the results by when represented
            as a string.
        run_label : str
            The label used to indicate the run number.
        time_unit : TimeUnit
            The original time unit used to benchmark the results.
        """
        self._results = results
        self._significance_results = significance_results
        self._benchmark_space = benchmark_space
        self._float_fmt = float_fmt
        self._sort_by = sort_by
        self._run_label = run_label
        self._time_unit = time_unit
        self._function_names = set(results.columns)

    def __repr__(self) -> str:
        """The full pandas :class:`pandas.DataFrame` containing all the runs as a string.

        Returns
        -------
        str
            The full benchmark results as a string.

        """
        return self._results.to_string()

    def __str__(self) -> str:
        """Returns a table of the summary statistics of the benchmark results as a string.

        Returns
        -------
        str
            The summary statistics of the benchmark results as a string.

        """
        summary = self.summary()
        groups = summary.groupby(list(self.benchmark_space))
        widths = self._get_max_column_widths(summary)
        header = self._stringify_header(summary.columns, widths)
        header_size = len(header)

        lines = ["=" * header_size]
        lines += [header]
        for i, (key, group) in enumerate(groups):
            separator = "=" if i == 0 else "-"
            lines.append(separator * header_size)
            lines.extend(self._stringify_group(group, widths))

        return "\n".join(lines)

    @property
    def benchmark_space(self) -> dict[str, list[T]]:
        """Return the parameters used to benchmark the functions.

        Returns
        -------
        dict[str, list[T]]
            The parameters used to produce these results.

        """
        return self._benchmark_space.copy()

    @require(lambda as_time_unit: as_time_unit in get_args(TimeUnit) if as_time_unit else True)
    def results(self, wide: bool = True, as_time_unit: Optional[TimeUnit] = None) -> pd.DataFrame:
        """Get a pandas ``DataFrame`` containing the results.

        Parameters
        ----------
        as_time_unit : TimeUnit, optional
            Return the results in this time unit instead of the one used
            during the benchmark.
        wide : bool, default = True
            If ``True`` return the results in the default wide format, which
            is easier to read. Otherwise, return the results in long format,
            which can be easier to use for plotting.

        Returns
        -------
        DataFrame
            The DataFrame containing the results, either in wide or long format.

        """
        results = self._results.copy(deep=True)

        if as_time_unit is not None:
            results = results.map(lambda t: change_time_unit(t, self._time_unit, as_time_unit))  # noqa

        if wide:
            return results

        return pd.melt(
            results.reset_index(),
            id_vars=[self._run_label] + list(self.benchmark_space.keys()),
            var_name="function",
            value_name="time"
        )

    @property
    def significance_results(self) -> pd.DataFrame:
        """Return the results of the significance tests as a :class:`pandas.DataFrame`.

        Returns
        -------
        DataFrame
            The results of the significance tests as a :class:`pandas.DataFrame`.

        """
        return self._significance_results.copy(deep=True)

    @require(lambda as_time_unit: as_time_unit in get_args(TimeUnit) if as_time_unit else True)
    def summary(self, wide: bool = True, as_time_unit: Optional[TimeUnit] = None) -> pd.DataFrame:
        """The summary statistics of the benchmark results.

        Parameters
        ----------
        wide : bool, default = True
            If ``True``, return the results in wide format, otherwise, return
            the results in long format.
        as_time_unit : TimeUnit, optional
            Return the results in this time unit instead of the one used during
            the benchmark.

        Returns
        -------
        pd.DataFrame
            The DataFrame with the summary statistics.

        """
        long_results = self.results(wide=False, as_time_unit=as_time_unit)
        group_by = ["function"] + list(self.benchmark_space)
        summary = long_results.groupby(group_by).agg({"time": ["min", "max", "mean", "std"]})
        summary.columns = summary.columns = [c2 or c1 for c1, c2 in summary.columns]
        summary.reset_index(inplace=True)

        summary = self._add_significance_to_summary(summary)

        if wide:
            return summary

        return summary.melt(
            id_vars=["function"] + list(self.benchmark_space),
            var_name="agg",
            value_name="value"
        )

    # noinspection PyTypeChecker
    @require(
        lambda self, functions:
            all(f in self._function_names for f in functions)
            if functions else
            True,
        "At least one of the functions provided is not in the benchmark results."
    )
    def plot(
            self,
            x_label: str = None,
            use_stat: Literal["min", "mean"] = "min",
            functions: Iterable[str] = None,
            show_points: bool = False,
            show_ribbon: bool = False,
            free_y: bool = False,
            theme_name: PlotTheme = None,
            figure_size: Optional[tuple[int, int]] = None,
            as_time_unit: Optional[TimeUnit] = None
    ) -> pn.ggplot:
        """Create and return a `ggplot <https://plotnine.org/reference/ggplot.html#plotnine.ggplot>`__
        object that visualizes the benchmark results.

        .. note::
            Use ``show` or ``save``` on the resulting object to render or save it.

        Parameters
        ----------
        x_label : str, optional
            Label the `x-axis` with this value, if given. Otherwise, the first
            key in the ``benchmark_space`` will be used.
        use_stat : str {min, mean}
            Which stat to plot.
        functions: Iterable[str], optional
            If defined, limit the plot to these functions.
        show_points : bool, default = False
            Show each individual run as a point on the graph.
        show_ribbon : bool, default = False
            If ``True``, include a ribbon that encompasses the minimum and
            maximum value over all the runs in a group.
        free_y : bool, default = False
            If ``True`` and the ``benchmark_space`` includes more than 1
            parameter, the y-axis is not constrained to be the same for each
            resulting plot.
        theme_name : PlotTheme, optional
            The name of a theme to style your plot with, otherwise, it will
            use the default theme.
        figure_size : tuple[int, int], optional,
            Override the size of the resulting figure. If not specified and
            there are more than one ``benchmark_space`` parameters a heuristic
            is used to try to ensure each subgraph will be legible.
        as_time_unit : TimeUnit, optional
            Display the results in this time unit instead of the one used
            during the benchmarking.

        Returns
        -------
        plotnine.ggplot
            The plot object.

        """
        results = self.results(wide=False, as_time_unit=as_time_unit)
        summary = self.summary(as_time_unit=as_time_unit)
        summary["lb"] = summary["mean"] - summary["std"]
        summary["ub"] = summary["mean"] + summary["std"]

        if functions is not None:
            results = results[results["function"].isin(functions)]
            summary = summary[summary["function"].isin(functions)]

        search_space_names = list(self._benchmark_space.keys())
        x = search_space_names[0]
        theme = _theme_name_to_theme.get(theme_name)

        plot = pn.ggplot(summary)

        if show_points:
            plot += pn.geom_point(
                data=results,
                mapping=pn.aes(x=x, y="time", color="function")
            )

        plot += pn.geom_line(
            mapping=pn.aes(
                x=x,
                y=use_stat,
                color="function"
            )
        )

        if show_ribbon:
            plot += pn.geom_ribbon(
                mapping=pn.aes(
                    x=x,
                    ymin="lb",
                    ymax="ub",
                    fill="function",
                ),
                inherit_aes=False,
                alpha=0.60
            )

            plot += pn.geom_ribbon(
                mapping=pn.aes(
                    x=x,
                    ymin="min",
                    ymax="max",
                    fill="function",
                ),
                inherit_aes=False,
                alpha=0.20
            )

        if x_label is not None:
            plot += pn.xlab(x_label)

        plot += pn.ylab(
            f"Time [{_time_unit_name_to_abbreviation[self._time_unit]}]"
        )

        scales = "free_y" if free_y else None
        if len(search_space_names) == 2:
            plot += pn.facet_grid(
                rows=search_space_names[1],
                scales=scales,
                labeller="label_both"
            )
        elif len(search_space_names) == 3 and not free_y:
            plot += pn.facet_grid(
                rows=search_space_names[1],
                cols=search_space_names[2],
                labeller="label_both",
                scales=scales
            )
        elif len(search_space_names) >= 3:
            ncol = len(self.benchmark_space[search_space_names[1]])
            plot += pn.facet_wrap(
                search_space_names[1:],
                ncol=ncol,
                scales=scales,
                labeller="label_both",
                dir="v"
            )

        if theme is not None:
            plot += theme()

        plot += pn.theme(
            figure_size=self._estimate_figure_size(figure_size),
        )

        return plot

    def _estimate_figure_size(
            self, figure_size: Optional[tuple[int, int]]
    ) -> Optional[tuple[int, int]]:
        if figure_size is not None:
            return figure_size

        if len(self._benchmark_space) < 3:
            return None

        search_space_values = list(self._benchmark_space.values())[1:]
        total_plots = np.prod([len(v) for v in search_space_values])

        sub_plot_width, sub_plot_height = 5, 4

        n_cols = len(search_space_values[0])
        n_rows = np.ceil(total_plots / n_cols)

        return sub_plot_width * n_cols, sub_plot_height * n_rows

    def _add_significance_to_summary(self, df: pd.DataFrame) -> pd.DataFrame:
        if self._significance_results is None:
            return df

        benchmark_space = list(self.benchmark_space)

        def _make_condition(g: pd.DataFrame, col: str) -> str:
            value = g[col].iloc[0]
            return f"{col} == '{value}'" if isinstance(value, str) else f"{col} == {value}"

        def _function(group: pd.DataFrame):
            group = group.sort_values("mean")
            base_conditions = [_make_condition(group, col) for col in benchmark_space]
            p_values = []
            for i in range(len(group.index) - 1):
                fn1 = group.iloc[i, 0]
                fn2 = group.iloc[i + 1, 0]
                group_conditions = base_conditions + [f"function == '{fn1}'"]
                query_expr = " and ".join(group_conditions)
                query_row = self._significance_results.query(query_expr)
                p_values.append(query_row[fn2].iloc[0])
            p_values.append(np.nan)

            group["p_value"] = p_values

            return group

        groups = df.groupby(benchmark_space)
        result = groups.apply(_function).reset_index(drop=True)
        columns = ["function", "p_value"] + benchmark_space + ["max", "min", "mean", "std"]
        result = result[columns]

        return result
        # return df


    def _get_max_column_widths(self, df: pd.DataFrame) -> dict[str, int]:
        header_widths = {h: len(h) for h in df.columns}
        data_widths = df.map(lambda x: len(self._stringify_value(x))).max().to_dict()

        return {h: max(hw, data_widths[h]) for h, hw in header_widths.items()}

    def _stringify_value(self, value: Any, width: Optional[int] = None) -> str:
        if isinstance(value, (float, np.floating)):
            raw = "-" if np.isnan(value) else  "{:{}}".format(value, self._float_fmt)
            return self._stringify_value(raw, width) if width else raw

        return "{:>{}}".format(str(value), width) if width else str(value)

    def _stringify_header(self, columns: Iterable[str], widths: dict[str, int]) -> str:
        return "  ".join(["{:>{}}".format(h, f"{widths[h]}s") for h in columns])

    def _stringify_group(self, group: pd.DataFrame, widths: dict[str, int]) -> list[str]:
        sorted_group = group.sort_values(by=self._sort_by)
        return [self._stringify_row(row, widths) for _, row in sorted_group.iterrows()]

    def _stringify_row(self, row: pd.Series, widths: dict[str, int]) -> str:
        return "  ".join(self._stringify_value(v, widths[str(i)]) for i, v in row.items())
