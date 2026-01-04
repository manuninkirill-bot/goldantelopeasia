from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import json
import os
import time
from pathlib import Path

app = Flask(__name__, static_folder='static', static_url_path='/static')

online_users = {}
ONLINE_TIMEOUT = 60
BASE_ONLINE = 287

# Данные хранятся в JSON файле по странам
DATA_FILE = "listings_data.json"

def create_empty_data():
    return {
        "restaurants": [],
        "tours": [],
        "transport": [],
        "real_estate": [],
        "money_exchange": [],
        "entertainment": [],
        "marketplace": [],
        "visas": [],
        "news": [],
        "medicine": [],
        "kids": [],
        "chat": []
    }

def load_data(country='vietnam'):
    country_file = f"listings_{country}.json"
    if os.path.exists(country_file):
        with open(country_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
            
            # Если данные в файле - список, распределяем по категориям
            result = create_empty_data()
            category_map = {
                'bikes': 'transport',
                'real_estate': 'real_estate',
                'exchange': 'money_exchange',
                'money_exchange': 'money_exchange',
                'food': 'restaurants'
            }
            for item in data:
                if not isinstance(item, dict): continue
                cat = item.get('category', 'chat')
                mapped_cat = category_map.get(cat, cat)
                if mapped_cat in result:
                    result[mapped_cat].append(item)
            return result
    
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            all_data = json.load(f)
            if country in all_data:
                return all_data[country]
    return create_empty_data()

def load_all_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        'vietnam': create_empty_data(),
        'thailand': create_empty_data(),
        'india': create_empty_data(),
        'indonesia': create_empty_data()
    }

