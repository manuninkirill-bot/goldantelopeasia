import os
import shutil
import re

BASE_PATH = "/home/poweramanita/goldantelopeasia/moto_nhatrang"

def get_clean_name(name):
    # Очищаем имя от "или аналог", "в нячанге", вьетнам и спецсимволов
    name = name.lower()
    name = name.split(" или")[0]
    name = name.split(" в ")[0]
    name = re.sub(r'[^a-z0-9]', '', name)
    return name

def merge_folders():
    folders = [d for d in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, d))]
    seen = {} # {clean_name: original_name}
    
    print("🔍 Анализ папок на дубликаты...")
    
    for f in folders:
        clean = get_clean_name(f)
        if not clean: continue
        
        if clean in seen:
            main_folder = seen[clean]
            duplicate_folder = f
            
            # Определяем, какую оставить (ту, что короче или уже существует)
            # В данном случае переносим из дубля в основную
            src = os.path.join(BASE_PATH, duplicate_folder)
            dst = os.path.join(BASE_PATH, main_folder)
            
            print(f"👯 Нашел дубль: [{duplicate_folder}] -> объединяю с [{main_folder}]")
            
            # Переносим файлы
            for item in os.listdir(src):
                s_file = os.path.join(src, item)
                # Чтобы не затереть фото, меняем имя при конфликте
                if item.endswith('.jpg'):
                    existing = len([img for img in os.listdir(dst) if img.endswith('.jpg')])
                    d_file = os.path.join(dst, f"photo_{existing + 1}.jpg")
                else:
                    d_file = os.path.join(dst, item)
                
                if not os.path.exists(d_file):
                    shutil.move(s_file, d_file)
            
            # Удаляем пустую папку дубликата
            try:
                os.rmdir(src)
            except:
                shutil.rmtree(src)
        else:
            seen[clean] = f

    print("\n🏁 Чистка завершена!")

if __name__ == "__main__":
    merge_folders()
