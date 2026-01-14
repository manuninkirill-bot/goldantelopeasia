import os, requests, time
from PIL import Image
from io import BytesIO

BASE_PATH = "/home/poweramanita/goldantelopeasia/auto_nhatrang"

def main():
    if not os.path.exists(BASE_PATH):
        print("❌ Директория auto_nhatrang не найдена!")
        return

    folders = [d for d in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, d))]
    print(f"🧐 Проверяю {len(folders)} папок на наличие фото...")

    for folder in folders:
        folder_path = os.path.join(BASE_PATH, folder)
        photo_path = os.path.join(folder_path, "photo.jpg")
        
        # Если фото нет или папка пуста
        if not os.path.exists(photo_path):
            print(f"📸 Качаю фото для: {folder}")
            # Формируем запрос для поиска
            query = folder.replace(' ', '+')
            url = f"https://source.unsplash.com/800x600/?car,{query}"
            
            try:
                res = requests.get(url, timeout=15)
                if res.status_code == 200:
                    img = Image.open(BytesIO(res.content)).convert("RGB")
                    img.thumbnail((800, 800))
                    img.save(photo_path, "JPEG", quality=60, optimize=True)
                    print(f"   ✅ Сохранено в {folder}")
                    time.sleep(1.5) # Пауза чтобы не забанили
                else:
                    print(f"   ⚠️ Ошибка сервера: {res.status_code}")
            except Exception as e:
                print(f"   ❌ Ошибка: {e}")

    print("\n🏁 Все папки проверены!")

if __name__ == "__main__":
    main()
