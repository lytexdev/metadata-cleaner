from PIL import Image
from PIL.ExifTags import TAGS
import pypdf
import os
import argparse

def extract_pdf_metadata(file_path):
    try:
        with open(file_path, "rb") as pdf_file:
            reader = pypdf.PdfReader(pdf_file)
            metadata = reader.metadata
            return {key[1:]: value for key, value in metadata.items() if value}
    except Exception as e:
        print(f"Error extracting metadata from PDF: {e}")
        return {}

def remove_pdf_metadata(file_path, output_path):
    try:
        with open(file_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            writer = PyPDF2.PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            writer.add_metadata({})
            with open(output_path, "wb") as output_pdf:
                writer.write(output_pdf)
        print(f"Metadata removed from PDF. Saved as {output_path}")
    except Exception as e:
        print(f"Error removing metadata from PDF: {e}")

def start():
    parser = argparse.ArgumentParser(description="Metadata Extractor and Cleaner")
    parser.add_argument("file", help="Path to the file")
    args = parser.parse_args()
    
    file_path = args.file
    if not os.path.exists(file_path):
        print("File not found!")
        return
    
    ext = os.path.splitext(file_path)[1].lower()
    metadata = {}

    if ext == ".pdf":
        metadata = extract_pdf_metadata(file_path)
    else:
        print("Unsupported file type.")
        return
    
    if metadata:
        print("\nExtracted Metadata:")
        for key, value in metadata.items():
            print(f"{key}: {value}")
        
        choice = input("\nDo you want to remove all metadata? (y/N): ")
        if choice.lower() == "y" or choice.lower() == "yes":
            output_path = "cleaned_" + os.path.basename(file_path)
            if ext == ".pdf":
                remove_pdf_metadata(file_path, output_path)
        else:
            print("Metadata was not removed.")
    else:
        print("No metadata found.")

if __name__ == "__main__":
    start()
