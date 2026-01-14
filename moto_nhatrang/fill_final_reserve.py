import os, requests, time
from PIL import Image
from io import BytesIO

BASE_PATH = "/home/poweramanita/goldantelopeasia/auto_nhatrang"

def main():
    folders = [d for d in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, d))]
    print(f"🧐 Проверяю пустые папки через резервный сервис...")

    for folder in folders:
        folder_path = os.path.join(BASE_PATH, folder)
        photo_path = os.path.join(folder_path, "photo.jpg")
        
        if not os.path.exists(photo_path):
            print(f"📸 Резервная загрузка для: {folder}")
            # Используем LoremFlickr - он хорошо отдает по ключевым словам
            query = folder.replace(' ', ',').split(',20')[0] # Берем марку и модель до года
            url = f"https://loremflickr.com/800/600/car,{query}/all"
            
            try:
                res = requests.get(url, timeout=20)
                if res.status_code == 200:
                    img = Image.open(BytesIO(res.content)).convert("RGB")
                    img.thumbnail((800, 800))
                    img.save(photo_path, "JPEG", quality=65, optimize=True)
                    print(f"   ✅ Успешно скачано")
                    time.sleep(2) 
                else:
                    print(f"   ⚠️ Снова ошибка: {res.status_code}")
            except Exception as e:
                print(f"   ❌ Ошибка: {e}")

    print("\n🏁 Проверка завершена!")

if __name__ == "__main__":
    main()
