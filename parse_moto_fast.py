import os, requests, re
from PIL import Image
from io import BytesIO

BASE_PATH = "/home/poweramanita/goldantelopeasia/moto_nhatrang"
URL = "https://nhatrang-exchange.com/arenda_baykov_nyachang.html"
WHATSAPP = "https://wa.me/84374961375"

if not os.path.exists(BASE_PATH): os.makedirs(BASE_PATH)

print(f"🌐 Подключаюсь к {URL}...")
headers = {"User-Agent": "Mozilla/5.0"}

try:
    response = requests.get(URL, headers=headers, timeout=15)
    html = response.text
    
    # 1. Ищем все ссылки на картинки (Tilda хранит их в разных атрибутах)
    images = re.findall(r'https?://[^\s"\'<>]+?\.(?:jpg|jpeg|png|webp)', html)
    # 2. Ищем названия байков (обычно они в кавычках или тегах)
    # Ищем слова типа Honda, Yamaha, Vision, AirBlade и т.д.
    bike_keywords = ["Honda", "Yamaha", "Vision", "AirBlade", "Lead", "PCX", "NVX", "Vario", "Sh Mode"]
    
    found_bikes = []
    for bike in bike_keywords:
        if bike.lower() in html.lower():
            found_bikes.append(bike)

    print(f"🔍 Найдено упоминаний брендов: {len(found_bikes)}")
    print(f"📸 Найдено ссылок на фото: {len(set(images))}")

    # Попробуем создать папки хотя бы по ключевым словам
    for bike in set(found_bikes):
        folder_path = os.path.join(BASE_PATH, bike)
        if not os.path.exists(folder_path): os.makedirs(folder_path)
        
        desc = f"🛵 Аренда {bike} в Нячанге\n\nОтличное состояние.\n\n✅ WhatsApp: {WHATSAPP}"
        with open(os.path.join(folder_path, "description.txt"), "w") as f:
            f.write(desc)
        print(f"📁 Создана папка: {bike}")

    print("\n⚠️ Сайт защищен. Если папки пусты, лучше скачать 5-6 фото байков вручную и закинуть в moto_nhatrang.")

except Exception as e:
    print(f"❌ Ошибка: {e}")

