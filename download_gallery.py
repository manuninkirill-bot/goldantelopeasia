import os, requests, time, re
from bs4 import BeautifulSoup

# Целевая папка
TARGET_FOLDER = "/home/poweramanita/goldantelopeasia/auto_nhatrang/KIA Seltos 2022-2023"
URL = "https://getmecar.ru/listing/kia-seltos-2022-2023-ili-analog-v-nyachange-vetnam/"

def main():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    
    if not os.path.exists(TARGET_FOLDER):
        os.makedirs(TARGET_FOLDER, exist_ok=True)
        print(f"📁 Создана папка: {TARGET_FOLDER}")

    print(f"📡 Подключение к странице KIA Seltos...")
    try:
        response = requests.get(URL, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        images = []
        # Ищем все ссылки на картинки в галерее (Fancybox)
        # На GetMeCar фото обычно лежат в ссылках с классом gallery-item или просто в ссылках на jpg
        links = soup.find_all('a', href=re.compile(r'\.(jpg|jpeg|png)$'))
        
        for link in links:
            img_url = link.get('href')
            if img_url:
                if not img_url.startswith('http'):
                    img_url = "https://getmecar.ru" + img_url
                if img_url not in images:
                    images.append(img_url)

        # Если ничего не нашли через ссылки, берем og:image
        if not images:
            og_img = soup.find('meta', property="og:image")
            if og_img:
                images.append(og_img['content'])

        print(f"📸 Найдено фото: {len(images)}")

        for i, img_url in enumerate(images):
            try:
                print(f"   📥 Скачиваю фото {i+1}...", end=" ")
                img_data = requests.get(img_url, timeout=10).content
                filename = f"photo_{i+1}.jpg"
                with open(os.path.join(TARGET_FOLDER, filename), "wb") as f:
                    f.write(img_data)
                print("✅")
            except:
                print("❌ ошибка")
            time.sleep(0.5)

    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
