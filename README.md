# Intelligent Gallery

### Would you like to know how to create an Image gallery that is powered by AI that runs on CPU? Imagine an app where you can search your images using text, for example, “smiling group photos” fetches your photos with your friends from 5 years back! Wouldn’t that be something?

### Well if you want to build such an app that also supports uploading new images and deduplication, you are in the right place!

For reading a step by step guide use: https://medium.com/@SachinKhandewal/intelligent-image-gallery-with-uploads-deduplication-and-text-based-search-using-vector-db-qdrant-6bca4190653b

![](https://raw.githubusercontent.com/sachink1729/intelligentgallery/main/demos/gallery%20preview.gif)
-------------------------------------------------------------------------------------------------------
# Get started!

Original device specs are: i5 10th gen + 1650 Nvidia GTX + 16GB RAM.

**GPU is only used for encoder Sentence Transformer model, which can be run on CPU as well!**

1. To clone this repo, use:
```
git clone https://github.com/sachink1729/intelligentgallery.git
```

2. Install the necessary requirements, run in terminal:

```
pip install -r requirements.txt
```

3. To start the app, Run:
```
python ./app.py
```

--------------------------------------------------------------------------------------------------------
# How to
## 1. Text search on images.
![](https://raw.githubusercontent.com/sachink1729/intelligentgallery/main/demos/text%20search%20on%20images.gif)

## 2. Upload a new Image.
![](https://raw.githubusercontent.com/sachink1729/intelligentgallery/main/demos/upload%20new%20image.gif)

## 3. Deduplication
![](https://raw.githubusercontent.com/sachink1729/intelligentgallery/main/demos/duplicate%20image.gif)

# Built using:
1) Qdrant: https://qdrant.tech/

![alt text](https://raw.githubusercontent.com/qdrant/qdrant/master/docs/logo.svg)

2) Gradio: https://www.gradio.app/

![alt text](https://avatars.githubusercontent.com/u/51063788?s=200&v=4)

3) SentenceTransformers: https://huggingface.co/sentence-transformers

![alt text](https://aeiljuispo.cloudimg.io/v7/https://cdn-uploads.huggingface.co/production/uploads/1609621322398-5eff4688ff69163f6f59e66c.png?w=200&h=200&f=face)
