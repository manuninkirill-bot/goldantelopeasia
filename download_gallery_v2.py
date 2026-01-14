import os, requests, time, re
from bs4 import BeautifulSoup

TARGET_FOLDER = "/home/poweramanita/goldantelopeasia/auto_nhatrang/KIA Seltos 2022-2023"
URL = "https://getmecar.ru/listing/kia-seltos-2022-2023-ili-analog-v-nyachange-vetnam/"

def main():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}
    os.makedirs(TARGET_FOLDER, exist_ok=True)

    print(f"📡 Глубокий поиск фото на странице KIA Seltos...")
    try:
        response = requests.get(URL, headers=headers, timeout=15)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        
        # Собираем все возможные ссылки на изображения
        images = set()
        
        # 1. Ищем во всех тегах <a> и <img>, включая data-атрибуты
        for tag in soup.find_all(['a', 'img']):
            for attr in ['href', 'src', 'data-src', 'data-lazy', 'data-thumb']:
                val = tag.get(attr)
                if val and any(ext in val.lower() for ext in ['.jpg', '.jpeg', '.png']):
                    # Отсекаем иконки и мусор (обычно фото машин содержат /upload/ или /wp-content/)
                    if 'upload' in val or 'wp-content' in val:
                        if not val.startswith('http'):
                            val = "https://getmecar.ru" + val
                        images.add(val)

        # 2. Ищем ссылки напрямую в тексте скриптов (JSON/Array)
        script_images = re.findall(r'https?://getmecar\.ru/upload/[^"\']+?\.(?:jpg|jpeg|png)', html)
        images.update(script_images)

        print(f"📸 Найдено потенциальных фото: {len(images)}")

        count = 0
        for i, img_url in enumerate(sorted(images)):
            try:
                # Пропускаем мелкие превью (обычно в названии есть размеры типа 100x75)
                if any(size in img_url for size in ['100_75', '50x50', 'avatar']):
                    continue
                    
                print(f"   📥 Скачиваю {img_url.split('/')[-1]}...", end=" ", flush=True)
                img_data = requests.get(img_url, timeout=10).content
                
                # Сохраняем только если файл больше 10 КБ (чтобы не качать пустые заглушки)
                if len(img_data) > 10000:
                    filename = f"photo_{count+1}.jpg"
                    with open(os.path.join(TARGET_FOLDER, filename), "wb") as f:
                        f.write(img_data)
                    print("✅")
                    count += 1
                else:
                    print("⏩ пропущено (мал)")
            except:
                print("❌ ошибка")
            
            if count >= 10: break # Нам хватит 10 основных фото
            time.sleep(0.3)

    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
