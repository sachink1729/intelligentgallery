"""
    Description: QdrantOps class, create new collections, insert vectors into the vector DB and search using the qdrant client.
    Author: Sachin Khandewal
    Email: sachinkhandewal5@gmail.com
"""

from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer, util
from qdrant_client.models import PointStruct
import torch
from datasets import load_dataset

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Running on: {device}.")

class QdrantOps:
    def __init__(self, collection_name):
        self.encoder = SentenceTransformer('clip-ViT-B-32', device=device)
        self.qdrant = QdrantClient(":memory:")
        self.df = self.load_dataset(datasets_id="cats_vs_dogs", num_of_images=100)
        self.coll_name = collection_name
        self.embed_size = 512 # Embedding size varies with used model
        self.create_collection(coll_name=self.coll_name, embed_size=self.embed_size)
        self.batch_insert_new_images(images=self.df['image'])

    def load_dataset(self,datasets_id: str,num_of_images: int):
        dataset = load_dataset(datasets_id, verification_mode='no_checks').shuffle()
        small_dataset = dataset['train'][:num_of_images]
        return small_dataset

    """ Create a new Qdrant collection with create_collection by specifying the collection name and embedding size. """

    def create_collection(self, coll_name, embed_size):
        self.qdrant.recreate_collection(
            collection_name=coll_name,
            vectors_config=models.VectorParams(
            size=embed_size,  
            distance=models.Distance.COSINE,
        ),)
    
    """ Insert vector representation of images/text using batch_insert_new_images in the created Qdrant collection. """

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
    
    """ Insert vector representation of a single image using insert_single_image in the created Qdrant collection. """

    def insert_single_image(self, input):
        self.df['image'].append(input)
        self.df['labels'].append("new") # optional, not needed 
        idx =  self.df['image'].index(self.df['image'][-1])
        self.qdrant.upsert(collection_name=self.coll_name,points=[
            PointStruct(
                id=self.df['image'].index(self.df['image'][-1]),
                payload={"label": self.df['labels'][-1] , "animal": idx},
                vector=self.encode_text_or_image(input),
                ),
            ],
        )
        print(f"inserted 1 new image with index {idx} in the collection.")

    """ Get k best matches (by default 3) for an input (image/text) using Qdrant's search function. """

    def search(self, query, k=3):
        hits = self.qdrant.search(collection_name=self.coll_name,
                                  query_vector=self.encode_text_or_image(query).tolist(),
                                  limit=k) # by default 3 best matches will be fetched)
        return hits

    """ Get vector representation for the input using Sentence Transformers model."""

    def encode_text_or_image(self, inp):
        vec=self.encoder.encode(inp)
        return vec