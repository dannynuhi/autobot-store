#!/usr/bin/env python3
"""
ULTIMATE BILINGUAL BOT – AutoBot v5
- 12 product types (6 English, 6 Spanish)
- Twitter with image upload
- SEO: Open Graph, JSON-LD, sitemap, RSS
- Self-replication with retries
- A/B price testing (simulated)
- Runs every 6 hours, replicates after 2 products
"""

import os, random, json, subprocess, time, requests, uuid, sys, math, textwrap
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageStat
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# ---------- CONFIG ----------
PAYPAL_EMAIL = os.environ.get("PAYPAL_EMAIL", "")
GITHUB_TOKEN = os.environ.get("GH_TOKEN", "")
REPLICATE_AFTER = 2
PRODUCT_COUNTER_FILE = "product_count.json"
INDEX_HTML = "index.html"
SITEMAP_XML = "sitemap.xml"
RSS_XML = "rss.xml"
PRICE_HISTORY = "price_history.json"
QUALITY_THRESHOLD = 8
MAX_RETRIES = 3
FONT_URL = "https://raw.githubusercontent.com/google/fonts/main/apache/roboto/Roboto-Regular.ttf"
FONT_FILE = "Roboto-Regular.ttf"

# API Keys (optional)
REDDIT_CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET", "")
REDDIT_USERNAME = os.environ.get("REDDIT_USERNAME", "")
REDDIT_PASSWORD = os.environ.get("REDDIT_PASSWORD", "")
TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY", "")
TWITTER_API_SECRET = os.environ.get("TWITTER_API_SECRET", "")
TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN", "")
TWITTER_ACCESS_SECRET = os.environ.get("TWITTER_ACCESS_SECRET", "")
PINTEREST_ACCESS_TOKEN = os.environ.get("PINTEREST_ACCESS_TOKEN", "")
PINTEREST_BOARD_ID = os.environ.get("PINTEREST_BOARD_ID", "")
MEDIUM_TOKEN = os.environ.get("MEDIUM_TOKEN", "")
TUMBLR_CONSUMER_KEY = os.environ.get("TUMBLR_CONSUMER_KEY", "")
TUMBLR_CONSUMER_SECRET = os.environ.get("TUMBLR_CONSUMER_SECRET", "")
TUMBLR_TOKEN = os.environ.get("TUMBLR_TOKEN", "")
TUMBLR_TOKEN_SECRET = os.environ.get("TUMBLR_TOKEN_SECRET", "")
TUMBLR_BLOG = os.environ.get("TUMBLR_BLOG", "")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
BING_API_KEY = os.environ.get("BING_API_KEY", "")
RENDER_API_KEY = os.environ.get("RENDER_API_KEY", "")
KOYEB_API_KEY = os.environ.get("KOYEB_API_KEY", "")

# ---------- SITE URL ----------
repo_full = os.environ.get("GITHUB_REPOSITORY", "dannynuhi/autobot-store")
owner, repo_name = repo_full.split("/") if "/" in repo_full else ("dannynuhi", "autobot-store")
SITE_URL = f"https://{owner}.github.io/{repo_name}/"

# ---------- FONT ----------
def download_font():
    if os.path.exists(FONT_FILE):
        return FONT_FILE
    print("⬇️ Downloading Roboto font...")
    for attempt in range(3):
        try:
            resp = requests.get(FONT_URL, timeout=10)
            if resp.status_code == 200:
                with open(FONT_FILE, "wb") as f:
                    f.write(resp.content)
                print("✅ Font downloaded")
                return FONT_FILE
        except:
            time.sleep(2)
    print("⚠️ Using fallback font")
    return None

def get_font(size):
    if os.path.exists(FONT_FILE):
        try:
            return ImageFont.truetype(FONT_FILE, size)
        except:
            pass
    return ImageFont.load_default()

