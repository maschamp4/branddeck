# Brand Agency Generator - Usage Guide

## Quick Start

### Command Line
```bash
python brand_agency_generator.py https://example.com
```

### Web Interface
```bash
python app.py
```
Then visit: http://localhost:5000

---

## What You Get

When you run the tool on any website, it automatically generates:

1. **`BrandName_Master_Template.pptx`**
   - 10 professionally designed slides
   - Each slide has a unique color scheme
   - All text guaranteed readable (WCAG AA compliant)
   - Brand fonts applied throughout
   - Shape styles matching website (rounded/sharp/pill)

2. **`BrandName_Brand_Guideline.md`**
   - Complete brand style guide
   - Typography specifications
   - Color palette (up to 8 colors)
   - Shape and UI element guidelines
   - Design principles
   - Automated validation checklist

3. **Font Files (`.woff2`)**
   - Primary and secondary fonts
   - Downloaded from website or Google Fonts
   - Instructions for PowerPoint installation

4. **`BrandName_Brand_Assets.zip`**
   - Everything packaged for easy sharing

---

## Understanding the Output

### Slide Color Schemes

Each slide uses a different combination of brand colors:

- **Slide 1 (Title Slide):** Primary color background
- **Slide 2-9 (Content Slides):** Rotating through:
  - Light backgrounds with colorful accents
  - Colorful backgrounds with contrasting accents
  - Different accent colors for visual variety
- **Slide 10 (Conclusion):** Secondary color background

### Text Readability

Every text element is automatically optimized:

- ✓ Checked against its actual background color
- ✓ Minimum 4.5:1 contrast ratio (WCAG AA)
- ✓ Automatically switched to white or black if needed
- ✓ Titles use primary font
- ✓ Body text uses secondary font

### Color Palette

The tool extracts and intelligently uses:

- **Primary Color:** Main brand identifier
- **Secondary Color:** Supporting color
- **Accent Colors 1-5:** Additional brand colors
- **Lightest Neutral:** Clean background color
- **Black/White:** Text and high-contrast elements

---

## Best Practices

### 1. Use Brand Websites
Point the tool at official brand websites for best results:
- ✓ `https://nike.com`
- ✓ `https://apple.com`
- ✓ `https://airbnb.com`

### 2. Check the Output
Always review the generated PPTX:
- Open `BrandName_Master_Template.pptx`
- Check each slide's color scheme
- Verify fonts are displaying correctly
- Read the validation checklist in the markdown

### 3. Install Fonts
For exact brand fonts:
1. Find `.woff2` files in the assets folder
2. Convert to `.ttf` using [CloudConvert](https://cloudconvert.com/woff2-to-ttf)
3. Install on your system
4. Restart PowerPoint

### 4. Customize Further
The generated template is a **starting point**:
- Modify text content
- Adjust layout elements
- Add images and graphics
- Maintain the color scheme and fonts

---

## Common Issues

### "Font not displaying correctly"
**Solution:** Install the font files (see step 3 above)

### "Colors look different than website"
**Solution:** The tool extracts computed styles. Some websites use images or gradients that can't be perfectly replicated in PowerPoint

### "Not enough colors extracted"
**Solution:** The tool prioritizes colorful brand colors over neutrals. If the website is very minimal, you'll get fewer colors

### "Text is all black or white"
**Solution:** This is intentional! The contrast verification system ensures readability. You can manually adjust if you prefer brand colors

---

## Advanced Features

### Validation Checklist
The markdown file includes an automated validation section:
```markdown
## 5. Automated Validation Checklist

- [x] Fonts match brand guidelines
- [x] Shape roundness matches border-radius style
- [x] Brand colors applied throughout slides
- [x] Layout modified from master template
- [x] Text contrast verified for readability (WCAG 4.5:1)
```

### Debug Output
Run with Python to see detailed extraction info:
```
=== COLOR PALETTE ===
Primary: #FF5733
Secondary: #3357FF
Accent 1: #33FF57
...

Processing Slide 1: BG=#FF5733, Accent=#3357FF
Processing Slide 2: BG=#FAFAFA, Accent=#FF5733
```

---

## Tips for Creative Directors

### Quick Brand Analysis
Use this tool to:
- Rapidly analyze competitor brands
- Extract color palettes for mood boards
- Create consistent client presentation templates
- Maintain brand guidelines across teams

### Customization Workflow
1. Generate base template
2. Review brand guideline markdown
3. Adjust specific slides as needed
4. Save as new template for team
5. Share zip file with collaborators

### Quality Checks
Always verify:
- [ ] Brand colors match website
- [ ] Fonts are correct (or acceptable substitutes)
- [ ] All text is readable
- [ ] Slide variety is sufficient
- [ ] Shape styles match brand (rounded vs. sharp)

---

## Technical Requirements

- Python 3.7+
- Playwright (for web scraping)
- python-pptx (for PowerPoint generation)
- Flask (for web interface)
- BeautifulSoup4 (for HTML parsing)

**Installation:**
```bash
pip install playwright python-pptx flask beautifulsoup4 requests
playwright install
```

---

## Troubleshooting

### Playwright Errors
```bash
playwright install chromium
```

### Missing Template
Ensure `Marketing_Agency_Template.pptx` is in the same directory as the script

### Subprocess Errors (Web Interface)
Make sure `brand_agency_generator.py` is in the same directory as `app.py`

---

## Support

For issues or questions:
1. Check the `IMPROVEMENTS_SUMMARY.md` for technical details
2. Review the generated validation checklist
3. Verify all dependencies are installed

---

*Transform any brand website into a professional presentation template in seconds.*
