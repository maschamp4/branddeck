# BrandDeck Deployment Guide
## Deploy to https://mascha.tech/tools/branddeck

---

## 🎯 Deployment Options

### Option 1: Deploy to Render (Recommended - Free & Easy)
**Best for:** Simple deployment with automatic SSL, free tier available

### Option 2: Deploy to Your Existing Server
**Best for:** If you already host mascha.tech on a server

### Option 3: Deploy to Railway
**Best for:** Easy deployment with free tier

---

## 📋 Prerequisites

1. **GitHub Account** (to host code)
2. **Hosting Platform Account** (Render, Railway, or your server)
3. **Domain Access** (to set up subdomain routing)

---

## 🚀 Step 1: Prepare for GitHub

### Create Required Files

I'll create these files for you:
- `requirements.txt` - Python dependencies
- `Procfile` - For deployment platforms
- `.gitignore` - Files to exclude from Git
- `runtime.txt` - Python version
- `README.md` - Project documentation

### What to Commit

```
Brand_Agency_Generator/
├── app.py
├── brand_agency_generator.py
├── requirements.txt
├── Procfile
├── runtime.txt
├── .gitignore
├── README.md
├── Marketing_Agency_Template.pptx  # Your template file
├── templates/
│   └── index.html
├── IMPROVEMENTS_SUMMARY.md
└── USAGE_GUIDE.md
```

---

## 🔧 Step 2: Deploy to Render (Recommended)

### Why Render?
- ✅ Free tier available (500 hours/month)
- ✅ Automatic HTTPS/SSL
- ✅ Easy GitHub integration
- ✅ Auto-deployment on push
- ✅ Custom domain support

### Steps:

1. **Push to GitHub:**
   ```bash
   cd Brand_Agency_Generator
   git init
   git add .
   git commit -m "Initial commit: BrandDeck tool"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/branddeck.git
   git push -u origin main
   ```

2. **Deploy on Render:**
   - Go to https://render.com
   - Sign up/Login with GitHub
   - Click "New +" → "Web Service"
   - Connect your `branddeck` repository
   - Configure:
     - **Name:** `branddeck`
     - **Environment:** `Python 3`
     - **Build Command:** `pip install -r requirements.txt && playwright install chromium`
     - **Start Command:** `gunicorn app:app`
     - **Instance Type:** `Free`
   - Click "Create Web Service"

3. **Custom Domain Setup:**
   - In Render dashboard, go to your service
   - Click "Settings" → "Custom Domain"
   - Add: `branddeck.mascha.tech` or `tools.mascha.tech`
   - Render will give you a CNAME record
   - Add this CNAME to your domain DNS:
     ```
     Type: CNAME
     Name: branddeck (or tools)
     Value: [provided by Render]
     ```

4. **Subdirectory Path (tools/branddeck):**
   
   Since Render deploys to root, you have two options:
   
   **Option A: Use subdomain**
   - Deploy at `branddeck.mascha.tech`
   - Then create a redirect from `mascha.tech/tools/branddeck` → `branddeck.mascha.tech`
   
   **Option B: Use reverse proxy**
   - Deploy on Render
   - On your main mascha.tech server, add nginx reverse proxy:
     ```nginx
     location /tools/branddeck {
         proxy_pass https://your-render-app.onrender.com;
         proxy_set_header Host $host;
         proxy_set_header X-Real-IP $remote_addr;
     }
     ```

---

## 🌐 Step 3: Alternative - Deploy to Your Server

### If you have SSH access to mascha.tech server:

1. **Upload Files:**
   ```bash
   scp -r Brand_Agency_Generator user@mascha.tech:/var/www/branddeck
   ```

2. **Install Dependencies:**
   ```bash
   ssh user@mascha.tech
   cd /var/www/branddeck
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   playwright install chromium
   ```

3. **Run with Gunicorn:**
   ```bash
   gunicorn --bind 0.0.0.0:8000 --workers 2 --timeout 300 app:app
   ```

4. **Setup Nginx Reverse Proxy:**
   ```nginx
   server {
       server_name mascha.tech;
       
       location /tools/branddeck {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_read_timeout 300;
       }
   }
   ```

5. **Setup Systemd Service (Auto-restart):**
   
   Create `/etc/systemd/system/branddeck.service`:
   ```ini
   [Unit]
   Description=BrandDeck Web Application
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/var/www/branddeck
   Environment="PATH=/var/www/branddeck/venv/bin"
   ExecStart=/var/www/branddeck/venv/bin/gunicorn --bind 0.0.0.0:8000 --workers 2 --timeout 300 app:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```
   
   Enable and start:
   ```bash
   sudo systemctl enable branddeck
   sudo systemctl start branddeck
   ```

---

## 🔐 Access Control & Security

### Will Everyone Be Able to Use It?

**Yes, by default** - anyone who visits the URL can use it.

### Options to Restrict Access:

