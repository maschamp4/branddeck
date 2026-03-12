# GitHub Setup & Deployment - Quick Guide

## 📋 Pre-Deployment Checklist

Before pushing to GitHub, make sure you have:

- ✅ All deployment files created (I did this for you!)
- ✅ Marketing_Agency_Template.pptx in the root folder
- ✅ Git installed on your computer
- ✅ GitHub account created

## 🚀 Step-by-Step GitHub Setup

### Step 1: Create GitHub Repository

1. Go to https://github.com
2. Click the "+" icon → "New repository"
3. **Repository name:** `branddeck`
4. **Description:** "Transform any website into a branded PowerPoint template"
5. **Visibility:** Choose:
   - **Public** - Anyone can see and use
   - **Private** - Only you (and invited collaborators) can see
6. **Do NOT check:** "Initialize with README" (we have one)
7. Click "Create repository"

### Step 2: Push Code to GitHub

Open your terminal in the Brand_Agency_Generator folder:

```bash
# Navigate to the folder
cd C:\Users\Mascha\Desktop\Mascha_Tools\Brand_Agency_Generator

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: BrandDeck v1.0"

# Add GitHub as remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/branddeck.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Note:** Replace `YOUR_USERNAME` with your actual GitHub username!

### Step 3: Verify Upload

Go to your GitHub repository page and verify you see:
- ✓ app.py
- ✓ brand_agency_generator.py
- ✓ requirements.txt
- ✓ Procfile
- ✓ templates/index.html
- ✓ Marketing_Agency_Template.pptx
- ✓ README.md

## 🌐 Deploy to Render (Easiest Option)

### Step 1: Create Render Account

1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub (easiest - auto-connects your repos)

### Step 2: Deploy Web Service

1. In Render Dashboard, click "New +" → "Web Service"
2. Find and select your `branddeck` repository
3. Configure settings:

```
Name: branddeck
Environment: Python 3
Region: Choose closest to your users (Europe for Germany)
Branch: main
Build Command: pip install -r requirements.txt && playwright install chromium
Start Command: gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 300 app:app
Instance Type: Free
```

4. Click "Create Web Service"

### Step 3: Wait for Deployment

- First deployment takes 5-10 minutes (installing Playwright)
- Watch the logs in real-time
- When you see "Your service is live 🎉", it's ready!

### Step 4: Test Your Deployment

Your app will be at: `https://branddeck-XXXX.onrender.com`

Test it:
1. Click the URL in Render dashboard
2. Enter a website (e.g., https://apple.com)
3. Click "Generate Slides"
4. Download and verify the output

## 🔗 Add Custom Domain (Optional)

### Option A: Subdomain (Recommended)

Use `branddeck.mascha.tech`:

1. In Render Dashboard → Your Service → "Settings"
2. Scroll to "Custom Domain"
3. Click "Add Custom Domain"
4. Enter: `branddeck.mascha.tech`
5. Render will show you a CNAME record

Then in your domain DNS (where you manage mascha.tech):
```
Type: CNAME
Name: branddeck
Value: [value provided by Render]
TTL: Automatic or 3600
```

Wait 5-60 minutes for DNS propagation.

### Option B: Path-Based (mascha.tech/tools/branddeck)

This requires a reverse proxy on your main mascha.tech server.

**If you use Nginx:**

Add to your mascha.tech nginx config:
```nginx
location /tools/branddeck {
    proxy_pass https://branddeck-XXXX.onrender.com;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_read_timeout 300;
}
```

Reload nginx:
```bash
sudo nginx -t
sudo systemctl reload nginx
```

## 🔐 Access Control Options

### Make It Public (Anyone Can Use)

**Current State:** Already public! Anyone with the URL can use it.

**Pros:**
- ✅ Great for portfolio/showcase
- ✅ Helps other designers
- ✅ Can go viral
- ✅ No maintenance needed

**Cons:**
- ❌ Server costs if too popular (Free tier: 500 hours/month)
- ❌ No control over who uses it

**Add to your portfolio:**
```html
<div class="project-card">
    <h3>BrandDeck</h3>
    <p>Transform any website into a branded presentation</p>
    <a href="https://branddeck.mascha.tech">Try it now →</a>
</div>
```

### Make It Private (Invite Only)

**Option 1: Simple Password**

Add to `app.py` before the routes:
```python
from functools import wraps
from flask import request, Response

PASSWORD = "your_secret_password_here"  # Change this!

def check_auth(password):
    return password == PASSWORD

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.password):
            return Response(
                'Login Required', 401,
                {'WWW-Authenticate': 'Basic realm="BrandDeck"'}
            )
        return f(*args, **kwargs)
    return decorated

# Add @requires_auth to both routes:
@app.route('/')
@requires_auth
def index():
    ...

@app.route('/', methods=['POST'])
@requires_auth  
def generate():
    ...
```

Then commit and push:
```bash
git add app.py
git commit -m "Added password protection"
git push
```

Render will auto-deploy the update.

**To access:** Browser will prompt for password.

**Option 2: Rate Limiting (Recommended for Public)**

Add to `requirements.txt`:
```
Flask-Limiter==3.5.0
```

Add to `app.py`:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["10 per day", "3 per hour"],
    storage_uri="memory://"
)

