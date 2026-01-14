import os
import shutil
import re

BASE_PATH = "/home/poweramanita/goldantelopeasia/moto_nhatrang"

def extract_info(text):
    text = text.lower()
    # Ищем объем двигателя (цифры перед cc)
    cc_match = re.search(r'(\[0-9\]{3})cc', text)
    cc = cc_match.group(1) if cc_match else None
    
    # Ключевые слова моделей
    models = ['nouvo', 'nvx', 'pcx', 'sh', 'lead', 'vision', 'vespa', 'shadow', 'z1000', 'burgman', 'lexi', 'impulse', 'elizabeth']
    found_model = None
    for m in models:
        if m in text.replace('nuvo', 'nouvo').replace('impuls', 'impulse'):
            found_model = m
            break
    return cc, found_model

def main():
    files = [f for f in os.listdir(BASE_PATH) if os.path.isfile(os.path.join(BASE_PATH, f)) and f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    folders = [d for d in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, d))]
    
    print(f"🧬 Анализируем {len(files)} фото по CC и модели...")

    for photo in files:
        p_cc, p_model = extract_info(photo)
        if not p_model:
            continue

        moved = False
        for folder in folders:
            f_cc, f_model = extract_info(folder)
            
            # Проверяем совпадение модели и (если есть) объема CC
            if p_model == f_model:
                # Если у обоих указан CC, они должны совпадать. Если у кого-то нет - верим модели.
                if p_cc and f_cc and p_cc != f_cc:
                    continue
                
                target_path = os.path.join(BASE_PATH, folder, "photo.jpg")
                if not os.path.exists(target_path):
                    shutil.move(os.path.join(BASE_PATH, photo), target_path)
                    print(f"🎯 Точное попадание: {photo} -> {folder}")
                    moved = True
                    break
        
        if not moved:
            print(f"🔍 Не нашел пустую папку для: {photo} (Model: {p_model}, CC: {p_cc})")

if __name__ == "__main__":
    main()
