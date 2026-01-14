import asyncio
import os
import re
from telethon import TelegramClient
from PIL import Image

api_id = 32881984
api_hash = 'd2588f09dfbc5103ef77ef21c07dbf8b'

CHANNELS = [
    'DaNangApartmentRent',
    'danang_arenda',
    'DaNangRentAFlat',
    'Danang_House',
    'danag_viet_life_rent'
]

BASE_PATH = '/home/poweramanita/goldantelopeasia'

def clean_text(text):
    if not text: return ""
    # Удаляем эмодзи и иконки, оставляя только текст и цифры
    clean = re.sub(r'[^\w\s\d\.,!?-]', '', text)
    return clean.strip()

async def compress_image(path):
    try:
        img = Image.open(path)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        
        quality = 80
        img.save(path, "JPEG", optimize=True, quality=quality)
        # Сжимаем, пока файл больше 100 КБ
        while os.path.getsize(path) > 105000 and quality > 20:
            quality -= 5
            img.save(path, "JPEG", optimize=True, quality=quality)
    except Exception as e:
        print(f"Ошибка сжатия {path}: {e}")

async def main():
    async with TelegramClient('session_da_nang', api_id, api_hash) as client:
        for channel in CHANNELS:
            print(f"\n--- 📂 КАНАЛ: {channel} ---")
            channel_dir = os.path.join(BASE_PATH, channel)
            os.makedirs(channel_dir, exist_ok=True)
            
            count = 0
            async for message in client.iter_messages(channel, limit=1000):
                if count >= 200: break
                
                if message.text and len(message.text) > 30 and message.grouped_id:
                    msgs = await client.get_messages(channel, ids=None, min_id=message.id-10, max_id=message.id+10)
                    album = [m for m in msgs if m.grouped_id == message.grouped_id and m.photo]
                    
                    if len(album) >= 4:
                        post_folder = os.path.join(channel_dir, f"post_{message.id}")
                        if os.path.exists(post_folder): continue
                        
                        os.makedirs(post_folder, exist_ok=True)
                        with open(os.path.join(post_folder, 'description.txt'), 'w', encoding='utf-8') as f:
                            f.write(clean_text(message.text))
                        
                        for i, m in enumerate(album):
                            p_path = os.path.join(post_folder, f"photo_{i+1}.jpg")
                            await client.download_media(m, file=p_path)
                            await compress_image(p_path)
                        
                        count += 1
                        print(f"✅ [{channel}] {count}/200")

        print("\n🏆 ГОТОВО! Проверь папки в goldantelopeasia")

if __name__ == '__main__':
    asyncio.run(main())
