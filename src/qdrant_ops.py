from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer, util
from qdrant_client.models import PointStruct
import torch
from datasets import load_dataset

device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)
dataset = load_dataset("cats_vs_dogs",verification_mode='no_checks').shuffle()
small_dataset = dataset['train'][:100]

class QdrantOps:
    def __init__(self, collection_name):
        self.encoder = SentenceTransformer('clip-ViT-B-32', device=device)
        self.qdrant = QdrantClient(":memory:")
        self.df = small_dataset
        self.coll_name = collection_name
        self.create_collection(self.coll_name)
        self.batch_insert_new_images(self.df['image'])

    def create_collection(self, coll_name):
        self.qdrant.recreate_collection(
            collection_name=coll_name,
            vectors_config=models.VectorParams(
            size=512,  # Vector size is defined by used model
            distance=models.Distance.COSINE,
        ),)
        
    def batch_insert_new_images(self, images):
        vectors = self.encoder.encode(images)
        self.qdrant.upsert(
            collection_name=self.coll_name,
            points=[
                PointStruct(
                    id=idx,
                    vector=vector.tolist(),
                    payload={"label": self.df['labels'][idx] , "animal": idx}
                )
                for idx, vector in enumerate(vectors)
            ]
        )
        print("inserted "+ str(len(vectors)) +" images in the collection.")
    
    def insert_single_image(self, input):
        self.df['image'].append(input)
        self.df['labels'].append("new") # optional, not needed 
        idx =  self.df['image'].index(self.df['image'][-1])
        self.qdrant.upsert(collection_name=self.coll_name,points=[
            PointStruct(
                id=self.df['image'].index(small_dataset['image'][-1]),
                payload={"label": self.df['labels'][-1] , "animal": idx},
                vector=self.encode_text_or_image(input),
                ),
            ],
        )
        print(f"inserted 1 new image with index {idx} in the collection.")

    def search(self, query):
        hits = self.qdrant.search(collection_name=self.coll_name,
                                  query_vector=self.encode_text_or_image(query).tolist(),
                                  limit=3) # 3 best matches will be fetched)
        return hits

    def encode_text_or_image(self, inp):
        vec=self.encoder.encode(inp)
        return vec