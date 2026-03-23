from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import json
import os
import sys

# Добавляем путь к текущей директории для импорта модулей
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from code_generator import CppCodeGenerator
from ui_parser import UIParser

# Создаем директории если их нет
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), 'frontend')
GENERATED_DIR = os.path.join(os.path.dirname(BASE_DIR), 'generated')

os.makedirs(FRONTEND_DIR, exist_ok=True)
os.makedirs(GENERATED_DIR, exist_ok=True)

app = Flask(__name__, 
            static_folder=FRONTEND_DIR,
            template_folder=FRONTEND_DIR)
CORS(app)  # Разрешаем CORS для всех источников

# Хранилище для текущего проекта
current_project = {
    'components': [],
    'name': 'MyApplication'
}

generator = CppCodeGenerator()
parser = UIParser()

@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')

@app.route('/api/components', methods=['GET'])
def get_components():
    """Получить все компоненты текущего проекта"""
    return jsonify(current_project['components'])

@app.route('/api/components', methods=['POST'])
def add_component():
    """Добавить новый компонент"""
    try:
        data = request.json
        # Если приходит массив компонентов, обновляем весь список
        if isinstance(data, list):
            current_project['components'] = data
            return jsonify({'success': True, 'count': len(data)})
        # Иначе добавляем один компонент
        elif isinstance(data, dict):
            if 'id' not in data:
                data['id'] = len(current_project['components']) + 1
            current_project['components'].append(data)
            return jsonify(data), 201
        else:
            return jsonify({'error': 'Invalid data format'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/components/<int:component_id>', methods=['PUT'])
def update_component(component_id):
    """Обновить компонент"""
    try:
        data = request.json
        for i, comp in enumerate(current_project['components']):
            if comp.get('id') == component_id:
                current_project['components'][i] = {**comp, **data}
                return jsonify(current_project['components'][i])
        return jsonify({'error': 'Component not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/components/<int:component_id>', methods=['DELETE'])
def delete_component(component_id):
    """Удалить компонент"""
    try:
        current_project['components'] = [c for c in current_project['components'] if c.get('id') != component_id]
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate', methods=['POST'])
def generate_code():
    """Сгенерировать C++ код"""
    try:
        data = request.json or {}
        project_name = data.get('name', 'MyApplication')
        components = data.get('components', current_project['components'])
        
        cpp_code = generator.generate_code(project_name, components)
        
        # Сохраняем сгенерированный код
        output_path = os.path.join(GENERATED_DIR, 'output.cpp')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(cpp_code)
        
        return jsonify({
            'code': cpp_code,
            'file_path': output_path,
            'success': True
        })
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/export', methods=['GET'])
def export_code():
    """Экспортировать сгенерированный код"""
    try:
        output_path = os.path.join(GENERATED_DIR, 'output.cpp')
        if os.path.exists(output_path):
            return send_file(output_path, as_attachment=True, download_name='ui_design.cpp')
        else:
            return jsonify({'error': 'No generated code found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/load', methods=['POST'])
def load_project():
    """Загрузить проект из JSON"""
    try:
        data = request.json
        if 'components' in data:
            current_project['components'] = data.get('components', [])
        if 'name' in data:
            current_project['name'] = data.get('name', 'MyApplication')
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/save', methods=['GET'])
def save_project():
    """Сохранить проект в JSON"""
    return jsonify(current_project)

@app.route('/api/preview', methods=['POST'])
def preview():
    """Создать превью UI"""
    try:
        data = request.json or {}
        components = data.get('components', current_project['components'])
        html_preview = parser.generate_preview(components)
        return jsonify({'html': html_preview, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/clear', methods=['POST'])
def clear_project():
    """Очистить проект"""
    current_project['components'] = []
    return jsonify({'success': True})

@app.route('/health', methods=['GET'])
def health_check():
    """Проверка работоспособности"""
    return jsonify({
        'status': 'ok',
        'components_count': len(current_project['components']),
        'server': 'running'
    })

if __name__ == '__main__':
    # Получаем IP адрес сервера для вывода в консоль
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print("\n" + "="*50)
    print("C++ UI Designer Server")
    print("="*50)
    print(f"Server is running on:")
    print(f"  - Local:   http://localhost:888")
    print(f"  - Network: http://{local_ip}:888")
    print("="*50)
    print("To access from another computer, use the Network URL")
    print("Make sure firewall allows port 888")
    print("Press Ctrl+C to stop the server\n")
    
    # Запускаем сервер на всех интерфейсах (0.0.0.0) на порту 888
    app.run(host='0.0.0.0', port=888, debug=True, threaded=True)
