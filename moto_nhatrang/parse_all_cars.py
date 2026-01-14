import os, requests, time, json
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

# API URL для получения всех листингов во Вьетнаме (ID локации 106 - Вьетнам)
# Мы запрашиваем сразу 100 позиций, чтобы покрыть все 51 авто
API_URL = "https://getmecar.ru/api/listings/?location=106&limit=100"
DOMAIN = "https://getmecar.ru"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json"
}
BASE_PATH = "/home/poweramanita/goldantelopeasia/moto_nhatrang"

def process_car(item):
    try:
        title_raw = item.get('title')
        slug = item.get('slug')
        if not title_raw or not slug: return
        
        url = f"{DOMAIN}/listing/{slug}/"
        folder_name = "".join([c if c.isalnum() else "_" for c in title_raw]).lower().strip("_")
        path = os.path.join(BASE_PATH, folder_name)
        
        if not os.path.exists(path): os.makedirs(path)
        
        print(f"📡 Обработка: {title_raw}")
        
        # 1. Загружаем страницу для полного описания
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        specs = soup.find('div', class_='listing-specs')
        desc = soup.find('div', class_='description')
        content = f"{title_raw}\n\n"
        if specs: content += "ХАРАКТЕРИСТИКИ:\n" + specs.get_text(separator="\n", strip=True) + "\n\n"
        if desc: content += "ОПИСАНИЕ:\n" + desc.get_text(separator="\n", strip=True)
        
        with open(os.path.join(path, "description.txt"), "w", encoding="utf-8") as f:
            f.write(content)

        # 2. Фото (берем из API или со страницы)
        img_url = item.get('image') # API часто отдает прямую ссылку
        if not img_url:
            img_tag = soup.find('meta', property='og:image')
            img_url = img_tag.get('content') if img_tag else None
            
        if img_url:
            img_res = requests.get(img_url, headers=HEADERS, timeout=10)
            img = Image.open(BytesIO(img_res.content)).convert("RGB")
            img.thumbnail((800, 800))
            img.save(os.path.join(path, "photo.jpg"), "JPEG", quality=55, optimize=True)
            
        print(f"   ✅ Готово")
        time.sleep(0.5) # Ускоряем процесс, так как лимиты API лояльнее
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

def main():
    print("🚀 Запрашиваю полный список авто через API...")
    try:
        r = requests.get(API_URL, headers=HEADERS)
        data = r.json()
        # В зависимости от структуры API GetMeCar, листинги могут быть в 'results' или корне
        items = data.get('results', data) if isinstance(data, dict) else data
        
        if not isinstance(items, list):
            print("❌ Не удалось получить список. Пробую старый метод через скрапинг ссылок...")
            return

        print(f"🚗 Всего найдено в базе: {len(items)}")
        for item in items:
            process_car(item)
            
    except Exception as e:
        print(f"❌ Критическая ошибка API: {e}")

if __name__ == "__main__":
    main()
