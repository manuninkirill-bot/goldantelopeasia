import os

BASE_PATH = "/home/poweramanita/goldantelopeasia/moto_nhatrang"
WHATSAPP = "https://wa.me/84374961375"

def main():
    if not os.path.exists(BASE_PATH):
        print("Папка не найдена")
        return

    folders = [d for d in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, d))]
    updated_count = 0

    for folder in folders:
        desc_path = os.path.join(BASE_PATH, folder, "description.txt")
        
        # Проверяем: нужно ли обновлять (если файла нет или он почти пустой)
        needs_update = False
        if not os.path.exists(desc_path):
            needs_update = True
        else:
            with open(desc_path, "r", encoding="utf-8") as f:
                if len(f.read().strip()) < 50:
                    needs_update = True

        if needs_update:
            # Делаем красивое имя из названия папки
            display_name = folder.replace('_', ' ').replace('moto', '').strip().title()
            
            # Текст примерно на 300 знаков
            text = (
                f"🛵 {display_name} — отличный выбор для дорог Нячанга! "
                f"Байк находится в превосходном техническом состоянии и полностью готов к аренде. "
                f"В стоимость уже включены два чистых шлема, качественные дождевики и держатель для телефона. "
                f"Мы гарантируем регулярное сервисное обслуживание и поддержку 24/7.\n\n"
                f"📲 Для бронирования и уточнения цены пишите в WhatsApp: {WHATSAPP}"
            )
            
            with open(desc_path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"✅ Описание создано для: {folder}")
            updated_count += 1

    print(f"\n🚀 Итог: Обновлено {updated_count} описаний.")

if __name__ == "__main__":
    main()
