When solving manually, Part 1 was not much of a problem. But extending to part 2 was more annoying.

1. changing handling of spaces (couldn't `strip` the input) made me have to change part1 code example
1. having to handle spaces in general needed a `if` cases that i only noticed after execution failed
1. iterating backwards via `range` took far too many tries

Funny side-story:
I tried to use `llm` to critique my code. Specifically if i could get it to use `-a` but that did not work at all (gemini ignored it/ if i tried to use `-` llm complained about only supporting "image" types)

so I tried using chat mode with gemini... Told it to

> critique my code and improve it !fragement day6/solve.py

and it proceeded to give me a hallucinated critique and produced a solution for AoC 2022 day 6.
I learned that `!fragement` needs to be on it's own line to work.

What worked, though it is very wordy and not great to read in the terminal with only Markdown but not formatting
```bash
llm  -m $MODEL -f day6/solve.py 'critique this code and improve it'
```
