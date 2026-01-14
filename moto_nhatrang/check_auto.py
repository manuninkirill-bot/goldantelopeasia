import os, re

BASE_PATH = "/home/poweramanita/goldantelopeasia/auto_nhatrang"
LIST_TEXT = """
Toyota Vios 2018-2020
Toyota Yaris 2016-2019
Honda City 2018-2020
Hyundai Kona автомат 2018-2021
Mazda2 2024-2025
Kia rondo 2019-2020
Mazda3 2018-2020
Kia Soluto 2020-2021
Honda City RS 2022-2023
Kia soluto автомат 2022-2024
Kia Cerato 2020-2021
Kia Seltos 2022-2023
Mitsubishi Expander 7 мест 2019-2020
Toyota Fortuner 2018-2021
Ford Everest 2018-2021
Mitsubishi Expander 2021-2023
Toyota Vios 2020-2022
Mitsubishi Expander 7 мест 2021-2023
Toyota Raize автомат 2022-2024
MG-5 2023-2024
Hyundai Venue автомат 2023-2025
MG-5 2023-2025
Hyundai Venue автомат 2023-2025
Hyundai Creta автомат 2022-2024
Honda City 2022-2024
Toyota Raize 2023-2024
Hyundai Accent 2022-2024
Mitsubishi X-Force White 2023-2025
Mitsubishi X-Force Gray 2023-2025
Toyota Veloz Cross 7 мест 2022-2023
Mitsubishi Expander 2022-2024
Hyundai Creta автомат 2022-2024
Kia Sorento 7 мест 2019-2020
Kia Seltos автомат 2022-2024
Kia Seltos автомат 2022-2024
Kia K3 2022-2023
Hyundai Creta 2022-2023
Honda HRV 2023-2025
VinFast LUX SA2.0 turbo 2020-2022
Kia Carnival 7 мест 2022-2023
Kia Sedona 7 мест 2019-2020
Peugeot 2008, 2022-2024
MG-5 2023-2024
Ford Territory 2.0 2022-2024
Mazda CX-5 2022-2024
Kia Carens 7 мест 2023-2025
KIA Carnival 7 мест 2024-2025
KIA Carnival 7 мест 2023-2024
KIA Carnival 2023-2024
VinFast VF9 7 мест 2024-2025
Mercedes E250 2018-2020
BMW Z4 2024-2025
"""

def clean_name(name):
    return name.strip().lower()

def main():
    expected_cars = [clean_name(line) for line in LIST_TEXT.strip().split('\n')]
    existing_folders = [f.lower() for f in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, f))]
    
    print(f"📊 Начинаю сверку (ожидаем ~{len(expected_cars)} авто)...")
    print("-" * 50)
    
    missing = []
    found_count = 0
    no_photo = []

    for car in expected_cars:
        # Ищем частичное совпадение (так как имена папок могут быть чуть короче)
        match = None
        for folder in existing_folders:
            if car in folder or folder in car:
                match = folder
                break
        
        if match:
            found_count += 1
            # Проверяем наличие фото
            full_path = os.path.join(BASE_PATH, match)
            if not any(f.endswith(('.jpg', '.png')) for f in os.listdir(full_path)):
                no_photo.append(match)
        else:
            missing.append(car)

    print(f"✅ Найдено папок: {found_count}")
    
    if missing:
        print(f"❌ Отсутствуют папки ({len(missing)}):")
        for m in missing: print(f"   - {m}")
    
    if no_photo:
        print(f"🖼 Нет фото в папках ({len(no_photo)}):")
        for p in no_photo: print(f"   - {p}")
        
    if not missing and not no_photo:
        print("🚀 Идеально! Все авто на месте и с фотографиями.")

if __name__ == "__main__":
    main()
