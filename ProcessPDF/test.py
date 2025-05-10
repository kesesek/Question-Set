import pdfplumber
import re
import json

file_path = "questions.pdf"

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def split_single_and_multiple(text):
    if "多选题" in text:
        parts = text.split("多选题", maxsplit=1)
        return parts[0], parts[1]
    else:
        return text, ""


def parse_questions(text, multiple=False):
    # 切分每一道题：以“数字.”开头的作为题目开始
    raw_questions = re.split(r'\n?\d+\.\s+', text)
    questions = []

    for block in raw_questions:
        if not block.strip():
            continue

        # 提取题干（直到 A. 出现）
        q_match = re.search(r'^(.*?)(?=\n?[A-F]\.)', block, re.DOTALL)
        if not q_match:
            continue
        question_text = q_match.group(1).strip()

        # 提取所有选项
        option_matches = re.findall(r'([A-F])\.\s*(.*?)\s*(?=(?:[A-F]\.|答案[:：]))', block, re.DOTALL)
        options = {key: val.strip() for key, val in option_matches}

        # 提取答案
        answer_match = re.search(r'答案[:：]\s*([A-F]+)', block)
        if not answer_match:
            continue
        raw_answer = answer_match.group(1).strip()
        answer = list(raw_answer) if multiple else raw_answer

        questions.append({
            "question": question_text,
            "options": options,
            "answer": answer
        })

    return questions


def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def process_pdf_to_json(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    single_text, multiple_text = split_single_and_multiple(text)
    
    single_questions = parse_questions(single_text, multiple=False)
    multiple_questions = parse_questions(multiple_text, multiple=True)
    
    save_json(single_questions, "single_choice.json")
    save_json(multiple_questions, "multiple_choice.json")

if __name__ == "__main__":
    process_pdf_to_json("questions.pdf")