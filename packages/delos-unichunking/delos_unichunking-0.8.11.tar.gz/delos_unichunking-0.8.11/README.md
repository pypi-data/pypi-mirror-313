# Unichunking

Extract LLM-friendly chunks from any file type.

Supported file types are :

 - DOCX & DOCX-like (DOC, ODT)
 - PPTX & PPTX-like (PPT, ODP)
 - XLSX & XLSX-like (XLS, ODS)
 - TXT, MD, CSV
 - IPYNB

# Installation

To install, run the following command:

```bash
python3 -m pip install delos-unichunking
```

# How to use

The main functions are :

 - `extract_subchunks` returns a list of all the text particles in the file.
 - `split_chunks_with_overlap` transforms a list of subchunks on a given page into a list of chunks following default or specified parameters for minimum/maximum token size and overlap.
 - `build_chunked_pages` returns a list of "pages", which are lists of formated chunks, following the structure of the document.
 - `compute_pages` approximates the pagination of a file that does not have a native pagination system (such as DOCX) by comparing it to a PDF version.

# Specificities

Please note that the package requires a LibreOffice installation to run `soffice` commands, used during file conversions : for instance, DOC/ODT are first converted to DOCX format and processed as such.

The page numbers computed for DOCX files are an approximation and can be off by a few pages for large files.

Artifical page numbers are used for page-less structures such as TXT files, or to split large XLSX sheets into multiple pages, to follow a tokens-per-page limit.
