class UIDesigner {
    constructor() {
        this.components = [];
        this.selectedComponent = null;
        this.nextId = 1;
        this.dragEnabled = false;
        this.dragStart = { x: 0, y: 0 };
        this.currentDragComponent = null;
        
        this.init();
        this.loadComponents();
    }
    
    init() {
        this.canvas = document.getElementById('canvas');
        this.codeOutput = document.getElementById('codeOutput');
        this.propertiesContent = document.getElementById('propertiesContent');
        
        if (!this.canvas) {
            console.error('Canvas element not found!');
            return;
        }
        
        this.setupEventListeners();
        this.setupDragAndDrop();
    }
    
    setupEventListeners() {
        // Save project
        const saveBtn = document.getElementById('saveProjectBtn');
        if (saveBtn) saveBtn.addEventListener('click', () => this.saveProject());
        
        // Load project
        const loadBtn = document.getElementById('loadProjectBtn');
        if (loadBtn) loadBtn.addEventListener('click', () => this.loadProject());
        
        // Generate code
        const generateBtn = document.getElementById('generateCodeBtn');
        if (generateBtn) generateBtn.addEventListener('click', () => this.generateCode());
        
        // Export code
        const exportBtn = document.getElementById('exportCodeBtn');
        if (exportBtn) exportBtn.addEventListener('click', () => this.exportCode());
        
        // Preview
        const previewBtn = document.getElementById('previewBtn');
        if (previewBtn) previewBtn.addEventListener('click', () => this.showPreview());
        
        // Copy code
        const copyBtn = document.getElementById('copyCodeBtn');
        if (copyBtn) copyBtn.addEventListener('click', () => this.copyCode());
        
        // Modal close
        const modal = document.getElementById('previewModal');
        if (modal) {
            const closeBtn = modal.querySelector('.close');
            if (closeBtn) closeBtn.onclick = () => modal.style.display = 'none';
            window.onclick = (event) => {
                if (event.target === modal) modal.style.display = 'none';
            };
        }
        
        // Canvas click to deselect
        if (this.canvas) {
            this.canvas.addEventListener('click', (e) => {
                if (e.target === this.canvas) {
                    this.selectComponent(null);
                }
            });
        }
    }
    
    setupDragAndDrop() {
        const componentItems = document.querySelectorAll('.component-item');
        
        componentItems.forEach(comp => {
            comp.setAttribute('draggable', 'true');
            
            comp.addEventListener('dragstart', (e) => {
                const type = comp.dataset.type;
                e.dataTransfer.setData('text/plain', type);
                e.dataTransfer.effectAllowed = 'copy';
                
                const dragImage = comp.cloneNode(true);
                dragImage.style.position = 'absolute';
                dragImage.style.top = '-1000px';
                document.body.appendChild(dragImage);
                e.dataTransfer.setDragImage(dragImage, 0, 0);
                setTimeout(() => document.body.removeChild(dragImage), 0);
            });
        });
        
        if (this.canvas) {
            this.canvas.addEventListener('dragover', (e) => {
                e.preventDefault();
                e.dataTransfer.dropEffect = 'copy';
                this.canvas.style.borderColor = '#007acc';
            });
            
            this.canvas.addEventListener('dragleave', (e) => {
                this.canvas.style.borderColor = '#3e3e3e';
            });
            
            this.canvas.addEventListener('drop', (e) => {
                e.preventDefault();
                this.canvas.style.borderColor = '#3e3e3e';
                
                const type = e.dataTransfer.getData('text/plain');
                if (!type) return;
                
                const rect = this.canvas.getBoundingClientRect();
                const scrollLeft = this.canvas.scrollLeft;
                const scrollTop = this.canvas.scrollTop;
                
                let x = e.clientX - rect.left + scrollLeft;
                let y = e.clientY - rect.top + scrollTop;
                
                x = Math.max(10, Math.min(x, rect.width - 100));
                y = Math.max(10, Math.min(y, rect.height - 50));
                
                this.addComponent(type, x, y);
            });
        }
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
            window: { 
                title: 'Window', 
                width: 400, 
                height: 300, 
                x: x, 
                y: y 
            },
            button: { 
                text: 'Button', 
                width: 100, 
                height: 35, 
                x: x, 
                y: y 
            },
            label: { 
                text: 'Label', 
                width: 100, 
                height: 25, 
                x: x, 
                y: y 
            },
            textbox: { 
                placeholder: 'Enter text', 
                width: 150, 
                height: 30, 
                x: x, 
                y: y 
            },
            checkbox: { 
                text: 'Checkbox', 
                checked: false, 
                width: 120, 
                height: 25, 
                x: x, 
                y: y 
            },
            radiobutton: { 
                text: 'Radio Button', 
                selected: false, 
                width: 120, 
                height: 25, 
                x: x, 
                y: y 
            },
            listbox: { 
                items: ['Item 1', 'Item 2', 'Item 3'], 
                width: 150, 
                height: 100, 
                x: x, 
                y: y 
            },
            panel: { 
                text: 'Panel', 
                width: 200, 
                height: 150, 
                x: x, 
                y: y 
            }
        };
        
