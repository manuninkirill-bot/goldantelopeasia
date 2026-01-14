import os, requests, re, time
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

BASE_PATH = "/home/poweramanita/goldantelopeasia/auto_nhatrang"
SOURCE_URL = "https://getmecar.ru/locations/vetnam/"

def slugify(text):
    text = text.lower()
    # Убираем лишний шум для точного поиска
    text = re.sub(r'или аналог.*|в нячанге.*|вьетнам.*|аренда.*|автомат.*', '', text)
    return "".join(re.findall(r'[a-z0-9]', text))

def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://getmecar.ru/"
    }
    
    print(f"🌐 Подключение к GetMeCar...")
    try:
        response = requests.get(SOURCE_URL, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"❌ Ошибка сети: {e}")
        return

    # На GetMeCar фото лежат в элементах с классом 'catalog-item'
    items = soup.find_all('div', class_=re.compile(r'catalog-item|item'))
    print(f"🔍 Найдено {len(items)} карточек на странице.")

    # Создаем базу: название -> ссылка на фото
    site_data = []
    for item in items:
        title_tag = item.find(['div', 'a', 'h3'], class_=re.compile(r'title|name'))
        img_tag = item.find('img')
        
        if title_tag and img_tag:
            name = title_tag.get_text(strip=True)
            # Извлекаем путь к фото (на сайте часто data-src для ленивой загрузки)
            img_url = img_tag.get('data-src') or img_tag.get('src') or img_tag.get('data-original')
            
            if img_url:
                if not img_url.startswith('http'):
                    img_url = "https://getmecar.ru" + img_url
                site_data.append({'name': name, 'url': img_url})

    # Сопоставление с локальными папками
    folders = [d for d in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, d))]
    success = 0

    for folder in folders:
        f_slug = slugify(folder)
        photo_path = os.path.join(BASE_PATH, folder, "photo.jpg")
        
        for car in site_data:
            c_slug = slugify(car['name'])
            # Если название папки совпадает с названием на сайте
            if f_slug in c_slug or c_slug in f_slug:
                print(f"📸 Скачиваю оригинал для: {folder}")
                try:
                    img_res = requests.get(car['url'], headers=headers, timeout=15)
                    if img_res.status_code == 200:
                        img = Image.open(BytesIO(img_res.content)).convert("RGB")
                        img.save(photo_path, "JPEG", quality=90)
                        success += 1
                        time.sleep(0.5) # Небольшая задержка
                        break
                except Exception as e:
                    print(f"   ❌ Ошибка: {e}")

    print(f"\n🏁 Готово! Скачано реальных фото: {success}")

if __name__ == "__main__":
    main()
