from dataclasses import dataclass
from typing import Union

from pricecypher.enums import TestStatus


@dataclass(frozen=True)
class ElementTestResult:
    """
    Defines a test result of one element of a test.

    key (str): Unique identifier of this element test result (lowercase kebab-case), e.g. 'nr_null'.

    label (str): Label of the element test result for displaying purposes, e.g. 'NULL values'.

    value (str or int): The formatted value of the element test result, e.g. '23,734'.
    """
    key: str
    label: str
    value: Union[str, int]


@dataclass(frozen=True)
class ElementTest:
    """
    Defines the test of a single element of a test case, having one or multiple test results. For instance, one element
    could be a single column of one test that checks the number of NULL values for all columns of a dataset.

    label (str): Label of this single element of the test for displaying purposes, e.g. the name of the column.

    message (str): Short message that describes the test results for displaying purposes, e.g. 'The column has no NULL'.

    results (list[ElementTestResult]): The test results for this single element. For instance, a count of the total
                                       number of values, a count of the NULL values, and the percentage of NULL values.
    """
    label: str
    message: str
    status: TestStatus
    results: list[ElementTestResult]


@dataclass(frozen=True)
class TestResult:
    """
    Defines one test case with overall status result and multiple test results.

    key (str): Unique identifier of the test (lowercase kebab-case), e.g. 'expect_no_null_values'.

    label (str): Label of the test for displaying purposes, e.g. 'Expect no NULL values in the dataset.'

    coverage (str): Short description to display what is covered by the test, e.g. '10 columns' or 'All transactions'.

    status (TestStatus): Overall status of the test.

    element_label (str): Label to display what the different test elements represent, e.g. 'Column' or 'Dataset'.

    elements (list[ElementTest]): Test results of all the different elements in the test. For instance, the test
                                  results of all the columns of the dataset.
    """
    key: str
    label: str
    coverage: str
    status: TestStatus
    element_label: str
    elements: list[ElementTest]


@dataclass(frozen=True)
class TestSuite:
    """
    One quality test script always produces one TestSuite response. A test suite (usually) contains multiple test cases.
    It also defines a category that can be used by front-ends to group multiple test suites together.

    label (str): Label of the test suite, e.g. 'Completeness'.

    key (str): Unique identifier of the test suite (lowercase kebab-case), e.g. 'basic-completeness'.

    category_key (str): Unique identifier of the category this test suite is in, e.g. 'basic' or 'advanced'.

    test_results (list[TestResult]): All test cases of this test suite, with their results.
    """
    label: str
    key: str
    category_key: str
    test_results: list[TestResult]
