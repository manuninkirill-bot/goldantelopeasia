import os

BASE_PATH = "/home/poweramanita/goldantelopeasia/moto_nhatrang"

def main():
    if not os.path.exists(BASE_PATH):
        print("❌ Ошибка: Папка moto_nhatrang не найдена.")
        return

    folders = [d for d in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, d))]
    total_folders = len(folders)
    
    with_photo = 0
    with_desc = 0
    full_ready = 0
    missing_data = []

    for folder in folders:
        folder_path = os.path.join(BASE_PATH, folder)
        files = os.listdir(folder_path)
        
        has_photo = any(f.lower() == "photo.jpg" for f in files)
        has_desc = any(f.lower() == "description.txt" for f in files)
        
        if has_photo: with_photo += 1
        if has_desc: with_desc += 1
        if has_photo and has_desc: 
            full_ready += 1
        else:
            missing_data.append(folder)

    print(f"📊 --- ОТЧЕТ ПО MOTO_NHATRANG ---")
    print(f"Всего папок (моделей): {total_folders}")
    print(f"Папок с фото (photo.jpg): {with_photo}")
    print(f"Папок с описанием (description.txt): {with_desc}")
    print(f"✅ ПОЛНОСТЬЮ ГОТОВЫ (фото + текст): {full_ready}")
    
    if missing_data:
        print(f"\n⚠️ Внимание! В этих папках чего-то не хватает:")
        for m in missing_data:
            print(f" - {m}")
    else:
        print(f"\n✨ ИДЕАЛЬНО: Во всех папках есть и фото, и описание!")

if __name__ == "__main__":
    main()
