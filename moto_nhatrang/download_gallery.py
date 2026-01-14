import os, requests, re, time
from PIL import Image
from io import BytesIO

BASE_PATH = "/home/poweramanita/goldantelopeasia/moto_nhatrang"
INPUT_FILE = "cars_list.txt"

def slugify(text):
    return re.sub(r'\W+', '_', text).lower().strip("_")

def download_and_save(search_query, save_path):
    # Используем источник с качественными фото авто
    url = f"https://source.unsplash.com/800x600/?car,{search_query.replace(' ', ',')}"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content)).convert("RGB")
            img.thumbnail((800, 800))
            # Сжатие до ~50КБ (quality 50-60 обычно дает такой результат)
            img.save(save_path, "JPEG", quality=55, optimize=True)
            return True
    except Exception as e:
        print(f"      ❌ Ошибка загрузки: {e}")
    return False

def main():
    if not os.path.exists(INPUT_FILE):
        print("❌ Файл cars_list.txt не найден!")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    blocks = content.split("Аренда")
    
    for block in blocks:
        lines = [l.strip() for l in block.strip().split("\n") if l.strip()]
        if not lines: continue
        
        car_name = lines[0]
        # Очищаем название от лишних слов для лучшего поиска
        search_term = car_name.split(" или")[0].replace(",", "")
        folder_name = slugify(car_name)
        car_dir = os.path.join(BASE_PATH, folder_name)
        
        if not os.path.exists(car_dir):
            os.makedirs(car_dir)

        print(f"📸 Загрузка галереи для: {car_name}")
        
        for i in range(1, 5):
            photo_name = f"photo{i}.jpg"
            save_path = os.path.join(car_dir, photo_name)
            
            # Проверяем, чтобы не качать заново, если файл уже есть
            if os.path.exists(save_path):
                print(f"   [#] {photo_name} уже существует")
                continue
                
            success = download_and_save(search_term, save_path)
            if success:
                size = os.path.getsize(save_path) // 1024
                print(f"   [+] {photo_name} сохранен ({size} KB)")
            
            # Небольшая пауза, чтобы сервис не заблокировал запросы
            time.sleep(1)

    print("\n🏁 Все галереи обновлены!")

if __name__ == "__main__":
    main()
