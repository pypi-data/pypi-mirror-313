# hex_htmltoimg

Convert HTML to images with ease and flexibility! 🖼️✨

## Overview

`hex_htmltoimg` is a powerful Python module that transforms HTML files into high-quality images with dynamic content replacement and customizable rendering.

## 🌟 Features

- **HTML to Image Conversion**: Seamlessly transform HTML content into crisp, professional images
- **Dynamic Content Placeholders**: Replace placeholders with personalized, real-time content
- **Flexible Image Sizing**: Customize output image dimensions effortlessly
- **Unique Filename Generation**: Automatically create distinct filenames for each generated image
- **Image Resizing**: Adjust image sizes post-generation with built-in tools

## 🚀 Installation

Install the module quickly using pip:

```bash
pip install hex_htmltoimg
```

## 💡 Usage Examples

### Basic Usage

```python
from hex_htmltoimg import generate_image_from_html

# Path to your HTML template
html_file_path = 'template.html'

# Dynamic content replacements
replacements = {
    '{{title}}': 'Hello, World!',
    '{{content}}': 'Dynamically generated image magic!'
}

# Generate image with custom dimensions
image_filename = generate_image_from_html(
    html_file_path, 
    replacements, 
    width=800, 
    height=600
)

print(f"Image saved: {image_filename}")
```

### HTML Template Example

```html
<!DOCTYPE html>
<html>
<body>
    <h1>{{header}}</h1>
    <p>{{content}}</p>
    <footer>{{footer}}</footer>
</body>
</html>
```

## 🔧 Parameters

| Parameter    | Description                                | Default |
|--------------|--------------------------------------------|---------| 
| `file_path`  | Path to the HTML file                      | Required |
| `replacements` | Dictionary of placeholder replacements    | {} |
| `width`      | Output image width                         | 650px |
| `height`     | Output image height                        | 1250px |

## ⚠️ Error Handling

The module handles various scenarios:
- Raises `FileNotFoundError` if HTML file is missing
- Validates width and height as positive integers
- Manages image generation exceptions

## 📄 License

MIT License - Free for personal and commercial use.

## 🤝 Contributing

Contributions are welcome! 
- Fork the repository
- Submit issues
- Create pull requests

## 📞 Support

For more information, check the [project repository](https://github.com/azharbhat-dev/hex_htmltoimg).

*Generated with ❤️ by azharbhat-dev*