from PIL import Image
from PIL.ExifTags import TAGS
import pypdf
import piexif
import os
import argparse
import mutagen
import docx
import olefile
import pandas as pd
import shutil

def extract_image_metadata(file_path):
    try:
        image = Image.open(file_path)
        exif_data = image.info.get("exif")
        metadata = {}
        if exif_data:
            exif_dict = piexif.load(exif_data)
            for tag, value in exif_dict["0th"].items():
                decoded = TAGS.get(tag, tag)
                metadata[decoded] = tag
        return metadata, exif_dict
    except:
        return {}, {}

def remove_image_metadata(file_path, output_path, keys_to_remove=None):
    try:
        image = Image.open(file_path)
        exif_data = image.info.get("exif")
        if exif_data:
            exif_dict = piexif.load(exif_data)
            if keys_to_remove:
                for tag in keys_to_remove:
                    tag_id = TAGS.get(tag)
                    if tag_id in exif_dict["0th"]:
                        del exif_dict["0th"][tag_id]
            else:
                exif_dict["0th"] = {}
            exif_bytes = piexif.dump(exif_dict)
            image.save(output_path, exif=exif_bytes)
        else:
            image.save(output_path)
    except:
        pass

def extract_pdf_metadata(file_path):
    try:
        with open(file_path, "rb") as pdf_file:
            reader = pypdf.PdfReader(pdf_file)
            metadata = reader.metadata
            return {key[1:]: value for key, value in metadata.items() if value}, metadata
    except:
        return {}, {}

def remove_pdf_metadata(file_path, output_path, keys_to_remove=None):
    try:
        with open(file_path, "rb") as pdf_file:
            reader = pypdf.PdfReader(pdf_file)
            writer = pypdf.PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            metadata = dict(reader.metadata)
            if keys_to_remove:
                for key in keys_to_remove:
                    if f'/{key}' in metadata:
                        del metadata[f'/{key}']
                writer.add_metadata(metadata)
            else:
                writer.add_metadata({})
            with open(output_path, "wb") as output_pdf:
                writer.write(output_pdf)
    except:
        pass

def extract_audio_video_metadata(file_path):
    try:
        metadata = mutagen.File(file_path, easy=True)
        return metadata.info if metadata else {}
    except:
        return {}

def extract_office_metadata(file_path):
    try:
        ext = os.path.splitext(file_path)[1].lower()
        metadata = {}
        if ext in [".docx", ".pptx", ".xlsx"]:
            doc = docx.Document(file_path)
            metadata = {
                'title': doc.core_properties.title,
                'author': doc.core_properties.author,
                'subject': doc.core_properties.subject,
                'keywords': doc.core_properties.keywords,
                'last_modified_by': doc.core_properties.last_modified_by,
                'created': doc.core_properties.created,
                'modified': doc.core_properties.modified,
                'comments': doc.core_properties.comments
            }
        elif ext in [".doc", ".ppt", ".xls"]:
            ole = olefile.OleFileIO(file_path)
            if ole.exists('SummaryInformation'):
                metadata = ole.get_metadata().__dict__
        return {k: v for k, v in metadata.items() if not k.startswith("_")}
    except:
        return {}

def remove_office_metadata(file_path, output_path):
    try:
        ext = os.path.splitext(file_path)[1].lower()
        if ext in [".docx", ".pptx", ".xlsx"]:
            doc = docx.Document(file_path)
            core_props = doc.core_properties
            core_props.last_modified_by = None
            core_props.title = None
            core_props.author = None
            core_props.subject = None
            core_props.comments = None
            doc.save(output_path)
        elif ext in [".doc", ".ppt", ".xls"]:
            shutil.copy(file_path, output_path)
    except:
        pass

def start():
    parser = argparse.ArgumentParser(description="Extract and remove metadata from images, PDFs, documents, and videos.")
    parser.add_argument("file", help="Path to the file")
    parser.add_argument("--remove", action="store_true", help="Remove all metadata")
    args = parser.parse_args()
    
    file_path = args.file
    if not os.path.exists(file_path):
        print("Error: File not found!")
        exit(1)
    
    output_dir = "cleaned_files"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, os.path.basename(file_path))
    
    ext = os.path.splitext(file_path)[1].lower()
    metadata = {}
    
    if ext in [".jpg", ".jpeg", ".png", ".heic"]:
        metadata, _ = extract_image_metadata(file_path)
    elif ext == ".pdf":
        metadata, _ = extract_pdf_metadata(file_path)
    elif ext in [".doc", ".docx", ".odt", ".ppt", ".pptx", ".xls", ".xlsx"]:
        metadata = extract_office_metadata(file_path)
    elif ext in [".mp4", ".mov", ".avi", ".mkv"]:
        metadata = extract_audio_video_metadata(file_path)
    else:
        print("Error: Unsupported file type.")
        exit(1)
    
    if not metadata:
        print("No metadata found.")
        exit(0)
    
    print("\nExtracted Metadata:")
    for key, value in metadata.items():
        print(f"{key}: {value}")
    
    choice = input("\nRemove all metadata? (y/n): ").strip().lower()
    if choice == "y" or choice == "yes":
        if ext in [".jpg", ".jpeg", ".png", ".heic"]:
            remove_image_metadata(file_path, output_path)
        elif ext == ".pdf":
            remove_pdf_metadata(file_path, output_path)
        elif ext in [".doc", ".docx", ".odt", ".ppt", ".pptx", ".xls", ".xlsx"]:
            remove_office_metadata(file_path, output_path)
        else:
            shutil.copy(file_path, output_path)
        print(f"Metadata removed. Saved in {output_path}")
    else:
        print("Invalid input.")
        exit(1)


if __name__ == "__main__":
    start()
