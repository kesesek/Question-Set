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
        answer_raw = answer_match.group(1).strip()
        answer = list(answer_raw) if multiple else answer_raw

        # 截断“答案”后的内容
        question_and_options = re.split(r'答案[:：][A-F]+\s*', block)[0].strip()

        # 倒着找出最后一个 A. ~ F. 的选项位置，作为选项部分起点
        last_option_match = list(re.finditer(r'\n([A-F])\.\s', question_and_options))
        if not last_option_match:
            continue  # 没有选项，跳过
        start = last_option_match[0].start()  # 最早出现的 A. 的位置

        question_text = question_and_options[:start].strip().replace("\n", " ")
        options_block = question_and_options[start:]

        option_matches = re.findall(r'([A-F])\.\s*(.*?)(?=\n[A-F]\.|\n?$)', options_block, re.DOTALL)
        options = {key: val.strip().replace("\n", " ") for key, val in sorted(option_matches)}

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