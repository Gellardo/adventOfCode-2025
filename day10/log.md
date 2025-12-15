## This is surely a graph problem
Part 1 was straight forward breadth-first Search.
Part 2, again, I wanted to reuse the algorithm and came up with a "simple" hashing algo to be able to keep using the same map approach.
But I think I messed up when trying to get the hashing to work with the toggles, so I'll restart from the beginning for part 2.

I fixed it without a full rewrite by keeping the options as lists longer and adding a few assertions to test that my conversion functions actually work the way I expect.
But BFS is far too slow, even the second machine takes more than 1 minute (killed it then).
Better algorithm needed, let's see how much I remember from the lectures.

## Part 2 is too large, but I bet it is my algorithm
Second try looks a bit like dijkstra... but I don't think it is quite right yet.
And it runs for far too long on the real input.
Debugging shows that my estimates explode but nothing reached the definitive step.

Found a test-case where going down the "best" road lead to a dead end, for which it breaks down completely.
Trying explicit depth-first search next, hopefully less error-prone.
I'm already thinking that this could easier be solved via linear algebra, but I really want the graph algorithms to work.
It seems to work alright but also  20x iterations for my first machine.
Second machine was stopped after a few minutes, showing it still is far too slow.

Another try, which felt different but in hindsight is also just a DFS search, just skipping ahead on using the same toggle multiple times.
Still the same problem, exploding state-space, no results for quite a while.

## Alright, I'll use LinAlg
Ok, I tried transforming everything into equations and solving them.
Only then noticing that I need to minimize them, not just solve since there can be multiple solutions.

## Acceptance: Just use an existing solver
Using z3, the problem becomes quite easy, especially since I already had thought about the involved equations in the previous iteration.
Only needed to look into the API a bit, not mess up the indices and convert the result to an actual number (arg.. `as_long`).
And everything is fine :smile:, perhaps I'll revisit this later.
