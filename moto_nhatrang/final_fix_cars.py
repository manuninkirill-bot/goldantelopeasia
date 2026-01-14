import os, re, requests, shutil
from PIL import Image
from io import BytesIO

BASE_PATH = "/home/poweramanita/goldantelopeasia/moto_nhatrang"

def get_clean_name(folder):
    # Пропускаем мотоциклы
    if folder.startswith(('moto-', 'Байк-', 'Motorbike_')):
        return folder
    # Очистка названия авто
    name = folder.replace('_', ' ')
    name = re.split(r' или| в | вьетнам', name, flags=re.IGNORECASE)[0].strip()
    name = name.title()
    for abbr in ['Kia', 'Mg', 'Bmw', 'Hrv', 'Cx-5', 'Vf9']:
        name = name.replace(abbr.title(), abbr.upper())
    return name

def download_photo(query, path):
    url = f"https://source.unsplash.com/800x600/?car,{query.replace(' ', ',')}"
    try:
        res = requests.get(url, timeout=10)
        img = Image.open(BytesIO(res.content)).convert("RGB")
        img.thumbnail((800, 800))
        img.save(path, "JPEG", quality=55, optimize=True)
        return True
    except:
        return False

# 1. Переименование
folders = [d for d in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, d))]
for f in folders:
    old_p = os.path.join(BASE_PATH, f)
    new_n = get_clean_name(f)
    new_p = os.path.join(BASE_PATH, new_n)
    
    if old_p != new_p:
        if not os.path.exists(new_p):
            os.rename(old_p, new_p)
            print(f"✅ Переименовано: {new_n}")
        else:
            for item in os.listdir(old_p):
                shutil.move(os.path.join(old_p, item), os.path.join(new_p, item))
            os.rmdir(old_p)
            print(f"📦 Объединено: {new_n}")

# 2. Докачка фото
for d in os.listdir(BASE_PATH):
    dir_p = os.path.join(BASE_PATH, d)
    if os.path.isdir(dir_p):
        photo_p = os.path.join(dir_p, "photo.jpg")
        if not os.path.exists(photo_p):
            print(f"📡 Качаю фото для: {d}")
            download_photo(d, photo_p)

print("\n🏁 Готово! Проверь папку ls")
