# Lezgi Numbers Python Package

**A Python package for converting numbers to Lezgi numerals and back.**

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Converting Numbers to Lezgi Numerals](#converting-numbers-to-lezgi-numerals)
  - [Converting Lezgi Numerals to Numbers](#converting-lezgi-numerals-to-numbers)
- [Examples](#examples)
- [Testing](#testing)

## Introduction

This Python package provides functions to convert integer numbers to their textual representation in the Lezgi language and vice versa. It supports numbers up to 9007199254740991 and down to -9007199254740991, which are the maximum safe integers in JavaScript/Typescript ([the original language of the package](https://github.com/LekiTech/lezgi-numbers)).

The Lezgi language is a Northeast Caucasian language spoken by the Lezgin people in southern Dagestan and northern Azerbaijan.

## Features

- Number to Lezgi Numeral Conversion: Convert integers to Lezgi text representation.
- Lezgi Numeral to Number Conversion: Convert Lezgi numerals back to integers.
- Supports Negative Numbers: Handles both positive and negative integers.
- Large Number Support: Works with very large numbers up to nonillion (1e30).
- Unit Tests Included: Comprehensive tests to ensure correctness.

## Installation

To install the package, you can either download it from pypi:

```bash
pip install lezgi-numbers
```

Or clone this repository and install it using `pip` in editable mode.

```bash
git clone https://github.com/LekiTech/lezgi-numbers-py.git
cd lezgi-numbers-py
pip install -e .
```

## Usage
The package provides two main functions:

- `numToLezgi(num: int) -> str`: Converts an integer to its Lezgi text representation.
- `lezgiToNum(lezgi_num_str: str) -> int`: Converts a Lezgi numeral string to an integer.

First, import the necessary functions:

```python
from lezgi_numbers import numToLezgi, lezgiToNum
```

### Converting Numbers to Lezgi Numerals
```python
number = 1986
lezgi_numeral = numToLezgi(number)
print(lezgi_numeral)  # Output: 'агъзурни кIуьд вишни кьудкъанни ругуд'
```

### Converting Lezgi Numerals to Numbers

```python
lezgi_num_str = 'кьве агъзурни къанни кьуд'
number = lezgiToNum(lezgi_num_str)
print(number)  # Output: 2024
```

## Examples

Here are additional examples demonstrating the usage of the package.

### Example 1: Converting Number to Lezgi Numeral

```python
from lezgi_numbers import numToLezgi

print(numToLezgi(700))          # Output: 'ирид виш'
print(numToLezgi(1001))         # Output: 'агъзурни сад'
print(numToLezgi(-102))         # Output: 'минус вишни кьвед'
print(numToLezgi(2024))         # Output: 'кьве агъзурни къанни кьуд'
```

### Example 2: Converting Lezgi Numeral to Number

```python
from lezgi_numbers import lezgiToNum

print(lezgiToNum('вишни кьвед'))           # Output: 102
print(lezgiToNum('минус вишни кьвед'))     # Output: -102
print(lezgiToNum('кьве агъзурни къанни кьуд'))  # Output: 2024
```

### Example 3: Handling Large Numbers

```python
from lezgi_numbers import numToLezgi, lezgiToNum

large_number = 9007199254740991
lezgi_numeral = numToLezgi(large_number)
print(lezgi_numeral)
# Output: 'кIуьд квадриллионни ирид триллионни вишни кьудкъанни цIекIуьд миллиардни кьве вишни яхцIурни цIикьуд миллионни ирид вишни яхцIур агъзурни кIуьд вишни кьудкъанни цIусад'

converted_back = lezgiToNum(lezgi_numeral)
print(converted_back)  # Output: 9007199254740991
```

## Testing

The package includes unit tests to verify the correctness of the conversion functions.

### Running Tests

```bash
python -m unittest discover -s tests  
```

### Test Coverage

The tests cover:

- Correct conversion of numbers to Lezgi numerals.
- Correct conversion of Lezgi numerals to numbers.
- Handling of invalid inputs (e.g., non-integer numbers, invalid strings).
- Edge cases, including large numbers and negative numbers.
