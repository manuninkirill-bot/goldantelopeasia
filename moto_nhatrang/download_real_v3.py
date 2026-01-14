import os, requests, re, time
from PIL import Image, ImageFile
from io import BytesIO

# Позволяет PIL работать с поврежденными файлами
ImageFile.LOAD_TRUNCATED_IMAGES = True

BASE_PATH = "/home/poweramanita/goldantelopeasia/auto_nhatrang"
SOURCE_URL = "https://getmecar.ru/locations/vetnam/"

def slugify(text):
    text = text.lower()
    text = re.sub(r'или аналог.*|в нячанге.*|вьетнам.*|аренда.*|автомат.*', '', text)
    return "".join(re.findall(r'[a-z0-9]', text))

def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "Referer": "https://getmecar.ru/"
    }
    
    print(f"🌐 Подключение к GetMeCar...")
    try:
        response = requests.get(SOURCE_URL, headers=headers, timeout=30)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"❌ Ошибка сети: {e}")
        return

    items = soup.find_all('div', class_=re.compile(r'catalog-item|item'))
    print(f"🔍 Найдено {len(items)} карточек. Начинаю сопоставление...")

    folders = [d for d in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, d))]
    success = 0

    for item in items:
        title_tag = item.find(['div', 'a', 'h3'], class_=re.compile(r'title|name'))
        img_tag = item.find('img')
        
        if title_tag and img_tag:
            name = title_tag.get_text(strip=True)
            img_url = img_tag.get('data-src') or img_tag.get('src') or img_tag.get('data-original')
            
            if not img_url: continue
            if not img_url.startswith('http'): img_url = "https://getmecar.ru" + img_url
            
            c_slug = slugify(name)

            for folder in folders:
                f_slug = slugify(folder)
                # Если нашли совпадение и в папке еще нет photo.jpg
                photo_path = os.path.join(BASE_PATH, folder, "photo.jpg")
                
                if (f_slug in c_slug or c_slug in f_slug) and not os.path.exists(photo_path):
                    print(f"📸 Загрузка для: {folder}...")
                    try:
                        img_res = requests.get(img_url, headers=headers, timeout=15)
                        if img_res.status_code == 200:
                            # Пробуем открыть и пересохранить в JPEG
                            img_data = BytesIO(img_res.content)
                            img = Image.open(img_data).convert("RGB")
                            img.save(photo_path, "JPEG", quality=85)
                            print(f"   ✅ Успешно")
                            success += 1
                            time.sleep(0.3)
                    except Exception as e:
                        print(f"   ❌ Ошибка PIL: {e}. Пробую сохранить файл напрямую...")
                        # Если PIL не узнал формат, сохраняем как есть (бинарно)
                        with open(photo_path, 'wb') as f:
                            f.write(img_res.content)
                        success += 1

    print(f"\n🏁 Итог: Реальные фото установлены в {success} папок.")

if __name__ == "__main__":
    main()
