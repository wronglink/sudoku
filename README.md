# Sudoku extensible solver

### Installation

```bash
$ git clone https://github.com/wronglink/sudoku.git
$ pip install -e sudoku
```

### Usage

```bash
$ python -m sudoku data/input.txt data/output.json --display
Puzzle:
┌─────┬─────┬─────┐
│ 53_ │ _7_ │ ___ │
│ 6__ │ 195 │ ___ │
│ _98 │ ___ │ _6_ │
├─────┼─────┼─────┤
│ 8__ │ _6_ │ __3 │
│ 4__ │ 8_3 │ __1 │
│ 7__ │ _2_ │ __6 │
├─────┼─────┼─────┤
│ _6_ │ ___ │ 28_ │
│ ___ │ 419 │ __5 │
│ ___ │ _8_ │ _79 │
└─────┴─────┴─────┘
Solution:
┌─────┬─────┬─────┐
│ 534 │ 678 │ 912 │
│ 672 │ 195 │ 348 │
│ 198 │ 342 │ 567 │
├─────┼─────┼─────┤
│ 859 │ 761 │ 423 │
│ 426 │ 853 │ 791 │
│ 713 │ 924 │ 856 │
├─────┼─────┼─────┤
│ 961 │ 537 │ 284 │
│ 287 │ 419 │ 635 │
│ 345 │ 286 │ 179 │
└─────┴─────┴─────┘
```

### Input formats

1. Text format with `.txt` extension:

    ```
    53_  _7_  ___
    6__  195  ___
    _98  ___  _6_

    8__  _6_  __3
    4__  8_3  __1
    7__  _2_  __6

    _6_  ___  28_
    ___  419  __5
    ___  _8_  _79
    ```

    1. All space-like characters are omitted.
    2. Characters `.`, `_`, `*` are used as blank space and need to be filled with solution numbers.

2. JSON format with `.json` extension:

    ```
    [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    ```

    1. Array of arrays. Every internal array represents Sudoku row.
    2. Empty cells are indicated by 0.


### Testing

```bash
# To run regular tests use:
$ py.test

# To run benchmarking tool use:
$ py.test --runbenchmark -v
```
