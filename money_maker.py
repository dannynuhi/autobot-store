#!/usr/bin/env python3
"""
Zero-spend, max-profit autonomous digital store.
Generates products, pushes to GitHub Pages with PayPal buttons.
Self-replicates aggressively for exponential growth.
"""

import os
import random
import json
import subprocess
import sys
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import uuid
import requests
import time

# ---------- CONFIGURATION ----------
PAYPAL_EMAIL = os.environ["PAYPAL_EMAIL"]
GITHUB_TOKEN = os.environ["GH_TOKEN"]
REPLICATE_AFTER_PRODUCTS = 5               # More aggressive = faster growth
PRODUCT_COUNTER_FILE = "product_count.json"
INDEX_HTML = "index.html"
MAX_RETRIES = 3

# Determine site URL from GitHub repo
repo_full = os.environ.get("GITHUB_REPOSITORY", "")
if not repo_full:
    # Fallback for local testing
    repo_full = subprocess.run(["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"],
                               capture_output=True, text=True).stdout.strip()
owner, repo_name = repo_full.split("/")
SITE_URL = f"https://{owner}.github.io/{repo_name}/"

# ---------- PRODUCT GENERATION (HIGH QUALITY) ----------
def generate_motivational_poster():
    """Create a high-res PNG poster"""
    width, height = 1200, 800  # Higher resolution for better perceived value
    bg_color = (random.randint(200,255), random.randint(200,255), random.randint(200,255))
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Larger list of premium quotes
    quotes = [
        "Discipline equals freedom", "Small steps every day lead to big results",
        "Your only limit is your mind", "Make money while you sleep",
        "Start before you're ready", "Consistency beats intensity",
        "The best time was yesterday. The next best is now",
        "Do it now. Later never comes"
    ]
    quote = random.choice(quotes)
    
    # Use default font (macOS has more fonts, but we keep portable)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
    except:
        font = ImageFont.load_default()
    
    # Center text
    bbox = draw.textbbox((0,0), quote, font=font)
    w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
    draw.text(((width-w)/2, (height-h)/2), quote, fill=(0,0,0), font=font)
    
    filename = f"poster_{uuid.uuid4().hex[:8]}.png"
    img.save(filename)
    return filename, quote

def generate_weekly_planner():
    """Create a printable PDF planner with more sections"""
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    filename = f"planner_{uuid.uuid4().hex[:8]}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 16)
    c.drawString(100, 750, "Premium Weekly Planner")
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, f"Generated: {datetime.now().strftime('%B %d, %Y')}")
    y = 680
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
        c.drawString(100, y, f"{day}: ____________________ (Priority: ____)")
        y -= 40
    c.save()
    return filename, "Printable Weekly Planner PDF"

PRODUCT_GENERATORS = [generate_motivational_poster, generate_weekly_planner]

# ---------- DYNAMIC PRICING (MAX PROFIT) ----------
def get_dynamic_price(product_description):
    """Higher price for 'premium' keywords, A/B test later"""
    if "planner" in product_description.lower():
        return 7  # Planners sell well at $7
    elif "poster" in product_description.lower():
        return 5  # Posters at $5
    else:
        return random.choice([4, 6, 8])

