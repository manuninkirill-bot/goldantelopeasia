import os, requests, time, re

BASE_PATH = "/home/poweramanita/goldantelopeasia/auto_nhatrang"
urls = [
    "https://getmecar.ru/listing/mitsubishi-expander-7-mest-2021-2023-ili-analog-v-nyachange-vetnam_670d1af892b0_8505fd98e009_fe00a4131112/",
    "https://getmecar.ru/listing/kia-carnival-2023-2024-ili-analog-v-nyachange-vetnam/",
    "https://getmecar.ru/listing/kia-carnival-2023-2024-ili-analog-v-nyachange-vetnam_1c2793d4b119_9c57e698e14d_6eb1ae71a42d/",
    "https://getmecar.ru/listing/honda-city-2018-2020-ili-analog-v-nyachange-vetnam_7d061e0632e4/",
    "https://getmecar.ru/listing/mg-5-2023-2024-ili-analog-v-nyachange-vetnam/",
    "https://getmecar.ru/listing/mazda3-2019-2020-ili-analog-v-nyachange-vetnam_294189d81002/",
    "https://getmecar.ru/listing/hyundai-creta-2022-2023-ili-analog-v-nyachange-vetnam/",
    "https://getmecar.ru/listing/toyota-raize-avtomat-2022-2024-ili-analog-v-nyachange-vetnam_41576f707114_20cb2aeec7ca_23436e6788c8/",
    "https://getmecar.ru/listing/kia-k3-2022-2023-ili-analog-v-nyachange-vetnam/"
]

def slugify(text):
    return "".join(re.findall(r'[a-z0-9]', text.lower().replace('xpander', 'expander')))

def main():
    headers = {"User-Agent": "Mozilla/5.0"}
    folders = [d for d in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, d))]
    
    print(f"🚀 Начинаю загрузку {len(urls)} фото...")
    
    for i, url in enumerate(urls, 1):
        model_slug = slugify(url.split('/')[-2].split('_')[0])
        print(f"[{i}/{len(urls)}] Поиск папки для {model_slug}...", end=" ", flush=True)
        
        target = next((f for f in folders if model_slug in slugify(f) or slugify(f) in model_slug), None)
        
        if target:
            try:
                # Ставим таймаут 10 секунд, чтобы не зависало
                res = requests.get(url, headers=headers, timeout=10)
                img_match = re.search(r'property="og:image" content="([^"]+)"', res.text)
                
                if img_match:
                    img_url = img_match.group(1)
                    img_data = requests.get(img_url, timeout=10).content
                    with open(os.path.join(BASE_PATH, target, "photo.jpg"), "wb") as f:
                        f.write(img_data)
                    print(f"✅ Сохранено в '{target}'")
                else:
                    print("❌ Фото не найдено в коде")
            except Exception as e:
                print(f"⚠️ Ошибка сервера: {e}")
        else:
            print("❓ Папка не найдена")
        time.sleep(1) # Пауза, чтобы не забанили

if __name__ == "__main__":
    main()
