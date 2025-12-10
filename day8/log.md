Took forever to realize that I can't just keep the smallest connection for each node but need to use all distances.

```
A - B ----- C -- D
```

Initial code only selected the short edges, and retried them multiple times because AB and CD are the shortest.
No node kept record of the long BC edge.

Once I fixed that, only messed up the circuit merge logic then it worked "flawlessly".

Part2 was really simple in comparison, just do the same but wait until everything is connected.
Copy paste for the win.
