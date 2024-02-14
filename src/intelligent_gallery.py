from src.qdrant_ops import QdrantOps
import gradio as gr

class IntelligentGallery:
    def __init__(self,coll_name):
        self.qdrant_obj = QdrantOps(collection_name=coll_name)
    
    def semantic_search(self,input):
        msg = ""
        scores=[]
        outs=[]
        for hit in self.qdrant_obj.search(input):
            scores.append(hit.score)
            outs.append(self.qdrant_obj.df['image'][hit.payload['animal']])
        return outs, scores
        
    def output_when_image_input(self, input):
        outs, scores = self.semantic_search(input)
        if scores[0]<0.95:
            self.qdrant_obj.insert_single_image(input)
            outs = self.qdrant_obj.df['image']
            msg = "Adding new image to the gallery."
            return [outs, msg]
        else:
            msg = "Duplicate image already present so removing the new image." + f"Matches fetched with the scores: {scores}." 
        return [outs, msg]
    
    def output_when_text_input(self,input):
        outs=[]
        scores=[]
        for hit in self.qdrant_obj.search(input):
            scores.append(hit.score)
            outs.append(self.qdrant_obj.df['image'][hit.payload['animal']])
        msg = f"Matches fetched with the scores: {scores}."
        return [outs, msg]
    
    def dummy(self,input):
        return self.qdrant_obj.df['image']

    def gradio_ui(self):
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
                    btn.click(fn=self.output_when_text_input, inputs=[gr.Textbox(label="Search for an image")],  outputs=[gallery,gr.Textbox(value="Status")]) #outputs=[tb1, match1, tb2, match2,tb3, match3])
                with gr.Row():
                    btn1 = gr.Button(value="Upload new image.", scale=0)
                    btn1.click(fn=self.output_when_image_input, inputs=[gr.Image(type="pil")], outputs=[gallery,gr.Textbox("Status")])
        demo.launch()

if __name__ == "__main__":
    int_gallery = IntelligentGallery("cats_and_dogs")
    int_gallery.gradio_ui()