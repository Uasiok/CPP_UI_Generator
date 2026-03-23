class UIParser:
    """Парсер UI для генерации превью"""
    
    def generate_preview(self, components):
        """Генерация HTML превью"""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                .preview-container {
                    position: relative;
                    background: #f5f5f5;
                    min-height: 400px;
                    border: 2px solid #ccc;
                    border-radius: 8px;
                    overflow: auto;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }
                .ui-component {
                    position: absolute;
                    padding: 5px 10px;
                    background: white;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    cursor: pointer;
                    transition: all 0.2s;
                }
                .ui-component:hover {
                    border-color: #007bff;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }
                .button {
                    background: #007bff;
                    color: white;
                    border: none;
                    cursor: pointer;
                }
                .button:hover {
                    background: #0056b3;
                }
                .label {
                    background: transparent;
                    border: none;
                    font-weight: bold;
                }
                .textbox {
                    background: white;
                    border: 1px solid #ccc;
                }
                .window {
                    background: #e6e6e6;
                    border: 2px solid #333;
                    border-radius: 8px;
                    overflow: hidden;
                }
                .window-title {
                    background: #333;
                    color: white;
                    padding: 5px;
                    font-weight: bold;
                }
                .checkbox {
                    background: transparent;
                    border: none;
                }
                .radiobutton {
                    background: transparent;
                    border: none;
                }
                .listbox {
                    background: white;
                    border: 1px solid #ccc;
                    overflow-y: auto;
                }
                .panel {
                    background: #f0f0f0;
                    border: 1px solid #ccc;
                }
            </style>
        </head>
        <body>
            <div class="preview-container" style="position: relative; min-height: 500px;">
        """
        
        for component in components:
            comp_type = component.get('type', 'button')
            props = component.get('properties', {})
            x = props.get('x', 50)
            y = props.get('y', 50)
            width = props.get('width', 100)
            height = props.get('height', 30)
            text = props.get('text', '')
            placeholder = props.get('placeholder', '')
            items = props.get('items', [])
            
            if comp_type == 'button':
                html += f"""
                <div class="ui-component button" style="left: {x}px; top: {y}px;">
                    {text}
                </div>
                """
            
            elif comp_type == 'label':
                html += f"""
                <div class="ui-component label" style="left: {x}px; top: {y}px;">
                    {text}
                </div>
                """
            
            elif comp_type == 'textbox':
                html += f"""
                <input type="text" class="ui-component textbox" placeholder="{placeholder}" 
                       style="left: {x}px; top: {y}px; width: {width}px;">
                """
            
            elif comp_type == 'window':
                html += f"""
                <div class="ui-component window" style="left: {x}px; top: {y}px; width: {width}px; height: {height}px;">
                    <div class="window-title">{text}</div>
                </div>
                """
            
            elif comp_type == 'checkbox':
                checked = props.get('checked', False)
                html += f"""
                <div class="ui-component checkbox" style="left: {x}px; top: {y}px;">
                    <input type="checkbox" {'checked' if checked else ''}> {text}
                </div>
                """
            
            elif comp_type == 'radiobutton':
                selected = props.get('selected', False)
                html += f"""
                <div class="ui-component radiobutton" style="left: {x}px; top: {y}px;">
                    <input type="radio" {'checked' if selected else ''}> {text}
                </div>
                """
            
            elif comp_type == 'listbox':
                html += f"""
                <select class="ui-component listbox" style="left: {x}px; top: {y}px; width: {width}px; height: {height}px;">
                    {''.join([f'<option>{item}</option>' for item in items])}
                </select>
                """
            
            elif comp_type == 'panel':
                html += f"""
                <div class="ui-component panel" style="left: {x}px; top: {y}px; width: {width}px; height: {height}px;">
                    
                </div>
                """
        
        html += """
            </div>
        </body>
        </html>
        """
        
        return html