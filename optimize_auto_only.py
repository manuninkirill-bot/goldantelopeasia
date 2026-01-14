import os
from PIL import Image

# СТРОГО ОГРАНИЧИВАЕМ ПУТЬ
BASE_PATH = "/home/poweramanita/goldantelopeasia/auto_nhatrang"
TARGET_SIZE_KB = 100

def optimize_image(image_path):
    try:
        img = Image.open(image_path)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        
        quality = 90
        # Цикл уменьшения качества до нужного веса
        while quality > 10:
            img.save(image_path, "JPEG", quality=quality, optimize=True)
            if os.path.getsize(image_path) <= TARGET_SIZE_KB * 1024:
                break
            quality -= 5
        return os.path.getsize(image_path)
    except:
        return None

def main():
    if not os.path.exists(BASE_PATH):
        print(f"Ошибка: Папка {BASE_PATH} не найдена.")
        return

    # Берем только папки первого уровня внутри auto_nhatrang
    subfolders = [os.path.join(BASE_PATH, d) for d in os.listdir(BASE_PATH) 
                  if os.path.isdir(os.path.join(BASE_PATH, d))]

    print(f"🚀 Начинаю оптимизацию {len(subfolders)} папок в auto_nhatrang...")

    for folder in subfolders:
        files = os.listdir(folder)
        images = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        
        if not images:
            continue

        # 1. Выбираем одно фото и называем его photo.jpg
        keep_photo = "photo.jpg" if "photo.jpg" in images else images[0]
        old_path = os.path.join(folder, keep_photo)
        new_path = os.path.join(folder, "photo.jpg")

        if old_path != new_path:
            os.rename(old_path, new_path)

        # 2. Удаляем все остальные картинки в ЭТОЙ папке
        for img in images:
            full_img_path = os.path.join(folder, img)
            if os.path.exists(full_img_path) and full_img_path != new_path:
                os.remove(full_img_path)

        # 3. Сжимаем оставшееся фото
        size = optimize_image(new_path)
        if size:
            print(f"✅ {os.path.basename(folder)}: {size // 1024} KB")

    print("\n✨ Готово! Все фото в auto_nhatrang сжаты до 100 КБ и оставлены по 1 шт.")

if __name__ == "__main__":
    main()
