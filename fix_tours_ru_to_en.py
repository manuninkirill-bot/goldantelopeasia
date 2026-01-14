import os
import shutil

BASE_PATH = "/home/poweramanita/goldantelopeasia/tours_nhatrang"
WHATSAPP = "https://wa.me/84374961375"

# Словарь для перевода названий из файлов в названия папок
translate = {
    "далат": "Dalat_Tour",
    "северные_острова": "North_Islands_Tour",
    "золотой_мост": "Golden_Bridge_Ba_Na_Hills",
    "фанранг": "Phan_Rang_Tour",
    "обзорная_нячанг": "Nha_Trang_City_Tour",
    "фуйне": "Mui_Ne_White_Dunes",
    "морские_звезды": "Starfish_Beach_Phu_Quoc",
    "халонг": "Ha_Long_Bay_Tour",
    "янгбей": "Yang_Bay_Waterfall_Park",
    "круиз": "Evening_Cruise_Nha_Trang",
    "бахо": "Ba_Ho_Waterfall_Hiking",
    "гастротур": "Nha_Trang_Food_Tour",
    "4_острова": "Four_Islands_Tour",
    "квадроциклы": "ATV_Quad_Bike_Adventure",
    "дайвинг": "Diving_and_Snorkeling",
    "южные_острова": "South_Islands_Tour",
    "сайгон": "Ho_Chi_Minh_City_Saigon",
    "дикий_фукуок": "Wild_Phu_Quoc_Island",
    "муйне": "Mui_Ne_Tour",
    "рач_вем": "Rach_Vem_Beach_Phu_Quoc",
    "сапа": "Sapa_Hiking_Tour"
}

def main():
    # 1. Получаем все фото в корне tours_nhatrang
    files = [f for f in os.listdir(BASE_PATH) if os.path.isfile(os.path.join(BASE_PATH, f)) and f.lower().endswith(('.jpg', '.jpeg'))]
    
    processed_files = 0

    for photo in files:
        photo_lower = photo.lower()
        target_folder_en = None
        
        # Определяем, к какой группе относится фото
        for ru_key, en_name in translate.items():
            if ru_key in photo_lower:
                target_folder_en = en_name
                break
        
        if not target_folder_en:
            target_folder_en = "Other_Tours"

        folder_path = os.path.join(BASE_PATH, target_folder_en)
        os.makedirs(folder_path, exist_ok=True)

        # Считаем фото в папке, чтобы дать имя photo_1, photo_2...
        existing_photos = [f for f in os.listdir(folder_path) if f.startswith('photo_')]
        new_photo_num = len(existing_photos) + 1
        
        # Переносим
        ext = os.path.splitext(photo)[1]
        dst = os.path.join(folder_path, f"photo_{new_photo_num}{ext}")
        shutil.move(os.path.join(BASE_PATH, photo), dst)
        
        # Создаем описание, если его еще нет
        desc_path = os.path.join(folder_path, "description.txt")
        if not os.path.exists(desc_path):
            display_name = target_folder_en.replace('_', ' ')
            text = (
                f"🌟 {display_name} in Vietnam\n\n"
                f"Discover the breathtaking beauty of {display_name}. This tour offers a unique experience "
                f"with professional guides, comfortable transfers, and an unforgettable itinerary. "
                f"We ensure high-quality service and attention to every detail of your journey.\n\n"
                f"✅ Tour includes: Transfer, Entrance tickets, Lunch, and Guide.\n"
                f"📲 Booking WhatsApp: {WHATSAPP}"
            )
            with open(desc_path, "w", encoding="utf-8") as f:
                f.write(text)
        
        processed_files += 1

    print(f"🚀 Успех! Распределено {processed_files} фото по английским папкам.")

if __name__ == "__main__":
    main()
