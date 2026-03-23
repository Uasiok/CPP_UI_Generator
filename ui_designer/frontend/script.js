class UIDesigner {
    constructor() {
        this.components = [];
        this.selectedComponent = null;
        this.nextId = 1;
        this.dragEnabled = false;
        this.dragStart = { x: 0, y: 0 };
        
        this.init();
        this.loadComponents();
    }
    
    init() {
        this.canvas = document.getElementById('canvas');
        this.codeOutput = document.getElementById('codeOutput');
        this.propertiesContent = document.getElementById('propertiesContent');
        
        this.setupEventListeners();
        this.setupDragAndDrop();
    }
    
    setupEventListeners() {
        // Save project
        document.getElementById('saveProjectBtn').addEventListener('click', () => this.saveProject());
        
        // Load project
        document.getElementById('loadProjectBtn').addEventListener('click', () => this.loadProject());
        
        // Generate code
        document.getElementById('generateCodeBtn').addEventListener('click', () => this.generateCode());
        
        // Export code
        document.getElementById('exportCodeBtn').addEventListener('click', () => this.exportCode());
        
        // Preview
        document.getElementById('previewBtn').addEventListener('click', () => this.showPreview());
        
        // Copy code
        document.getElementById('copyCodeBtn').addEventListener('click', () => this.copyCode());
        
        // Modal close
        const modal = document.getElementById('previewModal');
        const closeBtn = modal.querySelector('.close');
        closeBtn.onclick = () => modal.style.display = 'none';
        window.onclick = (event) => {
            if (event.target === modal) modal.style.display = 'none';
        };
        
        // Canvas click to deselect
        this.canvas.addEventListener('click', (e) => {
            if (e.target === this.canvas) {
                this.selectComponent(null);
            }
        });
    }
    
    setupDragAndDrop() {
        const components = document.querySelectorAll('.component-item');
        components.forEach(comp => {
            comp.addEventListener('dragstart', (e) => {
                e.dataTransfer.setData('type', comp.dataset.type);
                e.dataTransfer.effectAllowed = 'copy';
            });
        });
        
        this.canvas.addEventListener('dragover', (e) => {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'copy';
        });
        
        this.canvas.addEventListener('drop', (e) => {
            e.preventDefault();
            const rect = this.canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const type = e.dataTransfer.getData('type');
            
            this.addComponent(type, x, y);
        });
    }
    
    addComponent(type, x, y) {
        const component = {
            id: this.nextId++,
            type: type,
            properties: this.getDefaultProperties(type, x, y)
        };
        
        this.components.push(component);
        this.renderComponent(component);
        this.saveToBackend();
    }
    
    getDefaultProperties(type, x, y) {
        const defaults = {
            window: { title: 'Window', width: 400, height: 300, x: x, y: y },
            button: { text: 'Button', width: 100, height: 30, x: x, y: y },
            label: { text: 'Label', width: 80, height: 20, x: x, y: y },
            textbox: { placeholder: 'Enter text', width: 200, height: 30, x: x, y: y },
            checkbox: { text: 'Checkbox', checked: false, width: 100, height: 25, x: x, y: y },
            radiobutton: { text: 'Radio', selected: false, width: 100, height: 25, x: x, y: y },
            listbox: { items: ['Item 1', 'Item 2', 'Item 3'], width: 150, height: 100, x: x, y: y },
            panel: { width: 300, height: 200, x: x, y: y }
        };
        
        return defaults[type] || { text: type, width: 100, height: 30, x: x, y: y };
    }
    
    renderComponent(component) {
        const div = document.createElement('div');
        div.className = 'ui-component';
        div.id = `comp-${component.id}`;
        div.style.left = `${component.properties.x}px`;
        div.style.top = `${component.properties.y}px`;
        div.style.width = `${component.properties.width}px`;
        div.style.height = `${component.properties.height}px`;
        div.textContent = component.properties.text || component.properties.title || component.type;
        
        div.addEventListener('click', (e) => {
            e.stopPropagation();
            this.selectComponent(component);
        });
        
        div.addEventListener('mousedown', (e) => {
            if (e.target === div) {
                this.startDrag(component, e);
            }
        });
        
        this.canvas.appendChild(div);
    }
    
    selectComponent(component) {
        this.selectedComponent = component;
        
        // Remove selection highlight
        document.querySelectorAll('.ui-component').forEach(el => {
            el.classList.remove('selected');
        });
        
        if (component) {
            const el = document.getElementById(`comp-${component.id}`);
            if (el) el.classList.add('selected');
            this.showProperties(component);
        } else {
            this.propertiesContent.innerHTML = '<p class="info-text">Select a component to edit properties</p>';
        }
    }
    
    showProperties(component) {
        const props = component.properties;
        let html = `
            <div class="property-group">
                <label>Type:</label>
                <input type="text" value="${component.type}" disabled>
            </div>
        `;
        
        for (let [key, value] of Object.entries(props)) {
            if (key === 'x' || key === 'y') continue;
            
            if (typeof value === 'boolean') {
                html += `
                    <div class="property-group">
                        <label>${key}:</label>
                        <input type="checkbox" ${value ? 'checked' : ''} 
                               onchange="uiDesigner.updateProperty(${component.id}, '${key}', this.checked)">
                    </div>
                `;
            } else if (Array.isArray(value)) {
                html += `
                    <div class="property-group">
                        <label>${key}:</label>
                        <textarea rows="3" onchange="uiDesigner.updateProperty(${component.id}, '${key}', this.value.split('\\n'))">${value.join('\n')}</textarea>
                    </div>
                `;
            } else {
                html += `
                    <div class="property-group">
                        <label>${key}:</label>
                        <input type="${typeof value === 'number' ? 'number' : 'text'}" 
                               value="${value}" 
                               onchange="uiDesigner.updateProperty(${component.id}, '${key}', this.value)">
                    </div>
                `;
            }
        }
        
        html += `
            <div class="property-group">
                <label>X Position:</label>
                <input type="number" value="${props.x}" onchange="uiDesigner.updateProperty(${component.id}, 'x', parseInt(this.value))">
            </div>
            <div class="property-group">
                <label>Y Position:</label>
                <input type="number" value="${props.y}" onchange="uiDesigner.updateProperty(${component.id}, 'y', parseInt(this.value))">
            </div>
            <button class="btn-small" onclick="uiDesigner.deleteComponent(${component.id})" style="background: #dc3545; margin-top: 10px;">
                Delete Component
            </button>
        `;
        
        this.propertiesContent.innerHTML = html;
    }
    
    updateProperty(id, key, value) {
        const component = this.components.find(c => c.id === id);
        if (component) {
            if (key === 'items' && typeof value === 'string') {
                value = value.split('\n').filter(v => v.trim());
            }
            component.properties[key] = value;
            this.updateComponentPosition(id, component.properties.x, component.properties.y);
            this.saveToBackend();
            this.renderAllComponents();
            this.selectComponent(component);
        }
    }
    
    updateComponentPosition(id, x, y) {
        const el = document.getElementById(`comp-${id}`);
        if (el) {
            el.style.left = `${x}px`;
            el.style.top = `${y}px`;
        }
    }
    
    deleteComponent(id) {
        this.components = this.components.filter(c => c.id !== id);
        this.renderAllComponents();
        if (this.selectedComponent?.id === id) {
            this.selectComponent(null);
        }
        this.saveToBackend();
    }
    
    renderAllComponents() {
        this.canvas.innerHTML = '';
        this.components.forEach(comp => this.renderComponent(comp));
    }
    
    startDrag(component, e) {
        this.dragEnabled = true;
        this.dragStart = {
            x: e.clientX - component.properties.x,
            y: e.clientY - component.properties.y
        };
        
        const onMouseMove = (moveEvent) => {
            if (this.dragEnabled) {
                const newX = moveEvent.clientX - this.dragStart.x;
                const newY = moveEvent.clientY - this.dragStart.y;
                
                component.properties.x = Math.max(0, newX);
                component.properties.y = Math.max(0, newY);
                
                this.updateComponentPosition(component.id, component.properties.x, component.properties.y);
            }
        };
        
        const onMouseUp = () => {
            this.dragEnabled = false;
            document.removeEventListener('mousemove', onMouseMove);
            document.removeEventListener('mouseup', onMouseUp);
            this.saveToBackend();
        };
        
        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('mouseup', onMouseUp);
    }
    
    async saveToBackend() {
        try {
            await fetch('/api/components', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(this.components)
            });
        } catch (error) {
            console.error('Error saving to backend:', error);
        }
    }
    
    async loadComponents() {
        try {
            const response = await fetch('/api/components');
            if (response.ok) {
                this.components = await response.json();
                this.nextId = Math.max(...this.components.map(c => c.id), 0) + 1;
                this.renderAllComponents();
            }
        } catch (error) {
            console.error('Error loading components:', error);
        }
    }
    
    async saveProject() {
        const project = {
            name: prompt('Enter project name:', 'MyApplication'),
            components: this.components
        };
        
        if (project.name) {
            try {
                const response = await fetch('/api/save');
                const data = await response.json();
                const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${project.name}.ui.json`;
                a.click();
                URL.revokeObjectURL(url);
            } catch (error) {
                console.error('Error saving project:', error);
            }
        }
    }
    
    async loadProject() {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.json';
        input.onchange = async (e) => {
            const file = e.target.files[0];
            const text = await file.text();
            const project = JSON.parse(text);
            this.components = project.components || [];
            this.nextId = Math.max(...this.components.map(c => c.id), 0) + 1;
            this.renderAllComponents();
            this.saveToBackend();
        };
        input.click();
    }
    
    async generateCode() {
        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name: 'MyApplication',
                    components: this.components
                })
            });
            
            const data = await response.json();
            this.codeOutput.textContent = data.code;
        } catch (error) {
            console.error('Error generating code:', error);
            this.codeOutput.textContent = 'Error generating code. Make sure the backend is running.';
        }
    }
    
    async exportCode() {
        window.open('/api/export', '_blank');
    }
    
    async showPreview() {
        try {
            const response = await fetch('/api/preview', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ components: this.components })
            });
            
            const data = await response.json();
            const modal = document.getElementById('previewModal');
            const previewContent = document.getElementById('previewContent');
            previewContent.innerHTML = data.html;
            modal.style.display = 'block';
        } catch (error) {
            console.error('Error showing preview:', error);
        }
    }
    
    copyCode() {
        const code = this.codeOutput.textContent;
        navigator.clipboard.writeText(code).then(() => {
            alert('Code copied to clipboard!');
        });
    }
}

// Initialize the application
let uiDesigner;
document.addEventListener('DOMContentLoaded', () => {
    uiDesigner = new UIDesigner();
    window.uiDesigner = uiDesigner; // Make it accessible globally
});