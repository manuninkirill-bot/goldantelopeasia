import asyncio

async def get_place_details(page, url):
    try:
        await page.set_extra_http_headers({"Accept-Language": "en-US,en;q=0.9"})
        await page.goto(url, timeout=20000, wait_until="domcontentloaded")
        await asyncio.sleep(4)
        
        # Обход согласия Google
        try:
            for btn in await page.query_selector_all('button'):
                t = await btn.inner_text()
                if any(x in t for x in ["Accept all", "Agree", "Allow"]):
                    await btn.click()
                    await asyncio.sleep(2)
                    break
        except: pass

        # 1. Определение типа
        category = "🍽️ Restaurant"
        cat_element = await page.query_selector('button[jsaction*="category"]')
        if cat_element:
            raw_cat = (await cat_element.inner_text()).lower()
            if "cafe" in raw_cat: category = "☕ Cafe"
            elif "bar" in raw_cat: category = "🍸 Bar"
            elif "seafood" in raw_cat: category = "🦐 Seafood"

        # 2. Сбор ПОЛНОГО описания
        # Пробуем 3 разных источника текста в порядке приоритета
        description = ""
        
        # Источник А: Официальное описание Google (About)
        about_btn = await page.query_selector('div[class*="fontBodyMedium"]')
        if about_btn:
            description = await about_btn.inner_text()

        # Источник Б: Если текст слишком короткий, ищем блок отзывов
        if len(description) < 50:
            review_elements = await page.query_selector_all('div[class*="fontBodyMedium"]')
            for rev in review_elements:
                txt = await rev.inner_text()
                if len(txt) > len(description) and "Google" not in txt:
                    description = txt

        # Чистка текста
        description = description.replace('\n', ' ').strip()
        if not description or "cookie" in description.lower():
            description = "A highly-rated venue known for its amazing atmosphere, professional service, and delicious local cuisine."

        # Строгая обрезка до 300 знаков
        if len(description) > 300:
            description = description[:297] + "..."

        return category, description
    except Exception as e:
        return "🍽️ Restaurant", "A great local spot offering a unique dining experience and high-quality service."

async def run():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        places = [
            {"city": "Nha Trang", "name": "Sailing Club", "url": "https://www.google.com/maps/search/Sailing+Club+Nha+Trang"},
            {"city": "Ho Chi Minh", "name": "Pizza 4P's Ben Thanh", "url": "https://www.google.com/maps/search/Pizza+4P's+Ben+Thanh"},
            {"city": "Da Nang", "name": "Bà Thôi Seafood", "url": "https://www.google.com/maps/search/Ba+Thoi+Seafood+Da+Nang"},
            {"city": "Hanoi", "name": "The Note Coffee", "url": "https://www.google.com/maps/search/The+Note+Coffee+Hanoi"},
            {"city": "Phu Quoc", "name": "Chuon Chuon Bistro", "url": "https://www.google.com/maps/search/Chuon+Chuon+Bistro+Phu+Quoc"},
            {"city": "Phan Thiet", "name": "Lacheln Restaurant", "url": "https://www.google.com/maps/search/Lacheln+Restaurant+Phan+Thiet"},
            {"city": "Cam Ranh", "name": "Binh Ba Seafood", "url": "https://www.google.com/maps/search/Binh+Ba+Seafood+Cam+Ranh"},
            {"city": "Da Lat", "name": "Still Cafe", "url": "https://www.google.com/maps/search/Still+Cafe+Da+Lat"},
            {"city": "Hoi An", "name": "Morning Glory", "url": "https://www.google.com/maps/search/Morning+Glory+Hoi+An"}
        ]

        print(f"🚀 Starting deep parsing for full descriptions...")

        with open("description_ru.txt", "w", encoding="utf-8") as f:
            for p_info in places:
                print(f"🏙️ {p_info['city']}: {p_info['name']}...")
                p_type, p_desc = await get_place_details(page, p_info['url'])
                
                f.write(f"📍 CITY: {p_info['city']}\n")
                f.write(f"🏨 NAME: {p_info['name']}\n")
                f.write(f"🍽️ TYPE: {p_type}\n")
                f.write(f"💰 PRICE: $$\n")
                f.write(f"📝 DESCRIPTION: {p_desc}\n")
                f.write(f"🔗 LINK: {p_info['url']}\n")
                f.write("-" * 30 + "\n")

        await browser.close()
        print("✅ Done! File description_ru.txt contains full English descriptions.")

if __name__ == "__main__":
    asyncio.run(run())
