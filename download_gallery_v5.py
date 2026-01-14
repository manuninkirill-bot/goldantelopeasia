import os, requests, time, re

TARGET_FOLDER = "/home/poweramanita/goldantelopeasia/auto_nhatrang/KIA Seltos 2022-2023"
URL = "https://getmecar.ru/listing/kia-seltos-2022-2023-ili-analog-v-nyachange-vetnam/"

def main():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}
    
    if os.path.exists(TARGET_FOLDER):
        for file in os.listdir(TARGET_FOLDER):
            if file.startswith("photo_"): os.remove(os.path.join(TARGET_FOLDER, file))
    os.makedirs(TARGET_FOLDER, exist_ok=True)

    print(f"📡 Глубокое сканирование страницы KIA Seltos...")
    try:
        response = requests.get(URL, headers=headers, timeout=15)
        html_text = response.text
        
        # Ищем ВСЕ упоминания путей к картинкам в формате Bitrix (/upload/iblock/...)
        # Ищем совпадения типа /upload/iblock/xxx/xxxxxx.jpg или .jpeg
        pattern = r'/upload/iblock/[^"\']+?\.(?:jpg|jpeg|png)'
        raw_links = re.findall(pattern, html_text)
        
        images = []
        for link in raw_links:
            # Игнорируем превьюшки (resize_cache) и дубликаты
            if 'resize_cache' not in link:
                full_url = "https://getmecar.ru" + link if not link.startswith('http') else link
                if full_url not in images:
                    images.append(full_url)

        # Ограничиваем количество, если их слишком много (обычно в галерее 4-8 фото)
        # Первые фото в коде — это обычно галерея.
        print(f"📸 Найдено в коде оригинальных фото: {len(images)}")

        count = 0
        for i, img_url in enumerate(images):
            # Проверка: если в ссылке есть 'logo' или 'resize', пропускаем
            if 'logo' in img_url.lower(): continue
            
            try:
                print(f"   📥 Загрузка фото {count+1}...", end=" ", flush=True)
                img_data = requests.get(img_url, timeout=10).content
                
                # Сохраняем только если файл весомый (больше 20кб), чтобы не скачать иконки
                if len(img_data) > 20000:
                    filename = f"photo_{count+1}.jpg"
                    with open(os.path.join(TARGET_FOLDER, filename), "wb") as f:
                        f.write(img_data)
                    print("✅")
                    count += 1
                else:
                    print("⏩ пропущено (малый размер)")
            except:
                print("❌ ошибка")
            
            if count >= 8: break # Нам не нужно больше 8 фото одной машины
            time.sleep(0.3)

    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
