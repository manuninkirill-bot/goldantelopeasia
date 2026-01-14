import os
from PIL import Image

# Путь только к папке Нячанга
TARGET_PATH = '/home/poweramanita/goldantelopeasia/realty_gohomenhatrang'

def compress_to_50kb(file_path):
    try:
        img = Image.open(file_path)
        # Убираем альфа-канал, если он есть (для JPEG)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        
        # Начальные параметры
        quality = 80
        # Ограничиваем ширину до 1200px (для 50КБ это оптимальный максимум)
        if max(img.size) > 1200:
            img.thumbnail((1200, 1200), Image.Resampling.LANCZOS)

        # Сохраняем первый раз
        img.save(file_path, "JPEG", optimize=True, quality=quality)
        
        # Если файл все еще больше 50КБ, начинаем агрессивное сжатие
        while os.path.getsize(file_path) > 51200 and quality > 10:
            quality -= 5
            img.save(file_path, "JPEG", optimize=True, quality=quality)
            
            # Если качество упало до 30, а размер не падает — уменьшаем разрешение
            if quality <= 30 and os.path.getsize(file_path) > 51200:
                w, h = img.size
                img = img.resize((int(w*0.8), int(h*0.8)), Image.Resampling.LANCZOS)
                quality = 50 # Сброс качества для нового размера
                
        return True
    except Exception as e:
        print(f"Ошибка в файле {file_path}: {e}")
        return False

print(f"🚀 Начинаю сжатие фото в {TARGET_PATH}...")

img_count = 0
for root, dirs, files in os.walk(TARGET_PATH):
    for file in files:
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            full_path = os.path.join(root, file)
            if compress_to_50kb(full_path):
                img_count += 1
                if img_count % 100 == 0:
                    print(f"📉 Обработано: {img_count} фото")

print(f"\n✨ Готово! Всего в Нячанге сжато: {img_count} фото.")