@app.route('/', methods=['POST'])
@limiter.limit("5 per hour")  # Max 5 generations per hour per IP
def generate():
    ...
```

This prevents abuse while keeping it public.

## 📊 Monitor Usage

### View Logs in Render

1. Dashboard → Your Service
2. Click "Logs" tab
3. See real-time requests

### Add Google Analytics (Optional)

In `templates/index.html`, add before `</head>`:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');  // Your GA4 ID
</script>
```

## 🔄 Update Your App

Whenever you make changes:

```bash
# Make your changes to the code
# Then:
git add .
git commit -m "Description of changes"
git push

# Render automatically redeploys (takes 2-3 minutes)
```

## 💾 Backup Strategy

### Option 1: Git is Your Backup
Your code is safe on GitHub. Regenerate anytime.

### Option 2: Export Generated Files
Add download button to save user generations:
```python
# Already implemented in app.py!
# Users download ZIP files automatically
```

## 🎯 Integration with mascha.tech

### Add to Your Website Navigation

```html
<nav class="tools">
    <a href="https://branddeck.mascha.tech">
        <h4>BrandDeck</h4>
        <p>Website → Presentation</p>
    </a>
</nav>
```

### Create a Dedicated Tools Page

Create `mascha.tech/tools/index.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Tools | Mascha Sheludiakova</title>
</head>
<body>
    <h1>Creative Tools</h1>
    
    <div class="tool-grid">
        <a href="https://branddeck.mascha.tech" class="tool-card">
            <h2>BrandDeck</h2>
            <p>Transform any website into a branded PowerPoint template</p>
            <span class="badge">Free Tool</span>
        </a>
        
        <!-- Add more tools here -->
    </div>
</body>
</html>
```

## ✅ Final Checklist

Before you announce it publicly:

- [ ] Test on 5 different websites
- [ ] Verify all downloads work
- [ ] Check mobile responsiveness
- [ ] Add your branding (logo, colors)
- [ ] Setup monitoring/analytics
- [ ] Decide: Public or Private?
- [ ] Add rate limiting if public
- [ ] Create social media graphics
- [ ] Write announcement post
- [ ] Add to your portfolio

## 🎉 You're Ready!

### Public Launch Checklist:

1. **Share on LinkedIn:**
   ```
   🎨 Excited to launch BrandDeck!
   
   Turn any website into a branded PowerPoint template in seconds.
   
   Perfect for:
   ✓ Marketing agencies
   ✓ Brand designers  
   ✓ Creative directors
   
   Try it: https://branddeck.mascha.tech
   
   #design #branding #tools
   ```

2. **Share on Twitter/X:**
   ```
   🚀 Just launched BrandDeck - transform any website 
   into a presentation template instantly
   
   → Extract brand colors
   → Match fonts
   → 10 ready-to-use slides
   → Free to use
   
   Try it: branddeck.mascha.tech
   ```

3. **Add to Portfolio:**
   - Screenshots of the tool
   - Example outputs (Apple, Nike, etc.)
   - Technical challenges solved
   - Impact metrics

## 📞 Need Help?

Common issues and solutions in [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

**Ready to deploy?** Start with Step 1 above! 🚀
