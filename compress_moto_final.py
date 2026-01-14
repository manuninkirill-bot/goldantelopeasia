import os
from PIL import Image

BASE_PATH = "/home/poweramanita/goldantelopeasia/moto_nhatrang"
TARGET_SIZE_KB = 100

def compress_image(image_path):
    img = Image.open(image_path)
    # Если фото в RGBA (прозрачность), конвертируем в RGB для JPEG
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    
    quality = 95
    # Пытаемся сохранить с уменьшением качества, пока файл не станет < 100 КБ
    while quality > 5:
        img.save(image_path, "JPEG", quality=quality, optimize=True)
        if os.path.getsize(image_path) <= TARGET_SIZE_KB * 1024:
            break
        quality -= 5

def main():
    print("🚀 Начинаю сжатие фото в moto_nhatrang...")
    processed = 0
    
    for root, dirs, files in os.walk(BASE_PATH):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                file_path = os.path.join(root, file)
                try:
                    compress_image(file_path)
                    print(f"✅ Сжато: {file_path} ({os.path.getsize(file_path)//1024} КБ)")
                    processed += 1
                except Exception as e:
                    print(f"❌ Ошибка с файлом {file_path}: {e}")

    print(f"\n✨ Готово! Обработано изображений: {processed}")

if __name__ == "__main__":
    main()
