import os, re

base = os.path.expanduser("~/my_parser/restaurants_all/restaurants_danang")
src = os.path.join(base, "description_ru.txt")

if not os.path.exists(src):
    print("❌ Файл description_ru.txt не найден!")
    exit()

with open(src, "r", encoding="utf-8") as f:
    content = f.read()

# Разбиваем на блоки по цифрам (1. , 2. ...)
blocks = re.split(r'(?=\d+\.\s)', content)
blocks = [b.strip() for b in blocks if b.strip()]

# Получаем список всех папок ресторанов (сортируем их, чтобы был порядок)
folders = sorted([d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d))])

print(f"📂 Папок найдено: {len(folders)}")
print(f"📝 Описаний найдено: {len(blocks)}")

count = 0
# Берем столько, сколько есть и того, и другого
for i in range(min(len(blocks), len(folders))):
    folder = folders[i]
    block = blocks[i]
    
    dest_path = os.path.join(base, folder, "description_ru.txt")
    with open(dest_path, "w", encoding="utf-8") as out:
        out.write(block)
    
    print(f"✅ Готово: {folder}")
    count += 1

print(f"\n🏁 Завершено! Разложено {count} файлов.")
