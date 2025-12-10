Took forever to realize that I can't just keep the smallest connection for each node but need to use all distances.

```
A - B ----- C -- D
```

Initial code only selected the short edges, and retried them multiple times because AB and CD are the shortest.
No node kept record of the long BC edge.
