import os
import asyncio
from telethon import TelegramClient
from telethon.errors import ApiIdInvalidError

# Твои данные БЕЗ лишних символов
API_ID = 26581404
API_HASH = '1451f1542f5664155a0242203716d900'
CHANNEL = 'hanoi_rent'
LIMIT = 200
BASE_PATH = '/home/poweramanita/goldantelopeasia/HanoiRent'

async def main():
    # Используем новое имя сессии 'clean_session'
    client = TelegramClient('clean_session', API_ID, API_HASH)
    try:
        # Принудительный запуск с вводом телефона в консоли
        await client.start(phone=lambda: '+84343893121')
        print(f"✅ Вход выполнен успешно!")
        
        if not os.path.exists(BASE_PATH): os.makedirs(BASE_PATH)
        
        count = 0
        async for message in client.iter_messages(CHANNEL, limit=LIMIT):
            if not message.text: continue
            
            post_path = os.path.join(BASE_PATH, f"post_{message.id}")
            os.makedirs(post_path, exist_ok=True)
            
            # Сохраняем текст
            with open(os.path.join(post_path, 'description.txt'), 'w', encoding='utf-8') as f:
                f.write(message.text)
            
            # Если есть фото - качаем
            if message.photo:
                await message.download_media(file=os.path.join(post_path, 'photo.jpg'))
            
            count += 1
            if count % 10 == 0:
                print(f"📥 Загружено {count} объявлений...")
                
        print(f"✨ Готово! Всего собрано: {count}")

    except ApiIdInvalidError:
        print("❌ Ошибка: API_ID или API_HASH всё еще отклоняются.")
        print("Проверь на my.telegram.org: возможно, нужно пересоздать приложение (App).")
    except Exception as e:
        print(f"❌ Другая ошибка: {e}")
    finally:
        await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
