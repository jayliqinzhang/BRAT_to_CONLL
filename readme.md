# Change BRAT format to CONLL BIO format

This code is used to change the annotation format from BRAT to CONLL BIO format. 
It is designed to used in the [Dutch essay argument components annotation project](https://github.com/jayliqinzhang/A-Dutch-essay-corpus-with-argument-structures-and-quality-indicators), but it is applied other cases as well. 


## Use the code

Simply run the code 

```python
python brat_conll.py
```

There are sample `.txt` and `.ann` files in the `sample_input_folder` which are from the corpus of [Dutch essay argument components annotation project](https://github.com/jayliqinzhang/A-Dutch-essay-corpus-with-argument-structures-and-quality-indicators). You can see the resulted `.conll` files in the `output_folder` folder. 

Keep in mind you can replace the path to your path containing your .ann and .txt files:

```python
if __name__ == "__main__":
    write_result("<YOUR_INPUT_FOLDER>", "<YOUR_OUTPUT_FOLDER>")

```




## Introduction of the code

- `def process_ann()` and `def process_txt()`

Process the `.ann` annotation file and `.txt` its original text file.

Both functions return the indics of the characters with argument tags ("B-xxx" or "I-xxx") and non-argument tags ("O").

- `def get_char_index()`

Using the results of above functions and make the complete indics of all the characters in the essay text file. 

- `def get_result()`

Run this and get the result. Be noticed that the special sysmbols string are handled exclusively according to the needs of the specific [Dutch essay argument components annotation project](https://github.com/jayliqinzhang/A-Dutch-essay-corpus-with-argument-structures-and-quality-indicators). It may requires extra adaption based on the characteristics of your text files.

- `def write_result()`

Write the results to files. 







