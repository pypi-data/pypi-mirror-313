import gradio as gr
from PyPDF2 import PdfReader
import wordCount
import matplotlib.pyplot as plt
import sentimentAnalysis
def analyse(file,top_n):
    try:
        # Open and read the PDF file
        reader = PdfReader(file.name)
        text = " "    
        orig_text = " "
        for page in reader.pages:
            text += page.extract_text()
            orig_text += page.extract_text()
        text = wordCount.removeStopWords(text)
        text = wordCount.countWordFrequency(text)
        text = text.most_common(top_n)
        plot = PlotIt(text)
        # sentiment analysis
        sentiment = sentimentAnalysis.sentimentAnalysis(orig_text)
        label,score = sentiment['label'],sentiment['score']
        sentiment = "sentiment: "+label
        return sentiment,text,plot
    except Exception as e:
        return f"An error occurred: {e}"
    
    return res

def PlotIt(word_counts):
    words, frequencies = zip(*word_counts) if word_counts else ([], [])

    plt.figure(figsize=(10, 5))
    plt.bar(words,frequencies, color='skyblue')
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    plt.title("Word Frequency Bar Plot")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

     # Save plot to a temporary image file
    plot_path = "bar_plot.png"
    plt.savefig(plot_path)
    plt.close()
    
    return plot_path

demo = gr.Interface(
    fn=analyse,
    inputs=[gr.File(label="Upload PDF", file_types=[".pdf"]),
            gr.Slider(minimum=1, maximum=100, step=1, value=5, label="Top N Words")
            ],
    outputs=["text","text","image"]
)
demo.launch()

def showWindow():
    demo.launch()