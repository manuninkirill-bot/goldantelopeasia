import os, requests, re, time
from PIL import Image
from io import BytesIO

BASE_PATH = "/home/poweramanita/goldantelopeasia/moto_nhatrang"
INPUT_FILE = "cars_list.txt"

def slugify(text):
    return re.sub(r'\W+', '_', text).lower().strip("_")

def download_photo(car_name, path):
    # Пытаемся найти фото через превью-сервис по названию модели
    search_query = car_name.split(" или")[0].replace(" ", "+")
    # Используем проверенный источник для авто-фото
    img_url = f"https://api.duckduckgo.com/assets/logo.png" # Резерв
    # Попробуем напрямую имитировать поиск картинки
    test_url = f"https://source.unsplash.com/800x600/?car,{search_query}"
    
    try:
        res = requests.get(test_url, timeout=10)
        img = Image.open(BytesIO(res.content)).convert("RGB")
        img.thumbnail((800, 800))
        img.save(path, "JPEG", quality=55, optimize=True)
        return True
    except:
        return False

def main():
    if not os.path.exists(INPUT_FILE):
        print("❌ Файл не найден!")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Разделяем блоки по слову "Аренда"
    blocks = content.split("Аренда")
    
    for block in blocks:
        lines = [l.strip() for l in block.strip().split("\n") if l.strip()]
        if len(lines) < 2: continue
        
        car_name = lines[0]
        folder_name = slugify(car_name)
        car_dir = os.path.join(BASE_PATH, folder_name)
        
        print(f"🚗 Обработка: {car_name}")
        os.makedirs(car_dir, exist_ok=True)
        
        # Сохраняем описание
        with open(os.path.join(car_dir, "description.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
            
        # Качаем и сжимаем фото
        photo_path = os.path.join(car_dir, "photo.jpg")
        if download_photo(car_name, photo_path):
            size = os.path.getsize(photo_path) // 1024
            print(f"   ✅ Фото готово ({size} KB)")
        
        time.sleep(0.5)

if __name__ == "__main__":
    main()
