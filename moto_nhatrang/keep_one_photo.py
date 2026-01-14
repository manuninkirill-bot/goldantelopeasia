import os

BASE_PATH = "/home/poweramanita/goldantelopeasia/moto_nhatrang"

def main():
    folders = [d for d in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, d))]
    print(f"🧹 Начинаю очистку в {len(folders)} папках...")

    for folder in folders:
        folder_path = os.path.join(BASE_PATH, folder)
        # Получаем список всех изображений в папке
        photos = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        
        if not photos:
            print(f"⚠️ В папке [{folder}] нет фото.")
            continue
        
        # Оставляем первое фото
        keep_photo = photos[0]
        final_name = "photo.jpg"
        
        # Переименовываем выбранное фото в photo.jpg (если оно еще не так называется)
        src_path = os.path.join(folder_path, keep_photo)
        dst_path = os.path.join(folder_path, final_name)
        
        if src_path != dst_path:
            # Если photo.jpg уже существует, сначала удалим его, чтобы заменить на первое из списка
            if os.path.exists(dst_path):
                os.remove(dst_path)
            os.rename(src_path, dst_path)
        
        # Удаляем все остальные фото
        for extra_photo in photos[1:]:
            extra_path = os.path.join(folder_path, extra_photo)
            if os.path.exists(extra_path):
                os.remove(extra_path)
        
        print(f"✅ Готово: {folder} (оставлено только {final_name})")

    print("\n🏁 Теперь в каждой папке строго по 1 фотографии.")

if __name__ == "__main__":
    main()
