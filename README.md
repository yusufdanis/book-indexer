# book-indexer

**book-indexer** is a suite of tools designed to streamline the process of generating structured indexes from Markdown documents using the OpenAI API. Whether you're managing a large collection of documents or looking to automate index creation, book-indexer provides the necessary utilities to enhance your workflow.

Special thanks to the [Original Repository](https://github.com/kevingoldsmith/openaitools) for providing the inspiration for this project.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Creating Index Files](#creating-index-files)
  - [Combining Index Files](#combining-index-files)
  - [Converting DOCX to Markdown](#converting-docx-to-markdown)
  - [Extracting Terms](#extracting-terms)
  - [Main Pipeline](#main-pipeline)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Automated Index Generation:** Automatically generate JSON-formatted structured indexes from a collection of Markdown files.
- **Flexible Document Conversion:** Convert DOCX and PDF files to Markdown using provided shell scripts.
- **Master Index Compilation:** Combine individual index files into a comprehensive master index for easy access and management.
- **Term Extraction:** Extract and organize terms from the master index into a sorted list for quick reference.
- **Error Handling:** Robust error handling to ensure smooth execution and easy troubleshooting.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/openaitools.git
   cd openaitools
   ```

2. **Install Dependencies**

   Ensure you have Python 3.7 or higher installed. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. **Install Additional Tools**

   - **Pandoc:** Required for document conversions. Install Pandoc from [here](https://pandoc.org/installing.html).
   - **ImageMagick:** Required for image processing in PDF conversions. Install ImageMagick from [here](https://imagemagick.org/script/download.php).
   - **Tesseract OCR:** Required for OCR operations. Install Tesseract from [here](https://github.com/tesseract-ocr/tesseract).

## Configuration

1. **Set Up OpenAI API Key**

   Create a file named `openaiconfig.ini` in the root directory with the following content:

   ```ini
   [keys]
   openaikey = <your_open_ai_key>
   ```

   Replace `<your_open_ai_key>` with your actual OpenAI API key.

## Usage

### Creating Index Files

Generate JSON index files from Markdown documents located in the `data/mds` directory.

```bash
python create_index_files.py
```

### Combining Index Files

Combine all individual index JSON files into a single `master_index.json`.

```bash
python combine_indexes.py
```

### Converting DOCX to Markdown

Use the provided shell script to convert DOCX files to Markdown. Ensure you have the necessary permissions to execute the script.

```bash
./convert_docx_to_md.sh input.docx output.md
```

**Parameters:**
- `input.pdf`: Path to the input PDF file.
- `output.md`: Path where the converted Markdown file will be saved.
- `crop_amount`: Number of pixels to crop from the image borders.
- `language`: Language settings for OCR (e.g., `tur+eng`).

**Example:**

```bash
./convert_docx_to_md.sh input.docx output.md 100 tur+eng
```

### Extracting Terms

Extract and sort terms from the `data/master_index.json` into `data/index.txt`.

```bash
python extract_terms.py
```

### Main Pipeline

Run the entire pipeline: create index files, combine them, and extract terms.

```bash
python main_pipeline.py
```


## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. **Fork the Repository**

2. **Create a New Branch**

```bash
   git checkout -b feature/YourFeatureName
```

3. **Make Your Changes**

4. **Commit Your Changes**

```bash
   git commit -m "Add some feature"
```

5. **Push to the Branch**

```bash
   git push origin feature/YourFeatureName
```

6. **Open a Pull Request**

Please ensure your code follows the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.