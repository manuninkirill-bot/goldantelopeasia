import os, requests, re
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

BASE_PATH = "/home/poweramanita/goldantelopeasia/auto_nhatrang"
SOURCE_URL = "https://getmecar.ru/locations/vetnam/"

def slugify(text):
    # Убираем все лишнее, оставляем только латиницу и цифры
    text = text.lower()
    text = re.sub(r'или аналог.*|в нячанге.*|вьетнам.*|аренда.*', '', text)
    return "".join(re.findall(r'[a-z0-9]', text))

def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print(f"🌐 Подключаюсь к {SOURCE_URL}...")
    try:
        res = requests.get(SOURCE_URL, headers=headers, timeout=30)
        soup = BeautifulSoup(res.text, 'html.parser')
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return

    # Собираем абсолютно все картинки и ищем текст в их родительских блоках
    data_map = []
    for img in soup.find_all('img'):
        # Ищем ссылку на фото
        src = img.get('data-src') or img.get('src') or img.get('data-original')
        if not src or 'logo' in src.lower() or 'icon' in src.lower():
            continue
            
        if not src.startswith('http'):
            src = "https://getmecar.ru" + src

        # Ищем текст (название машины) в ближайшем окружении картинки
        container = img.find_parent('div', class_=re.compile(r'item|card|product|info'))
        if not container:
            container = img.find_parent('div')
        
        text = container.get_text(" ", strip=True) if container else ""
        if len(text) > 5:
            data_map.append({'name': text, 'url': src})

    print(f"✅ Найдено потенциальных фото на странице: {len(data_map)}")

    folders = [d for d in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, d))]
    updated = 0

    for folder in folders:
        f_slug = slugify(folder)
        # Если в папке уже есть photo.jpg, мы его перезапишем реальным фото
        photo_path = os.path.join(BASE_PATH, folder, "photo.jpg")
        
        for item in data_map:
            c_slug = slugify(item['name'])
            # Проверяем, есть ли совпадение (например "toyotavios" есть в тексте карточки)
            if f_slug in c_slug or c_slug in f_slug:
                print(f"📸 Нашел оригинал для: {folder}")
                try:
                    img_res = requests.get(item['url'], headers=headers, timeout=15)
                    img = Image.open(BytesIO(img_res.content)).convert("RGB")
                    img.save(photo_path, "JPEG", quality=85)
                    updated += 1
                    break
                except:
                    continue

    print(f"\n🏁 Успешно обновлено: {updated} фото.")

if __name__ == "__main__":
    main()
