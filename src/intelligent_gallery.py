"""
    Description: IntelligentGallery class, similarity search with Qdrant, upload new images into gallery, text search on images.
    Author: Sachin Khandewal
    Email: sachinkhandewal5@gmail.com
"""

from src.qdrant_ops import QdrantOps
import gradio as gr

class IntelligentGallery:
    def __init__(self,coll_name):
        self.qdrant_obj = QdrantOps(collection_name=coll_name)
        self.duplicate_threshold = 0.95 # above this score image is considered as a duplicate
    
    """ Fetch best matches and scores given the input uisng QdrantOps search function. """

    def semantic_search(self,input):
        scores=[]
        outs=[]
        for hit in self.qdrant_obj.search(input):
            scores.append(hit.score)
            outs.append(self.qdrant_obj.df['image'][hit.payload['animal']])
        return outs, scores
    
    """ Output logic when the input is an image. """
        
    def output_when_image_input(self, input):
        msg=""
        outs, scores = self.semantic_search(input)
        if scores[0]<self.duplicate_threshold:
            self.qdrant_obj.insert_single_image(input)
            outs = self.qdrant_obj.df['image']
            msg = "Adding new image to the gallery."
            return [outs, msg]
        else:
            msg = "Duplicate image already present so removing the new image." + f"Matches fetched with the scores: {scores}." 
        return [outs, msg]
    
    """ Output logic when the input is a text. """

    def output_when_text_input(self,input):
        msg=""
        outs, scores = self.semantic_search(input=input)
        msg = f"Matches fetched with the scores: {scores}."
        return [outs, msg]
    
    """ Dummy function for gradio gallery to reload the images. """

    def dummy(self,input):
        return self.qdrant_obj.df['image']

    """ Gradio UI initiator runs in public and local mode. """

    def gradio_ui(self, mode):
        with gr.Blocks() as demo:
            with gr.Tab("SMART GALLERY"):
                with gr.Row():
                    data = self.qdrant_obj.df['image']
                    gallery = gr.Gallery(value = data, show_label=False, elem_id="gallery", 
                           columns=[6], 
                           rows=[1], 
                           object_fit="contain", 
                           height="auto",
                           every=1)
                    btn2 = gr.Button(value="Reload Gallery", scale=0)
                    btn2.click(fn=self.dummy, outputs=gallery)
                with gr.Row():
                    btn = gr.Button(value="Search using text.", scale=0)
                    btn.click(fn=self.output_when_text_input, inputs=[gr.Textbox(label="Search for an image")],  outputs=[gallery,gr.Textbox(label="Status")]) #outputs=[tb1, match1, tb2, match2,tb3, match3])
                with gr.Row():
                    btn1 = gr.Button(value="Upload new image.", scale=0)
                    btn1.click(fn=self.output_when_image_input, inputs=[gr.Image(type="pil")], outputs=[gallery,gr.Textbox(label="Status")])
        if mode == 'public':
            demo.launch(share=True)
        else:
            demo.launch(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    int_gallery = IntelligentGallery("cats_and_dogs")
    int_gallery.gradio_ui()