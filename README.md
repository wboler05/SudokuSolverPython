# Sudoku Solver

I wanted to challenge myself to write a Sudoku solver in python using some set theory.  It's not the most neat code, but it gets the problem accomplished. 

## Setup

Just have the latest Python 3.  No special librarires are used. 

## Execution

### Input File
You're going to need a text file of the starting solution prompt to the Sudoku puzzle.  The code takes an input as follows:
* Starting solutions are entered as numerical values from 0-9, where empty spaces are replaced with a period (.). 
* The text file expects the basic 9x9 (a couple of simple changes would need to be made to support larger puzzles)

An example is provided below:

```
.65.3.8..
7......14
.....1...
.9...8..2
..8.7.6..
4..5...8.
...3.....
61......3
..3.9.72.
```

### Program Execution

Call the python script passing the path to the input file: 

```
python main.py .\input.txt
```

The output will show as following:

```
Begin :: 
- - - - - - - - - - - - - 
|   6 5 |   3   | 8     | 
| 7     |       |   1 4 | 
|       |     1 |       | 
- - - - - - - - - - - - - 
|   9   |     8 |     2 | 
|     8 |   7   | 6     | 
| 4     | 5     |   8   | 
- - - - - - - - - - - - - 
|       | 3     |       | 
| 6 1   |       |     3 | 
|     3 |   9   | 7 2   | 
- - - - - - - - - - - - - 
Iteration 0
- - - - - - - - - - - - - 
|   6 5 |   3   | 8     | 
| 7     |       |   1 4 | 
|       |     1 |       | 
- - - - - - - - - - - - - 
|   9   |     8 |     2 | 
|     8 |   7   | 6     | 
| 4     | 5     |   8   | 
- - - - - - - - - - - - - 
|       | 3     |       | 
| 6 1   |       |     3 | 
|     3 |   9   | 7 2   | 
- - - - - - - - - - - - - 

...

Iteration 31
- - - - - - - - - - - - -
| 1 6 5 |   3   | 8 9 7 |
| 7 3 2 | 9 8 6 | 5 1 4 |
| 9 8 4 | 7 5 1 | 2 3 6 |
- - - - - - - - - - - - -
| 5 9 1 | 4 6 8 | 3 7 2 |
| 3 2 8 | 1 7 9 | 6 4 5 |
| 4 7 6 | 5 2 3 | 1 8 9 |
- - - - - - - - - - - - -
| 2     | 3 1 7 | 4 6 8 |
| 6 1 7 | 8 4 2 | 9 5 3 |
| 8 4 3 | 6 9 5 | 7 2 1 |
- - - - - - - - - - - - -
Iteration 32
- - - - - - - - - - - - -
| 1 6 5 | 2 3 4 | 8 9 7 |
| 7 3 2 | 9 8 6 | 5 1 4 |
| 9 8 4 | 7 5 1 | 2 3 6 |
- - - - - - - - - - - - -
| 5 9 1 | 4 6 8 | 3 7 2 |
| 3 2 8 | 1 7 9 | 6 4 5 |
| 4 7 6 | 5 2 3 | 1 8 9 |
- - - - - - - - - - - - -
| 2 5 9 | 3 1 7 | 4 6 8 |
| 6 1 7 | 8 4 2 | 9 5 3 |
| 8 4 3 | 6 9 5 | 7 2 1 |
- - - - - - - - - - - - -
Solution ::
- - - - - - - - - - - - -
| 1 6 5 | 2 3 4 | 8 9 7 |
| 7 3 2 | 9 8 6 | 5 1 4 |
| 9 8 4 | 7 5 1 | 2 3 6 |
- - - - - - - - - - - - -
| 5 9 1 | 4 6 8 | 3 7 2 | 
| 3 2 8 | 1 7 9 | 6 4 5 | 
| 4 7 6 | 5 2 3 | 1 8 9 | 
- - - - - - - - - - - - -
| 2 5 9 | 3 1 7 | 4 6 8 |
| 6 1 7 | 8 4 2 | 9 5 3 |
| 8 4 3 | 6 9 5 | 7 2 1 |
- - - - - - - - - - - - -
```

# Solution

## Set Relaxation

I tinkered around with some concepts, which is potentially why the puzzle looks a bit jumbled.  First, I considered set relaxation.  The idea is as follows.

Sudoku requires the specific rules that for each row, column, and block, there should exist exactly one unique value and no repeats.  We can consider that at each element in the grid, every element starts with a potential set of values from 0 - 9. 

```
Element (0, 0): {1, 2, 3, 4, 5, 6, 7, 8, 9}
Element (0, 1): {1, 2, 3, 4, 5, 6, 7, 8, 9}
...
Element (8, 8): {1, 2, 3, 4, 5, 6, 7, 8, 9}
```

