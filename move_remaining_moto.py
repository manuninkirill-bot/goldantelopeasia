import os
import shutil
import re

BASE_PATH = "/home/poweramanita/goldantelopeasia/moto_nhatrang"

def get_keywords(text):
    # Разбиваем название на слова и берем только значимые (длиной > 2 симв)
    words = re.findall(r'[a-z0-9]{3,}', text.lower())
    return set(words)

def main():
    # 1. Получаем список фото в корне
    root_files = [f for f in os.listdir(BASE_PATH) if os.path.isfile(os.path.join(BASE_PATH, f))]
    image_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    photos = [f for f in root_files if f.lower().endswith(image_extensions)]
    
    # 2. Получаем список папок
    folders = [d for d in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, d))]
    
    print(f"🧐 Анализируем {len(photos)} оставшихся фото...")

    moved_count = 0

    for photo in photos:
        photo_stem = os.path.splitext(photo)[0].lower()
        photo_keywords = get_keywords(photo_stem)
        
        best_match = None
        
        for folder in folders:
            folder_keywords = get_keywords(folder)
            
            # Если хотя бы два ключевых слова совпали (например, "Yamaha" и "Nouvo")
            # Или если одно уникальное (например, "Vespa")
            common = photo_keywords.intersection(folder_keywords)
            
            if common:
                # Если папка пустая, это наш кандидат
                if not os.path.exists(os.path.join(BASE_PATH, folder, "photo.jpg")):
                    best_match = folder
                    break
        
        if best_match:
            src = os.path.join(BASE_PATH, photo)
            dst = os.path.join(BASE_PATH, best_match, "photo.jpg")
            shutil.move(src, dst)
            print(f"✅ Найдено: '{photo}' перемещено в '{best_match}'")
            moved_count += 1
        else:
            print(f"❓ Не удалось сопоставить: {photo}")

    print("-" * 30)
    print(f"🚀 Итог: Перенесено еще {moved_count} фото.")

if __name__ == "__main__":
    main()
