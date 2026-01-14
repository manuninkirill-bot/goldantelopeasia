import os, requests, re, subprocess, time
from bs4 import BeautifulSoup

BASE_PATH = "/home/poweramanita/goldantelopeasia/auto_nhatrang"
SOURCE_URL = "https://getmecar.ru/locations/vetnam/"

def slugify(text):
    text = text.lower()
    text = re.sub(r'или аналог.*|в нячанге.*|вьетнам.*|аренда.*|автомат.*', '', text)
    return "".join(re.findall(r'[a-z0-9]', text))

def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print(f"🌐 Получаю список реальных ссылок...")
    try:
        res = requests.get(SOURCE_URL, headers=headers, timeout=30)
        soup = BeautifulSoup(res.text, 'html.parser')
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return

    items = soup.find_all('div', class_=re.compile(r'catalog-item|item'))
    folders = [d for d in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, d))]
    
    found_count = 0
    for item in items:
        title_tag = item.find(['div', 'a', 'h3'], class_=re.compile(r'title|name'))
        img_tag = item.find('img')
        
        if title_tag and img_tag:
            name = title_tag.get_text(strip=True)
            img_url = img_tag.get('data-src') or img_tag.get('src') or img_tag.get('data-original')
            if not img_url: continue
            if not img_url.startswith('http'): img_url = "https://getmecar.ru" + img_url
            
            c_slug = slugify(name)
            for folder in folders:
                f_slug = slugify(folder)
                photo_path = os.path.join(BASE_PATH, folder, "photo.jpg")
                
                if (f_slug in c_slug or c_slug in f_slug) and not os.path.exists(photo_path):
                    print(f"📡 Качаю через CURL для: {folder}")
                    # Используем curl с заголовками браузера
                    cmd = [
                        "curl", "-L", img_url,
                        "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                        "-H", "Referer: https://getmecar.ru/",
                        "-o", photo_path,
                        "--silent"
                    ]
                    subprocess.run(cmd)
                    
                    # Проверяем размер
                    if os.path.exists(photo_path) and os.path.getsize(photo_path) > 5000:
                        print(f"   ✅ OK ({os.path.getsize(photo_path) // 1024} KB)")
                        found_count += 1
                    else:
                        if os.path.exists(photo_path): os.remove(photo_path)
                        print(f"   ❌ Ошибка (блокировка или пустой файл)")
                    time.sleep(0.5)

    print(f"\n🏁 Завершено! Успешно скачано: {found_count} фото.")

if __name__ == "__main__":
    main()
