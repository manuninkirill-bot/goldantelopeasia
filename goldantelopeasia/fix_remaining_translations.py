import os
from langdetect import detect, DetectorFactory
from deep_translator import GoogleTranslator

DetectorFactory.seed = 0
BASE_PATH = '/home/poweramanita/goldantelopeasia'
translator = GoogleTranslator(source='en', target='ru')

print("🔍 Поиск объявлений без перевода...")

count = 0
for root, dirs, files in os.walk(BASE_PATH):
    if 'description.txt' in files and 'description_ru.txt' not in files:
        try:
            with open(os.path.join(root, 'description.txt'), 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            # Если текст не на русском, переводим
            if len(content) > 10 and detect(content) != 'ru':
                print(f"🌐 Перевожу: {os.path.relpath(root, BASE_PATH)}")
                translated = translator.translate(content)
                with open(os.path.join(root, 'description_ru.txt'), 'w', encoding='utf-8') as f_ru:
                    f_ru.write(translated)
                count += 1
        except Exception as e:
            print(f"⚠️ Ошибка в {root}: {e}")

print(f"\n✅ Готово! Добавлено {count} новых переводов.")