# ---------- ENGLISH GENERATORS ----------
def generate_poster_en():
    width, height = 800, 600
    attempts = 0
    while attempts < 10:
        r = random.randint(180, 255)
        g = random.randint(180, 255)
        b = random.randint(180, 255)
        maxc = max(r,g,b)
        minc = min(r,g,b)
        if maxc == 0:
            continue
        sat = (maxc - minc) / maxc
        if sat < 0.35 and (r+g+b)/3 > 200:
            bg = (r,g,b)
            break
        attempts += 1
    else:
        bg = (240, 240, 240)
    img = Image.new("RGB", (width, height), color=bg)
    draw = ImageDraw.Draw(img)
    quotes = [
        "Discipline = Freedom", "Small steps daily", "Your only limit is your mind",
        "Make money while you sleep", "Start before you are ready", "Consistency beats intensity",
        "Progress not perfection", "Dream big, start small"
    ]
    quote = random.choice(quotes)
    font_size = 60
    while font_size > 20:
        font = get_font(font_size)
        bbox = draw.textbbox((0,0), quote, font=font)
        tw = bbox[2]-bbox[0]
        if tw < width * 0.9:
            break
        font_size -= 2
    font = get_font(font_size)
    bbox = draw.textbbox((0,0), quote, font=font)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    x = (width - tw) // 2
    y = (height - th) // 2
    draw.text((x, y), quote, fill=(0,0,0), font=font)
    fname = f"poster_{uuid.uuid4().hex[:8]}.png"
    img.save(fname)
    return fname, f"Motivational Poster: {quote}"

def generate_planner_en():
    fname = f"planner_{uuid.uuid4().hex[:8]}.pdf"
    c = canvas.Canvas(fname, pagesize=letter)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(100, 750, "Weekly Goal Planner")
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, f"Date: {datetime.now().strftime('%B %d, %Y')}")
    y = 680
    sections = ["Top 3 Goals", "To-Do List", "Appointments", "Notes"]
    for sec in sections:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, y, sec)
        c.setFont("Helvetica", 11)
        y -= 25
        for i in range(4):
            c.drawString(120, y - i*20, "__________________")
        y -= 80
    c.save()
    return fname, "Weekly Goal Planner PDF"

def generate_checklist_en():
    fname = f"checklist_{uuid.uuid4().hex[:8]}.pdf"
    c = canvas.Canvas(fname, pagesize=letter)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(100, 750, "Daily Checklist")
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, f"Date: {datetime.now().strftime('%B %d, %Y')}")
    y = 680
    for i in range(10):
        c.drawString(100, y - i*35, f"[ ] Task {i+1}: ________________________")
    c.save()
    return fname, "Daily Checklist PDF"

def generate_habit_tracker_en():
    fname = f"habits_{uuid.uuid4().hex[:8]}.pdf"
    c = canvas.Canvas(fname, pagesize=letter)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(100, 750, "Monthly Habit Tracker")
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, f"Month: {datetime.now().strftime('%B %Y')}")
    y = 680
    for i in range(5):
        c.drawString(100, y - i*40, f"Habit {i+1}:")
        for j in range(7):
            c.drawString(250 + j*40, y - i*40, "[_]")
    c.save()
    return fname, "Habit Tracker PDF"

def generate_goal_sheet_en():
    fname = f"goals_{uuid.uuid4().hex[:8]}.pdf"
    c = canvas.Canvas(fname, pagesize=letter)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(100, 750, "Goal Setting Worksheet")
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, f"Date: {datetime.now().strftime('%B %d, %Y')}")
    y = 680
    items = ["My Goal:", "Why it matters:", "Steps:", "Deadline:"]
    for item in items:
        c.drawString(100, y, item)
        c.line(250, y+5, 500, y+5)
        y -= 40
    c.save()
    return fname, "Goal Setting Worksheet PDF"

def generate_daily_planner_en():
    fname = f"daily_{uuid.uuid4().hex[:8]}.pdf"
    c = canvas.Canvas(fname, pagesize=letter)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(100, 750, "Daily Planner")
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, f"Date: {datetime.now().strftime('%B %d, %Y')}")
    y = 680
    sections = ["Priority 1:", "Priority 2:", "Priority 3:", "Schedule:", "Notes:"]
    for sec in sections:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, y, sec)
        c.setFont("Helvetica", 11)
        c.line(200, y+5, 500, y+5)
        y -= 50
    c.save()
    return fname, "Daily Planner PDF"

