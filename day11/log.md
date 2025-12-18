Part 1 was simple, just BFS and count how often `out` comes up.

For part 2 I decided early to solve just my case, not all of them, unrolling the 2 options in code.
Adding exclusions to the existing alg was no problem at all, in hindsight it is also not important since the graph (for the exercises purposes) has to be cycle-free.
Therefore there can be no acceptable path that goes through any of the "targets" twice.

But my BFS algorithm ran into a large sub-path, taking forever (and blowing up memory), which I first thought was a loop.
Writing a second DFS solution showed me that the first 1000 found paths indicated that the subgraph was highly connected, with only the last few steps changing.
Adopting the algorithm to memoize values was relatively easy and fixed the runtime as well.
