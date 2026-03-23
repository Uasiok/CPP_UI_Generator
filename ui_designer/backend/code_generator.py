class CppCodeGenerator:
    """Генератор Win32 GUI кода для C++ (ANSI версия)"""
    
    def generate_code(self, project_name, components):
        """Генерация полного Win32 GUI кода"""
        
        # Очищаем имя проекта
        project_name = ''.join(c for c in project_name if c.isalnum() or c == '_')
        if not project_name:
            project_name = "MyApplication"
        
        # Начало кода
        code = f"""// Generated Win32 GUI Code for {project_name}
// Compile with: g++ -o {project_name}.exe {project_name}.cpp -lgdi32 -mwindows

#include <windows.h>
#include <string>
#include <vector>
#include <map>

using namespace std;

// Resource IDs
#define IDC_MAIN_WINDOW    1000
"""

        # Генерируем ID для каждого компонента
        id_counter = 1001
        for component in components:
            comp_id = f"IDC_{component['type'].upper()}_{component['id']}"
            code += f"#define {comp_id}    {id_counter}\n"
            component['resource_id'] = comp_id
            component['numeric_id'] = id_counter
            id_counter += 1

        code += f"""
// Global variables
HINSTANCE g_hInst;
HWND g_hMainWnd;
map<int, HWND> g_Controls;

// Forward declarations
LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);
void CreateControls(HWND hwnd);

// Entry point
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
                   LPSTR lpCmdLine, int nCmdShow)
{{
    g_hInst = hInstance;
    
    WNDCLASSEX wc = {{0}};
    wc.cbSize = sizeof(WNDCLASSEX);
    wc.lpfnWndProc = WndProc;
    wc.hInstance = hInstance;
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
    wc.lpszClassName = "{project_name}Class";
    
    RegisterClassEx(&wc);
    
    g_hMainWnd = CreateWindowEx(
        0,
        "{project_name}Class",
        "{project_name} - GUI Designer",
        WS_OVERLAPPEDWINDOW | WS_VISIBLE,
        CW_USEDEFAULT, CW_USEDEFAULT, 800, 600,
        NULL, NULL, hInstance, NULL
    );
    
    if (!g_hMainWnd)
        return FALSE;
    
    ShowWindow(g_hMainWnd, nCmdShow);
    UpdateWindow(g_hMainWnd);
    
    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0))
    {{
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }}
    
    return msg.wParam;
}}

// Window procedure
LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam)
{{
    switch (msg)
    {{
        case WM_CREATE:
            CreateControls(hwnd);
            return 0;
            
        case WM_COMMAND:
        {{
            int wmId = LOWORD(wParam);
            int wmEvent = HIWORD(wParam);
            HWND hControl = (HWND)lParam;
            
            switch (wmId)
            {{
"""
        
        # Генерируем обработчики для кнопок
        for component in components:
            if component.get('type') == 'button':
                resource_id = component['resource_id']
                code += f"""
                case {resource_id}:
                    if (wmEvent == BN_CLICKED)
                    {{
                        MessageBox(hwnd, "Button clicked!", "Action", MB_OK);
                    }}
                    break;
"""
        
        code += """
                default:
                    return DefWindowProc(hwnd, msg, wParam, lParam);
            }
            break;
        }
        
        case WM_DESTROY:
            PostQuitMessage(0);
            return 0;
    }
    
    return DefWindowProc(hwnd, msg, wParam, lParam);
}}

// Create all UI controls
void CreateControls(HWND hwnd)
{
"""
        
        # Генерируем создание компонентов
        for component in components:
            comp_type = component.get('type', 'button')
            props = component.get('properties', {})
            x = props.get('x', 50)
            y = props.get('y', 50)
            width = props.get('width', 100)
            height = props.get('height', 30)
            resource_id = component['resource_id']
            
            if comp_type == 'button':
                text = props.get('text', 'Button')
                # Экранируем кавычки
                text = text.replace('"', '\\"')
                code += f"""
    // Button: {text}
    g_Controls[{resource_id}] = CreateWindow("BUTTON", "{text}",
        WS_VISIBLE | WS_CHILD | BS_PUSHBUTTON,
        {x}, {y}, {width}, {height},
        hwnd, (HMENU){resource_id}, g_hInst, NULL);
"""
            elif comp_type == 'label':
                text = props.get('text', 'Label')
                text = text.replace('"', '\\"')
                code += f"""
    // Label: {text}
    g_Controls[{resource_id}] = CreateWindow("STATIC", "{text}",
        WS_VISIBLE | WS_CHILD,
        {x}, {y}, {width}, {height},
        hwnd, (HMENU){resource_id}, g_hInst, NULL);
"""
            elif comp_type == 'textbox':
                placeholder = props.get('placeholder', 'Enter text')
                placeholder = placeholder.replace('"', '\\"')
                code += f"""
    // TextBox
    g_Controls[{resource_id}] = CreateWindow("EDIT", "{placeholder}",
        WS_VISIBLE | WS_CHILD | WS_BORDER | ES_AUTOHSCROLL,
        {x}, {y}, {width}, {height},
        hwnd, (HMENU){resource_id}, g_hInst, NULL);
"""
            elif comp_type == 'checkbox':
                text = props.get('text', 'Checkbox')
                text = text.replace('"', '\\"')
                checked = "BST_CHECKED" if props.get('checked', False) else "BST_UNCHECKED"
                code += f"""
    // Checkbox: {text}
    g_Controls[{resource_id}] = CreateWindow("BUTTON", "{text}",
        WS_VISIBLE | WS_CHILD | BS_AUTOCHECKBOX,
        {x}, {y}, {width}, {height},
        hwnd, (HMENU){resource_id}, g_hInst, NULL);
    SendMessage(g_Controls[{resource_id}], BM_SETCHECK, {checked}, 0);
"""
            elif comp_type == 'radiobutton':
                text = props.get('text', 'Radio')
                text = text.replace('"', '\\"')
                selected = "BST_CHECKED" if props.get('selected', False) else "BST_UNCHECKED"
                code += f"""
    // RadioButton: {text}
    g_Controls[{resource_id}] = CreateWindow("BUTTON", "{text}",
        WS_VISIBLE | WS_CHILD | BS_AUTORADIOBUTTON,
        {x}, {y}, {width}, {height},
        hwnd, (HMENU){resource_id}, g_hInst, NULL);
    SendMessage(g_Controls[{resource_id}], BM_SETCHECK, {selected}, 0);
"""
            elif comp_type == 'listbox':
                items = props.get('items', ['Item 1', 'Item 2', 'Item 3'])
                code += f"""
    // ListBox
    g_Controls[{resource_id}] = CreateWindow("LISTBOX", NULL,
        WS_VISIBLE | WS_CHILD | WS_BORDER | WS_VSCROLL | LBS_NOTIFY,
        {x}, {y}, {width}, {height},
        hwnd, (HMENU){resource_id}, g_hInst, NULL);
"""
                for item in items:
                    item = item.replace('"', '\\"')
                    code += f'    SendMessage(g_Controls[{resource_id}], LB_ADDSTRING, 0, (LPARAM)"{item}");\n'
            
            elif comp_type == 'panel':
                text = props.get('text', 'Group')
                text = text.replace('"', '\\"')
                code += f"""
    // Panel (Group Box)
    g_Controls[{resource_id}] = CreateWindow("BUTTON", "{text}",
        WS_VISIBLE | WS_CHILD | BS_GROUPBOX,
        {x}, {y}, {width}, {height},
        hwnd, (HMENU){resource_id}, g_hInst, NULL);
"""
        
        code += """
}

"""
        
        return code
