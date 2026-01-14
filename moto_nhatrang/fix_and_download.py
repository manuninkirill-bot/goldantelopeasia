import os, requests, re, time
from PIL import Image
from io import BytesIO

BASE_PATH = "/home/poweramanita/goldantelopeasia/moto_nhatrang"

def download_and_save(search_query, save_path):
    # Используем проверенный источник
    url = f"https://source.unsplash.com/800x600/?car,{search_query.replace(' ', ',')}"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content)).convert("RGB")
            img.thumbnail((800, 800))
            img.save(save_path, "JPEG", quality=55, optimize=True)
            return True
    except:
        return False

def main():
    # Проходим по всем папкам в директории
    folders = [d for d in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, d))]
    
    print(f"📁 Найдено папок для проверки: {len(folders)}")

    for folder in folders:
        folder_path = os.path.join(BASE_PATH, folder)
        
        # Получаем имя для поиска (чистим подчеркивания)
        search_term = folder.replace('_', ' ').split(' или')[0]
        
        # Считаем сколько уже есть фото (jpg)
        existing_photos = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]
        count = len(existing_photos)
        
        if count < 4:
            needed = 4 - count
            print(f"📦 Папка: {folder} (есть {count}, нужно еще {needed})")
            
            for i in range(1, 5):
                photo_name = f"photo{i}.jpg"
                save_path = os.path.join(folder_path, photo_name)
                
                # Если такого файла еще нет - качаем
                if not os.path.exists(save_path):
                    if download_and_save(search_term, save_path):
                        print(f"   [+] {photo_name} скачан")
                        time.sleep(1) # Защита от бана
        else:
            print(f"✅ Папка {folder} уже заполнена")

if __name__ == "__main__":
    main()
