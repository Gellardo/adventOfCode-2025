After solving it manually, i decided to see how llms fare.

So after `C^a` `C^c` of the page, i basically just ask for a solution and pipe it into a file. 

```
pbpaste | llm -s 'give me python code to solve this. include a test to check the examples as well.' -m $MODEL -x > MODEL.py
```

| Model | cost | solved | Notes |
|---|---|---|---|
| sonnet 4.5 | 2.25 cent | 1st try | also included file reading as a comment |
| haiku 4.5 | 1.54 cent | 2nd try | needed prompting to include input file reading |
| gemini 2.5 flash lite | 0 cent | 2nd try | first iteration tried to enumerate ids (same as i did), but fixed after I complained about runtime |
| quen3-coder-30b | ? | 3rd try | feels worse then online models, first iteration enumeration-based, second iteration forgot about the input reading, third iteration works but forgot the tests. That might be because of the prompting but still. Gut reaction to first and second iteration was: code not great. |
