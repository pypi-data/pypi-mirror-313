# H@H Gallery Parser (h2h-galleryinfo-parser)

H@H Gallery Parser is a Python package designed to parse downloaded gallery files from H@H, a gallery download tool. When H@H downloads a gallery, it creates a folder named after the gallery, containing image files and a `galleryinfo.txt` file. This package helps extract useful information from the `galleryinfo.txt` file for further use.

## Features

The package provides three core functionalities:

1. **Parse Gallery ID**: Extract the gallery ID from a given gallery folder.

2. **Gallery Information Parsing**: The `GalleryInfoParser` class represents a parser for extracting detailed gallery information, including the gallery name, ID, paths of files, modification time, title, upload and download times, comments, uploader account, tags, and the number of pages.

3. **Parse Gallery Information**: Extracts all relevant details from the given folder and returns an instance of `GalleryInfoParser` containing the parsed information.

## Installation

You can install this package using pip:

```sh
pip install h2h-galleryinfo-parser
```

## Usage

Here's a quick example of how to use H@H Gallery Parser:

```python
from h2h_galleryinfo_parser import parse_gid, parse_galleryinfo

# Parse gallery ID from folder path
gallery_id = parse_gid('/path/to/gallery/folder')
print(f'Gallery ID: {gallery_id}')

# Parse gallery information
gallery_info = parse_galleryinfo('/path/to/gallery/folder')
print(f'Gallery Title: {gallery_info.title}')
print(f'Tags: {gallery_info.tags}')
```

## License

This project is distributed under the terms of the GNU General Public Licence (GPL). For detailed licence terms, see the `LICENSE` file included in this distribution.
