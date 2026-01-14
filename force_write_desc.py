import os

BASE_PATH = "/home/poweramanita/goldantelopeasia/moto_nhatrang"
WHATSAPP = "wa.me/84374961375"

def main():
    if not os.path.exists(BASE_PATH):
        print("Папка не найдена")
        return

    folders = [d for d in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, d))]
    print(f"Найдено папок: {len(folders)}")

    for folder in folders:
        # Упрощенное название для текста из имени папки
        display_name = folder.replace('_', ' ').split('_')[0] 
        path = os.path.join(BASE_PATH, folder, "description.txt")
        
        # Генерируем текст на лету на основе имени папки
        text = (
            f"🛵 {display_name}\n\n"
            f"💰 Стоимость: от 80к-150к/сут или 1.6-4 млн/мес (зависит от модели)\n"
            f"🛡 Депозит: $150-500 или паспорт\n\n"
            f"✅ Шлемы и дождевики включены.\n"
            f"📲 WhatsApp: {WHATSAPP}"
        )
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Записано: {folder}")

if __name__ == "__main__":
    main()
