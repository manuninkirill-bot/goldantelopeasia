import os
import shutil
import re

BASE_PATH = "/home/poweramanita/goldantelopeasia/moto_nhatrang"

def get_clean_tokens(text):
    # Заменяем популярные опечатки и убираем лишнее
    text = text.lower().replace('nuvo', 'nouvo').replace('impuls', 'impulse')
    # Ищем все слова и отдельно цифры
    tokens = re.findall(r'[a-z]+|\d+', text)
    return set(tokens)

def main():
    # 1. Список файлов в корне
    files = [f for f in os.listdir(BASE_PATH) if os.path.isfile(os.path.join(BASE_PATH, f)) and f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    # 2. Список папок
    folders = [d for d in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, d))]
    
    print(f"📊 Найдено фото для распределения: {len(files)}")

    moved_count = 0

    for photo in files:
        photo_tokens = get_clean_tokens(photo)
        best_folder = None
        max_overlap = 0

        for folder in folders:
            folder_tokens = get_clean_tokens(folder)
            # Считаем количество совпавших слов и цифр
            overlap = len(photo_tokens.intersection(folder_tokens))
            
            if overlap > max_overlap:
                # Проверяем, нет ли там уже фото
                if not os.path.exists(os.path.join(BASE_PATH, folder, "photo.jpg")):
                    max_overlap = overlap
                    best_folder = folder

        if best_folder and max_overlap >= 2: # Минимум 2 совпадения (например, модель + цифра)
            src = os.path.join(BASE_PATH, photo)
            dst = os.path.join(BASE_PATH, best_folder, "photo.jpg")
            shutil.move(src, dst)
            print(f"✅ {photo} -> {best_folder}")
            moved_count += 1
        else:
            print(f"❓ Не нашел точного места для: {photo}")

    print(f"\n🚀 Итог: Перенесено {moved_count} фото.")

if __name__ == "__main__":
    main()
