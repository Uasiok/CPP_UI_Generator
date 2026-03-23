from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import json
import os
from code_generator import CppCodeGenerator
from ui_parser import UIParser

app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')
CORS(app)

# Создаем директорию для сгенерированных файлов
os.makedirs('../generated', exist_ok=True)

# Хранилище для текущего проекта
current_project = {
    'components': [],
    'name': 'MyApplication'
}

generator = CppCodeGenerator()
parser = UIParser()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/components', methods=['GET'])
def get_components():
    """Получить все компоненты текущего проекта"""
    return jsonify(current_project['components'])

@app.route('/api/components', methods=['POST'])
def add_component():
    """Добавить новый компонент"""
    component = request.json
    component['id'] = len(current_project['components']) + 1
    current_project['components'].append(component)
    return jsonify(component), 201

@app.route('/api/components/<int:component_id>', methods=['PUT'])
def update_component(component_id):
    """Обновить компонент"""
    data = request.json
    for i, comp in enumerate(current_project['components']):
        if comp['id'] == component_id:
            current_project['components'][i] = {**comp, **data}
            return jsonify(current_project['components'][i])
    return jsonify({'error': 'Component not found'}), 404

@app.route('/api/components/<int:component_id>', methods=['DELETE'])
def delete_component(component_id):
    """Удалить компонент"""
    current_project['components'] = [c for c in current_project['components'] if c['id'] != component_id]
    return jsonify({'success': True})

@app.route('/api/generate', methods=['POST'])
def generate_code():
    """Сгенерировать C++ код"""
    data = request.json
    project_name = data.get('name', 'MyApplication')
    components = data.get('components', current_project['components'])
    
    cpp_code = generator.generate_code(project_name, components)
    
    # Сохраняем сгенерированный код
    output_path = '../generated/output.cpp'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cpp_code)
    
    return jsonify({
        'code': cpp_code,
        'file_path': output_path
    })

@app.route('/api/export', methods=['GET'])
def export_code():
    """Экспортировать сгенерированный код"""
    return send_file('../generated/output.cpp', as_attachment=True, download_name='ui_design.cpp')

@app.route('/api/load', methods=['POST'])
def load_project():
    """Загрузить проект из JSON"""
    data = request.json
    current_project['components'] = data.get('components', [])
    current_project['name'] = data.get('name', 'MyApplication')
    return jsonify({'success': True})

@app.route('/api/save', methods=['GET'])
def save_project():
    """Сохранить проект в JSON"""
    return jsonify(current_project)

@app.route('/api/preview', methods=['POST'])
def preview():
    """Создать превью UI"""
    components = request.json.get('components', current_project['components'])
    html_preview = parser.generate_preview(components)
    return jsonify({'html': html_preview})

if __name__ == '__main__':
    app.run(debug=True, port=5000)