# Greenscale AI Python SDK

Python SDK for interacting with the Greenscale AI APIs.

## Installation

```bash
pip install greenscale-ai
```

## Usage

```python
from greenscale_ai import GreenscaleAI

# Initialize the SDK
app = GreenscaleAI()

# Scrape a URL
result = app.scrape_url("https://example.com")
```

## Free Trial vs API Key

### Free Trial

```python
# Free trial (no API key required)
app = GreenscaleAI()  # Uses default free trial key
result = app.scrape_url("https://example.com")
```

**Rate Limits**: Free trial is limited and shared across all users.

### Personal API Key

```python
# Using your personal API key
app = GreenscaleAI(api_key="your_api_key_here")
result = app.scrape_url("https://example.com")
```

**Rate Limits**: Personal API keys have more relaxed limits based on your subscription tier.

To get your personal API key, email us at hello@greenscale.ai

## Advanced Usage

You can customize the scraping behavior using optional parameters:

```python
# Example with all available parameters
params = {
    "formats": ["markdown", "html"],  # Output formats (default: ["markdown"])
    "include_metadata": True,         # Include page metadata (title, description, etc.)
    "include_menu_links": True        # Extract navigation menu links
}

result = app.scrape_url("https://example.com", params=params)
```

### Parameters Explanation:

- `formats`: List of desired output formats. Available options: "markdown" and "html"
- `include_metadata`: When True, returns page metadata like title, description, OpenGraph and custom tags
- `include_menu_links`: When True, extracts and returns navigation menu links from the page
