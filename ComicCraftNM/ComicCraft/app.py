from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs
from html import escape
import random

HOST = "127.0.0.1"
PORT = 8000

def create_panels(prompt):
    prompt = prompt.strip() or "A brave student discovers a mysterious secret"
    rng = random.Random(sum(map(ord, prompt)))

    hero = rng.choice(["Arun", "Maya", "Kavin", "Nila", "Ravi"])
    places = ["an old library", "a quiet village", "a city rooftop",
              "a mysterious forest", "a science lab"]
    objects = ["a glowing key", "a strange map", "a tiny robot",
               "a magic book", "a silver compass"]
    place = rng.choice(places)
    obj = rng.choice(objects)

    return [
        ("💡", "PANEL 1 — THE IDEA",
         f"{hero} gets an exciting idea from: {prompt}.",
         f'{hero}: "I have to find out what this is about!"'),
        ("🔎", "PANEL 2 — THE DISCOVERY",
         f"While exploring {place}, {hero} discovers {obj}.",
         f'{hero}: "Whoa! What is this?"'),
        ("⚡", "PANEL 3 — THE CHALLENGE",
         f"The discovery leads {hero} into a difficult challenge.",
         f'{hero}: "I will not give up!"'),
        ("🧠", "PANEL 4 — THE SOLUTION",
         f"{hero} studies the clue carefully and finds the solution.",
         f'{hero}: "Yes! The clue was right here!"'),
        ("🏆", "PANEL 5 — THE ENDING",
         f"{hero} completes the adventure and learns something valuable.",
         f'{hero}: "Every adventure starts with one brave idea."'),
    ]

def render(prompt="", panels=None):
    cards = ""
    if panels:
        for emoji, title, scene, dialogue in panels:
            cards += f"""
            <article class="panel">
              <div class="number">{escape(title)}</div>
              <div class="art">{emoji}</div>
              <h2>{escape(title.split("—",1)[-1].strip())}</h2>
              <div class="bubble">{escape(dialogue)}</div>
              <p><b>Scene:</b> {escape(scene)}</p>
            </article>
            """

    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ComicCraft</title>
<style>
*{{box-sizing:border-box}}
body{{margin:0;background:#f6e7b5;color:#111;font-family:Arial,sans-serif}}
header{{background:#111;color:#fff;text-align:center;padding:22px;border-bottom:7px solid #f5c542}}
.logo{{font-size:42px;font-weight:900;text-shadow:4px 4px #e53935}}
.tag{{font-weight:700;margin-top:5px}}
.wrap{{max-width:1150px;margin:auto;padding:25px 18px}}
.box{{background:#fff;border:5px solid #111;border-radius:18px;padding:25px;box-shadow:9px 9px #111}}
h1{{margin-top:0}}
label{{font-weight:900;display:block;margin-bottom:8px}}
textarea{{width:100%;min-height:120px;border:4px solid #111;border-radius:12px;padding:14px;font-size:18px}}
button{{margin-top:14px;padding:14px 24px;background:#e53935;color:#fff;border:4px solid #111;border-radius:12px;font-size:18px;font-weight:900;box-shadow:5px 5px #111;cursor:pointer}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;margin-top:30px}}
.panel{{background:#fff;border:5px solid #111;border-radius:15px;padding:18px;box-shadow:7px 7px #111;min-height:350px}}
.number{{display:inline-block;background:#111;color:#fff;padding:7px;border-radius:6px;font-weight:900;font-size:12px}}
.art{{height:110px;margin:15px 0;border:4px solid #111;border-radius:10px;background:#f5c542;display:flex;align-items:center;justify-content:center;font-size:65px}}
h2{{margin:8px 0;font-size:25px}}
.bubble{{display:inline-block;border:4px solid #111;border-radius:18px;padding:12px;font-weight:800}}
p{{line-height:1.5}}
.note{{margin-top:18px;font-weight:700;font-size:14px}}
</style>
</head>
<body>
<header>
<div class="logo">💥 COMICCRAFT 💥</div>
<div class="tag">Create a 5-panel comic from your story idea</div>
</header>
<main class="wrap">
<section class="box">
<h1>📝 Story Prompt</h1>
<form method="post" action="/generate">
<label for="prompt">Enter your story idea</label>
<textarea id="prompt" name="prompt" placeholder="Example: A student finds a mysterious robot...">{escape(prompt, quote=True)}</textarea>
<button type="submit">🎨 CREATE COMIC</button>
</form>
<div class="note">Clean local version: Python standard library only. No Gemini, no .env, no FastAPI, no pip install.</div>
</section>
{('<section class="grid">'+cards+'</section>') if cards else ''}
</main>
</body>
</html>"""

class Handler(BaseHTTPRequestHandler):
    def send_page(self, content, status=200):
        data = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/":
            self.send_page(render())
        else:
            self.send_page("<h1>404 - Page not found</h1>", 404)

    def do_POST(self):
        if self.path != "/generate":
            self.send_page("<h1>404 - Page not found</h1>", 404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8", errors="replace")
        prompt = parse_qs(body).get("prompt", [""])[0]
        self.send_page(render(prompt, create_panels(prompt)))

    def log_message(self, fmt, *args):
        print("[ComicCraft]", fmt % args)

if __name__ == "__main__":
    print("ComicCraft running at http://127.0.0.1:8000")
    print("Press Ctrl+C to stop.")
    try:
        ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\nComicCraft stopped.")
    except OSError as e:
        print(f"\nCould not start ComicCraft: {e}")
        print("Port 8000 may already be in use. Close the other server and run again.")
