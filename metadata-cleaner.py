from PIL import Image
from PIL.ExifTags import TAGS
import pypdf
import piexif
import os
import argparse

def extract_image_metadata(file_path):
    try:
        image = Image.open(file_path)
        exif_data = image.info.get("exif")
        metadata = {}
        if exif_data:
            exif_dict = piexif.load(exif_data)
            for tag, value in exif_dict["0th"].items():
                decoded = TAGS.get(tag, tag)
                metadata[decoded] = value
        return metadata
    except:
        return {}

def remove_image_metadata(file_path, output_path, keys_to_remove=None):
    try:
        image = Image.open(file_path)
        exif_data = image.info.get("exif")
        if exif_data:
            exif_dict = piexif.load(exif_data)
            if keys_to_remove:
                for tag in keys_to_remove:
                    if tag in exif_dict["0th"]:
                        del exif_dict["0th"][tag]
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
            return {key[1:]: value for key, value in metadata.items() if value}
    except:
        return {}

def remove_pdf_metadata(file_path, output_path, keys_to_remove=None):
    try:
        with open(file_path, "rb") as pdf_file:
            reader = pypdf.PdfReader(pdf_file)
            writer = pypdf.PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            metadata = reader.metadata
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

def start():
    parser = argparse.ArgumentParser(description="Extract and remove metadata from images (JPEG, PNG, HEIC) and PDFs.")
    parser.add_argument("file", help="Path to the file")
    parser.add_argument("--remove", action="store_true", help="Remove all metadata")
    args = parser.parse_args()
    
    file_path = args.file
    if not os.path.exists(file_path):
        print("Error: File not found!")
        exit(1)
    
    ext = os.path.splitext(file_path)[1].lower()
    metadata = {}
    if ext in [".jpg", ".jpeg", ".png", ".heic"]:
        metadata = extract_image_metadata(file_path)
    elif ext == ".pdf":
        metadata = extract_pdf_metadata(file_path)
    else:
        print("Error: Unsupported file type.")
        exit(1)
    
    if not metadata:
        print("No metadata found.")
        exit(0)
    
    print("\nExtracted Metadata:")
    keys = list(metadata.keys())
    for i, key in enumerate(keys):
        print(f"[{i}] {key}: {metadata[key]}")
    
    choice = input("\nRemove all metadata? (y/n): ").strip().lower()
    if choice == "y":
        output_path = "cleaned_" + os.path.basename(file_path)
        if ext in [".jpg", ".jpeg", ".png", ".heic"]:
            remove_image_metadata(file_path, output_path)
        elif ext == ".pdf":
            remove_pdf_metadata(file_path, output_path)
        print(f"Metadata removed. Saved as {output_path}")
    elif choice == "n":
        indices = input("Enter numbers of metadata fields to remove (comma-separated): ").strip()
        try:
            selected_keys = [keys[int(i)] for i in indices.split(",")]
        except:
            print("Invalid selection.")
            exit(1)
        output_path = "cleaned_" + os.path.basename(file_path)
        if ext in [".jpg", ".jpeg", ".png", ".heic"]:
            remove_image_metadata(file_path, output_path, selected_keys)
        elif ext == ".pdf":
            remove_pdf_metadata(file_path, output_path, selected_keys)
        print(f"Selected metadata removed. Saved as {output_path}")
    else:
        print("Invalid input.")
        exit(1)

if __name__ == "__main__":
    start()
