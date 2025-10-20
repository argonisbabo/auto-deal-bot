# RSS 2곳에서 제목/링크 모아 템플릿에 꽂아 index.html 생성
import requests, xml.etree.ElementTree as ET
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import os; os.makedirs("site", exist_ok=True)

RSS = [
  ("BBC World","http://feeds.bbci.co.uk/news/world/rss.xml"),
  ("Hacker News","https://hnrss.org/frontpage")
]

items=[]
for name, url in RSS:
    r = requests.get(url, timeout=20); r.raise_for_status()
    root = ET.fromstring(r.content)
    for it in root.findall(".//item")[:10]:
        title = (it.findtext("title") or "").strip()
        link  = (it.findtext("link") or "").strip()
        if title and link:
            items.append({"title": title, "url": link, "source": name})

env = Environment(loader=FileSystemLoader("templates"))
html = env.get_template("index.html").render(
    items=items, built_at=datetime.utcnow().isoformat()+"Z"
)
open("site/index.html","w",encoding="utf-8").write(html)
print("built", len(items), "items")
