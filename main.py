from bullet_summarizer import summarize_chunk, create_hierarchical_summary
from utils import segment_sentences, embed_sentences, detect_change_points, chunk_by_breakpoints
from evaluation import evaluate_summary
from deterministic_summary import set_deterministic


set_deterministic(enable=True)
SEED = 42
TEMPERATURE = 0  # Use 0 for deterministic; raise for creative variation


# Toggle evaluation mode
EVALUATION_MODE = False  # Set to False to disable

# Load input
with open("input.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Step 1: Sentence segmentation
sentences = segment_sentences(text)

# Step 2: Sentence embeddings
embeddings = embed_sentences(sentences)

# Step 3: Change point detection
breakpoints = detect_change_points(embeddings)

# Step 4: Group into chunks
chunks = chunk_by_breakpoints(sentences, breakpoints)

# Step 5: Summarize each chunk
chunk_summaries = []
for i, chunk in enumerate(chunks, 1):
    summary = summarize_chunk(chunk, i, temperature=TEMPERATURE, seed=SEED)
    chunk_summaries.append(f"📍 ตอนที่ {i}:\n{summary}")
    print(f"\n📘 Chunk {i} Summary:\n{summary}")

# Step 6: Hierarchical summary
final_summary = create_hierarchical_summary(chunk_summaries, temperature=TEMPERATURE, seed=SEED)
print("\n🧠 Bullet Summary:\n", final_summary)

# Optional Evaluation
if EVALUATION_MODE:
    reference_summary = text  # Use original input as reference
    evaluate_summary(final_summary, reference_summary)