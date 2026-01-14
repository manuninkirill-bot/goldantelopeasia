import os, requests, time, re
from bs4 import BeautifulSoup

TARGET_FOLDER = "/home/poweramanita/goldantelopeasia/auto_nhatrang/KIA Seltos 2022-2023"
URL = "https://getmecar.ru/listing/kia-seltos-2022-2023-ili-analog-v-nyachange-vetnam/"

def main():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}
    
    if os.path.exists(TARGET_FOLDER):
        for file in os.listdir(TARGET_FOLDER):
            if file.startswith("photo_"): os.remove(os.path.join(TARGET_FOLDER, file))
    os.makedirs(TARGET_FOLDER, exist_ok=True)

    print(f"📡 Анализ структуры страницы KIA Seltos...")
    try:
        response = requests.get(URL, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Находим ВСЕ картинки, которые лежат в папке iblock (это и есть фото машин на этом сайте)
        # И исключаем те, что содержат 'resize_cache' (превьюшки)
        all_imgs = soup.find_all('img')
        images = []
        
        for img in all_imgs:
            src = img.get('src') or img.get('data-src')
            if src and '/upload/iblock/' in src and 'resize_cache' not in src:
                if not src.startswith('http'): src = "https://getmecar.ru" + src
                if src not in images:
                    images.append(src)

        # Если список пуст, попробуем взять ссылки (<a>)
        if not images:
            links = soup.find_all('a', href=re.compile(r'/upload/iblock/.*?\.(jpg|jpeg)'))
            for link in links:
                href = link.get('href')
                if href and 'resize_cache' not in href:
                    if not href.startswith('http'): href = "https://getmecar.ru" + href
                    if href not in images: images.append(href)

        print(f"📸 Найдено оригиналов: {len(images)}")

        for i, img_url in enumerate(images):
            print(f"   📥 Загрузка фото {i+1}...", end=" ", flush=True)
            img_data = requests.get(img_url, timeout=10).content
            
            filename = f"photo_{i+1}.jpg"
            with open(os.path.join(TARGET_FOLDER, filename), "wb") as f:
                f.write(img_data)
            print("✅")
            time.sleep(0.3)

    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
