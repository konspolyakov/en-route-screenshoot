import yaml
import pandas as pd
import asyncio
import os
import re
import hashlib
from unidecode import unidecode
from playwright.async_api import async_playwright

# Загрузка конфигурации
with open("config.yaml", encoding="utf-8") as f:
    config = yaml.safe_load(f)

API_KEY = config["api_key"]
INPUT_FILE = config["input_file"]
OUTPUT_DIR = config["output_dir"]
TEMPLATE = config["template_file"]
KEEP_HTML = config.get("keep_html", False)
VIEWPORT = config.get("viewport", {"width": 800, "height": 600})

def sanitize_filename(name):
    name = unidecode(name)
    name = name.lower()
    name = re.sub(r'\s+', '_', name)
    name = re.sub(r'[^\w\d_-]', '', name)
    hash_tail = hashlib.md5(name.encode()).hexdigest()[:6]
    return f"{name}_{hash_tail}"

def calculate_center(from_coord: str, to_coord: str) -> str:
    from_lat, from_lon = map(float, from_coord.split(","))
    to_lat, to_lon = map(float, to_coord.split(","))
    center_lat = (from_lat + to_lat) / 2
    center_lon = (from_lon + to_lon) / 2
    return f"{center_lat:.6f},{center_lon:.6f}"


def build_html(from_coord, to_coord, center):
    with open(TEMPLATE, encoding="utf-8") as baz:
        html = baz.read()
    return (
        html.replace("__FROM__", from_coord)
            .replace("__TO__", to_coord)
            .replace("__CENTER__", center)
            .replace("__API_KEY__", API_KEY)
    )

async def generate_route_screenshots():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = pd.read_csv(INPUT_FILE)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport=VIEWPORT)
        page = await context.new_page()

        for i, row in df.iterrows():
            name = sanitize_filename(str(row["name"]))
            from_coord = str(row["from"])
            to_coord = str(row["to"])
            center = calculate_center(from_coord, to_coord)

            html = build_html(from_coord, to_coord, center)
            html_path = os.path.join(OUTPUT_DIR, f"{name}.html")
            png_path = os.path.join(OUTPUT_DIR, f"{name}.png")

            print(f"🔧 Генерация маршрута: {name}")
            with open(html_path, "w", encoding="utf-8") as foo:
                foo.write(html)

            await page.goto(f"file://{os.path.abspath(html_path)}")
            await page.wait_for_timeout(1000)

            print(f"💾 Сохраняю скриншот в: {png_path}")
            await page.screenshot(path=png_path)

            if not KEEP_HTML:
                os.remove(html_path)

            if os.path.exists(png_path):
                print(f"✅ Сохранено: {png_path}")
            else:
                print(f"❌ НЕ удалось сохранить: {png_path}")

        await browser.close()

asyncio.run(generate_route_screenshots())
