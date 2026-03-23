class CppCodeGenerator:
    """Генератор C++ кода для UI"""
    
    def __init__(self):
        self.component_templates = {
            'button': self._generate_button,
            'label': self._generate_label,
            'textbox': self._generate_textbox,
            'window': self._generate_window,
            'checkbox': self._generate_checkbox,
            'radiobutton': self._generate_radiobutton,
            'listbox': self._generate_listbox,
            'panel': self._generate_panel
        }
    
    def generate_code(self, project_name, components):
        """Генерация полного C++ кода"""
        
        code = f"""// Generated UI Code for {project_name}
// This code uses standard C++ libraries for UI rendering
// Supports Windows console UI with Windows API (for Windows)
// For cross-platform, uses standard output with ANSI escape codes

#include <iostream>
#include <vector>
#include <string>
#include <memory>
#include <functional>
#include <map>
#include <windows.h>  // Windows API for console UI

using namespace std;

// ANSI color codes for console styling
namespace Colors {{
    const string RESET = "\\033[0m";
    const string RED = "\\033[31m";
    const string GREEN = "\\033[32m";
    const string YELLOW = "\\033[33m";
    string BLUE = "\\033[34m";
    string MAGENTA = "\\033[35m";
    string CYAN = "\\033[36m";
    string WHITE = "\\033[37m";
    
    const string BG_RED = "\\033[41m";
    const string BG_GREEN = "\\033[42m";
    const string BG_BLUE = "\\033[44m";
}}

// Base UI Component Class
class UIComponent {{
protected:
    int x, y, width, height;
    string text;
    bool visible;
    bool enabled;
    
public:
    UIComponent(int x = 0, int y = 0, int width = 10, int height = 1, string text = "")
        : x(x), y(y), width(width), height(height), text(text), visible(true), enabled(true) {{}}
    
    virtual ~UIComponent() = default;
    
    virtual void draw() = 0;
    virtual void handleInput(int key) {{}}
    
    void setPosition(int newX, int newY) {{ x = newX; y = newY; }}
    void setText(const string& newText) {{ text = newText; }}
    void setVisible(bool v) {{ visible = v; }}
    void setEnabled(bool e) {{ enabled = e; }}
    
    bool isVisible() const {{ return visible; }}
    bool isEnabled() const {{ return enabled; }}
    int getX() const {{ return x; }}
    int getY() const {{ return y; }}
}};

"""
        
        # Генерируем классы для каждого типа компонента
        for component in components:
            component_type = component.get('type', 'button')
            generator_func = self.component_templates.get(component_type, self._generate_default)
            code += generator_func(component)
        
        # Генерируем главный класс приложения
        code += self._generate_main_class(project_name, components)
        
        # Генерируем функцию main
        code += self._generate_main_function(project_name, components)
        
        return code
    
    def _generate_button(self, component):
        """Генерация кнопки"""
        props = component.get('properties', {})
        text = props.get('text', 'Button')
        x = props.get('x', 10)
        y = props.get('y', 10)
        width = props.get('width', 15)
        
        return f"""
class Button{component['id']} : public UIComponent {{
public:
    function<void()> onClick;
    
    Button{component['id']}(int x, int y) : UIComponent(x, y, {width}, 1, "{text}") {{}}
    
    void draw() override {{
        if (!visible) return;
        
        HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
        COORD cursorPosition = {{ (SHORT)x, (SHORT)y }};
        SetConsoleCursorPosition(hConsole, cursorPosition);
        
        cout << Colors::CYAN << "[" << text << "]" << Colors::RESET;
    }}
    
    void handleInput(int key) override {{
        if (key == 13 && onClick) {{  // Enter key
            onClick();
        }}
    }}
}};

"""
    
    def _generate_label(self, component):
        """Генерация метки"""
        props = component.get('properties', {})
        text = props.get('text', 'Label')
        x = props.get('x', 10)
        y = props.get('y', 10)
        
        return f"""
class Label{component['id']} : public UIComponent {{
public:
    Label{component['id']}(int x, int y) : UIComponent(x, y, {len(text)}, 1, "{text}") {{}}
    
    void draw() override {{
        if (!visible) return;
        
        HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
        COORD cursorPosition = {{ (SHORT)x, (SHORT)y }};
        SetConsoleCursorPosition(hConsole, cursorPosition);
        
        cout << Colors::WHITE << text << Colors::RESET;
    }}
}};

"""
    
    def _generate_textbox(self, component):
        """Генерация текстового поля"""
        props = component.get('properties', {})
        placeholder = props.get('placeholder', 'Enter text')
        x = props.get('x', 10)
        y = props.get('y', 10)
        width = props.get('width', 30)
        
        return f"""
class TextBox{component['id']} : public UIComponent {{
private:
    string value;
    
public:
    TextBox{component['id']}(int x, int y) : UIComponent(x, y, {width}, 1, "") {{
        value = "";
    }}
    
    void draw() override {{
        if (!visible) return;
        
        HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
        COORD cursorPosition = {{ (SHORT)x, (SHORT)y }};
        SetConsoleCursorPosition(hConsole, cursorPosition);
        
        cout << Colors::GREEN << "[" << value;
        if (value.length() < width) {{
            for (int i = value.length(); i < width; i++) cout << " ";
        }}
        cout << "]" << Colors::RESET;
    }}
    
    void handleInput(int key) override {{
        if (key >= 32 && key <= 126 && value.length() < width) {{  // Printable characters
            value += (char)key;
        }}
        else if (key == 8 && !value.empty()) {{  // Backspace
            value.pop_back();
        }}
    }}
    
    string getValue() const {{ return value; }}
}};

"""
    
    def _generate_window(self, component):
        """Генерация окна"""
        props = component.get('properties', {})
        title = props.get('title', 'Window')
        x = props.get('x', 0)
        y = props.get('y', 0)
        width = props.get('width', 60)
        height = props.get('height', 20)
        
        return f"""
class Window{component['id']} : public UIComponent {{
private:
    vector<unique_ptr<UIComponent>> children;
    
public:
    Window{component['id']}(int x, int y) : UIComponent(x, y, {width}, {height}, "{title}") {{}}
    
    void addChild(unique_ptr<UIComponent> child) {{
        children.push_back(move(child));
    }}
    
    void draw() override {{
        if (!visible) return;
        
        // Draw window border
        for (int i = 0; i <= width; i++) {{
            HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
            COORD cursorPosition;
            
            cursorPosition = {{ (SHORT)(x + i), (SHORT)y }};
            SetConsoleCursorPosition(hConsole, cursorPosition);
            cout << "=";
            
            cursorPosition = {{ (SHORT)(x + i), (SHORT)(y + height) }};
            SetConsoleCursorPosition(hConsole, cursorPosition);
            cout << "=";
        }}
        
        for (int i = 0; i <= height; i++) {{
            HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
            COORD cursorPosition = {{ (SHORT)x, (SHORT)(y + i) }};
            SetConsoleCursorPosition(hConsole, cursorPosition);
            cout << "|";
            
            cursorPosition = {{ (SHORT)(x + width), (SHORT)(y + i) }};
            SetConsoleCursorPosition(hConsole, cursorPosition);
            cout << "|";
        }}
        
        // Draw title
        HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
        COORD cursorPosition = {{ (SHORT)(x + 2), (SHORT)y }};
        SetConsoleCursorPosition(hConsole, cursorPosition);
        cout << Colors::YELLOW << text << Colors::RESET;
        
        // Draw children
        for (auto& child : children) {{
            child->draw();
        }}
    }}
    
    void handleInput(int key) override {{
        for (auto& child : children) {{
            child->handleInput(key);
        }}
    }}
}};

"""
    
    def _generate_checkbox(self, component):
        """Генерация чекбокса"""
        props = component.get('properties', {})
        text = props.get('text', 'Checkbox')
        x = props.get('x', 10)
        y = props.get('y', 10)
        checked = props.get('checked', False)
        
        return f"""
class CheckBox{component['id']} : public UIComponent {{
private:
    bool checked;
    
public:
    CheckBox{component['id']}(int x, int y) : UIComponent(x, y, {len(text) + 4}, 1, "{text}"), checked({str(checked).lower()}) {{}}
    
    void draw() override {{
        if (!visible) return;
        
        HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
        COORD cursorPosition = {{ (SHORT)x, (SHORT)y }};
        SetConsoleCursorPosition(hConsole, cursorPosition);
        
        cout << Colors::MAGENTA << "[" << (checked ? "X" : " ") << "] " << text << Colors::RESET;
    }}
    
    void handleInput(int key) override {{
        if (key == 32) {{  // Space key
            checked = !checked;
        }}
    }}
    
    bool isChecked() const {{ return checked; }}
}};

"""
    
    def _generate_radiobutton(self, component):
        """Генерация радио-кнопки"""
        props = component.get('properties', {})
        text = props.get('text', 'Radio')
        x = props.get('x', 10)
        y = props.get('y', 10)
        selected = props.get('selected', False)
        
        return f"""
class RadioButton{component['id']} : public UIComponent {{
private:
    bool selected;
    
public:
    RadioButton{component['id']}(int x, int y) : UIComponent(x, y, {len(text) + 4}, 1, "{text}"), selected({str(selected).lower()}) {{}}
    
    void draw() override {{
        if (!visible) return;
        
        HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
        COORD cursorPosition = {{ (SHORT)x, (SHORT)y }};
        SetConsoleCursorPosition(hConsole, cursorPosition);
        
        cout << Colors::YELLOW << "(" << (selected ? "*" : " ") << ") " << text << Colors::RESET;
    }}
    
    void handleInput(int key) override {{
        if (key == 32) {{  // Space key
            selected = true;
        }}
    }}
    
    bool isSelected() const {{ return selected; }}
}};

"""
    
    def _generate_listbox(self, component):
        """Генерация списка"""
        props = component.get('properties', {})
        items = props.get('items', ['Item 1', 'Item 2', 'Item 3'])
        x = props.get('x', 10)
        y = props.get('y', 10)
        height = props.get('height', 5)
        
        items_str = ', '.join([f'"{item}"' for item in items])
        
        return f"""
class ListBox{component['id']} : public UIComponent {{
private:
    vector<string> items;
    int selectedIndex;
    
public:
    ListBox{component['id']}(int x, int y) : UIComponent(x, y, 20, {height}, ""), selectedIndex(0) {{
        items = {{{items_str}}};
    }}
    
    void draw() override {{
        if (!visible) return;
        
        HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
        for (int i = 0; i < items.size() && i < height; i++) {{
            COORD cursorPosition = {{ (SHORT)x, (SHORT)(y + i) }};
            SetConsoleCursorPosition(hConsole, cursorPosition);
            
            if (i == selectedIndex) {{
                cout << Colors::BG_BLUE << Colors::WHITE << items[i];
                for (int j = items[i].length(); j < width; j++) cout << " ";
                cout << Colors::RESET;
            }} else {{
                cout << Colors::WHITE << items[i];
                for (int j = items[i].length(); j < width; j++) cout << " ";
            }}
        }}
    }}
    
    void handleInput(int key) override {{
        if (key == 72 && selectedIndex > 0) {{  // Up arrow
            selectedIndex--;
        }}
        else if (key == 80 && selectedIndex < items.size() - 1) {{  // Down arrow
            selectedIndex++;
        }}
    }}
    
    string getSelectedItem() const {{
        return items[selectedIndex];
    }}
}};

"""
    
    def _generate_panel(self, component):
        """Генерация панели"""
        props = component.get('properties', {})
        x = props.get('x', 5)
        y = props.get('y', 5)
        width = props.get('width', 40)
        height = props.get('height', 10)
        
        return f"""
class Panel{component['id']} : public UIComponent {{
private:
    vector<unique_ptr<UIComponent>> children;
    
public:
    Panel{component['id']}(int x, int y) : UIComponent(x, y, {width}, {height}, "") {{}}
    
    void addChild(unique_ptr<UIComponent> child) {{
        children.push_back(move(child));
    }}
    
    void draw() override {{
        if (!visible) return;
        
        HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
        
        // Draw panel background
        for (int i = 0; i < height; i++) {{
            COORD cursorPosition = {{ (SHORT)x, (SHORT)(y + i) }};
            SetConsoleCursorPosition(hConsole, cursorPosition);
            
            for (int j = 0; j < width; j++) {{
                cout << ".";
            }}
        }}
        
        // Draw children
        for (auto& child : children) {{
            child->draw();
        }}
    }}
    
    void handleInput(int key) override {{
        for (auto& child : children) {{
            child->handleInput(key);
        }}
    }}
}};

"""
    
    def _generate_default(self, component):
        """Генерация дефолтного компонента"""
        return f"""
class Component{component['id']} : public UIComponent {{
public:
    Component{component['id']}(int x, int y) : UIComponent(x, y, 10, 1, "Component") {{}}
    
    void draw() override {{
        if (!visible) return;
        
        HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
        COORD cursorPosition = {{ (SHORT)x, (SHORT)y }};
        SetConsoleCursorPosition(hConsole, cursorPosition);
        
        cout << text;
    }}
}};

"""
    
    def _generate_main_class(self, project_name, components):
        """Генерация главного класса приложения"""
        code = f"""
class {project_name}App {{
private:
    vector<unique_ptr<UIComponent>> components;
    
public:
    {project_name}App() {{
        // Initialize UI components
"""
        
        for component in components:
            props = component.get('properties', {})
            x = props.get('x', 10)
            y = props.get('y', 10)
            comp_type = component.get('type', 'button')
            comp_class = f"{comp_type.capitalize()}{component['id']}"
            
            code += f"""
        auto {comp_type}{component['id']} = make_unique<{comp_class}>({x}, {y});
        components.push_back(move({comp_type}{component['id']}));
"""
        
        code += """
    }
    
    void draw() {
        system("cls");  // Clear screen
        for (auto& component : components) {
            component->draw();
        }
    }
    
    void handleInput() {
        HANDLE hStdin = GetStdHandle(STD_INPUT_HANDLE);
        INPUT_RECORD ir;
        DWORD events;
        
        ReadConsoleInput(hStdin, &ir, 1, &events);
        
        if (ir.EventType == KEY_EVENT && ir.Event.KeyEvent.bKeyDown) {
            int key = ir.Event.KeyEvent.wVirtualKeyCode;
            for (auto& component : components) {
                component->handleInput(key);
            }
        }
    }
    
    void run() {
        draw();
        while (true) {
            handleInput();
            draw();
            Sleep(50);
        }
    }
};
"""
        return code
    
    def _generate_main_function(self, project_name, components):
        """Генерация функции main"""
        return f"""
int main() {{
    // Set console title
    SetConsoleTitle(TEXT("{project_name}"));
    
    // Get console handle and set cursor visibility
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    CONSOLE_CURSOR_INFO cursorInfo;
    GetConsoleCursorInfo(hConsole, &cursorInfo);
    cursorInfo.bVisible = FALSE;
    SetConsoleCursorInfo(hConsole, &cursorInfo);
    
    // Create and run application
    {project_name}App app;
    app.run();
    
    return 0;
}}
"""