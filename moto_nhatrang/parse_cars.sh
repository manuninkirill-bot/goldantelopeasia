#!/bin/bash
BASE_PATH="/home/poweramanita/goldantelopeasia/moto_nhatrang"
TARGET_URL="https://getmecar.ru/locations/vetnam/"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

echo "📡 Начинаю глубокий парсинг машин с getmecar.ru..."

# 1. Скачиваем страницу во временный файл
curl -s -L -A "$UA" "$TARGET_URL" > page.html

# 2. Извлекаем блоки машин (Название и Фото)
# Мы ищем src картинок и текст заголовков внутри карточек
grep -oP '(?<=<img class="card-img-top lazy" data-src=").*?(?=")|(?<=class="card-title">).*?(?=</a>)' page.html > raw_data.txt

# 3. Обрабатываем данные парами (Фото и следующее за ним Название)
while read -r line; do
    if [[ $line == http* ]]; then
        img_url="$line"
    else
        # Это название машины
        title=$(echo "$line" | sed 's/<[^>]*>//g' | xargs)
        folder_name=$(echo "$title" | tr ' ' '_' | tr -d '[:punct:]' | tr '[:upper:]' '[:lower:]')
        
        if [ -z "$folder_name" ]; then continue; fi

        echo "🚗 Обработка: $title"
        mkdir -p "$BASE_PATH/$folder_name"
        
        # Качаем фото
        curl -s -L -A "$UA" "$img_url" -o "$BASE_PATH/$folder_name/photo.jpg"
        
        # Создаем пустой файл описания
        touch "$BASE_PATH/$folder_name/description.txt"
        
        # Сжимаем фото до 50КБ, если файл скачался
        if [ -f "$BASE_PATH/$folder_name/photo.jpg" ]; then
            mogrify -resize 800x800 -define jpeg:extent=50kb "$BASE_PATH/$folder_name/photo.jpg"
            echo "   ✅ Фото скачано и сжато"
        fi
    fi
done < raw_data.txt

rm page.html raw_data.txt
echo "🏁 Все готово! Проверь содержимое папки moto_nhatrang"
