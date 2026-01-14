import os, requests, time, re

BASE_PATH = "/home/poweramanita/goldantelopeasia/auto_nhatrang"
# Оставшиеся ссылки
urls = [
    "https://getmecar.ru/listing/mitsubishi-expander-7-mest-2021-2023-ili-analog-v-nyachange-vetnam_670d1af892b0_8505fd98e009_fe00a4131112/",
    "https://getmecar.ru/listing/mazda3-2019-2020-ili-analog-v-nyachange-vetnam_294189d81002/",
    "https://getmecar.ru/listing/toyota-raize-avtomat-2022-2024-ili-analog-v-nyachange-vetnam_41576f707114_20cb2aeec7ca_23436e6788c8/"
]

def clean(name):
    return "".join(re.findall(r'[a-z0-9]', name.lower().replace('xpander', 'expander')))

def main():
    headers = {"User-Agent": "Mozilla/5.0"}
    folders = [d for d in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, d))]
    
    for url in urls:
        raw_name = url.split('/')[-2].split('_')[0]
        url_slug = clean(raw_name)
        
        # Улучшенный поиск: ищем частичное совпадение
        target = None
        for f in folders:
            f_slug = clean(f)
            if url_slug[:15] in f_slug or f_slug[:15] in url_slug:
                target = f
                break
        
        if target:
            print(f"🎯 Найдено: '{target}' для {raw_name}...", end=" ", flush=True)
            try:
                res = requests.get(url, headers=headers, timeout=10)
                img_match = re.search(r'property="og:image" content="([^"]+)"', res.text)
                if img_match:
                    img_data = requests.get(img_match.group(1), timeout=10).content
                    with open(os.path.join(BASE_PATH, target, "photo.jpg"), "wb") as f:
                        f.write(img_data)
                    print("✅")
            except: print("❌")
        else:
            print(f"❓ Не удалось сопоставить: {raw_name}")

if __name__ == "__main__":
    main()