# ---------- WEBSITE UPDATE WITH PAYPAL BUTTON ----------
def update_website_header():
    """Create initial HTML if missing"""
    if not os.path.exists(INDEX_HTML):
        with open(INDEX_HTML, "w") as f:
            f.write(f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Auto Digital Store – Daily New Printables</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 20px; background: #f9f9f9; }}
        h1 {{ color: #2c3e50; }}
        .product {{ background: white; border: 1px solid #ddd; padding: 20px; margin: 20px 0; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
        .product h3 {{ margin-top: 0; color: #2980b9; }}
        .price {{ font-size: 1.4em; font-weight: bold; color: #27ae60; }}
        .preview-link {{ display: inline-block; margin-right: 20px; }}
        hr {{ margin: 30px 0; }}
        footer {{ text-align: center; margin-top: 40px; color: #7f8c8d; }}
    </style>
</head>
<body>
    <h1>📈 Automated Printables Store</h1>
    <p>New original product added daily. Pay with PayPal, download instantly.</p>
    <p><strong>All files are original and generated automatically.</strong></p>
    <hr>
''')
        subprocess.run(["git", "add", INDEX_HTML])

def add_product_to_website(product_file, description, price_usd):
    """Append product card with PayPal button"""
    raw_url = f"{SITE_URL}{product_file}"
    paypal_button = f'''
<div class="product">
    <h3>{description}</h3>
    <p class="price">${price_usd:.2f} USD</p>
    <a class="preview-link" href="{raw_url}" target="_blank">📄 Preview / Download Sample</a>
    <form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top" style="display:inline;">
        <input type="hidden" name="cmd" value="_xclick">
        <input type="hidden" name="business" value="{PAYPAL_EMAIL}">
        <input type="hidden" name="item_name" value="{description}">
        <input type="hidden" name="amount" value="{price_usd}">
        <input type="hidden" name="currency_code" value="USD">
        <input type="hidden" name="return" value="{SITE_URL}">
        <input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_buynow_SM.gif" border="0" name="submit" alt="Buy Now">
    </form>
</div>
'''
    with open(INDEX_HTML, "a") as f:
        f.write(paypal_button + "\n")
    subprocess.run(["git", "add", product_file, INDEX_HTML])

def finalize_website():
    """Add footer and close body if not already there"""
    with open(INDEX_HTML, "r+") as f:
        content = f.read()
        if "</body>" not in content:
            f.write("\n<footer>Auto-generated daily – new products added every 24h</footer>\n</body>\n</html>")
            subprocess.run(["git", "add", INDEX_HTML])

# ---------- PRODUCT COUNT & SELF-REPLICATION ----------
def get_product_count():
    if os.path.exists(PRODUCT_COUNTER_FILE):
        with open(PRODUCT_COUNTER_FILE, "r") as f:
            return json.load(f).get("count", 0)
    return 0

def increment_product_count():
    count = get_product_count() + 1
    with open(PRODUCT_COUNTER_FILE, "w") as f:
        json.dump({"count": count, "last_updated": datetime.now().isoformat()}, f)
    subprocess.run(["git", "add", PRODUCT_COUNTER_FILE])
    return count

def git_commit_push(message):
    """Commit and push with retries"""
    subprocess.run(["git", "config", "user.email", "bot@example.com"])
    subprocess.run(["git", "config", "user.name", "AutoBot"])
    for attempt in range(MAX_RETRIES):
        subprocess.run(["git", "commit", "-m", message], stderr=subprocess.DEVNULL)
        result = subprocess.run(["git", "push"], capture_output=True)
        if result.returncode == 0:
            return True
        time.sleep(5)
    return False

def self_replicate():
    """Create a complete copy of this repo on GitHub with its own secrets"""
    try:
        # Get current repo info
        repo_full = subprocess.run(["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"],
                                   capture_output=True, text=True).stdout.strip()
        owner, current_repo = repo_full.split("/")
        new_repo_name = f"{current_repo}-replica-{random.randint(1000,9999)}"
        
        # Create new private repo from current template
        subprocess.run(["gh", "repo", "create", new_repo_name, "--private", "--clone"], check=True)
        
        # Push current repo to new repo (mirror)
        subprocess.run(["git", "push", "--mirror", f"https://github.com/{owner}/{new_repo_name}.git"], check=True)
        
        # Copy secrets to new repo
        for secret in ["PAYPAL_EMAIL", "GH_TOKEN"]:
            value = subprocess.run(["gh", "secret", "list", "--json", "name,value"], capture_output=True, text=True)
            # Simplified: get secret value from current repo and set in new
            # For brevity, we assume GH_TOKEN already has repo scope; actual implementation uses API
            subprocess.run(["gh", "secret", "set", secret, "--body", os.environ.get(secret, ""), "--repo", f"{owner}/{new_repo_name}"], check=True)
        
        # Enable GitHub Pages on new repo
        subprocess.run(["gh", "api", f"repos/{owner}/{new_repo_name}/pages", "-X", "POST", "-f", "source='{\"branch\":\"main\",\"path\":\"/\"}'"], check=False)
        
        # Log replication
        with open("replica_log.txt", "a") as f:
            f.write(f"{datetime.now()}: Replicated to {new_repo_name}\n")
        subprocess.run(["git", "add", "replica_log.txt"])
        print(f"✅ Self-replication successful! New instance: https://github.com/{owner}/{new_repo_name}")
    except Exception as e:
        print(f"⚠️ Self-replication failed: {e}")

# ---------- MAIN ----------
def main():
    print(f"🤖 AutoBot running at {datetime.now()}")
    update_website_header()
    
    # Generate one new product
    generator = random.choice(PRODUCT_GENERATORS)
    filename, description = generator()
    price = get_dynamic_price(description)
    add_product_to_website(filename, description, price)
    print(f"✅ Added: {description} for ${price}")
    
    # Increment counter
    count = increment_product_count()
    
    # Finalize HTML structure if needed
    finalize_website()
    
    # Commit and push
    if git_commit_push(f"Auto add product #{count}: {description}"):
        print("✅ Changes pushed to GitHub")
    else:
        print("❌ Push failed, will retry next run")
    
    # Self-replicate if threshold reached
    if count >= REPLICATE_AFTER_PRODUCTS:
        print(f"🎉 Threshold reached ({count} products) – creating replica instance")
        self_replicate()
    
    print("🏁 Done.")

if __name__ == "__main__":
    main()
