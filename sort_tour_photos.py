import os
import shutil
import re

BASE_PATH = "/home/poweramanita/goldantelopeasia/tours_nhatrang"

def main():
    # Список файлов в корне tours_nhatrang
    files = [f for f in os.listdir(BASE_PATH) if os.path.isfile(os.path.join(BASE_PATH, f)) and f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    folders = [d for d in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, d))]
    
    print(f"📸 Найдено {len(files)} фото для распределения по экскурсиям...")

    # Маппинг ключевых слов к папкам
    mapping = {
        "Vinpearl_Island_Tour": ["vinpearl", "wonders", "hon_tre"],
        "Four_Islands_Snorkeling": ["island", "snorkeling", "mun", "boat", "sea"],
        "Dalat_City_Escape": ["dalat", "waterfall", "flower", "crazy_house"],
        "Ba_Ho_Waterfalls_Hiking": ["ba_ho", "baho", "hiking", "jungle"],
        "Cham_Towers_Cultural_Tour": ["cham", "tower", "nagar", "pagoda", "culture"]
    }

    stats = {f: 0 for f in folders}

    for photo in files:
        photo_lower = photo.lower()
        target_folder = None
        
        # Ищем совпадение по ключевым словам
        for folder, keywords in mapping.items():
            if any(key in photo_lower for key in keywords):
                if stats[folder] < 5: # Лимит 5 фото на папку
                    target_folder = folder
                    break
        
        if target_folder:
            stats[target_folder] += 1
            src = os.path.join(BASE_PATH, photo)
            # Переименовываем для красоты: photo_1.jpg, photo_2.jpg...
            ext = os.path.splitext(photo)[1]
            dst = os.path.join(BASE_PATH, target_folder, f"photo_{stats[target_folder]}{ext}")
            shutil.move(src, dst)
            print(f"✅ {photo} -> {target_folder}/photo_{stats[target_folder]}{ext}")
        else:
            print(f"❓ Не удалось определить папку для: {photo}")

    print("\n🚀 Распределение завершено!")
    for f, count in stats.items():
        print(f"📍 {f}: {count} фото")

if __name__ == "__main__":
    main()
