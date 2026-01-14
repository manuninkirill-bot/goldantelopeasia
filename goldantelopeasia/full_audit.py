import os
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0
BASE_PATH = '/home/poweramanita/goldantelopeasia'

print(f"{'Папка':<60} | {'RU текст':<10} | {'Фото < 50KB':<12}")
print("-" * 88)

stats = {"total": 0, "no_ru": 0, "large_photo": 0}

for root, dirs, files in os.walk(BASE_PATH):
    if 'description.txt' in files:
        stats["total"] += 1
        
        # 1. Проверка перевода
        has_ru = "description_ru.txt" in files
        is_ru_origin = False
        
        try:
            with open(os.path.join(root, 'description.txt'), 'r', encoding='utf-8') as f:
                text = f.read().strip()
                if len(text) > 10:
                    lang = detect(text)
                    if lang == 'ru':
                        is_ru_origin = True
        except:
            pass

        translation_status = "✅" if (has_ru or is_ru_origin) else "❌"
        if not (has_ru or is_ru_origin): stats["no_ru"] += 1

        # 2. Проверка размера фото
        photo_status = "---"
        if 'photo.jpg' in files:
            size_kb = os.path.getsize(os.path.join(root, 'photo.jpg')) / 1024
            if size_kb <= 51: # небольшой запас
                photo_status = f"✅ {int(size_kb)}K"
            else:
                photo_status = f"❌ {int(size_kb)}K"
                stats["large_photo"] += 1
        
        # Выводим только проблемные или кратко все
        if translation_status == "❌" or "❌" in photo_status:
            relative_path = os.path.relpath(root, BASE_PATH)
            print(f"{relative_path[:60]:<60} | {translation_status:^10} | {photo_status:<12}")

print("-" * 88)
print(f"📊 ИТОГО:")
print(f"📁 Всего объявлений: {stats['total']}")
print(f"🌐 Нужен перевод: {stats['no_ru']}")
print(f"🖼 Тяжелых фото (>50KB): {stats['large_photo']}")
