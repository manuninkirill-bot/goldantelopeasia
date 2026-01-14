import os
import hashlib

BASE_PATH = "/home/poweramanita/goldantelopeasia/moto_nhatrang"

def main():
    text_hashes = {}
    duplicates = []

    print("🔍 Проверка описаний на дубликаты...")

    for root, dirs, files in os.walk(BASE_PATH):
        if "description.txt" in files:
            path = os.path.join(root, "description.txt")
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    continue
                
                # Создаем хеш текста для сравнения
                content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
                
                folder_name = os.path.basename(root)
                if content_hash in text_hashes:
                    duplicates.append((folder_name, text_hashes[content_hash]))
                else:
                    text_hashes[content_hash] = folder_name

    if duplicates:
        print(f"⚠️ Найдено {len(duplicates)} папок с идентичным описанием:")
        for dup, original in duplicates:
            print(f"Повтор: [{dup}] <==> Такой же как в: [{original}]")
    else:
        print("✅ Все описания уникальны!")

if __name__ == "__main__":
    main()
