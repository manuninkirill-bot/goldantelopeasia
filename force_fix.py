import os, requests

BASE = "/home/poweramanita/goldantelopeasia/auto_nhatrang"

# Словарь: Прямой путь к папке -> Ссылка на фото
mapping = {
    "Toyota Raize Автомат 2022-2024": "https://getmecar.ru/listing/toyota-raize-avtomat-2022-2024-ili-analog-v-nyachange-vetnam_41576f707114_20cb2aeec7ca_23436e6788c8/",
    "Toyota Raize 2023-2024": "https://getmecar.ru/listing/toyota-raize-avtomat-2022-2024-ili-analog-v-nyachange-vetnam_41576f707114_20cb2aeec7ca_23436e6788c8_f83a669985e7/",
    "Mitsubishi Expander 2022-2024": "https://getmecar.ru/listing/mitsubishi-expander-2022-2024-ili-analog-v-nyachange-vetnam_e76e0fdd75d5/",
    "Mitsubishi Expander 7 Мест 2021-2023": "https://getmecar.ru/listing/mitsubishi-expander-7-mest-2021-2023-ili-analog-v-nyachange-vetnam_670d1af892b0_8505fd98e009_fe00a4131112/",
    "KIA Carnival 7 Мест 2023-2024": "https://getmecar.ru/listing/kia-carnival-7-mest-2022-2023-ili-analog-v-nyachange-vetnam/",
    "Hyundai Creta Автомат 2022-2024": "https://getmecar.ru/listing/hyundai-creta-2022-2023-ili-analog-v-nyachange-vetnam/",
    "MG 5 2023 2025": "https://getmecar.ru/listing/mg-5-2023-2024-ili-analog-v-nyachange-vetnam/",
    "KIA Seltos Автомат 2022-2024": "https://getmecar.ru/listing/kia-seltos-2022-2023-ili-analog-v-nyachange-vetnam/"
}

headers = {"User-Agent": "Mozilla/5.0"}

for folder, url in mapping.items():
    full_path = os.path.join(BASE, folder)
    if os.path.exists(full_path):
        print(f"📥 Качаю для {folder}...", end=" ", flush=True)
        try:
            res = requests.get(url, headers=headers, timeout=10)
            import re
            img_match = re.search(r'property="og:image" content="([^"]+)"', res.text)
            if img_match:
                img_url = img_match.group(1)
                img_data = requests.get(img_url, timeout=10).content
                with open(os.path.join(full_path, "photo.jpg"), "wb") as f:
                    f.write(img_data)
                print("✅")
            else:
                print("❌ не нашел фото в коде")
        except:
            print("❌ ошибка сети")
    else:
        print(f"⚠️ Папка не найдена: {folder}")

