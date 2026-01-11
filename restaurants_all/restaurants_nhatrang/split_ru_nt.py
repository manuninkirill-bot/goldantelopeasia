import os
import re

# Путь к папке Нячанга
base_path = os.path.expanduser("~/my_parser/restaurants_all/restaurants_nhatrang")
source_file = os.path.join(base_path, "description_ru.txt")

if not os.path.exists(source_file):
    print(f"❌ Файл не найден: {source_file}")
    print("Загрузи файл description_ru.txt в папку restaurants_nhatrang и запусти снова.")
    exit()

with open(source_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Разрезаем файл на блоки по номерам (1. , 2. и т.д.)
blocks = re.split(r'\n(?=\d+\.\s)', content)
folders = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]

print(f"🔄 Ресторанов в папке: {len(folders)}")
print(f"📝 Описаний в файле: {len(blocks)}")

for block in blocks:
    block = block.strip()
    if not block: continue
    
    # Берем название из первой строки блока
    first_line = block.split('\n')[0]
    match = re.match(r'^\d+\.\s+(.+)', first_line)
    
    if match:
        res_name_raw = match.group(1).strip()
        # Готовим имя для поиска (маленькие буквы, пробелы -> подчеркивания)
        search_name = res_name_raw.lower().replace(" ", "_")
        
        target_folder = None
        for folder in folders:
            # Ищем совпадение (например, "al_sham" в "al_sham_nhatrang_123")
            if search_name in folder.lower().replace("-", "_"):
                target_folder = folder
                break
        
        if target_folder:
            dest_path = os.path.join(base_path, target_folder, "description_ru.txt")
            with open(dest_path, 'w', encoding='utf-8') as f_out:
                f_out.write(block)
            print(f"✅ Готово: {target_folder}")
        else:
            print(f"⚠️ Папка не найдена для: '{res_name_raw}'")

print("\n🏁 Распределение в Нячанге завершено!")
