import os
import shutil
import re

BASE_PATH = "/home/poweramanita/goldantelopeasia/moto_nhatrang"

def extract_info(text):
    text = text.lower().replace('nuvo', 'nouvo').replace('impuls', 'impulse').replace('elizabethmax', 'elizabeth')
    cc_match = re.search(r'(\d{3})cc', text)
    cc = cc_match.group(1) if cc_match else ""
    
    models = ['nouvo', 'nvx', 'pcx', 'sh', 'lead', 'vision', 'vespa', 'shadow', 'z1000', 'burgman', 'lexi', 'impulse', 'elizabeth']
    found_model = None
    for m in models:
        if m in text:
            found_model = m
            break
    # Особый случай для Shadow, чтобы не путал с SH
    if 'shadow' in text: found_model = 'shadow'
    
    return cc, found_model

def main():
    files = [f for f in os.listdir(BASE_PATH) if os.path.isfile(os.path.join(BASE_PATH, f)) and f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    folders = [d for d in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, d))]
    
    print(f"🛠 Обработка {len(files)} оставшихся фото...")

    for photo in files:
        p_cc, p_model = extract_info(photo)
        if not p_model: 
            print(f"❌ Не определена модель для: {photo}")
            continue

        # Ищем базовую папку для этой модели
        target_folder = None
        for folder in folders:
            f_cc, f_model = extract_info(folder)
            if p_model == f_model:
                target_folder = folder
                break
        
        if target_folder:
            # Создаем уникальное имя папки, если основная уже занята
            base_new_name = target_folder
            counter = 2
            final_folder = base_new_name
            
            while os.path.exists(os.path.join(BASE_PATH, final_folder, "photo.jpg")):
                final_folder = f"{base_new_name}_{counter}"
                counter += 1
            
            new_dir = os.path.join(BASE_PATH, final_folder)
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)
                # Копируем описание из родительской папки, если оно там есть
                src_desc = os.path.join(BASE_PATH, target_folder, "description.txt")
                if os.path.exists(src_desc):
                    shutil.copy2(src_desc, os.path.join(new_dir, "description.txt"))

            # Перемещаем фото
            shutil.move(os.path.join(BASE_PATH, photo), os.path.join(new_dir, "photo.jpg"))
            print(f"✅ Создана папка и добавлено фото: {final_folder}")
        else:
            print(f"❓ Не найдена база для модели {p_model} ({photo})")

if __name__ == "__main__":
    main()
