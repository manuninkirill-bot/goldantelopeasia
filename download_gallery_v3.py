import os, requests, time, re
from bs4 import BeautifulSoup

TARGET_FOLDER = "/home/poweramanita/goldantelopeasia/auto_nhatrang/KIA Seltos 2022-2023"
URL = "https://getmecar.ru/listing/kia-seltos-2022-2023-ili-analog-v-nyachange-vetnam/"

def main():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}
    
    # Очищаем папку от старых попыток (чтобы не было мусора)
    if os.path.exists(TARGET_FOLDER):
        for file in os.listdir(TARGET_FOLDER):
            if file.startswith("photo_") and file.endswith(".jpg"):
                os.remove(os.path.join(TARGET_FOLDER, file))
    os.makedirs(TARGET_FOLDER, exist_ok=True)

    print(f"📡 Получаю галерею KIA Seltos...")
    try:
        response = requests.get(URL, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        images = []
        
        # 1. Ищем только внутри блока галереи (на GetMeCar это обычно 'listing-gallery' или 'slick-track')
        gallery_container = soup.find('div', class_='listing-gallery') or soup.find('div', class_='images')
        
        if gallery_container:
            links = gallery_container.find_all('a', href=re.compile(r'\.(jpg|jpeg|png)$'))
            for link in links:
                img_url = link.get('href')
                if img_url and img_url not in images:
                    if not img_url.startswith('http'): img_url = "https://getmecar.ru" + img_url
                    images.append(img_url)
        
        # 2. Если в контейнере пусто, берем через Fancybox (самый точный метод для этого сайта)
        if not images:
            fancy_links = soup.find_all('a', {'data-fancybox': 'listing-gallery'})
            for link in fancy_links:
                img_url = link.get('href')
                if img_url and img_url not in images:
                    if not img_url.startswith('http'): img_url = "https://getmecar.ru" + img_url
                    images.append(img_url)

        print(f"📸 Найдено реальных фото машины: {len(images)}")

        for i, img_url in enumerate(images):
            # Пропускаем, если это явно не фото машины (логотипы, иконки)
            if any(x in img_url.lower() for x in ['logo', 'icon', 'avatar', 'app-android', 'app-ios']):
                continue
                
            print(f"   📥 Скачиваю фото {i+1}...", end=" ", flush=True)
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
