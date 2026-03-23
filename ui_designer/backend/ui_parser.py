class UIParser:
    """Парсер UI для генерации превью"""
    
    def generate_preview(self, components):
        """Генерация HTML превью"""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                .preview-container {
                    position: relative;
                    background: #f5f5f5;
                    min-height: 500px;
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
            title = props.get('title', '')
            placeholder = props.get('placeholder', '')
            items = props.get('items', [])
            checked = props.get('checked', False)
            selected = props.get('selected', False)
            
            if comp_type == 'button':
                html += f"""
                <button class="ui-component button" style="left: {x}px; top: {y}px; width: {width}px; height: {height}px;">
                    {text}
                </button>
                """
            
            elif comp_type == 'label':
                html += f"""
                <div class="ui-component label" style="left: {x}px; top: {y}px; width: {width}px;">
                    {text}
                </div>
                """
            
            elif comp_type == 'textbox':
                html += f"""
                <input type="text" class="ui-component textbox" placeholder="{placeholder}" 
                       style="left: {x}px; top: {y}px; width: {width}px; height: {height}px;">
                """
            
            elif comp_type == 'window':
                html += f"""
                <div class="ui-component window" style="left: {x}px; top: {y}px; width: {width}px; height: {height}px;">
                    <div class="window-title">{title}</div>
                    <div style="padding: 10px;">Window Content</div>
                </div>
                """
            
            elif comp_type == 'checkbox':
                html += f"""
                <div class="ui-component checkbox" style="left: {x}px; top: {y}px;">
                    <input type="checkbox" {'checked' if checked else ''}> {text}
                </div>
                """
            
            elif comp_type == 'radiobutton':
                html += f"""
                <div class="ui-component radiobutton" style="left: {x}px; top: {y}px;">
                    <input type="radio" name="radio_group" {'checked' if selected else ''}> {text}
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
                    Panel Content
                </div>
                """
        
        html += """
            </div>
        </body>
        </html>
        """
        
        return html
