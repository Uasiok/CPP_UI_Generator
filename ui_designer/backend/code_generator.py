class CppCodeGenerator:
    """Генератор Win32 GUI кода для C++"""
    
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
        """Генерация полного Win32 GUI кода"""
        
        # Очищаем имя проекта от специальных символов
        project_name = ''.join(c for c in project_name if c.isalnum() or c == '_')
        if not project_name:
            project_name = "MyApplication"
        
        # Начало файла с ресурсами
        code = f"""// Generated Win32 GUI Code for {project_name}
// This code creates a native Windows GUI application
// Compile with: g++ -o {project_name}.exe {project_name}.cpp -lgdi32 -mwindows
// Or use CodeBlocks: Create Win32 GUI Project and replace main.cpp

#include <windows.h>
#include <string>
#include <vector>
#include <map>
#include <functional>

using namespace std;

// Resource IDs for controls
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
void UpdateControlValues();

// Application entry point
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
                   LPSTR lpCmdLine, int nCmdShow)
{{
    g_hInst = hInstance;
    
    // Register window class
    WNDCLASSEX wc = {{0}};
    wc.cbSize = sizeof(WNDCLASSEX);
    wc.lpfnWndProc = WndProc;
    wc.hInstance = hInstance;
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
    wc.lpszClassName = L"{project_name}Class";
    
    RegisterClassEx(&wc);
    
    // Create main window
    g_hMainWnd = CreateWindowEx(
        0,
        L"{project_name}Class",
        L"{project_name} - UI Designer",
        WS_OVERLAPPEDWINDOW | WS_VISIBLE,
        CW_USEDEFAULT, CW_USEDEFAULT, 800, 600,
        NULL, NULL, hInstance, NULL
    );
    
    if (!g_hMainWnd)
        return FALSE;
    
    ShowWindow(g_hMainWnd, nCmdShow);
    UpdateWindow(g_hMainWnd);
    
    // Message loop
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
        
        # Генерируем обработчики для каждого компонента
        for component in components:
            comp_type = component.get('type', 'button')
            comp_id = component['numeric_id']
            resource_id = component['resource_id']
            
            if comp_type == 'button':
                code += f"""
                case {resource_id}:
                    if (wmEvent == BN_CLICKED)
                    {{
                        MessageBox(hwnd, L"Button clicked!", L"Action", MB_OK);
                        // Add your button click handler here
                    }}
                    break;
"""
            elif comp_type == 'checkbox':
                code += f"""
                case {resource_id}:
                    if (wmEvent == BN_CLICKED)
                    {{
                        BOOL isChecked = (SendMessage(hControl, BM_GETCHECK, 0, 0) == BST_CHECKED);
                        // Handle checkbox state change
                    }}
                    break;
"""
            elif comp_type == 'radiobutton':
                code += f"""
                case {resource_id}:
                    if (wmEvent == BN_CLICKED)
                    {{
                        // Handle radio button selection
                        SendMessage(hControl, BM_SETCHECK, BST_CHECKED, 0);
                    }}
                    break;
"""
            elif comp_type == 'textbox':
                code += f"""
                case {resource_id}:
                    if (wmEvent == EN_CHANGE)
                    {{
                        wchar_t text[256];
                        GetWindowText(hControl, text, 256);
                        // Handle text change
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
}

// Create all UI controls
void CreateControls(HWND hwnd)
{
"""
        
        # Генерируем создание каждого компонента
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
                code += f"""
    // Button: {text}
    g_controls[{resource_id}] = CreateWindow(L"BUTTON", L"{text}",
        WS_VISIBLE | WS_CHILD | BS_PUSHBUTTON,
        {x}, {y}, {width}, {height},
        hwnd, (HMENU){resource_id}, g_hInst, NULL);
"""
            elif comp_type == 'label':
                text = props.get('text', 'Label')
                code += f"""
    // Label: {text}
    g_controls[{resource_id}] = CreateWindow(L"STATIC", L"{text}",
        WS_VISIBLE | WS_CHILD,
        {x}, {y}, {width}, {height},
        hwnd, (HMENU){resource_id}, g_hInst, NULL);
"""
            elif comp_type == 'textbox':
                placeholder = props.get('placeholder', 'Enter text')
                code += f"""
    // TextBox: {placeholder}
    g_controls[{resource_id}] = CreateWindow(L"EDIT", L"{placeholder}",
        WS_VISIBLE | WS_CHILD | WS_BORDER | ES_AUTOHSCROLL,
        {x}, {y}, {width}, {height},
        hwnd, (HMENU){resource_id}, g_hInst, NULL);
"""
            elif comp_type == 'checkbox':
                text = props.get('text', 'Checkbox')
                checked = "BST_CHECKED" if props.get('checked', False) else "BST_UNCHECKED"
                code += f"""
    // Checkbox: {text}
    g_controls[{resource_id}] = CreateWindow(L"BUTTON", L"{text}",
        WS_VISIBLE | WS_CHILD | BS_AUTOCHECKBOX,
        {x}, {y}, {width}, {height},
        hwnd, (HMENU){resource_id}, g_hInst, NULL);
    SendMessage(g_controls[{resource_id}], BM_SETCHECK, {checked}, 0);
"""
            elif comp_type == 'radiobutton':
                text = props.get('text', 'Radio')
                selected = "BST_CHECKED" if props.get('selected', False) else "BST_UNCHECKED"
                code += f"""
    // RadioButton: {text}
    g_controls[{resource_id}] = CreateWindow(L"BUTTON", L"{text}",
        WS_VISIBLE | WS_CHILD | BS_AUTORADIOBUTTON,
        {x}, {y}, {width}, {height},
        hwnd, (HMENU){resource_id}, g_hInst, NULL);
    SendMessage(g_controls[{resource_id}], BM_SETCHECK, {selected}, 0);
"""
            elif comp_type == 'listbox':
                items = props.get('items', ['Item 1', 'Item 2', 'Item 3'])
                code += f"""
    // ListBox
    g_controls[{resource_id}] = CreateWindow(L"LISTBOX", NULL,
        WS_VISIBLE | WS_CHILD | WS_BORDER | WS_VSCROLL | LBS_NOTIFY,
        {x}, {y}, {width}, {height},
        hwnd, (HMENU){resource_id}, g_hInst, NULL);
"""
                for i, item in enumerate(items):
                    code += f'    SendMessage(g_controls[{resource_id}], LB_ADDSTRING, 0, (LPARAM)L"{item}");\n'
            
            elif comp_type == 'panel':
                code += f"""
    // Panel (Group Box)
    g_controls[{resource_id}] = CreateWindow(L"BUTTON", L"Panel",
        WS_VISIBLE | WS_CHILD | BS_GROUPBOX,
        {x}, {y}, {width}, {height},
        hwnd, (HMENU){resource_id}, g_hInst, NULL);
"""
        
        code += """
}

// Helper function to update control values
void UpdateControlValues()
{
    // Add code to update control values dynamically
}
"""
        
        return code
