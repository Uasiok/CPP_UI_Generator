#!/usr/bin/env python3
import os
import sys

def check_and_create_files():
    """Проверка и создание необходимых файлов"""
    
    project_dir = os.path.dirname(os.path.abspath(__file__))
    frontend_dir = os.path.join(project_dir, 'frontend')
    
    # Создаем директорию frontend если её нет
    if not os.path.exists(frontend_dir):
        print(f"Creating frontend directory: {frontend_dir}")
        os.makedirs(frontend_dir)
    
    # Проверяем файлы
    files = ['index.html', 'style.css', 'script.js']
    missing_files = []
    
    for file in files:
        file_path = os.path.join(frontend_dir, file)
        if not os.path.exists(file_path):
            missing_files.append(file)
            print(f"❌ Missing: {file_path}")
        else:
            print(f"✅ Found: {file_path}")
    
    if missing_files:
        print(f"\n⚠️  Missing files: {', '.join(missing_files)}")
        print("Please copy the files to the frontend directory")
        return False
    
    print("\n✅ All files are in place!")
    return True

if __name__ == '__main__':
    check_and_create_files()
