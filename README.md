# Metadata Cleaner 📄🔍

## Overview
This script allows you to extract and remove metadata from various file types, including:
- **Images**: JPEG, PNG, HEIC
- **Documents**: PDF, DOCX, PPTX, XLSX
- **Videos**: MP4, MOV, AVI, MKV

## Features
- Extract metadata from supported file types
- Remove metadata from images, PDFs, and Office documents
- Save cleaned files in the `cleaned_files/` directory

## Installation

**Clone the repository**
```bash
git clone https://github.com/lytexdev/metadata-cleaner.git
cd metadata-cleaner
```

**Create a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Install dependencies**
```bash
pip install -r requirements.txt
```

## Usage
### Extract and remove metadata
Run the script with the file you want to inspect:
```bash
python metadata_cleaner.py path/to/file
```
**Lists all metadata in the file and asks you if you want to remove it.**

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