#### Option 1: Simple Password Protection
Add to `app.py`:
```python
from functools import wraps
from flask import request, Response

def check_auth(username, password):
    return username == 'admin' and password == 'your_secure_password'

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return Response('Login Required', 401, 
                          {'WWW-Authenticate': 'Basic realm="Login Required"'})
        return f(*args, **kwargs)
    return decorated

@app.route('/')
@requires_auth
def index():
    # ... existing code
```

#### Option 2: IP Whitelist
```python
ALLOWED_IPS = ['your.ip.address', '192.168.1.1']

@app.before_request
def limit_remote_addr():
    if request.remote_addr not in ALLOWED_IPS:
        abort(403)
```

#### Option 3: Token-Based Access
```python
SECRET_TOKEN = "your_secret_token_here"

@app.before_request
def check_token():
    token = request.args.get('token') or request.headers.get('X-Access-Token')
    if token != SECRET_TOKEN:
        abort(403)
```

#### Option 4: Rate Limiting
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["5 per hour"]  # Max 5 generations per hour per IP
)

@app.route('/', methods=['POST'])
@limiter.limit("5 per hour")
def generate():
    # ... existing code
```

---

## ⚡ Performance & Scaling

### Expected Resource Usage:
- **CPU:** High during generation (Playwright + image processing)
- **Memory:** ~500MB per request
- **Time:** 15-30 seconds per generation
- **Storage:** Each generation creates ~5-20MB of files

### Recommendations:

1. **Use Background Jobs** (for better UX):
   - Install Redis and Celery
   - Process generations asynchronously
   - Show progress bar to user

2. **Cleanup Generated Files:**
   ```python
   import schedule
   
   def cleanup_old_files():
       # Delete files older than 1 hour
       os.system('find . -name "*_Brand_Assets*" -mmin +60 -delete')
   
   schedule.every().hour.do(cleanup_old_files)
   ```

3. **Set Request Timeout:**
   - Gunicorn: `--timeout 300` (5 minutes)
   - Nginx: `proxy_read_timeout 300;`

4. **Monitor Usage:**
   - Add Google Analytics to track usage
   - Log generations to file for analysis

---

## 🔄 Auto-Deployment (GitHub → Render)

Once set up, any push to GitHub automatically redeploys:

```bash
# Make changes
git add .
git commit -m "Updated feature"
git push

# Render automatically rebuilds and deploys
```

---

## 📊 Monitoring & Logs

### View Logs on Render:
- Dashboard → Your Service → "Logs" tab
- Real-time logging of all requests

### View Logs on Server:
```bash
sudo journalctl -u branddeck -f
```

---

## 🎨 Integrate with mascha.tech

### Add Link from Main Site:

In your mascha.tech navigation:
```html
<nav>
    <a href="/tools/branddeck">BrandDeck Tool</a>
</nav>
```

### Embed in Existing Page:

Use iframe (not recommended for this use case):
```html
<iframe src="https://branddeck.mascha.tech" 
        width="100%" height="800px" 
        frameborder="0">
</iframe>
```

Or redirect:
```html
<a href="https://branddeck.mascha.tech" 
   class="tool-card">
    <h3>BrandDeck</h3>
    <p>Transform any website into a presentation</p>
</a>
```

---

## 🛠️ Maintenance

### Update the Tool:
```bash
git pull origin main
sudo systemctl restart branddeck  # If on your server
# Or push to GitHub (auto-deploys on Render)
```

### Backup:
```bash
# Backup generated assets folder
tar -czf branddeck_backup_$(date +%Y%m%d).tar.gz Brand_Agency_Generator/
```

---

## 💡 Cost Estimates

### Render (Free Tier):
- **Cost:** $0/month
- **Limits:** 500 hours/month, spins down after 15 min inactive
- **Storage:** Ephemeral (files deleted on restart)

### Render (Paid):
- **Cost:** $7/month (Starter)
- **Always on:** No spin-down
- **Better performance:** More CPU/RAM

### Your Own Server:
- **Cost:** Depends on existing hosting
- **Resources:** Shared with mascha.tech
- **Control:** Full control

---

## 🎯 Recommended Setup

**For Public Tool (Free):**
1. Deploy to Render (free tier)
2. Use subdomain: `branddeck.mascha.tech`
3. Add rate limiting (5 per hour per IP)
4. Setup auto-cleanup of old files
5. Monitor usage with analytics

**For Private/Team Use:**
1. Deploy to your server
2. Add basic auth password
3. Use `/tools/branddeck` path
4. No rate limiting needed
5. Keep generated files for team

---

## 🆘 Troubleshooting

### "Playwright browser not found"
```bash
playwright install chromium
```

### "Generation takes too long / times out"
- Increase timeout in Gunicorn: `--timeout 300`
- Increase timeout in Nginx: `proxy_read_timeout 300;`

### "Running out of disk space"
- Setup automatic cleanup cron job
- Use ephemeral storage (Render default)

---

## 📝 Next Steps

1. **I'll create all deployment files for you**
2. **Choose your deployment platform**
3. **Follow the specific guide above**
4. **Test at your deployed URL**
5. **Add link to mascha.tech**

Ready to proceed? Let me know which deployment option you prefer!
