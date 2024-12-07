# sugarplum

[![PyPI - Version](https://img.shields.io/pypi/v/sugarplum.svg)](https://pypi.org/project/sugarplum)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sugarplum.svg)](https://pypi.org/project/sugarplum)

-----

Sugarplum is a library for managing inputs (both regular and test inputs) for Advent of
Code puzzles.


## Why sugarplum

The creators of Advent of Code have asked that inputs not be shared, including test
inputs (see the links below). However, it can be helpful to not have to download
the puzzle inputs each time switching computers, or to have the test inputs stored for
running unit tests. That is where sugarplum comes in. It allows you to have a seperate 
directory, most likely a private repo, where these are stored, but easily retrieve them
for use in puzzle solutions and tests.

https://www.reddit.com/r/adventofcode/wiki/faqs/copyright/inputs/

https://www.reddit.com/r/adventofcode/comments/zh2hk0/comment/iznly9w/?context=3

## Installation

```console
pip install sugarplum
```

## Usage

The environment variable "SUGARPLUM_BASE_PATH" must be set to the base path of the 
directory where the inputs reside. At the moment, sugarplum is opinionated, expecting a
specific file structure and file names. It expects the directory structure to be one of
YYYY/DD.

Within each day's directory, for puzzle inputs it expects them to live in a file named 
data.in. For test inputs, they can either live in test-{part-number}.in with the result
in test-{part-number}.out or, for parametrized inputs, test-{part-number}{letter}.in for 
inputs and test-{part-number}{letter}.out for the results.

For example:

    2015/01/data.in
    2015/01/test-1.in
    2015/01/test-1.out
    2015/01/test-2.in
    2015/01/test-2.out

Or

    2015/01/data.in
    2015/01/test-1a.in
    2015/01/test-1a.out
    2015/01/test-1b.in
    2015/01/test-1b.out
    2015/01/test-2a.in
    2015/01/test-2b.in
    2015/01/test-2a.out
    2015/01/test-2b.out

An example set of input and output files for tests for a challenge that is to add up all
values in a list would look like:

**test-1.in**

```
1
2
3
4
5
```

**test-1.out**

```
15
```

### Getting puzzle input

Call get_input passing the year and day.

```
from sugarplum import get_input

get_input(2015, 16)
```

### Getting test data

Call get_test_data passing the year, day, and part number.

```
from sugarplum import get_test_data

part_1_test_data = get_test_data(2015, 24, 1)
part_2_test_data = get_test_data(2015, 24, 2)
```