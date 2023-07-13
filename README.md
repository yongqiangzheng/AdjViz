# AdjViz

A tool for visualizing adjacency matrices of graph neural networks

Based on dependency and constituency parsing tree

## Requirements
benepar==0.2.0

Flask==2.2.3

matplotlib==3.7.1

nltk==3.8.1

seaborn==0.12.2

spacy==3.3.1

torch==2.0.0

transformers==4.27.4

protobuf==3.20.0

## Usage

### Step 1
run this code in the terminal
```
python app.py
```

### Step 2

Access http://127.0.0.1:5000 in your browser

### Step 3

write your text in **Input text** and click **submit**

## Example

Input text: Great food but the service was dreadful !

![](static/depgcn.png)

![](static/consgcn.png)

![](static/depconsgcn.png)
