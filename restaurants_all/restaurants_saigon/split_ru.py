import os
import re

# Указываем путь к папке Saigon
base_path = os.path.expanduser("~/my_parser/restaurants_all/restaurants_saigon")
source_file = os.path.join(base_path, "description_ru.txt")

if not os.path.exists(source_file):
    print(f"❌ Файл не найден по пути: {source_file}")
    exit()

with open(source_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Разбиваем общий файл на блоки (по цифрам в начале строки: 1. , 2. и т.д.)
blocks = re.split(r'\n(?=\d+\.\s)', content)
folders = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]

print(f"🔄 Всего папок в Saigon: {len(folders)}")
print(f"📝 Описаний в файле: {len(blocks)}")

for block in blocks:
    block = block.strip()
    if not block: continue
    
    # Извлекаем имя из первой строки блока (например, "1. Al Sham Saigon")
    first_line = block.split('\n')[0]
    match = re.match(r'^\d+\.\s+(.+)', first_line)
    
    if match:
        res_name_raw = match.group(1).strip()
        # Подготавливаем имя для поиска (нижний регистр, пробелы в подчеркивания)
        search_name = res_name_raw.lower().replace(" ", "_")
        
        target_folder = None
        for folder in folders:
            # Ищем, содержит ли имя папки название ресторана
            if search_name in folder.lower().replace("-", "_"):
                target_folder = folder
                break
        
        if target_folder:
            dest_path = os.path.join(base_path, target_folder, "description_ru.txt")
            with open(dest_path, 'w', encoding='utf-8') as f_out:
                f_out.write(block)
            print(f"✅ Готово: {target_folder}/description_ru.txt")
        else:
            print(f"⚠️ Папка для '{res_name_raw}' не найдена")

print("\n🏁 Распределение завершено!")
