import os
import hashlib

BASE_PATH = "/home/poweramanita/goldantelopeasia/moto_nhatrang"

def get_image_hash(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def main():
    hashes = {}
    duplicates = []
    
    print("🔍 Сканирование на наличие дубликатов фото...")
    
    for root, dirs, files in os.walk(BASE_PATH):
        for file in files:
            if file.lower().startswith('photo') and file.lower().endswith(('.jpg', '.jpeg', '.png')):
                path = os.path.join(root, file)
                f_hash = get_image_hash(path)
                
                if f_hash in hashes:
                    duplicates.append((path, hashes[f_hash]))
                else:
                    hashes[f_hash] = path

    if duplicates:
        print(f"⚠️ Найдено {len(duplicates)} дубликатов фото:")
        for dup, original in duplicates:
            print(f"Копия: {os.path.basename(os.path.dirname(dup))}  <==>  Оригинал: {os.path.basename(os.path.dirname(original))}")
    else:
        print("✅ Идентичных фото не найдено.")

if __name__ == "__main__":
    main()
