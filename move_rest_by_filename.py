import os
import shutil

BASE_PATH = "/home/poweramanita/goldantelopeasia/moto_nhatrang"
WHATSAPP = "https://wa.me/84374961375"

def main():
    # Получаем все файлы в корне
    files = [f for f in os.listdir(BASE_PATH) if os.path.isfile(os.path.join(BASE_PATH, f)) and f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    print(f"📦 Обработка оставшихся {len(files)} фото...")

    for photo in files:
        # Имя папки = имя файла без расширения
        folder_name = os.path.splitext(photo)[0].replace('-', '_').replace(' ', '_')
        folder_path = os.path.join(BASE_PATH, folder_name)
        
        # Создаем папку
        os.makedirs(folder_path, exist_ok=True)
        
        # Переносим фото
        src = os.path.join(BASE_PATH, photo)
        dst = os.path.join(folder_path, "photo.jpg")
        shutil.move(src, dst)
        
        # Создаем описание
        display_name = folder_name.replace('_', ' ').replace('moto ', '').title()
        description = (
            f"🛵 {display_name}\n\n"
            f"💰 Стоимость и доступность уточняйте у менеджера.\n"
            f"✅ Шлемы и дождевики включены в стоимость аренды.\n\n"
            f"📲 WhatsApp для связи: {WHATSAPP}"
        )
        
        with open(os.path.join(folder_path, "description.txt"), "w", encoding="utf-8") as f:
            f.write(description)
            
        print(f"✅ Создана папка: {folder_name}")

    print("\n🚀 Все остатки распределены!")

if __name__ == "__main__":
    main()
