import os
import asyncio
from telethon import TelegramClient
from telethon.errors import ApiIdInvalidError
from PIL import Image
from langdetect import detect
from deep_translator import GoogleTranslator

# НОВЫЕ ДАННЫЕ
API_ID = 32881984
API_HASH = 'd2588f09dfbc5103ef77ef21c07dbf8b'
CHANNEL = 'hanoi_rent'
LIMIT = 200
BASE_PATH = '/home/poweramanita/goldantelopeasia/HanoiRent'

def compress_image(path):
    try:
        img = Image.open(path)
        if img.mode in ("RGBA", "P"): img = img.convert("RGB")
        img.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
        quality = 70
        img.save(path, "JPEG", optimize=True, quality=quality)
        while os.path.getsize(path) > 51200 and quality > 15:
            quality -= 5
            img.save(path, "JPEG", optimize=True, quality=quality)
    except: pass

async def main():
    translator = GoogleTranslator(source='en', target='ru')
    client = TelegramClient('hanoi_final_session', API_ID, API_HASH)
    
    try:
        await client.start(phone=lambda: '+84343893121')
        print(f"✅ Успешный вход! Начинаю сбор 200 постов из @{CHANNEL}...")
        
        if not os.path.exists(BASE_PATH): os.makedirs(BASE_PATH)
        
        count = 0
        async for message in client.iter_messages(CHANNEL, limit=LIMIT):
            if not message.text: continue
            
            post_folder = f"post_{message.id}"
            post_path = os.path.join(BASE_PATH, post_folder)
            os.makedirs(post_path, exist_ok=True)

            # 1. Текст (Оригинал)
            with open(os.path.join(post_path, 'description.txt'), 'w', encoding='utf-8') as f:
                f.write(message.text)
            
            # 2. Перевод
            try:
                if detect(message.text) == 'en':
                    ru_text = translator.translate(message.text)
                    with open(os.path.join(post_path, 'description_ru.txt'), 'w', encoding='utf-8') as f:
                        f.write(ru_text)
            except: pass

            # 3. Фото + Сжатие
            if message.photo:
                photo_path = await message.download_media(file=os.path.join(post_path, 'photo.jpg'))
                compress_image(photo_path)

            count += 1
            if count % 10 == 0:
                print(f"📈 Обработано: {count}/200...")

        print(f"✨ Готово! Все данные в: {BASE_PATH}")

    except ApiIdInvalidError:
        print("❌ Ошибка: Даже новые ключи отклонены. Проверь API_HASH на наличие пробелов.")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
