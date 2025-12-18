## Part2 much later

I wanted to visualize the dataset to see what kind of tricky geometry my "is this inside the shape" code has to solve.
Since it is not directly part of the solution, I feel fine to use an llm for that:

```bash
llm -m haiku 'give me a small, minimal python program that turns a list of x,y coords into an svg. the coords are a circular path. only use the python standard libs. read coords from input.txt. make sure that it viewable in a browser, since its size is approx 90000px. Use a strokewitdh of 15' -x > visualize.py
```

The result shows a rough circle with a large rectangle cut out from it's center.
This shows me that I don't have to solve the general case, but can optimize for the 2 possible starting points (`O`) on the right end of the rectangle.

```
    #####
  ##-----##
 #---------#
#########O--#
         #--#
#########O--#
 #---------#
  ##-----##
    #####
```

Still took 2 tries, with me extending the visualization to include the found rectangles.
First I found the largest rectangle, but forgot that it coult also leave the circle on the top.
After playing a bit with the svg coordinates, I found useful boundaries to ensure the rectangle would be fully inside.

Semi-manual but for just getting this done so I can finish day 12 it is sufficient.
Especially since day 12 part 1 also had a shortcut without actually solving the problem.