If the starting solution contains the value of 8 in (0, 0) (top-left corner), then we know that 8 is no longer a potential value for all elements within that row, column and block, except for (0, 0) element:

```
Element (0, 0): {8}
Element (0, 1): {1, 2, 3, 4, 5, 6, 7, 9}
Element (0, 2): {1, 2, 3, 4, 5, 6, 7, 9}
...
Element (1, 3): {1, 2, 3, 4, 5, 6, 7, 8, 9}
Element (1, 4): {1, 2, 3, 4, 5, 6, 7, 8, 9}
...
Element (0, 3): {1, 2, 3, 4, 5, 6, 7, 9}
Element (0, 4): {1, 2, 3, 4, 5, 6, 7, 9}
...
Element (1, 3): {1, 2, 3, 4, 5, 6, 7, 8, 9}
Element (1, 4): {1, 2, 3, 4, 5, 6, 7, 9, 9}
...
```

In this case, we can store the potential sets for every element, every row, every column, and every block.  We identify blocks by establishing a consistent relationship between a block ID and the element's row and column.  

```
bid = row * 3 + col
```

### Relaxation by rows, columns, and blocks

We can continue forth by scanning every potential solution set to every element and finding the intersection between it's row, column, and block potential solutions.  If we find that an intersection causes a change, we update that element with the intersection.

As potential element sets reduce to a cardinality of 1, where the cardinality is the length of the set, we can update the solution matrix with the solution value and remove that value from all associated sets. We update that a change has been made, and continue relaxation iteratively. 

## Pair/Triplet/Etc matching

For simple Sudoku puzzle, simple set relaxation may be all that's needed to identify a solution.  But for more complex puzzles, we need to take it a step further.  Forgive me for not knowing the proper Sudoku language to describe these situations. 

We may become deadlocked with simple set relaxation, where there does not exist a single potential value for any element.  Instead, we are left with pairs, triplets, and so forth.  We are left with the following.

Say for instance, a particular row looks as follows:

```
...
| 1 2 _ | 4 5 6 | 7 _ 9 |
...
```

A human can identify that columns 2 and 7 (starting from 0 indexing) have the potential sets of {3, 8}. 

Let's say instead it looks like this:

```
...
| 1 _ _ | 4 5 6 | 7 _ 9 |
...
```

Now `1`, `2`, and `7` have the potential sets of {2, 3, 8}. But, let's say that for some reason that 3 cannot exist in column `1` and `7`.  We're also going to ignore that our previous set-relaxation technique may catch this.  Now the solutions look as follows: 

* `1: { 2, 8}`
* `2: { 2, 3, 8 }`
* `7: { 2, 8 }`

A human can identify this and say that because elements `1` and `7` can only contain { 2, 8 }, then element `2` must be the set { 3 }, making its solution 3.  

* `1: { 2, 8 }`
* `2: { 3 }`
* `7: { 2, 8 }`

We can implement this by creating a map that tracks all the `unions` for each available element in a row. 

* `(1, 2): { 2, 3, 8 }`
* `(1, 7): { 2, 8 }`
* `(2, 7): { 2, 3, 8 }`

We can store each of these `unions` as keys to the map, with values being the list of elements: 

* `map[{ 2, 3, 8 }]: [( 1, 2 ), ( 2, 7 )]`
* `map[{ 2, 8 }]: [( 1, 7 )]`

Scanning across the map, we want to find `unions` with cardinalities that match the length of elements in the list.  Then we will subtract those sets from all other elements not defined in the element list.
1) `|| {2, 3, 8} || == || {1, 2, 7} || == 3`
2) `|| {2, 8} || == || {1, 7} || == 2`

In the first case, subtracting the difference of the 3 element sets will not produce a change.  No action will happen either, because the element list contains all valid elements (2, 3, and 7), leaving no other elements to subtract.  

* `1: { 2, 8}`
* `2: { 2, 3, 8 }`
* `7: { 2, 8 }`

But in the second case, we will remove {2, 8} from element `2`, because `2` is not part of the elements listed in (1, 7): 

* `1: { 2, 8}`
* `2: {2, 3, 8} - {2, 8} = { 3 }`
* `7: { 2, 8 }`

We process this across all rows, columns, and blocks (blocks have not been tested but is a valid check). If a change is identified, continue iterating back to the intitial simple set relaxation step. 

## Completeness
I haven't bothered to check if my solution is complete, only that it's valid.  I also haven't checked the block pair relaxation step, due to row and column being sufficient for all example puzzles tested.  This was just a fun exercise that made me think pretty hard without looking up any current Sudoku theories. 