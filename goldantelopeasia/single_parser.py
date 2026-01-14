import os
import asyncio
from telethon import TelegramClient

API_ID = 32881984
API_HASH = 'd2588f09dfbc5103ef77ef21c07dbf8b'
CHANNEL = 'Viet_life_niachang'
LIMIT = 300 # Берем чуть больше сообщений, чтобы закрыть дыры
OUTPUT_DIR = '/home/poweramanita/my_parser/realty_all/realty_Nha_Trang/viet_life_niachang'

async def main():
    async with TelegramClient('anon', API_ID, API_HASH) as client:
        print(f"🚀 Докачиваем недостающее в {CHANNEL}...")
        
        groups = {}

        async for message in client.iter_messages(CHANNEL, limit=LIMIT):
            # Группируем по альбомам или по ID сообщения
            folder_id = message.grouped_id if message.grouped_id else message.id
            post_folder = os.path.join(OUTPUT_DIR, f"tg_{folder_id}")
            
            if not os.path.exists(post_folder):
                os.makedirs(post_folder, exist_ok=True)

            # 1. Добавляем описание, если его еще нет
            desc_path = os.path.join(post_folder, "description.txt")
            if message.text and not os.path.exists(desc_path):
                with open(desc_path, "w", encoding="utf-8") as f:
                    f.write(message.text)
                print(f"  📝 Добавлено описание для {folder_id}")

            # 2. Добавляем фото, пока их не станет 4
            existing_photos = [f for f in os.listdir(post_folder) if f.startswith("photo_")]
            if message.photo and len(existing_photos) < 4:
                # Находим следующий свободный номер фото
                for i in range(1, 5):
                    p_name = f"photo_{i}.jpg"
                    if not os.path.exists(os.path.join(post_folder, p_name)):
                        await message.download_media(file=os.path.join(post_folder, p_name))
                        print(f"  📸 Добавлено фото {i} в папку {folder_id}")
                        break

        print(f"✨ Дозапись завершена!")

if __name__ == '__main__':
    asyncio.run(main())
