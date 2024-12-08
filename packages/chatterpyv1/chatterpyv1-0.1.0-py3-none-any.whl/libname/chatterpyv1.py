import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from openai import AzureOpenAI

index = None
paragraphs = []
model = SentenceTransformer('all-MiniLM-L6-v2')

class AzureOpenAIs:
    def __init__(self, azure_endpoint, api_key, api_version):
        self.endpoint = azure_endpoint
        self.api_key = api_key
        self.api_version = api_version
        self.client = AzureOpenAI(
            azure_endpoint=self.endpoint,
            api_key=self.api_key,
            api_version=self.api_version
        )

    def get_completion(self, deployment, chat_prompt):
        try:
            completion = self.client.chat.completions.create(
                model=deployment,
                messages=chat_prompt,
                max_tokens=1500,
                temperature=0.7,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None,
                stream=False
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error occurred: {e}"

def process_txt_file(txt_file_path, azure_endpoint, subscription_key, deployment_name, api_version):
    global index, paragraphs

    client = AzureOpenAIs(azure_endpoint, subscription_key, api_version)

    with open(txt_file_path, 'r') as file:
        content = file.read()

    paragraphs = content.split("\n\n")  

    if not paragraphs:
        return {"message": "No content to index"}

    embeddings = model.encode(paragraphs)
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    return {"message": "FAISS index created", "paragraphs": paragraphs}

def search_faiss_db(query, azure_endpoint, subscription_key, deployment_name, api_version):
    global index, paragraphs

    if not index:
        return {"message": "FAISS index not created"}
    query_embedding = model.encode([query])
    _, indices = index.search(query_embedding, k=5)

    closest_match = [paragraphs[idx] for idx in indices[0]]

    chat_prompt = [
        {
            "role": "system",
            "content": "You are an AI assistant that answers questions based on the provided context."
        },
        {
            "role": "user",
            "content": f"""Here are 5 most relevant paragraphs:\n\n{closest_match}\n\n
                           Answer the following question based on this context: {query}"""
        }
    ]

    client = AzureOpenAIs(azure_endpoint, subscription_key, api_version)
    processed_answer = client.get_completion(deployment_name, chat_prompt)
    return {"answer": processed_answer}
