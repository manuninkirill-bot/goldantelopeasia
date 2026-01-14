import os, requests, re
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

BASE_PATH = "/home/poweramanita/goldantelopeasia/moto_nhatrang"
URL = "https://nhatrang-exchange.com/arenda_baykov_nyachang.html"
# Новый контакт WhatsApp
WHATSAPP = "https://wa.me/84374961375"

def optimize_save(img_data, path):
    try:
        img = Image.open(BytesIO(img_data))
        if img.mode in ("RGBA", "P"): img = img.convert("RGB")
        q = 85
        while q > 10:
            img.save(path, "JPEG", quality=q, optimize=True)
            if os.path.getsize(path) <= 100 * 1024: break
            q -= 5
        return True
    except: return False

def main():
    if not os.path.exists(BASE_PATH): os.makedirs(BASE_PATH)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    print(f"🌐 Загрузка страницы {URL}...")
    try:
        res = requests.get(URL, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
    except Exception as e:
        print(f"❌ Ошибка загрузки сайта: {e}")
        return

    # Поиск блоков карточек Tilda
    items = soup.find_all('div', class_=re.compile(r't-card__container|t754__col|t754__wrapper|t-tile'))
    
    if not items:
        print("❌ Блоки не найдены. Пробую поиск по всем колонкам...")
        items = soup.find_all('div', class_=re.compile(r't-col'))

    print(f"🔍 Найдено объектов: {len(items)}")

    count = 0
    for item in items:
        title_tag = item.find(['div', 'div'], class_=re.compile(r'title|name'))
        if not title_tag or len(title_tag.text.strip()) < 3:
            continue
            
        name = title_tag.text.strip().replace('Аренда ', '')
        # Очистка имени для папки
        clean_name = re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '_')
        folder_path = os.path.join(BASE_PATH, clean_name)
        
        if not os.path.exists(folder_path): os.makedirs(folder_path)
        
        # Парсим описание
        desc_tag = item.find('div', class_=re.compile(r'descr|text'))
        full_text = desc_tag.get_text(separator='\n').strip() if desc_tag else "Описание уточняйте."
        
        # Формируем итоговый текст
        description = f"🛵 {name}\n\n{full_text}\n\n✅ Для бронирования пишите в WhatsApp:\n{WHATSAPP}"
        
        with open(os.path.join(folder_path, "description.txt"), "w", encoding="utf-8") as f:
            f.write(description)

        # Парсим фото
        img_tag = item.find('img')
        if img_tag:
            img_url = img_tag.get('data-original') or img_tag.get('src')
            if img_url:
                if img_url.startswith('//'): img_url = 'https:' + img_url
                try:
                    img_res = requests.get(img_url, timeout=10)
                    if optimize_save(img_res.content, os.path.join(folder_path, "photo.jpg")):
                        print(f"✅ {name}: Описание и фото готовы")
                    else:
                        print(f"⚠️ {name}: Описание готово, фото не сжалось")
                except:
                    print(f"⚠️ {name}: Только описание (фото не скачалось)")
        
        count += 1

    print(f"\n✨ Готово! Обработано {count} моделей в папке moto_nhatrang")

if __name__ == "__main__":
    main()
