Part 1 was straight forward breadth-first Search.
Part 2, again, I wanted to reuse the algorithm and came up with a "simple" hashing algo to be able to keep using the same map approach.
But I think I messed up when trying to get the hashing to work with the toggles, so I'll restart from the beginning for part 2.

I fixed it without a full rewrite by keeping the options as lists longer and adding a few assertions to test that my conversion functions actually work the way I expect.
But BFS is far too slow, even the second machine takes more than 1 minute (killed it then).
Better algorithm needed, let's see how much I remember from the lectures.

Second try looks a bit like dijkstra... but I don't think it is quite right yet.
And it runs for far too long on the real input.
