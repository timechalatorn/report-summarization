import torch
import numpy as np
from transformers import AutoTokenizer, AutoModel
from pythainlp.tokenize import sent_tokenize
import ruptures as rpt
from config import MODEL_NAME

# --- Load Thai BERT tokenizer and model ---
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)

# --- Sentence segmentation ---
def segment_sentences(text):
    return sent_tokenize(text)

# --- Embedding functions ---
def embed_sentence(sentence):
    inputs = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].squeeze().numpy()

def embed_sentences(sentences):
    return np.array([embed_sentence(sent) for sent in sentences])

# --- Change point detection ---
def detect_change_points(embeddings, penalty=0.9):   ###### effect the number of the chunk
    model = rpt.Pelt(model="rbf").fit(embeddings)
    return model.predict(pen=penalty)

# --- Chunk grouping ---
def chunk_by_breakpoints(sentences, breakpoints):
    chunks = []
    start = 0
    for end in breakpoints:
        chunks.append(" ".join(sentences[start:end]))
        start = end
    return chunks