        return defaults[type] || { 
            text: type, 
            width: 100, 
            height: 30, 
            x: x, 
            y: y 
        };
    }
    
    renderComponent(component) {
        const div = document.createElement('div');
        div.className = 'ui-component';
        div.id = `comp-${component.id}`;
        div.style.left = `${component.properties.x}px`;
        div.style.top = `${component.properties.y}px`;
        div.style.width = `${component.properties.width}px`;
        div.style.height = `${component.properties.height}px`;
        
        let displayText = '';
        if (component.type === 'button' || component.type === 'label' || component.type === 'checkbox' || component.type === 'radiobutton') {
            displayText = component.properties.text || component.type;
        } else if (component.type === 'window') {
            displayText = component.properties.title || 'Window';
        } else if (component.type === 'panel') {
            displayText = component.properties.text || 'Panel';
        } else {
            displayText = component.type;
        }
        
        const iconMap = {
            'window': '📂',
            'button': '🔘',
            'label': '📝',
            'textbox': '📧',
            'checkbox': '✅',
            'radiobutton': '🔘',
            'listbox': '📋',
            'panel': '▯'
        };
        
        div.innerHTML = `${iconMap[component.type] || ''} ${displayText}`;
        
        div.addEventListener('click', (e) => {
            e.stopPropagation();
            this.selectComponent(component);
        });
        
        div.addEventListener('mousedown', (e) => {
            if (e.target === div || div.contains(e.target)) {
                e.stopPropagation();
                this.startDrag(component, e);
            }
        });
        
        this.canvas.appendChild(div);
    }
    
    selectComponent(component) {
        this.selectedComponent = component;
        
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
            <div class="property-group">
                <label>ID:</label>
                <input type="text" value="${component.id}" disabled>
            </div>
        `;
        
        for (let [key, value] of Object.entries(props)) {
            if (key === 'x' || key === 'y') continue;
            
            if (typeof value === 'boolean') {
                html += `
                    <div class="property-group">
                        <label>${this.capitalize(key)}:</label>
                        <input type="checkbox" ${value ? 'checked' : ''} 
                               onchange="uiDesigner.updateProperty(${component.id}, '${key}', this.checked)">
                    </div>
                `;
            } else if (Array.isArray(value)) {
                html += `
                    <div class="property-group">
                        <label>${this.capitalize(key)} (one per line):</label>
                        <textarea rows="4" onchange="uiDesigner.updateProperty(${component.id}, '${key}', this.value.split('\\n').filter(v => v.trim()))">${value.join('\n')}</textarea>
                    </div>
                `;
            } else if (typeof value === 'number') {
                html += `
                    <div class="property-group">
                        <label>${this.capitalize(key)}:</label>
                        <input type="number" value="${value}" 
                               onchange="uiDesigner.updateProperty(${component.id}, '${key}', parseInt(this.value))">
                    </div>
                `;
            } else {
                html += `
                    <div class="property-group">
                        <label>${this.capitalize(key)}:</label>
                        <input type="text" value="${value.replace(/"/g, '&quot;')}" 
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
            <div class="property-group">
                <label>Width:</label>
                <input type="number" value="${props.width}" onchange="uiDesigner.updateProperty(${component.id}, 'width', parseInt(this.value))">
            </div>
            <div class="property-group">
                <label>Height:</label>
                <input type="number" value="${props.height}" onchange="uiDesigner.updateProperty(${component.id}, 'height', parseInt(this.value))">
            </div>
            <button class="btn-small" onclick="uiDesigner.deleteComponent(${component.id})" style="background: #dc3545; margin-top: 10px; width: 100%;">
                🗑️ Delete Component
            </button>
        `;
        
        this.propertiesContent.innerHTML = html;
    }
    
    capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }
    
    updateProperty(id, key, value) {
        const component = this.components.find(c => c.id === id);
        if (component) {
            component.properties[key] = value;
            
            const el = document.getElementById(`comp-${id}`);
            if (el) {
                el.style.left = `${component.properties.x}px`;
                el.style.top = `${component.properties.y}px`;
                el.style.width = `${component.properties.width}px`;
                el.style.height = `${component.properties.height}px`;
                
                let displayText = '';
                if (component.type === 'button' || component.type === 'label' || component.type === 'checkbox' || component.type === 'radiobutton') {
                    displayText = component.properties.text || component.type;
                } else if (component.type === 'window') {
                    displayText = component.properties.title || 'Window';
                } else if (component.type === 'panel') {
                    displayText = component.properties.text || 'Panel';
                } else {
                    displayText = component.type;
                }
                
                const iconMap = {
                    'window': '📂',
                    'button': '🔘',
                    'label': '📝',
                    'textbox': '📧',
                    'checkbox': '✅',
                    'radiobutton': '🔘',
                    'listbox': '📋',
                    'panel': '▯'
                };
                el.innerHTML = `${iconMap[component.type] || ''} ${displayText}`;
            }
            
            this.saveToBackend();
            if (this.selectedComponent?.id === id) {
                this.showProperties(component);
            }
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
        if (confirm('Are you sure you want to delete this component?')) {
            this.components = this.components.filter(c => c.id !== id);
            const el = document.getElementById(`comp-${id}`);
            if (el) el.remove();
            
            if (this.selectedComponent?.id === id) {
                this.selectComponent(null);
            }
            this.saveToBackend();
        }
    }
    
    renderAllComponents() {
        if (!this.canvas) return;
        this.canvas.innerHTML = '';
        this.components.forEach(comp => this.renderComponent(comp));
    }
    
    startDrag(component, e) {
        this.dragEnabled = true;
        this.currentDragComponent = component;
        
        const startX = e.clientX;
        const startY = e.clientY;
        const startLeft = component.properties.x;
        const startTop = component.properties.y;
        
        const onMouseMove = (moveEvent) => {
            if (this.dragEnabled && this.currentDragComponent) {
                const deltaX = moveEvent.clientX - startX;
                const deltaY = moveEvent.clientY - startY;
                
                const newX = Math.max(0, startLeft + deltaX);
                const newY = Math.max(0, startTop + deltaY);
                
                component.properties.x = newX;
                component.properties.y = newY;
                
                this.updateComponentPosition(component.id, newX, newY);
                
                if (this.selectedComponent?.id === component.id) {
                    this.showProperties(component);
                }
            }
        };
        
        const onMouseUp = () => {
            this.dragEnabled = false;
            this.currentDragComponent = null;
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
                if (this.components.length > 0) {
                    this.nextId = Math.max(...this.components.map(c => c.id), 0) + 1;
                }
                this.renderAllComponents();
            }
        } catch (error) {
            console.error('Error loading components:', error);
        }
    }
    
    async saveProject() {
        const projectName = prompt('Enter project name:', 'MyApplication');
        
        if (projectName) {
            try {
                const response = await fetch('/api/save');
                const data = await response.json();
                const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${projectName}.ui.json`;
                a.click();
                URL.revokeObjectURL(url);
                
                alert(`Project "${projectName}" saved successfully!`);
            } catch (error) {
                console.error('Error saving project:', error);
                alert('Error saving project');
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
            if (this.components.length > 0) {
                this.nextId = Math.max(...this.components.map(c => c.id), 0) + 1;
            }
            this.renderAllComponents();
            this.saveToBackend();
            alert('Project loaded successfully!');
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
            if (data.success) {
                this.codeOutput.textContent = data.code;
                alert('Win32 GUI code generated successfully!');
            } else {
                this.codeOutput.textContent = 'Error generating code: ' + (data.error || 'Unknown error');
            }
        } catch (error) {
            console.error('Error generating code:', error);
            this.codeOutput.textContent = 'Error generating code. Make sure the backend is running.';
            alert('Error generating code');
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
            if (data.success) {
                const modal = document.getElementById('previewModal');
                const previewContent = document.getElementById('previewContent');
                previewContent.innerHTML = data.html;
                modal.style.display = 'block';
            } else {
                alert('Error generating preview: ' + (data.error || 'Unknown error'));
            }
        } catch (error) {
            console.error('Error showing preview:', error);
            alert('Error showing preview');
        }
    }
    
    copyCode() {
        const code = this.codeOutput.textContent;
        if (code && code !== 'No code generated yet' && code !== 'Error generating code. Make sure the backend is running.') {
            navigator.clipboard.writeText(code).then(() => {
                alert('Code copied to clipboard!');
            });
        } else {
            alert('No code to copy. Generate code first.');
        }
    }
}

// Initialize the application
let uiDesigner;
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, initializing UI Designer...');
    uiDesigner = new UIDesigner();
    window.uiDesigner = uiDesigner;
});
