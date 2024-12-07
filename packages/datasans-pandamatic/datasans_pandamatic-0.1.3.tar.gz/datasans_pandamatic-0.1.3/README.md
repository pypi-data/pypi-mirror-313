# Datasans Pandamatic

An AI-powered code generator for dataframe processing.

## Installation

```bash
pip install datasans-pandamatic
```

## Usage

```python
from datasans_pandamatic import PandaMatic

# Initialize with your key code
generator = PandaMatic(key_code="your-key-code")

# With proxy (optional)
generator = PandaMatic(key_code="your-key-code", proxy="http://your-proxy:port")

# Define your dataframe
df = pd.read_csv("your_data.csv")

# Use the generator
code = generator.gencode(df, "Your prompt here")
code
```

## Features

- AI-powered code generation
- Smart data type handling
- Comprehensive error handling
- Powered by Open AI GPT 4o Mini

## Changelog

### 0.1.3
- Fixed OpenAI client initialization with httpx
- Improved proxy handling and configuration
- Added timeout settings
- Updated error messages

### 0.1.2
- Fixed OpenAI client initialization
- Added proper proxy handling
- Improved error handling
- Added httpx dependency

### 0.1.1
- Fixed module import issues
- Improved package structure
- Updated documentation

### 0.1.0
- Initial release
