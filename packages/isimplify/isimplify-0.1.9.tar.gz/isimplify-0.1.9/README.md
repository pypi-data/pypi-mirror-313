# Word Frequency and Sentiment Analysis Package

isimplify is a Python library for dealing with word frequency.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install isimplify.

```bash
pip install isimplify
```
additional requirments
```
pip install gradio matplotlib PyPDF2

```


# overview
 This Python package allows you to analyze word frequencies from text or PDF files, visualize the results using bar plots, and perform sentiment analysis on the text. It includes functionalities to remove stop words, customize the list of stop words, and generate plots for the most frequent words.

The package also provides an interactive Gradio interface to upload PDFs, perform analysis, and view the results.

# using UI to interact and visualize the word freq
```python
import isimplify

isimplify.showWindow()

```

## Usage
# get word freq by reading pdf 

```python
import isimplify

word_freq = isimplify.getWord_freq_file_removingStopWords("example.pdf")
print(word_freq)

```
# get word freq by reading pdf (without removing stop words)

```python
import isimplify

text = "This is an example text to analyze."
word_freq = isimplify.getWord_freq_text_removing_StopWords(text)
print(word_freq)


```
# save the plot
```python
import isimplify

text = "This is an example text to analyze."
plot_path = isimplify.plot_top_n_words_text(text, top_n=5)
print(f"Plot saved at: {plot_path}")

```



## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)