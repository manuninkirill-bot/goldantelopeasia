import asyncio
import os
import shutil
from telethon import TelegramClient

# Твои рабочие ключи
api_id = 32881984
api_hash = 'd2588f09dfbc5103ef77ef21c07dbf8b'

channel = 'Viet_life_niachang'
base_path = '/home/poweramanita/goldantelopeasia/viet_life_niachang'

async def main():
    # Используем новое имя сессии, чтобы не конфликтовать
    client = TelegramClient('session_vlife', api_id, api_hash)
    await client.start()
    
    print(f"📡 Подключение успешно. Начинаю поиск 500 объектов в {channel}...")
    os.makedirs(base_path, exist_ok=True)
    
    count = 0
    # Просматриваем до 3000 сообщений, чтобы набрать 500 качественных
    async for message in client.iter_messages(channel, limit=3000):
        if count >= 500:
            break
            
        # Нам нужны посты с текстом
        if message.text and len(message.text) > 30:
            # Проверяем наличие альбома (grouped_id)
            if message.grouped_id:
                # Ищем все сообщения из этого альбома
                album_messages = await client.get_messages(channel, ids=None, min_id=message.id-12, max_id=message.id+12)
                photos = [m for m in album_messages if m.grouped_id == message.grouped_id and m.photo]
                
                # Если фото 4 или больше — забираем
                if len(photos) >= 4:
                    folder_path = os.path.join(base_path, f"post_{message.id}")
                    if os.path.exists(folder_path):
                        continue
                        
                    os.makedirs(folder_path, exist_ok=True)
                    
                    # Сохраняем текст
                    with open(os.path.join(folder_path, 'description.txt'), 'w', encoding='utf-8') as f:
                        f.write(message.text)
                    
                    # Качаем фото
                    for i, p in enumerate(photos):
                        await client.download_media(p, file=os.path.join(folder_path, f"photo_{i+1}.jpg"))
                    
                    count += 1
                    print(f"✅ [{count}/500] Сохранен пост {message.id} ({len(photos)} фото)")
    
    print(f"\n✨ Готово! Папка {base_path} пополнена.")
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
