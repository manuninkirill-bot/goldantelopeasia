import os
import hashlib

BASE_DIR = '/home/poweramanita/my_parser/realty_all/realty_Nha_Trang/viet_life_niachang'

def get_file_hash(path):
    if not os.path.exists(path): return None
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def clean_duplicates():
    seen_texts = {}  # Текст -> путь к папке
    dirs = [d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d))]
    
    removed_count = 0
    print(f"🧐 Проверка {len(dirs)} папок на дубликаты...")

    for d in sorted(dirs):
        path = os.path.join(BASE_DIR, d)
        desc_path = os.path.join(path, 'description.txt')
        
        if os.path.exists(desc_path):
            with open(desc_path, 'r', encoding='utf-8') as f:
                text = f.read().strip()
            
            # Если текст короче 10 символов, это мусор
            if len(text) < 10:
                os.system(f'rm -rf "{path}"')
                removed_count += 1
                continue

            # Проверка на дубликат текста
            if text in seen_texts:
                print(f"🗑️ Удален дубликат: {d} (совпадает с {seen_texts[text]})")
                os.system(f'rm -rf "{path}"')
                removed_count += 1
            else:
                seen_texts[text] = d

    print(f"✨ Проверка завершена. Удалено {removed_count} папок.")

if __name__ == '__main__':
    clean_duplicates()
