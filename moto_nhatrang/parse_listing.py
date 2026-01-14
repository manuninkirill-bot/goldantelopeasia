import os, requests, re
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

BASE_PATH = "/home/poweramanita/goldantelopeasia/auto_nhatrang"
SOURCE_URL = "https://getmecar.ru/listing/"

def slugify(text):
    # Убираем лишние слова и оставляем только суть (бренд модель год)
    text = re.sub(r'или аналог.*|в нячанге.*|вьетнам.*', '', text, flags=re.IGNORECASE)
    # Оставляем только буквы и цифры
    return "".join(re.findall(r'[a-z0-9]', text.lower().replace(' ', '')))

def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }
    
    print(f"🌐 Загружаю список авто с {SOURCE_URL}...")
    try:
        response = requests.get(SOURCE_URL, headers=headers, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"❌ Ошибка сети: {e}")
        return

    # Находим карточки авто. На GetMeCar это обычно блоки с классом 'listing-item' или 'card'
    car_data = []
    # Ищем все изображения, которые находятся внутри ссылок на объявления
    for card in soup.find_all(['div', 'a'], class_=re.compile(r'item|card|listing')):
        title_tag = card.find(['h3', 'h4', 'div', 'a'], class_=re.compile(r'title|name'))
        img_tag = card.find('img')
        
        if title_tag and img_tag:
            name = title_tag.get_text(strip=True)
            # Извлекаем URL картинки из разных возможных атрибутов
            src = img_tag.get('data-src') or img_tag.get('src') or img_tag.get('data-original') or img_tag.get('srcset')
            
            if src:
                # Очистка URL, если там srcset
                src = src.split(' ')[0]
                if not src.startswith('http'):
                    src = "https://getmecar.ru" + src
                car_data.append({'name': name, 'url': src})

    print(f"✅ Найдено фото на странице: {len(car_data)}")

    if not car_data:
        print("🤔 Не удалось найти карточки. Возможно, изменилась верстка.")
        return

    folders = [d for d in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, d))]
    updated = 0

    for folder in folders:
        f_slug = slugify(folder)
        photo_path = os.path.join(BASE_PATH, folder, "photo.jpg")
        
        for car in car_data:
            c_slug = slugify(car['name'])
            # Проверка на пересечение названий
            if f_slug in c_slug or c_slug in f_slug:
                print(f"📸 Обновляю фото для: {folder}")
                try:
                    res = requests.get(car['url'], headers=headers, timeout=15)
                    img = Image.open(BytesIO(res.content)).convert("RGB")
                    img.thumbnail((1000, 1000))
                    img.save(photo_path, "JPEG", quality=80, optimize=True)
                    updated += 1
                    break
                except Exception as e:
                    print(f"   ❌ Ошибка загрузки {folder}: {e}")
                    continue

    print(f"\n🏁 Итог: Реальные фото установлены в {updated} папок.")

if __name__ == "__main__":
    main()