# ---------- SPANISH GENERATORS (México/LatAm) ----------
def generate_poster_es():
    width, height = 800, 600
    attempts = 0
    while attempts < 10:
        r = random.randint(180, 255)
        g = random.randint(180, 255)
        b = random.randint(180, 255)
        maxc = max(r,g,b)
        minc = min(r,g,b)
        if maxc == 0:
            continue
        sat = (maxc - minc) / maxc
        if sat < 0.35 and (r+g+b)/3 > 200:
            bg = (r,g,b)
            break
        attempts += 1
    else:
        bg = (240, 240, 240)
    img = Image.new("RGB", (width, height), color=bg)
    draw = ImageDraw.Draw(img)
    quotes = [
        "Disciplina = Libertad", "Pasos pequeños cada día", "Tu único límite es tu mente",
        "Gana dinero mientras duermes", "Empieza antes de estar listo", "La constancia vence a la intensidad",
        "Progreso, no perfección", "Sueña en grande, empieza pequeño"
    ]
    quote = random.choice(quotes)
    font_size = 60
    while font_size > 20:
        font = get_font(font_size)
        bbox = draw.textbbox((0,0), quote, font=font)
        tw = bbox[2]-bbox[0]
        if tw < width * 0.9:
            break
        font_size -= 2
    font = get_font(font_size)
    bbox = draw.textbbox((0,0), quote, font=font)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    x = (width - tw) // 2
    y = (height - th) // 2
    draw.text((x, y), quote, fill=(0,0,0), font=font)
    fname = f"poster_{uuid.uuid4().hex[:8]}.png"
    img.save(fname)
    return fname, f"Póster Motivacional: {quote}"

def generate_planner_es():
    fname = f"planner_{uuid.uuid4().hex[:8]}.pdf"
    c = canvas.Canvas(fname, pagesize=letter)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(100, 750, "Planificador Semanal de Metas")
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, f"Fecha: {datetime.now().strftime('%d de %B de %Y')}")
    y = 680
    sections = ["Top 3 Metas", "Lista de Tareas", "Citas", "Notas"]
    for sec in sections:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, y, sec)
        c.setFont("Helvetica", 11)
        y -= 25
        for i in range(4):
            c.drawString(120, y - i*20, "__________________")
        y -= 80
    c.save()
    return fname, "Planificador Semanal PDF"

def generate_checklist_es():
    fname = f"checklist_{uuid.uuid4().hex[:8]}.pdf"
    c = canvas.Canvas(fname, pagesize=letter)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(100, 750, "Lista de Verificación Diaria")
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, f"Fecha: {datetime.now().strftime('%d de %B de %Y')}")
    y = 680
    for i in range(10):
        c.drawString(100, y - i*35, f"[ ] Tarea {i+1}: ________________________")
    c.save()
    return fname, "Lista de Verificación PDF"

def generate_habit_tracker_es():
    fname = f"habits_{uuid.uuid4().hex[:8]}.pdf"
    c = canvas.Canvas(fname, pagesize=letter)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(100, 750, "Rastreador de Hábitos Mensual")
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, f"Mes: {datetime.now().strftime('%B de %Y')}")
    y = 680
    for i in range(5):
        c.drawString(100, y - i*40, f"Hábito {i+1}:")
        for j in range(7):
            c.drawString(250 + j*40, y - i*40, "[_]")
    c.save()
    return fname, "Rastreador de Hábitos PDF"

def generate_goal_sheet_es():
    fname = f"goals_{uuid.uuid4().hex[:8]}.pdf"
    c = canvas.Canvas(fname, pagesize=letter)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(100, 750, "Hoja de Establecimiento de Metas")
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, f"Fecha: {datetime.now().strftime('%d de %B de %Y')}")
    y = 680
    items = ["Mi Meta:", "¿Por qué es importante?", "Pasos:", "Fecha límite:"]
    for item in items:
        c.drawString(100, y, item)
        c.line(250, y+5, 500, y+5)
        y -= 40
    c.save()
    return fname, "Hoja de Metas PDF"

def generate_daily_planner_es():
    fname = f"daily_{uuid.uuid4().hex[:8]}.pdf"
    c = canvas.Canvas(fname, pagesize=letter)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(100, 750, "Planificador Diario")
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, f"Fecha: {datetime.now().strftime('%d de %B de %Y')}")
    y = 680
    sections = ["Prioridad 1:", "Prioridad 2:", "Prioridad 3:", "Horario:", "Notas:"]
    for sec in sections:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, y, sec)
        c.setFont("Helvetica", 11)
        c.line(200, y+5, 500, y+5)
        y -= 50
    c.save()
    return fname, "Planificador Diario PDF"

