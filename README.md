# 🎄 Advent of Code 2021 🎄

![](https://img.shields.io/badge/day%20📅-10-blue)
![](https://img.shields.io/badge/stars%20⭐-19-yellow)
![](https://img.shields.io/badge/days%20completed-9-red)

## Summary

This year I will post my solutions to the [Advent of code](https://adventofcode.com/), even though I think they are nothing special.
I'm also writing my bachelor thesis right now, so I'm not sure if I'll do all the puzzles - but we'll see 😎.

## Overview

| Day                                       | Name                      | Status | Notes  |
| ----------------------------------------- | ------------------------- | ------ | ------ |
| [01](https://adventofcode.com/2021/day/1) | Sonar Sweep               |  ⭐⭐  | I think the pandas solution looks nice (a one liner each 😎) - also there is a nice trick in it that shows that the puzzle is solvable without an sliding window 😉. |
| [02](https://adventofcode.com/2021/day/2) | Dive!                     |  ⭐⭐  | The solution was really straight forward and only little code was needed. |
| [03](https://adventofcode.com/2021/day/3) | Binary Diagnostic         |  ⭐⭐  | I did some `beautiful` (in my opinion not really) python magic |
| [04](https://adventofcode.com/2021/day/4) | Giant Squid               |  ⭐⭐  | Here the python magic was nice 😊 - also I used a class for the board. |
| [05](https://adventofcode.com/2021/day/5) | Hydrothermal Venture      |  ⭐⭐  | This was just fun 😊 - I wanted to avoided creating a `line` or a `point` class - so I made heavy use of tuples and list comprehensions |
| [06](https://adventofcode.com/2021/day/6) | Lanternfish               |  ⭐⭐  | A little growth simulation was fun and I learned something about the `defaultdict`. |
| [07](https://adventofcode.com/2021/day/7) | The Treachery of Whales   |  ⭐⭐  | Ahh this was cool - the computational complexity was greatly reduced (from `n³` to `n²`) after finding an explicit formula for the sum of the first n numbers! I learned that these numbers are called triangular numbers. - nice refresher in finite series - a dynamic programming approach would have also reduced the time complexity but would have increased the storage complexity... and I wanted to use the explicit formula since I found one 😁 - I added a smarter way where the complexity is even much lower (avg: 807μs vs 280ms) |
| [08](https://adventofcode.com/2021/day/8) | Seven Segment Search      |  ⭐⭐  | Was easier than I thought in the beginning. - would have been far more complex if not always all numbers would be there, then I had written an algorithm that uses permutations and tries to find an solution to the problem - but the puzzle was fun, even with an hard codable algorithm |
| [09](https://adventofcode.com/2021/day/9) | Smoke Basin               |  ⭐⭐  | I found a really nice way of doing this puzzle by heavily leveraging `scipy` in particular the `generic_filter` and the `label` functions 🤩😍  |
