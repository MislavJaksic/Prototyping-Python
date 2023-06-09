"""
    protopy.py
    ------------------

    Runs the project.

    :copyrgiht: 2019 MislavJaksic
    :license: MIT License
"""
import os
import sys
import PyPDF2
import re


def main(args):
    """main() will be run if you run this script directly"""

    pdf_file_path = './file.pdf'
    check_file_exists(pdf_file_path)
    extracted_questions = extract_questions_from_pdf(pdf_file_path)

    with open("questions.txt", 'w', encoding="utf-8") as output:
        for question in extracted_questions:
            output.write(question.replace("-\n", "").replace("\n", " ").replace("  "," ").replace("   "," "))
            output.write("\n")


def check_file_exists(file_path):
    if os.path.exists(file_path):
        print(f"The file '{file_path}' exists.")
    else:
        print(f"The file '{file_path}' does not exist.")


def extract_questions_from_pdf(file_path):
    questions = []

    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)

        print(f"pages={len(pdf_reader.pages)}")

        for page_num in range(50, len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()

            question_pattern = r"(?:^|\b)([A-Z][^?!.]*\?)"
            matches = re.findall(question_pattern, text, re.MULTILINE)

            for match in matches:
                question = match.strip()
                questions.append(question)

        return questions

def run():
    """Entry point for the runnable script."""
    sys.exit(main(sys.argv[1:]))


if __name__ == "__main__":
    """main calls run()."""
    run()