# ---------- PRODUCT GENERATORS LIST ----------
PRODUCT_GENERATORS = [
    generate_poster_en, generate_planner_en, generate_checklist_en,
    generate_habit_tracker_en, generate_goal_sheet_en, generate_daily_planner_en,
    generate_poster_es, generate_planner_es, generate_checklist_es,
    generate_habit_tracker_es, generate_goal_sheet_es, generate_daily_planner_es
]

# ---------- QUALITY CONTROL ----------
def contrast_ratio(color1, color2):
    def luminance(rgb):
        r,g,b = [x/255.0 for x in rgb]
        for c in (r,g,b):
            if c <= 0.03928:
                c = c/12.92
            else:
                c = ((c+0.055)/1.055)**2.4
        return 0.2126*r + 0.7152*g + 0.0722*b
    l1 = luminance(color1)
    l2 = luminance(color2)
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)

def evaluate_poster(image_path, quote):
    score = 0
    issues = []
    img = Image.open(image_path)
    w, h = img.size
    if w >= 800 and h >= 600:
        score += 2
    else:
        issues.append("Resolution too low")
    extrema = img.getextrema()
    if extrema[0][0] == extrema[0][1] and extrema[1][0] == extrema[1][1] and extrema[2][0] == extrema[2][1]:
        issues.append("Image is uniform")
    else:
        score += 1
    points = [(w//4, h//4), (w//4, 3*h//4), (3*w//4, h//4), (3*w//4, 3*h//4), (w//2, h//2)]
    contrast_ok = True
    for px in points:
        bg_color = img.getpixel(px)
        cr = contrast_ratio(bg_color, (0,0,0))
        if cr < 4.0:
            contrast_ok = False
            issues.append(f"Low contrast at {px}: {cr:.2f}")
    if contrast_ok:
        score += 2
    else:
        issues.append("Contrast too low at some points")
    avg = ImageStat.Stat(img).mean
    lightness = (avg[0] + avg[1] + avg[2]) / 3 / 255 * 100
    if 55 <= lightness <= 90:
        score += 2
    else:
        issues.append(f"Background lightness: {lightness:.0f}%")
    bg_color = img.getpixel((w//2, h//2))
    maxc = max(bg_color)
    minc = min(bg_color)
    sat = (maxc - minc) / maxc if maxc > 0 else 0
    if sat < 0.35:
        score += 1
    else:
        issues.append(f"Background too saturated: {sat:.2f}")
    return min(score, 10), issues

def evaluate_planner(pdf_path):
    score = 0
    issues = []
    if os.path.getsize(pdf_path) > 15000:
        score += 5
    else:
        issues.append("PDF too small")
    if pdf_path.endswith(".pdf"):
        score += 3
    else:
        issues.append("Not a PDF")
    score += 2
    return min(score, 10), issues

def generate_quality_product():
    download_font()
    for attempt in range(MAX_RETRIES):
        gen = random.choice(PRODUCT_GENERATORS)
        fname, desc = gen()
        if gen in (generate_poster_en, generate_poster_es):
            score, issues = evaluate_poster(fname, desc)
        else:
            score, issues = evaluate_planner(fname)
        if score >= QUALITY_THRESHOLD:
            print(f"✅ Product scored {score}/10 – publishing")
            return fname, desc, score
        else:
            print(f"⚠️ Attempt {attempt+1}: score {score}/10 – issues: {', '.join(issues)}")
            os.remove(fname)
    print("🛡️ Using safe fallback")
    return safe_generate()

def safe_generate():
    if random.choice([True, False]):
        return safe_generate_poster()
    else:
        return safe_generate_planner()

def safe_generate_poster():
    width, height = 800, 600
    bg = (245, 245, 245)
    img = Image.new("RGB", (width, height), color=bg)
    draw = ImageDraw.Draw(img)
    quote = "Discipline equals freedom"
    font = get_font(60)
    bbox = draw.textbbox((0,0), quote, font=font)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    x = (width - tw) // 2
    y = (height - th) // 2
    draw.text((x, y), quote, fill=(0,0,0), font=font)
    draw.rectangle([(10,10), (width-10, height-10)], outline=(200,200,200), width=2)
    fname = f"poster_safe_{uuid.uuid4().hex[:8]}.png"
    img.save(fname)
    return fname, quote

def safe_generate_planner():
    fname = f"planner_safe_{uuid.uuid4().hex[:8]}.pdf"
    c = canvas.Canvas(fname, pagesize=letter)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, 750, "Weekly Planner")
    c.setFont("Helvetica", 14)
    c.drawString(100, 720, "Date: ________________")
    y = 680
    for i in range(7):
        c.drawString(100, y, f"Day {i+1}: ____________________")
        y -= 40
    c.save()
    return fname, "Safe Weekly Planner"

# ---------- WEBSITE WITH SEO ----------
def update_website_header():
    if not os.path.exists(INDEX_HTML):
        with open(INDEX_HTML, "w") as f:
            f.write('''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="description" content="Daily new digital printables – planners, posters, checklists. Instant download, PayPal checkout.">
    <meta name="keywords" content="printables,planners,posters,digital products,productivity,checklist,habit tracker">
    <meta name="author" content="Danny's Digital Goods">
    <meta property="og:title" content="Danny's Digital Goods – Daily Printables Store">
    <meta property="og:description" content="New original product every day. Pay with PayPal, download instantly.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://dannynuhi.github.io/autobot-store/">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Danny's Digital Goods">
    <meta name="twitter:description" content="Daily new printables – planners, posters, checklists.">
    <title>Danny's Digital Goods – Daily Printables Store</title>
    <style>
        body { font-family: system-ui, -apple-system, sans-serif; margin: 20px; background: #f9f9f9; line-height: 1.6; }
        .product { background: white; padding: 20px; margin: 20px 0; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
        .price { font-size: 1.4em; font-weight: bold; color: #27ae60; }
        .share-buttons a { margin-right: 10px; }
        footer { margin-top: 40px; text-align: center; color: #7f8c8d; }
        @media (max-width: 600px) { body { margin: 10px; } .product { padding: 15px; } }
    </style>
</head>
<body>
    <h1>📈 Danny's Digital Goods</h1>
    <p>New product every day. <a href="/rss.xml">RSS</a> | <a href="/sitemap.xml">Sitemap</a></p>
    <hr>
''')
        subprocess.run(["git", "add", INDEX_HTML], stderr=subprocess.DEVNULL)

def add_product_to_website(product_file, description, price_usd):
    raw_url = f"{SITE_URL}{product_file}"
    json_ld = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org/",
  "@type": "Product",
  "name": "{description}",
  "description": "Printable digital product – instant download after PayPal payment.",
  "offers": {{
    "@type": "Offer",
    "price": "{price_usd}",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock"
  }}
}}
</script>'''
    with open(INDEX_HTML, "a") as f:
        f.write(f'''
<div class="product" itemscope itemtype="https://schema.org/Product">
    <h3 itemprop="name">{description}</h3>
    <p class="price" itemprop="price" content="{price_usd}">${price_usd:.2f} USD</p>
    <a href="{raw_url}" target="_blank" itemprop="image">📄 Preview</a>
    <form action="https://www.paypal.com/cgi-bin/webscr" method="post" style="display:inline;">
        <input type="hidden" name="cmd" value="_xclick">
        <input type="hidden" name="business" value="{PAYPAL_EMAIL}">
        <input type="hidden" name="item_name" value="{description}">
        <input type="hidden" name="amount" value="{price_usd}">
        <input type="hidden" name="currency_code" value="USD">
        <input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_buynow_SM.gif">
    </form>
    <div class="share-buttons">
        <a href="https://twitter.com/intent/tweet?text={description.replace(' ','%20')}&url={raw_url}" target="_blank">🐦 Tweet</a>
        <a href="https://www.facebook.com/sharer/sharer.php?u={raw_url}" target="_blank">📘 Share</a>
        <a href="https://pinterest.com/pin/create/button/?url={raw_url}&media={raw_url}" target="_blank">📌 Pin</a>
    </div>
    {json_ld}
</div>
''')
    subprocess.run(["git", "add", product_file, INDEX_HTML], stderr=subprocess.DEVNULL)

def finalize_website():
    with open(INDEX_HTML, "r+") as f:
        content = f.read()
        if "</body>" not in content:
            f.write("\n<footer>Auto-generated daily – new products every 6 hours</footer></body></html>")
            subprocess.run(["git", "add", INDEX_HTML], stderr=subprocess.DEVNULL)

def generate_sitemap(products):
    with open(SITEMAP_XML, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for url, lastmod in products:
            f.write(f'<url><loc>{url}</loc><lastmod>{lastmod}</lastmod><priority>0.8</priority></url>\n')
        f.write('</urlset>')
    subprocess.run(["git", "add", SITEMAP_XML], stderr=subprocess.DEVNULL)
    # Ping Google
    requests.get(f"https://www.google.com/ping?sitemap={SITE_URL}sitemap.xml")
    print("📡 Sitemap submitted to Google")

def generate_rss(products):
    with open(RSS_XML, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0">\n<channel>\n')
        f.write(f'<title>Danny\'s Digital Goods</title>\n<link>{SITE_URL}</link>\n<description>Daily new printables</description>\n')
        for title, link, desc, pub in products[-20:]:
            f.write(f'<item>\n<title>{title}</title>\n<link>{link}</link>\n<description>{desc}</description>\n<pubDate>{pub}</pubDate>\n</item>\n')
        f.write('</channel></rss>')
    subprocess.run(["git", "add", RSS_XML], stderr=subprocess.DEVNULL)

# ---------- SOCIAL MEDIA PROMOTION ----------
def post_to_twitter_with_image(description, url, image_path):
    if not (TWITTER_API_KEY and TWITTER_ACCESS_TOKEN):
        print("Skipping Twitter – no keys")
        return
    try:
        import tweepy
        auth = tweepy.OAuth1UserHandler(TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
        api = tweepy.API(auth)
        media_ids = []
        if image_path and os.path.exists(image_path) and image_path.endswith(('.png','.jpg','.jpeg')):
            media = api.media_upload(image_path)
            media_ids.append(media.media_id)
        tweet_text = f"New: {description}\nDownload: {url}\n#printables #productivity #planner"
        if media_ids:
            api.update_status(status=tweet_text, media_ids=media_ids)
        else:
            api.update_status(tweet_text)
        print("✅ Tweeted with image")
    except Exception as e:
        print(f"Twitter error: {e}")

def post_to_reddit(title, url):
    if not REDDIT_CLIENT_ID:
        return
    try:
        import praw
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            username=REDDIT_USERNAME,
            password=REDDIT_PASSWORD,
            user_agent="AutoBot/1.0"
        )
        for sub in ["freebies", "digitalfreebies", "free_printables"]:
            reddit.subreddit(sub).submit(title=f"New {title}", url=url)
            time.sleep(30)
        print("✅ Reddit posted")
    except Exception as e:
        print(f"Reddit error: {e}")

def post_to_pinterest(title, url, image_path):
    if not PINTEREST_ACCESS_TOKEN:
        return
    headers = {"Authorization": f"Bearer {PINTEREST_ACCESS_TOKEN}"}
    try:
        files = {"image": open(image_path, "rb")}
        resp = requests.post("https://api.pinterest.com/v3/media/", headers=headers, files=files)
        if resp.status_code == 201:
            media_id = resp.json()["media_id"]
            pin_data = {"board_id": PINTEREST_BOARD_ID, "title": title, "description": url, "media_source": {"source_type": "image_id", "id": media_id}}
            requests.post("https://api.pinterest.com/v5/pins", headers=headers, json=pin_data)
            print("✅ Pinterest posted")
    except Exception as e:
        print(f"Pinterest error: {e}")

def post_to_medium(title, url):
    if not MEDIUM_TOKEN:
        return
    headers = {"Authorization": f"Bearer {MEDIUM_TOKEN}", "Content-Type": "application/json"}
    try:
        user = requests.get("https://api.medium.com/v1/me", headers=headers).json()
        user_id = user["data"]["id"]
        data = {"title": title, "contentFormat": "html", "content": f'<p><a href="{url}">{url}</a></p>', "publishStatus": "public"}
        requests.post(f"https://api.medium.com/v1/users/{user_id}/posts", headers=headers, json=data)
        print("✅ Medium posted")
    except Exception as e:
        print(f"Medium error: {e}")

def post_to_tumblr(title, url, image_path=None):
    if not TUMBLR_CONSUMER_KEY:
        return
    try:
        from pytumblr import TumblrClient
        client = TumblrClient(TUMBLR_CONSUMER_KEY, TUMBLR_CONSUMER_SECRET, TUMBLR_TOKEN, TUMBLR_TOKEN_SECRET)
        if image_path:
            with open(image_path, "rb") as f:
                client.create_photo(TUMBLR_BLOG, state="published", caption=f"{title}<br>{url}", data=f)
        else:
            client.create_text(TUMBLR_BLOG, state="published", title=title, body=f"Download: {url}")
        print("✅ Tumblr posted")
    except Exception as e:
        print(f"Tumblr error: {e}")

def promote_product(product_name, product_url, image_path=None):
    post_to_twitter_with_image(product_name, product_url, image_path)
    post_to_reddit(product_name, product_url)
    if image_path:
        post_to_pinterest(product_name, product_url, image_path)
        post_to_tumblr(product_name, product_url, image_path)
    else:
        post_to_tumblr(product_name, product_url)
    post_to_medium(product_name, product_url)

# ---------- SELF-REPLICATION (with retries) ----------
def self_replicate():
    for attempt in range(3):
        try:
            new_repo = f"autobot-replica-{random.randint(1000,9999)}"
            subprocess.run(["gh", "repo", "create", new_repo, "--private", "--clone"], check=True)
            subprocess.run(["git", "push", "--mirror", f"https://github.com/{owner}/{new_repo}.git"], check=True)
            subprocess.run(["gh", "secret", "set", "PAYPAL_EMAIL", "--body", PAYPAL_EMAIL, "--repo", f"{owner}/{new_repo}"], check=True)
            subprocess.run(["gh", "secret", "set", "GH_TOKEN", "--body", GITHUB_TOKEN, "--repo", f"{owner}/{new_repo}"], check=True)
            print(f"✅ Replica created: {new_repo}")
            return
        except Exception as e:
            print(f"Replica attempt {attempt+1} failed: {e}")
            time.sleep(30)
    print("⚠️ Self-replication failed after 3 attempts")

# ---------- PRICING (A/B testing) ----------
def load_price_history():
    if os.path.exists(PRICE_HISTORY):
        with open(PRICE_HISTORY, "r") as f:
            return json.load(f)
    return {"sales": [], "best_price": 5}

def save_price_history(hist):
    with open(PRICE_HISTORY, "w") as f:
        json.dump(hist, f)

def get_optimal_price():
    hist = load_price_history()
    if len(hist["sales"]) < 5:
        return random.choice([3,5,7,9])
    return hist.get("best_price", 5)

def record_sale(price):
    hist = load_price_history()
    hist["sales"].append({"price": price, "time": datetime.now().isoformat()})
    hist["sales"] = hist["sales"][-100:]
    from collections import Counter
    prices = [s["price"] for s in hist["sales"]]
    if prices:
        hist["best_price"] = Counter(prices).most_common(1)[0][0]
    save_price_history(hist)

# ---------- PRODUCT COUNT & GIT ----------
def get_product_count():
    if os.path.exists(PRODUCT_COUNTER_FILE):
        with open(PRODUCT_COUNTER_FILE, "r") as f:
            return json.load(f).get("count", 0)
    return 0

def increment_product_count():
    count = get_product_count() + 1
    with open(PRODUCT_COUNTER_FILE, "w") as f:
        json.dump({"count": count, "last": datetime.now().isoformat()}, f)
    subprocess.run(["git", "add", PRODUCT_COUNTER_FILE], stderr=subprocess.DEVNULL)
    return count

def git_commit_push(msg):
    subprocess.run(["git", "config", "user.email", "bot@example.com"])
    subprocess.run(["git", "config", "user.name", "AutoBot"])
    subprocess.run(["git", "commit", "-m", msg], stderr=subprocess.DEVNULL)
    subprocess.run(["git", "push"], stderr=subprocess.DEVNULL)

# ---------- MAIN ----------
def main():
    print(f"🚀 ULTIMATE BILINGUAL BOT started at {datetime.now()}")
    download_font()
    update_website_header()
    fname, desc, score = generate_quality_product()
    price = get_optimal_price()
    add_product_to_website(fname, desc, price)
    finalize_website()
    product_url = f"{SITE_URL}{fname}"
    product_urls = [(product_url, datetime.now().strftime("%Y-%m-%d"))]
    rss_items = [(desc, product_url, desc, datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000"))]
    generate_sitemap(product_urls)
    generate_rss(rss_items)
    count = increment_product_count()
    git_commit_push(f"Add product #{count}: {desc} (QC {score}/10)")
    # Promote on all platforms
    promote_product(desc, product_url, fname if fname.endswith(".png") else None)
    # Replicate if threshold reached
    if count >= REPLICATE_AFTER:
        print("🔄 Replication threshold reached")
        self_replicate()
    print("✅ Done")

if __name__ == "__main__":
    sys.exit(main())
