import os
import shutil

BASE_PATH = "/home/poweramanita/goldantelopeasia/moto_nhatrang"

def main():
    # 1. Список всех фото в корне
    files = [f for f in os.listdir(BASE_PATH) 
             if f.lower().endswith(('.jpg', '.jpeg', '.png')) 
             and os.path.isfile(os.path.join(BASE_PATH, f))]
    
    # 2. Список всех папок
    folders = [d for d in os.listdir(BASE_PATH) 
               if os.path.isdir(os.path.join(BASE_PATH, d))]

    print(f"🔍 Найдено {len(files)} фото в корне. Начинаю сопоставление...")

    moved = 0
    for file_name in files:
        # Очищаем имя файла для поиска (убираем расширение и делаем мелкий шрифт)
        clean_name = file_name.lower().split('.')[0].replace('_', ' ').replace('-', ' ')
        
        # Пытаемся найти папку, в которой есть слова из имени файла
        found_folder = None
        for folder in folders:
            # Если хотя бы одно значимое слово из названия файла есть в названии папки
            # (например "vios" есть в "toyota_vios_2018...")
            words = [w for w in clean_name.split() if len(w) > 2] # Игнорируем короткие слова
            if any(word in folder.lower() for word in words):
                found_folder = folder
                break
        
        if found_folder:
            src = os.path.join(BASE_PATH, file_name)
            target_dir = os.path.join(BASE_PATH, found_folder)
            
            # Считаем текущие фото в папке для нового имени
            count = len([f for f in os.listdir(target_dir) if f.endswith('.jpg')])
            new_name = f"photo{count + 1}.jpg"
            
            shutil.move(src, os.path.join(target_dir, new_name))
            print(f"✅ {file_name} -> {found_folder}/{new_name}")
            moved += 1
        else:
            print(f"❓ Не нашел папку для: {file_name}")

    print(f"\n🏁 Перемещено: {moved} из {len(files)}")

if __name__ == "__main__":
    main()
