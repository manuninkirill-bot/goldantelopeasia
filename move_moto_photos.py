import os
import shutil
import re

BASE_PATH = "/home/poweramanita/goldantelopeasia/moto_nhatrang"

def slugify(text):
    # Убираем все кроме букв и цифр для точного сравнения
    return "".join(re.findall(r'[a-z0-9]', text.lower()))

def main():
    # 1. Список всех файлов в корне moto_nhatrang
    root_files = [f for f in os.listdir(BASE_PATH) if os.path.isfile(os.path.join(BASE_PATH, f))]
    image_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    root_photos = [f for f in root_files if f.lower().endswith(image_extensions)]
    
    # 2. Список папок (моделей байков)
    folders = [d for d in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, d))]
    
    print(f"📸 Найдено фото в корне: {len(root_photos)}")
    print(f"📁 Папок для заполнения: {len(folders)}")
    print("-" * 30)

    moved_count = 0

    for photo in root_photos:
        photo_name_slug = slugify(os.path.splitext(photo)[0])
        
        for folder in folders:
            folder_slug = slugify(folder)
            target_path = os.path.join(BASE_PATH, folder, "photo.jpg")
            
            # Если папка уже содержит фото, пропускаем её
            if os.path.exists(target_path):
                continue
                
            # Проверка соответствия (например, "hondalead" в "hondalead2024")
            if photo_name_slug in folder_slug or folder_slug in photo_name_slug:
                src_path = os.path.join(BASE_PATH, photo)
                shutil.move(src_path, target_path)
                print(f"✅ Перенесено: {photo} -> {folder}/photo.jpg")
                moved_count += 1
                break

    print("-" * 30)
    print(f"🚀 Итог: {moved_count} фото распределено по папкам.")

if __name__ == "__main__":
    main()
