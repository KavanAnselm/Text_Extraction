import fitz
import spacy
import re
from textblob import TextBlob
from difflib import SequenceMatcher
from collections import Counter

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    extracted_text = "\n\n".join([page.get_text("text") for page in doc])
    return extracted_text

def correct_spelling(text):
    blob = TextBlob(text)
    corrected_text = blob.correct()
    return str(corrected_text)

def remove_unnecessary_words(text):
    unnecessary_words = {"the", "a", "an", "is", "are", "was", "were", "that", "this", "there", "here"}
    words = text.split()
    filtered_text = " ".join([word for word in words if word.lower() not in unnecessary_words])
    return filtered_text

def preprocess_text(text):
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = correct_spelling(text)  # Correct spelling errors
    text = remove_unnecessary_words(text)  # Remove unnecessary words
    return text.strip()

def segment_into_paragraphs(text):
    doc = nlp(text)
    paragraphs = []
    current_paragraph = []
    
    for sent in doc.sents:
        current_paragraph.append(sent.text)
        if len(current_paragraph) >= 3:  # Form paragraphs of at least 3 sentences
            paragraphs.append(" ".join(current_paragraph))
            current_paragraph = []
    
    if current_paragraph:
        paragraphs.append(" ".join(current_paragraph))
    
    return "\n\n".join(paragraphs)

def compare_texts(original_text, cleaned_text):
    similarity_ratio = SequenceMatcher(None, original_text, cleaned_text).ratio()
    return similarity_ratio * 100  # Convert to percentage

def final_cleaning_check(original_text, cleaned_text):
    similarity = compare_texts(original_text, cleaned_text)
    print(f"Document similarity: {similarity:.2f}%")
    
    if similarity < 90:
        print("There are notable differences. Consider reviewing the cleaned text.")
    
    return cleaned_text

def save_extracted_text(extracted_text, output_path):
    with open(output_path, "w", encoding="utf-8") as text_file:
        text_file.write(extracted_text)

def main():
    pdf_path = r"C:\Users\Downloads\Sample.pdf"  # Actual file path
    output_path = r"C:\Users\Downloads\Sample.txt"  # Output file path

    extracted_text = extract_text_from_pdf(pdf_path)
    preprocessed_text = preprocess_text(extracted_text)
    segmented_text = segment_into_paragraphs(preprocessed_text)
    final_text = final_cleaning_check(extracted_text, segmented_text)
    save_extracted_text(final_text, output_path)
    print("Text extraction, spelling correction, unnecessary words removal, and segmentation completed. Saved to:", output_path)

if __name__ == "__main__":
    main()
