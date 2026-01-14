import os
from langdetect import detect, DetectorFactory
from deep_translator import GoogleTranslator

# Фиксируем seed для стабильности определения языка
DetectorFactory.seed = 0
BASE_PATH = '/home/poweramanita/goldantelopeasia'
translator = GoogleTranslator(source='en', target='ru')

def translate_text(text):
    if not text.strip():
        return ""
    # Разбиваем на блоки по 2000 символов, чтобы не превышать лимиты API
    chunks = [text[i:i+2000] for i in range(0, len(text), 2000)]
    translated_chunks = [translator.translate(chunk) for chunk in chunks]
    return "".join(translated_chunks)

print("🌍 Поиск новых английских текстов для перевода...")

translated_count = 0
skipped_count = 0

for root, dirs, files in os.walk(BASE_PATH):
    if 'description.txt' in files:
        ru_path = os.path.join(root, 'description_ru.txt')
        en_path = os.path.join(root, 'description.txt')

        # ШАГ 1: Пропускаем, если перевод уже готов
        if 'description_ru.txt' in files:
            skipped_count += 1
            continue

        # ШАГ 2: Если перевода нет, проверяем язык оригинала
        try:
            with open(en_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            if len(content) > 10 and detect(content) == 'en':
                translated = translate_text(content)
                with open(ru_path, 'w', encoding='utf-8') as f_ru:
                    f_ru.write(translated)
                
                translated_count += 1
                print(f"✅ [{translated_count}] Переведено: {root}")
        except Exception as e:
            print(f"❌ Ошибка в {root}: {e}")

print(f"\n--- ИТОГ ---")
print(f"⏭️ Пропущено (уже переведены): {skipped_count}")
print(f"✨ Новых переводов создано: {translated_count}")