def save_data(country='vietnam', data=None):
    if not data or not isinstance(data, dict):
        return
    
    # Сохраняем в файл страны
    country_file = f"listings_{country}.json"
    try:
        with open(country_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving country file {country_file}: {e}")
    
    # Синхронизируем с общим файлом listings_data.json
    try:
        all_data = {}
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                all_data = json.load(f)
        
        all_data[country] = data
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error syncing with listings_data.json: {e}")

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/ping')
def ping():
    user_id = request.args.get('uid', request.remote_addr)
    online_users[user_id] = time.time()
    now = time.time()
    active = sum(1 for t in online_users.values() if now - t < ONLINE_TIMEOUT)
    return jsonify({'online': active})

@app.route('/api/online')
def get_online():
    now = time.time()
    active = sum(1 for t in online_users.values() if now - t < ONLINE_TIMEOUT)
    return jsonify({'online': active})

@app.route('/api/groups-stats')
def groups_stats():
    """Статистика по группам: охват, онлайн, объявления"""
    country = request.args.get('country', 'thailand')
    data = load_data(country)
    
    # Подсчет объявлений по категориям
    listings_count = {}
    for cat, items in data.items():
        if cat != 'chat':
            listings_count[cat] = len(items)
    
    # Загружаем статистику групп для конкретной страны
    stats_file = f'groups_stats_{country}.json'
    groups = []
    updated = None
    
    # ЗАЩИТА: Не загружаем статистику если файл не существует или пуст для этой страны
    if os.path.exists(stats_file):
        with open(stats_file, 'r', encoding='utf-8') as f:
            stats_data = json.load(f)
            groups = stats_data.get('groups', [])
            updated = stats_data.get('updated')
            
            # Если для этой страны нет данных, НЕ показываем данные от других стран
            if not groups and country != 'thailand':
                # Возвращаем пустой результат вместо fallback на другую страну
                return jsonify({
                    'updated': datetime.now().isoformat(),
                    'categories': {},
                    'groups': [],
                    'total_participants': 0,
                    'total_online': 0,
                    'message': f'Статистика по {country} еще собирается...'
                })
    
    # Агрегируем по категориям
    category_stats = {}
    for g in groups:
        cat = g.get('category', 'Другое')
        if cat not in category_stats:
            category_stats[cat] = {'participants': 0, 'online': 0, 'groups': 0, 'listings': 0}
        category_stats[cat]['participants'] += g.get('participants', 0)
        category_stats[cat]['online'] += g.get('online', 0)
        category_stats[cat]['groups'] += 1
    
    # Добавляем количество объявлений
    cat_key_map = {
        'Недвижимость': 'real_estate',
        'Чат': 'chat',
        'Рестораны': 'restaurants',
        'Для детей': 'entertainment',
        'Барахолка': 'marketplace',
        'Новости': 'news',
        'Визаран': 'visas',
        'Экскурсии': 'tours',
        'Обмен денег': 'money_exchange',
        'Транспорт': 'transport',
        'Медицина': 'medicine'
    }
    
    for cat_name, cat_key in cat_key_map.items():
        if cat_name in category_stats:
            category_stats[cat_name]['listings'] = listings_count.get(cat_key, 0)
    
    return jsonify({
        'updated': updated,
        'categories': category_stats,
        'groups': groups,
        'total_participants': sum(g.get('participants', 0) for g in groups),
        'total_online': sum(g.get('online', 0) for g in groups)
    })

@app.route('/api/status')
def status():
    country = request.args.get('country', 'vietnam')
    data = load_data(country)
    total_items = sum(len(v) for v in data.values())
    total_listings = sum(len(v) for k, v in data.items() if k != 'chat')
    
    # Количество людей на портале по странам
    online_counts = {
        'vietnam': 342,
        'thailand': 287,
        'india': 156,
        'indonesia': 419
    }
    
    return jsonify({
        'parser_status': 'connected',
        'total_items': total_items,
        'total_listings': total_listings,
        'categories': {k: len(v) for k, v in data.items()},
        'last_update': datetime.now().isoformat(),
        'channels_active': 0,
        'country': country,
        'online_count': online_counts.get(country, 100)
    })

@app.route('/api/listings/<category>')
def get_listings(category):
    country = request.args.get('country', 'vietnam')
    data = load_data(country)
    
    category_aliases = {
        'exchange': 'money_exchange',
        'money_exchange': 'money_exchange',
        'bikes': 'transport',
        'realestate': 'real_estate',
        'admin': 'restaurants',
        'settings': 'restaurants',
        'stats': 'restaurants'
    }
    category = category_aliases.get(category, category)
    
    if category not in data:
        return jsonify([])
    
    listings = data[category]
    
    # Фильтры
    filters = request.args
    filtered = listings
    
    if category == 'transport':
        # Фильтр по типу (sale, rent)
        if 'type' in filters and filters['type']:
            type_filter = filters['type'].lower()
            if type_filter == 'sale':
                keywords = ['продаж', 'куплю', 'продам', 'цена', '$', '₫', 'доллар']
                filtered = [x for x in filtered if any(kw in x.get('description', '').lower() for kw in keywords)]
            elif type_filter == 'rent':
                keywords = ['аренд', 'сдам', 'сдаю', 'наём', 'прокат', 'почасово']
                filtered = [x for x in filtered if any(kw in x.get('description', '').lower() for kw in keywords)]
        
        if 'model' in filters and filters['model']:
            filtered = [x for x in filtered if filters['model'].lower() in (x.get('model') or '').lower()]
        if 'year' in filters and filters['year']:
            filtered = [x for x in filtered if str(x.get('year', '')) == filters['year']]
        if 'price_min' in filters and 'price_max' in filters and filters['price_min'] and filters['price_max']:
            try:
                min_p, max_p = float(filters['price_min']), float(filters['price_max'])
                filtered = [x for x in filtered if min_p <= x.get('price', 0) <= max_p]
            except:
                pass
    
    elif category == 'real_estate':
        if 'rooms' in filters and filters['rooms']:
            filtered = [x for x in filtered if str(x.get('rooms', '')) == filters['rooms']]
        if 'location' in filters and filters['location']:
            filtered = [x for x in filtered if filters['location'].lower() in (x.get('location') or '').lower()]
        if 'price_min' in filters and 'price_max' in filters and filters['price_min'] and filters['price_max']:
            try:
                min_p, max_p = float(filters['price_min']), float(filters['price_max'])
                filtered = [x for x in filtered if min_p <= x.get('price', 0) <= max_p]
            except:
                pass
    
    # Сортировка по дате - новые сверху
    filtered.sort(key=lambda x: x.get('date', x.get('added_at', '1970-01-01')), reverse=True)
    
    return jsonify(filtered[:100])

@app.route('/api/add-listing', methods=['POST'])
def add_listing():
    country = request.json.get('country', 'vietnam')
    data = load_data(country)
    listing = request.json
    
    category = listing.get('category')
    if category and category in data:
        listing['added_at'] = datetime.now().isoformat()
        data[category].append(listing)
        save_data(country, data)
        return jsonify({'success': True, 'message': 'Объявление добавлено'})
    
    return jsonify({'error': 'Invalid category'}), 400

import shutil
from werkzeug.utils import secure_filename

BANNER_CONFIG_FILE = "banner_config.json"
UPLOAD_FOLDER = 'static/images/banners'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def load_banner_config():
    if os.path.exists(BANNER_CONFIG_FILE):
        with open(BANNER_CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        'vietnam': ['/static/images/banners/vietnam1.jpg', '/static/images/banners/vietnam2.jpg', '/static/images/banners/vietnam3.jpg', '/static/images/banners/vietnam4.jpg'],
        'thailand': ['/static/images/banner_thailand.jpg'],
        'india': ['/static/images/banner_india.jpg'],
        'indonesia': ['/static/images/banner_indonesia.jpg']
    }

def save_banner_config(config):
    with open(BANNER_CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

@app.route('/api/banners')
def get_banners():
    return jsonify(load_banner_config())

@app.route('/api/admin/upload-banner', methods=['POST'])
def admin_upload_banner():
    password = request.form.get('password', '')
    admin_key = os.environ.get('ADMIN_KEY', 'goldantelope2025')
    if password != admin_key:
        return jsonify({'error': 'Unauthorized'}), 401
    
    country = request.form.get('country', 'vietnam')
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filename = secure_filename(f"{country}_{int(time.time())}_{file.filename}")
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        url = f'/static/images/banners/{filename}'
        config = load_banner_config()
        if country not in config:
            config[country] = []
        config[country].append(url)
        save_banner_config(config)
        
        return jsonify({'success': True, 'url': url})

@app.route('/api/admin/delete-banner', methods=['POST'])
def admin_delete_banner():
    password = request.json.get('password', '')
    admin_key = os.environ.get('ADMIN_KEY', 'goldantelope2025')
    if password != admin_key:
        return jsonify({'error': 'Unauthorized'}), 401
    
    country = request.json.get('country')
    url = request.json.get('url')
    
    config = load_banner_config()
    if country in config and url in config[country]:
        config[country].remove(url)
        save_banner_config(config)
        # Мы не удаляем файл физически для безопасности, просто убираем из конфига
        return jsonify({'success': True})
    return jsonify({'error': 'Banner not found'}), 404

@app.route('/api/admin/reorder-banners', methods=['POST'])
def admin_reorder_banners():
    password = request.json.get('password', '')
    admin_key = os.environ.get('ADMIN_KEY', 'goldantelope2025')
    if password != admin_key:
        return jsonify({'error': 'Unauthorized'}), 401
    
    country = request.json.get('country')
    urls = request.json.get('urls')
    
    config = load_banner_config()
    if country in config:
        config[country] = urls
        save_banner_config(config)
        return jsonify({'success': True})
    return jsonify({'error': 'Country not found'}), 404

@app.route('/api/admin/auth', methods=['POST'])
def admin_auth():
    password = request.json.get('password', '')
    admin_key = os.environ.get('ADMIN_KEY', 'goldantelope2025')
    
    if password == admin_key:
        return jsonify({'success': True, 'authenticated': True})
    return jsonify({'success': False, 'error': 'Invalid password'}), 401

@app.route('/api/admin/delete-listing', methods=['POST'])
def admin_delete():
    password = request.json.get('password', '')
    admin_key = os.environ.get('ADMIN_KEY', 'goldantelope2025')
    
    if password != admin_key:
        return jsonify({'error': 'Unauthorized'}), 401
    
    country = request.json.get('country', 'vietnam')
    category = request.json.get('category')
    listing_id = request.json.get('listing_id')
    
    data = load_data(country)
    
    if category in data:
        data[category] = [x for x in data[category] if x.get('id') != listing_id]
        save_data(country, data)
        return jsonify({'success': True, 'message': f'Объявление {listing_id} удалено'})
    
    return jsonify({'error': 'Category not found'}), 404

@app.route('/api/admin/move-listing', methods=['POST'])
def admin_move():
    password = request.json.get('password', '')
    admin_key = os.environ.get('ADMIN_KEY', 'goldantelope2025')
    
    if password != admin_key:
        return jsonify({'error': 'Unauthorized'}), 401
    
    country = request.json.get('country', 'vietnam')
    from_category = request.json.get('from_category')
    to_category = request.json.get('to_category')
    listing_id = request.json.get('listing_id')
    
    data = load_data(country)
    
    if from_category not in data or to_category not in data:
        return jsonify({'error': 'Invalid category'}), 404
    
    # Найти объявление
    listing = None
    if from_category in data:
        for i, item in enumerate(data[from_category]):
            if item.get('id') == listing_id:
                listing = data[from_category].pop(i)
                break
    
    if not listing:
        return jsonify({'success': False, 'error': 'Listing not found'}), 404
    
    # Обновить категорию и переместить
    listing['category'] = to_category
    if to_category not in data:
        data[to_category] = []
    data[to_category].insert(0, listing)
    save_data(country, data)
    
    return jsonify({'success': True, 'message': f'Объявление перемещено в {to_category}'})

@app.route('/api/parser-config', methods=['GET', 'POST'])
def parser_config():
    country = request.args.get('country', 'vietnam')
    config_file = f'parser_config_{country}.json'
    
    if request.method == 'POST':
        config = request.json
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return jsonify({'success': True})
    
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    
    return jsonify({
        'channels': [],
        'keywords': [],
        'auto_parse_interval': 300
    })

@app.route('/api/parse-thailand', methods=['POST'])
def parse_thailand():
    try:
        from bot_parser import run_bot_parser
        result = run_bot_parser()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/thailand-channels')
def get_thailand_channels():
    channels_file = 'thailand_channels.json'
    if os.path.exists(channels_file):
        with open(channels_file, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    return jsonify({})

@app.route('/bot/webhook', methods=['POST'])
def bot_webhook():
    from telegram_bot import handle_start, handle_app, send_message
    
    data = request.json
    if not data:
        return jsonify({'ok': True})
    
    message = data.get('message', {})
    chat_id = message.get('chat', {}).get('id')
    text = message.get('text', '')
    user = message.get('from', {})
    user_name = user.get('first_name', 'друг')
    
    if not chat_id:
        return jsonify({'ok': True})
    
    if text == '/start':
        handle_start(chat_id, user_name)
    elif text == '/app':
        handle_app(chat_id)
    elif text == '/help':
        send_message(chat_id, '🦌 <b>Goldantelope ASIA</b>\n\n/start - Главное меню\n/app - Открыть приложение\n/thailand - Тайланд\n/vietnam - Вьетнам')
    elif text == '/thailand':
        send_message(chat_id, '🇹🇭 <b>Тайланд</b>\n\n70+ каналов:\n- Пхукет\n- Паттайя\n- Бангкок\n- Самуи\n\nНажмите /app чтобы открыть!')
    elif text == '/vietnam':
        send_message(chat_id, '🇻🇳 <b>Вьетнам</b>\n\nКаналы скоро будут добавлены!\n\nНажмите /app чтобы открыть!')
    elif text == '/auth':
        send_message(chat_id, '🔐 <b>Авторизация Telethon</b>\n\nКод был отправлен в приложение Telegram на номер +84342893121.\n\nНайдите сообщение от "Telegram" с 5-значным кодом и отправьте его сюда!')
    elif text and text.isdigit() and len(text) == 5:
        with open('pending_code.txt', 'w') as f:
            f.write(text)
        send_message(chat_id, f'✅ Код {text} получен! Пробую авторизацию...')
    
    return jsonify({'ok': True})

@app.route('/bot/setup', methods=['POST'])
def setup_bot_webhook():
    import requests
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    domains = os.environ.get('REPLIT_DOMAINS', '')
    
    if domains:
        webhook_url = f"https://{domains.split(',')[0]}/bot/webhook"
        url = f'https://api.telegram.org/bot{bot_token}/setWebhook'
        result = requests.post(url, data={'url': webhook_url}).json()
        return jsonify(result)
    
    return jsonify({'error': 'No domain found'})

# ============ УПРАВЛЕНИЕ КАНАЛАМИ ============

def load_channels(country):
    """Загрузить каналы для страны"""
    channels_file = f'{country}_channels.json'
    if os.path.exists(channels_file):
        with open(channels_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('channels', {})
    return {}

def save_channels(country, channels):
    """Сохранить каналы для страны"""
    channels_file = f'{country}_channels.json'
    with open(channels_file, 'w', encoding='utf-8') as f:
        json.dump({'channels': channels}, f, ensure_ascii=False, indent=2)

@app.route('/api/admin/channels', methods=['GET'])
def get_channels():
    """Получить список каналов по странам"""
    country = request.args.get('country', 'vietnam')
    channels = load_channels(country)
    return jsonify({'country': country, 'channels': channels})

@app.route('/api/admin/add-channel', methods=['POST'])
def add_channel():
    """Добавить канал"""
    password = request.json.get('password', '')
    admin_key = os.environ.get('ADMIN_KEY', 'goldantelope2025')
    
    if password != admin_key:
        return jsonify({'error': 'Unauthorized'}), 401
    
    country = request.json.get('country', 'vietnam')
    category = request.json.get('category', 'chat')
    channel = request.json.get('channel', '').strip().replace('@', '')
    
    if not channel:
        return jsonify({'error': 'Channel name required'}), 400
    
    channels = load_channels(country)
    
    if category not in channels:
        channels[category] = []
    
    if channel in channels[category]:
        return jsonify({'error': 'Channel already exists'}), 400
    
    channels[category].append(channel)
    save_channels(country, channels)
    
    return jsonify({'success': True, 'message': f'Канал @{channel} добавлен в {category}'})

@app.route('/api/admin/remove-channel', methods=['POST'])
def remove_channel():
    """Удалить канал"""
    password = request.json.get('password', '')
    admin_key = os.environ.get('ADMIN_KEY', 'goldantelope2025')
    
    if password != admin_key:
        return jsonify({'error': 'Unauthorized'}), 401
    
    country = request.json.get('country', 'vietnam')
    category = request.json.get('category')
    channel = request.json.get('channel')
    
    channels = load_channels(country)
    
    if category in channels and channel in channels[category]:
        channels[category].remove(channel)
        save_channels(country, channels)
        return jsonify({'success': True, 'message': f'Канал @{channel} удален'})
    
    return jsonify({'error': 'Channel not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
