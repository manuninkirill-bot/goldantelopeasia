import os
import requests
from bs4 import BeautifulSoup
import re
from PIL import Image
from io import BytesIO

BASE_PATH = "/home/poweramanita/goldantelopeasia/auto_nhatrang"
SOURCE_URL = "https://getmecar.ru/locations/vetnam/"

def slugify(text):
    return re.sub(r'\W+', ' ', text).lower().strip()

def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    print(f"🌐 Подключаюсь к {SOURCE_URL}...")
    try:
        response = requests.get(SOURCE_URL, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return

    # Находим все карточки машин
    # На GetMeCar карточки обычно в div с определенным классом (например 'car-item' или по ссылкам)
    cards = soup.find_all('div', class_='catalog-item') # Класс может меняться, адаптируем под структуру
    
    if not cards:
        # Пробуем найти альтернативным способом (по ссылкам на авто)
        cards = soup.find_all('a', class_='catalog-item__title')
        print(f"🔍 Найдено {len(cards)} потенциальных карточек.")

    # Создаем карту: "название" -> "ссылка на фото"
    car_photos = {}
    for card in soup.select('.catalog-item'):
        name_tag = card.select_one('.catalog-item__title')
        img_tag = card.select_one('img')
        
        if name_tag and img_tag:
            name = name_tag.get_text(strip=True)
            img_url = img_tag.get('src') or img_tag.get('data-src')
            if img_url:
                if not img_url.startswith('http'):
                    img_url = "https://getmecar.ru" + img_url
                car_photos[slugify(name)] = img_url

    print(f"✅ Собрано ссылок на фото: {len(car_photos)}")

    # Сопоставляем с нашими папками
    local_folders = [d for d in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, d))]
    
    success_count = 0
    for folder in local_folders:
        folder_slug = slugify(folder)
        photo_path = os.path.join(BASE_PATH, folder, "photo.jpg")
        
        # Ищем совпадение в спарсенных данных
        match_url = None
        for name_slug, url in car_photos.items():
            if folder_slug in name_slug or name_slug in folder_slug:
                match_url = url
                break
        
        if match_url:
            print(f"📸 Качаю оригинал для: {folder}")
            try:
                img_res = requests.get(match_url, headers=headers, timeout=15)
                img = Image.open(BytesIO(img_res.content)).convert("RGB")
                img.thumbnail((1200, 1200)) # Оригиналы лучше в чуть большем качестве
                img.save(photo_path, "JPEG", quality=75, optimize=True)
                print(f"   [+] Сохранено")
                success_count += 1
            except Exception as e:
                print(f"   [!] Ошибка загрузки: {e}")

    print(f"\n🏁 Итог: Обновлено {success_count} фото из реальных объявлений.")

if __name__ == "__main__":
    main()
