# FastParser 🚀

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A high-performance, asynchronous content parser that supports both HTML and PDF extraction with special handling for arXiv papers.

## ✨ Features

- 🚄 Asynchronous content fetching
- 📄 PDF extraction support
- 🌐 HTML parsing
- 📚 Special handling for arXiv URLs
- 📦 Batch processing capability
- 🔄 Progress tracking with tqdm

## 🛠️ Installation

```bash
pip install fastparser

# Dependencies
pip install aiohttp PyPDF2 tqdm
```

## 🚀 Quick Start

```python
from fastparser import parse

# Single URL parsing
text = parse("https://example.com")

# Batch processing
urls = [
    "https://example.com",
    "https://arxiv.org/abs/2301.01234",
    "https://example.com/document.pdf"
]
texts = parse(urls)
```

## 📖 Detailed Usage

### Basic Parser Configuration

```python
from fastparser import FastParser

# Initialize with PDF extraction (default: True)
parser = FastParser(extract_pdf=True)

# Single URL
content = parser.fetch("https://example.com")

# Multiple URLs
contents = parser.fetch_batch([
    "https://example.com",
    "https://arxiv.org/abs/2301.01234"
])
```

### Working with arXiv Papers

The parser automatically handles different arXiv URL formats:

```python
parser = FastParser()

# These will be automatically converted to appropriate formats
urls = [
    "https://arxiv.org/abs/2301.01234",  # Will fetch PDF if extract_pdf=True
    "http://arxiv.org/html/2301.01234",  # Will fetch HTML or PDF based on settings
]
contents = parser.fetch_batch(urls)
```

### PDF-Only Processing

```python
parser = FastParser(extract_pdf=True)

pdf_urls = [
    "https://example.com/document.pdf",
    "https://arxiv.org/pdf/2301.01234.pdf"
]
pdf_contents = parser.fetch_batch(pdf_urls)
```

## 🔧 API Reference

### FastParser Class

```python
class FastParser:
    def __init__(self, extract_pdf: bool = True)
    def fetch(self, url: str) -> str
    def fetch_batch(self, urls: list) -> list
    def __call__(self, urls: str|list) -> str|list
```

### Main Functions

- `parse(urls: str|list) -> str|list`: Convenience function for quick parsing
- `_async_html_parser(urls: list)`: Internal async processing method
- `_fetch_pdf_content(pdf_urls: list)`: Internal PDF processing method
- `_arxiv_url_fix(url: str)`: Internal arXiv URL formatting method

## ⚡ Performance

The parser uses asynchronous operations for optimal performance:

- Concurrent URL fetching
- Batch processing capabilities
- Progress tracking with tqdm
- Memory-efficient PDF processing

## 🔍 Example: Advanced Usage

```python
import asyncio
from fastparser import FastParser

async def process_large_dataset():
    parser = FastParser(extract_pdf=True)
    
    # Process URLs in batches
    all_urls = ["url1", "url2", ..., "url1000"]
    batch_size = 50
    
    results = []
    for i in range(0, len(all_urls), batch_size):
        batch = all_urls[i:i + batch_size]
        batch_results = parser.fetch_batch(batch)
        results.extend(batch_results)
        
    return results

# Run with asyncio
results = asyncio.run(process_large_dataset())
```

## ⚠️ Error Handling

The parser includes robust error handling:

- Failed URL fetches return empty strings
- PDF processing errors are caught gracefully
- HTTP status checks
- Invalid URL format handling

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Dependencies

- `aiohttp`: Async HTTP client/server framework
- `PyPDF2`: PDF processing library
- `tqdm`: Progress bar library
- Custom `FastHTMLParserV3` module

## 📋 TODO

- [ ] Add support for more document types
- [ ] Implement caching mechanism
- [ ] Add timeout configurations
- [ ] Improve error reporting
- [ ] Add proxy support

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Made with ❤️ by [Your Name]