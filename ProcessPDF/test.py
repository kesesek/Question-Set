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
    # split text into 3 parts: title, single-choice, and multiple-choice
    if "选题" in text:
        parts = text.split("选题", maxsplit=2)
        # don't need parts[0]. It's title
        return parts[1], parts[2]
    else:
        return text, ""


def parse_questions(text, multiple=False):
    questions = []
    # split text using "number. Question"
    blocks = re.split(r'\n?\d+\.\s+Question', text)
    
    for block in blocks:
        # skip empty blocks
        if not block.strip():
            continue

        # get answers
        answer_match = re.search(r'答案[:：]\s*([A-F]+)', block)
        if not answer_match:
            continue
        answer_text = answer_match.group(1).strip()
        answer = list(answer_text) if multiple else answer_text

        # splite by "答案：...", keep the first part(it's question body)
        question_body = re.split(r'答案[:：][A-F]+\s*', block)[0]

        # get options
        option_matches = re.findall(r'([A-F])\.\s*(.*?)(?=\n[A-F]\.|\n答案[:：]|$)', question_body, re.DOTALL)
        options = {opt: txt.strip().replace("\n", " ") for opt, txt in sorted(option_matches)}

        # get question body before A
        if option_matches:
            first_option_letter = option_matches[0][0]
            question_text = question_body.split(f"{first_option_letter}.", 1)[0].strip().replace("\n", " ")
        else:
            question_text = ""

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
    # print(text[:1000])
    # return
    
    single_text, multiple_text = split_single_and_multiple(text)
    
    single_questions = parse_questions(single_text, multiple=False)
    multiple_questions = parse_questions(multiple_text, multiple=True)
    
    save_json(single_questions, "single_choice.json")
    save_json(multiple_questions, "multiple_choice.json")

if __name__ == "__main__":
    process_pdf_to_json("questions.pdf")