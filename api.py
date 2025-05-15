from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bullet_summarizer import summarize_chunk, create_hierarchical_summary
from utils import segment_sentences, embed_sentences, detect_change_points, chunk_by_breakpoints

app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.post("/summarize/")
def summarize_text(input_data: TextInput):
    try:
        # Step 1: Segment into sentences
        sentences = segment_sentences(input_data.text)

        # Step 2: Sentence embeddings
        embeddings = embed_sentences(sentences)

        # Step 3: Detect change points
        breakpoints = detect_change_points(embeddings)

        # Step 4: Chunking
        chunks = chunk_by_breakpoints(sentences, breakpoints)

        # Step 5: Summarize each chunk
        chunk_summaries = [
            f"📍 ตอนที่ {i}:\n{summarize_chunk(chunk, i)}"
            for i, chunk in enumerate(chunks, 1)
        ]

        # Step 6: Hierarchical summary
        final_summary = create_hierarchical_summary(chunk_summaries)

        return {
            "chunk_summaries": chunk_summaries,
            "final_summary": final_summary
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
