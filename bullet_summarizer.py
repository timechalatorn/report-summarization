import requests
from config import OLLAMA_API_URL, OLLAMA_MODEL_NAME

def summarize_chunk(text, index, temperature=0.7, seed=None):
    prompt = f"📍 ตอนที่ {index}\n\nสรุปบทความต่อไปนี้แบบมีรายละเอียด แต่กระชับ:\n{text}\n\nตอบเป็นย่อหน้าเดียว"
    payload = {
        "model": OLLAMA_MODEL_NAME,
        "prompt": prompt.strip(),
        "stream": False,
        "num_predict": 16384,
        "temperature": temperature
    }
    if seed is not None:
        payload["seed"] = seed
    response = requests.post(OLLAMA_API_URL, json=payload)
    if response.status_code == 200:
        return response.json().get("response", "[No summary returned]")
    return f"❌ Error: {response.status_code} - {response.text}"


def clean_summary_text(text):
    """
    Remove polite intros/outros or filler phrases added by the model.
    """
    phrases_to_remove = [
        "แน่นอนครับ",
        "นี่คือสรุปเนื้อหาจากบทความ",
        "หวังว่าสรุปนี้จะเป็นประโยชน์",
        "หากมีข้อสงสัยเพิ่มเติม",
        "ตามความต้องการของคุณ",
        "ครับ",  # use with caution; may strip useful content
        "ค่ะ"
    ]
    for phrase in phrases_to_remove:
        text = text.replace(phrase, "")
    return text.strip()


def create_hierarchical_summary(chunk_summaries, temperature=0.7, seed=None):
    """
    Combines chunk summaries into a structured, hierarchical bullet summary.
    """
    refinement_prompt = f"""
ด้านล่างนี้คือสรุปบทความในรูปแบบ bullet points ที่แบ่งตามตอนต่าง ๆ:

{chr(10).join(chunk_summaries)}

กรุณาสร้างสรุปเนื้อหาโดยมีลำดับดังนี้:

**🧾 Overview**
- สรุปภาพรวมของบทความในรูปแบบย่อหน้าเดียว
- ระบุจำนวน “ประเด็นหลัก” ให้ตรงกับจำนวนหัวข้อหลักที่สรุปไว้ใน Bullet Summary ด้านล่าง (เช่น 2, 3, หรือ 4 หัวข้อหลัก)
- ห้ามสังเคราะห์หรือเดาเองจากเนื้อหา
- ใช้สำนวนเป็นกลาง เช่น “บทความนี้กล่าวถึงประเด็นหลักสามเรื่อง ได้แก่...”
- นำเสนอใจความจากแต่ละ chunk อย่างครอบคลุมและเรียงตามลำดับ แต่ยังคงอยู่ในรูปแบบย่อหน้าเดียว

**📌 Bullet Summary**
กรุณารวบรวมเนื้อหาด้านบนให้เป็นสรุปแบบหัวข้อย่อยตามลำดับ เช่น:
    1. หัวข้อหลัก
        1.1 หัวข้อย่อย
            - bullet point (สั้น กระชับ)
            - bullet point ที่ซับซ้อนควรมีคำอธิบายเพิ่มเติม 1–2 บรรทัด เพื่อให้เข้าใจได้ชัดเจน
            - bullet point ที่มีคำเฉพาะ เช่น ชื่อแนวคิด/นโยบาย/เทคโนโลยี (เช่น “No Meeting Friday”) **ต้องมีคำอธิบายประกอบ** 1–2 บรรทัด ว่าคืออะไร มีจุดประสงค์อย่างไร หรือมีผลกระทบอย่างไร
    ...

**ข้อกำหนด**:
- เริ่มด้วย Overview แบบที่กล่าวข้างต้น
- ตามด้วย Bullet Summary
- ใช้ bullet point พร้อมเลขหัวข้อ (1, 1.1, 1.2, ...)
- อย่าใส่คำขึ้นต้นหรือคำปิดท้าย เช่น “หวังว่าจะเป็นประโยชน์...”
- ห้ามสังเคราะห์หรือแสดงความเห็นที่เกินจากเนื้อหาจริง
"""

    payload = {
    "model": OLLAMA_MODEL_NAME,
    "prompt": refinement_prompt.strip(),
    "stream": False,
    "num_predict": 16384,
    "temperature": temperature
}
    if seed is not None:
        payload["seed"] = seed
    response = requests.post(OLLAMA_API_URL, json=payload)
    if response.status_code == 200:
        return response.json().get("response", "[No structured summary returned]")
    return f"❌ Error: {response.status_code} - {response.text}"
