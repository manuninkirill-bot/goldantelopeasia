import os
import shutil
import re

BASE_PATH = "/home/poweramanita/goldantelopeasia/auto_nhatrang"

def slugify(text):
    # Очистка имени для точного сравнения (только буквы и цифры)
    return "".join(re.findall(r'[a-z0-9]', text.lower()))

def main():
    # 1. Получаем список всех фото в корне
    root_files = [f for f in os.listdir(BASE_PATH) if os.path.isfile(os.path.join(BASE_PATH, f))]
    image_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    root_photos = [f for f in root_files if f.lower().endswith(image_extensions)]
    
    # 2. Получаем список всех папок
    folders = [d for d in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, d))]
    
    print(f"🔎 Найдено фото в корне: {len(root_photos)}")
    print(f"📂 Всего папок для проверки: {len(folders)}")
    print("-" * 30)

    moved_count = 0

    for folder in folders:
        folder_path = os.path.join(BASE_PATH, folder)
        photo_target = os.path.join(folder_path, "photo.jpg")
        
        # Проверяем, если в папке еще нет фото
        if not os.path.exists(photo_target):
            folder_slug = slugify(folder)
            
            # Ищем подходящее фото в корне
            for photo_name in root_photos:
                photo_slug = slugify(os.path.splitext(photo_name)[0])
                
                # Если имя фото содержится в названии папки или наоборот
                if photo_slug in folder_slug or folder_slug in photo_slug:
                    print(f"✅ Найдено соответствие: '{photo_name}' -> папка '{folder}'")
                    shutil.copy2(os.path.join(BASE_PATH, photo_name), photo_target)
                    moved_count += 1
                    break # Берем только одно фото для папки

    print("-" * 30)
    print(f"🚀 Итог: Добавлено {moved_count} новых фото в пустые папки.")

if __name__ == "__main__":
    main()
