#!/bin/bash
BASE_PATH="/home/poweramanita/goldantelopeasia/moto_nhatrang"
TARGET_URL="https://getmecar.ru/locations/vetnam/"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

echo "🔎 Шаг 1: Глубокий поиск всех 50+ ссылок..."
# Собираем абсолютно все ссылки на листинги
links=$(lynx -dump -listonly "$TARGET_URL" | grep "/listing/" | awk '{print $2}' | sort -u)

count=$(echo "$links" | wc -l)
echo "🚗 Найдено уникальных адресов: $count"

for url in $links; do
    # Название папки из хвоста ссылки
    name=$(echo $url | sed 's|/$||' | awk -F/ '{print $NF}' | cut -d'_' -f1)
    
    if [ -z "$name" ]; then continue; fi
    
    echo "📥 Загружаю: $name..."
    mkdir -p "$BASE_PATH/$name"
    
    # Скачиваем страницу целиком во временный файл
    tmp_file="$BASE_PATH/$name/page.html"
    curl -s -L -A "$UA" "$url" -o "$tmp_file"
    
    # 1. Извлекаем текст (удаляем теги, берем первые 50 строк контента)
    sed -e 's/<[^>]*>//g' "$tmp_file" | grep -v '^[[:space:]]*$' | head -n 60 > "$BASE_PATH/$name/description.txt"
    
    # 2. Извлекаем фото
    img_url=$(grep -oP '(?<=og:image" content=").*?(?=")' "$tmp_file" | head -1)
    if [ -n "$img_url" ]; then
        curl -s -L -A "$UA" "$img_url" -o "$BASE_PATH/$name/photo.jpg"
        # Сжимаем фото до 50кб
        mogrify -resize 800x800 -define jpeg:extent=50kb "$BASE_PATH/$name/photo.jpg" 2>/dev/null
        echo "   ✅ Текст и фото (50КБ) сохранены"
    else
        echo "   ⚠️ Только текст сохранен"
    fi
    
    rm "$tmp_file"
    sleep 1
done
echo "🏁 Миссия завершена!"
