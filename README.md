# š Advent of Code 2021 š

![](https://img.shields.io/badge/day%20š-31-blue)
![](https://img.shields.io/badge/stars%20ā­-47-yellow)
![](https://img.shields.io/badge/days%20completed-23-red)

## Summary

This year I will post my solutions to the [Advent of code](https://adventofcode.com/), even though I think they are nothing special.
I'm also writing my bachelor thesis right now, so I'm not sure if I'll do all the puzzles - but we'll see š.

## Overview

| Day                                       | Name                      | Status | Notes  |
| ----------------------------------------- | ------------------------- | ------ | ------ |
| [01](https://adventofcode.com/2021/day/1) | Sonar Sweep               |  ā­ā­  | I think the pandas solution looks nice (a one liner each š) - also there is a nice trick in it that shows that the puzzle is solvable without an sliding window š. |
| [02](https://adventofcode.com/2021/day/2) | Dive!                     |  ā­ā­  | The solution was really straight forward and only little code was needed. |
| [03](https://adventofcode.com/2021/day/3) | Binary Diagnostic         |  ā­ā­  | I did some `beautiful` (in my opinion not really) python magic |
| [04](https://adventofcode.com/2021/day/4) | Giant Squid               |  ā­ā­  | Here the python magic was nice š - also I used a class for the board. |
| [05](https://adventofcode.com/2021/day/5) | Hydrothermal Venture      |  ā­ā­  | This was just fun š - I wanted to avoided creating a `line` or a `point` class - so I made heavy use of tuples and list comprehensions |
| [06](https://adventofcode.com/2021/day/6) | Lanternfish               |  ā­ā­  | A little growth simulation was fun and I learned something about the `defaultdict`. |
| [07](https://adventofcode.com/2021/day/7) | The Treachery of Whales   |  ā­ā­  | Ahh this was cool - the computational complexity was greatly reduced (from `nĀ³` to `nĀ²`) after finding an explicit formula for the sum of the first n numbers! I learned that these numbers are called triangular numbers. - nice refresher in finite series - a dynamic programming approach would have also reduced the time complexity but would have increased the storage complexity... and I wanted to use the explicit formula since I found one š - I added a smarter way where the complexity is even much lower (avg: 807Ī¼s vs 280ms) |
| [08](https://adventofcode.com/2021/day/8) | Seven Segment Search      |  ā­ā­  | Was easier than I thought in the beginning. - would have been far more complex if not always all numbers would be there, then I had written an algorithm that uses permutations and tries to find an solution to the problem - but the puzzle was fun, even with an hard codable algorithm |
| [09](https://adventofcode.com/2021/day/9) | Smoke Basin               |  ā­ā­  | I found a really nice way of doing this puzzle by heavily leveraging `scipy` in particular the `generic_filter` and the `label` functions š¤©š  |
| [10](https://adventofcode.com/2021/day/10) | Syntax Scoring           |  ā­ā­  | `reduce` the reduce function was the mvp in this challenge. At least for me ^^  (the for else was also not bad) - This time it felt like I'm a step closer to a pythonic coding style š (a style that leverages Python's features to write code that is readable and beautiful) |
| [11](https://adventofcode.com/2021/day/11) | Dumbo Octopus            |  ā­ā­  | generic_filter ftw š¤£ - I also did a small visualization on the branch `visualizations` - the visualization can be also found as a [video on youtube](https://www.youtube.com/watch?v=hQPM04spcao)  |
| [12](https://adventofcode.com/2021/day/12) | Passage Pathing          |  ā­ā­  | I failed again for memory views vs copies .... š yeah that happens š¤£ |
| [13](https://adventofcode.com/2021/day/13) | Transparent Origami      |  ā­ā­  | A friend of mine had an `bug` in his input.. not really a bug more like an edge case that my input lacked... And yes my code does not work for an fold where the first half is smaller than the second - but as far as I can tell this was never needed... but for completeness it would be desirable ^^ |
| [14](https://adventofcode.com/2021/day/14) | Extended Polymerization  |  ā­ā­  | For solution 1 I created a linked list that is iterable but that was of course not nearly enough for solution 2. Solution 2 is just hacked together ... maybe later on the day I will revisit this puzzle. ^^  |
| [15](https://adventofcode.com/2021/day/15) | Chiton                   |  ā­ā­  | With the networkx library it was doable in just a few lines of code - but the docu of networkx could be "more verbose" š |
| [16](https://adventofcode.com/2021/day/16) | Packet Decoder           |  ā­ā­  | That was fun but it was also the challenge that took the most time ^^ so many small silly bugs š |
| [17](https://adventofcode.com/2021/day/17) | Trick Shot               |  ā­ā­  | I'm not really proud of the solution because I brute forced instead of using the superposition principle .... but hey I found the solution and it only took me a few minutes š¤£ (code executes in a second or two) |
| [20](https://adventofcode.com/2021/day/20) |  Trench Map   |  ā­ā­  | The generic filter does it all ^^ |
| [21](https://adventofcode.com/2021/day/21) |  Dirac Dice   |  ā­ā­  | With a cache this was quite fast - I just have to remember that dimensions should not interfere with each other š (I summed the scores in the for loop - that was a stupid mistake that took me too long to see) - but the puzzle was fun š |
