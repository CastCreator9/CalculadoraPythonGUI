import PySimpleGUI as sg

#-----CONFIGURACION---------------------------------------------#
cb: dict = {'size':(7,2), 'font':('Franklin Gothic Book', 24), 'button_color':("black","#F8F8F8")}
ci: dict = {'size':(15,2), 'font':('Franklin Gothic Book', 24), 'button_color':("black","#F8F8F8"), 'focus' : True}

#-----INTERFAZ--------------------------------------------------#
layout: list = [
    [sg.Text('0', size=(18,1), justification='right', background_color='black', text_color='white',
        font=('Digital-7',48), relief='sunken', key="_DISPLAY_")],
    [sg.Button('C',**cb), sg.Button('CE',**cb), sg.Button('%',**cb), sg.Button("/",**cb)],
    [sg.Button('7',**cb), sg.Button('8',**cb), sg.Button('9',**cb), sg.Button("*",**cb)],
    [sg.Button('4',**cb), sg.Button('5',**cb), sg.Button('6',**cb), sg.Button("+",**cb)],
    [sg.Button('1',**cb), sg.Button('2',**cb), sg.Button('3',**cb), sg.Button("-",**cb)],
    [sg.Button('0',**cb), sg.Button('.',**cb), sg.Button('=',**ci)]
]

window = sg.Window('Calculadora - PySimpleGUI', layout=layout, background_color="#252850", size=(580, 660), return_keyboard_events=True)

#-----FUNCIONES PARA CALCULAR-------------------------------------#
var: dict = {'front':[], 'back':[], 'decimal':False, 'x_val':0.0, 'y_val':0.0, 'result':0.0, 'operator':''}

#-----CREACION DEL FORMATO DE NUMEROS-----------------------------#
def format_number() -> float:
    '''Creamos una cadena de números solida'''
    return float(''.join(var['front']) + '.' + ''.join(var['back']))

def update_display(display_value: str):
    '''Actualizamos el display despues de cada evento'''
    try:
        window['_DISPLAY_'].update(value='{:,.4f}'.format(display_value))
    except:
        window['_DISPLAY_'].update(value=display_value)


#-----EVENTO POR FUNCION NUMERICA------------------#
def number_click(event: str):
    '''Evento por numero clickeado'''
    global var
    if var['decimal']:
        var['back'].append(event)
    else:
        var['front'].append(event)
    update_display(format_number())

def clear_click():
    '''Resetear el Display si tenemos C o CE'''
    global var
    var['front'].clear()
    var['back'].clear()
    var['decimal'] = False


def operator_click(event: str):
    '''Operaciones * / - +'''
    global var
    var['operator'] = event
    try:
        var['x_val'] = format_number()
    except:
        var['x_val'] = var['result']
    clear_click()


def calculate_click():
    '''Ecuacion a calcular'''
    global var
    var['y_val'] = format_number()
    try:
        var['result'] = eval(str(var['x_val']) + var['operator'] + str(var['y_val']))
        update_display(var['result'])
        clear_click
    except:
        update_display("ERROR")
        clear_click



#-----ASIGNADOR DEL EVENTO---------------------------------------#

while True:
    event, values = window.read()
    print(event)
    if event is None:
        break
    if event in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        number_click(event)
    if event in ['C', 'CE']:
        clear_click()
        update_display(0.0)
        var['result'] = 0.0
    if event in ['+','-','*','/']:
        operator_click(event)
    if event == '=':
        calculate_click()
    if event == '.':
        var['decimal'] = True
    if event == '%':
        update_display(var['result'] / 100.0)
