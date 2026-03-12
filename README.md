# BrandDeck - Website to Presentation Converter

Transform any website into a professional, brand-consistent PowerPoint template in seconds.

![BrandDeck](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.12-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

## 🎨 Features

- **Automatic Brand Extraction:** Analyzes any website and extracts colors, fonts, and design elements
- **10 Unique Slides:** Each slide uses a different color scheme from the brand palette
- **WCAG Compliant:** Guarantees readable text with 4.5:1 contrast ratio
- **Professional Output:** Production-ready presentations for creative directors
- **Font Detection:** Captures and downloads web fonts automatically
- **Shape Matching:** Replicates button styles (rounded, pill, or sharp)
- **Comprehensive Guide:** Generates detailed brand guideline documentation

## 🚀 Quick Start

### Web Interface

```bash
python app.py
```

Visit http://localhost:5000 and enter any website URL.

### Command Line

```bash
python brand_agency_generator.py https://example.com
```

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/branddeck.git
cd branddeck

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

## 🎯 What You Get

When you input a website URL, BrandDeck generates:

1. **Master Template PPTX** - 10 professionally designed slides
2. **Brand Guideline** - Markdown file with complete style guide
3. **Font Files** - Downloaded web fonts (.woff2)
4. **ZIP Package** - Everything bundled for easy sharing

## 🛠️ Technology Stack

- **Python 3.12**
- **Flask** - Web framework
- **Playwright** - Headless browser for style extraction
- **python-pptx** - PowerPoint generation
- **BeautifulSoup4** - HTML parsing
- **Gunicorn** - Production server

## 📖 Documentation

- [Usage Guide](USAGE_GUIDE.md) - Detailed usage instructions
- [Improvements Summary](IMPROVEMENTS_SUMMARY.md) - Technical enhancements
- [Deployment Guide](DEPLOYMENT_GUIDE.md) - How to deploy

## 🎨 How It Works

1. **Analysis:** Playwright renders the website and extracts computed CSS styles
2. **Extraction:** Identifies primary/secondary colors, fonts, and shape styles
3. **Generation:** Creates 10 unique slides with different color combinations
4. **Validation:** Ensures all text meets WCAG accessibility standards
5. **Packaging:** Bundles everything into a downloadable ZIP file

## 🌈 Color Palette

BrandDeck extracts up to **8 brand colors**:
- Primary Color (main brand identifier)
- Secondary Color (supporting color)
- 5 Accent Colors (for diversity)
- Lightest Neutral (clean backgrounds)

Each slide uses a unique combination for visual variety while maintaining brand consistency.

## ✅ Text Readability

Every text element is automatically checked against its background:
- Calculates WCAG contrast ratio
- Enforces minimum 4.5:1 ratio
- Automatically switches to white/black if needed
- Works with complex backgrounds

## 🎭 Slide Themes

- **Slide 1 (Title):** Primary color background
- **Slides 2-9 (Content):** Rotating color schemes
- **Slide 10 (Conclusion):** Secondary color background

## 📊 Examples

### Input
```
https://apple.com
```

### Output
- ✓ Colors: #0071E3, #0066CC, #1D1D1F, #000000, #FFFFFF
- ✓ Fonts: SF Pro Text, SF Pro Display
- ✓ Style: Sharp edges (0px border-radius)
- ✓ 10 slides with Apple's brand identity

## 🔒 Rate Limiting

Optional rate limiting to prevent abuse:

```python
@limiter.limit("5 per hour")
```

Limits each IP to 5 generations per hour.

## 🌐 Deployment

Deploy to:
- **Render** (recommended, free tier)
- **Railway**
- **Your own server**

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for details.

## 🤝 Contributing

Contributions welcome! Please read our contributing guidelines first.

## 📝 License

MIT License - feel free to use for personal and commercial projects.

## 👤 Author

**Mascha Sheludiakova**
- Website: [mascha.tech](https://mascha.tech)
- LinkedIn: [mascha-sheludiakova](https://www.linkedin.com/in/mascha-sheludiakova/)
- Role: Visual Artist, Creative Technologist

## 🙏 Acknowledgments

- Built with Python and modern web technologies
- Inspired by the need for rapid brand-consistent presentation creation
- Designed for creative directors and marketing teams

## 📧 Support

For issues or questions, please open an issue on GitHub.

---

*Transform any brand website into a professional presentation template in seconds.*
