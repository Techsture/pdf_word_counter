import re
import PyPDF2
from collections import Counter
import argparse

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text() + "\n"
    # Replace common ligatures with their standard forms
    text = text.replace("ﬁ", "fi").replace("ﬂ", "fl")
    # Remove page numbers (assuming they appear as standalone numbers)
    text = re.sub(r'\b\d+\b', '', text)
    return text

def count_word_occurrences(text):
    words = re.findall(r"\b\w+(?:'\w+)?\b", text.lower())  # Extract words, including those with apostrophes
    word_count = Counter(words)
    return word_count

def main():
    parser = argparse.ArgumentParser(description="Count word occurrences in a PDF file.")
    parser.add_argument('pdf_path', type=str, help="Path to the PDF file")
    args = parser.parse_args()
    
    text = extract_text_from_pdf(args.pdf_path)
    word_count = count_word_occurrences(text)
    
    # Sort by occurrences first, then alphabetically
    sorted_word_count = sorted(word_count.items(), key=lambda x: (-x[1], x[0]))
    
    for word, count in sorted_word_count:
        print(f"{word}: {count}")

if __name__ == "__main__":
    main()
