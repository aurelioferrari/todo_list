import PySimpleGUI as sg
import datetime as datetime
import time


list = ['00:00', '00:30', '01:00', '01:30', '02:00', '02:30', '03:00', '03:30', '04:00', '04:30', '05:00', '05:30',
        '06:00', '06:30', '07:00', '07:30', '08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30',
        '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30',
        '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00', '23:30']

sg.theme('DarkBlue13')
fonts = ('Any', 15)
layout = [
    [sg.Text('Escolha ou digite um horário'), sg.Combo(list, key='lista'),  sg.Checkbox('Organizar Automaticamente', key='auto_org', default=False), sg.Push(), sg.B('i', key='info', size=(3, 1), button_color='green')],
    [sg.T('Escreva a tarefa'), sg.I(key='task', font=('None 15'), size=(32, 1)), sg.Push(), sg.B('Adicionar', button_color='green', bind_return_key=True)],
    [sg.Table(selected_row_colors='yellow on black',alternating_row_color='green', values='', headings=['Índice', 'Horário', 'Tarefa'], key='Tabela', size=(2000, 10), auto_size_columns=False, col_widths=[5, 9, 35], vertical_scroll_only=False, justification='c', font='None 13', enable_click_events=True)],
    [ sg.B('Deletar', key='deletar', button_color='red'), sg.B('Deletar Tudo', key='deletar_tudo', button_color='red'), sg.B('Topo da lista', key='topo', button_color='green'), sg.Push(), sg.B('Organizar', key='organizar')],
    [sg.T('Selecione a ordem da tarefa'), sg.I(key='novo', size=(3, 1)), sg.B('Mudar', key='mudar'), sg.Push(), sg.B('Marcar como Feito', key='feito', button_color='orange'), sg.Push(), sg.B('Marcar como Não Feito', key='nao_feito', button_color='green')],
    [sg.T('', size=(20, 1), font=fonts, key='tempo'), sg.Push(), sg.Exit('Sair')]
]

counter = 1
tasks = []
window = sg.Window('iFazer v1.2', layout, finalize=True)
counter_save = []
window['tempo'].update(time.strftime('%H:%M'))
try:

    f = open('save.txt', 'r')
    tarefas = f.read().splitlines()
    print(tarefas)
    if len(tarefas) == 0:
        pass
    else:
        for i in range(0, len(tarefas)):
            tarefas_separadas = tarefas[i].split(',')
            counter = int(tarefas_separadas[0])
            counter_save.append(counter)
            data = tarefas_separadas[1]
            desc_tarefa = tarefas_separadas[2]
            task = [[counter, data, desc_tarefa]]
            tasks += task
        window['Tabela'].update(tasks)
        counter = max(counter_save) + 1

except:
    pass


timeout = 10000
while True:
    event, values = window.read(timeout=timeout)
    if event == 'info':
        sg.popup_ok('Novidades da Versão 1.2:\n'
                    '- Botões Marcar como Lido e Não Lido Adicionados.\n'
                    '- Você receberá notificação da tarefa no horário.\n'
                    '- Relógio na base da janela.\n'
                    '- Novo posicionamento do botão Adicionar.\n'
                    '\nINSTRUÇÕES\n'
                    '- Você pode digitar um horário personalizado. O padrão é H:MM ou HH:MM.\n'
                    '- Ativar a caixa de "Organizar Automaticamente" fará com que\n'
                    'as tarefas sejam adicionadas e organizadas de acordo com os horários.\n'
                    '- Botão Adicionar adiciona um item no fim da lista.\n'
                    '- Botão Deletar deleta o item selecionado.\n'
                    '- Botão Sair fecha o programa.\n'
                    '- Botão Topo da Lista coloca o item selecionado no topo.\n'
                    '- Botão Organizar organiza a lista de acordo com os horários.\n'
                    '- Botão Mudar posiciona o item selecionado na linha digitada\n'
                    '- Botão Deletar Tudo deleta todas as tarefas.\n'
                    '- NÃO É POSSÍVEL criar duas tarefas com o mesmo horário.')
    if event in ("Sair", sg.WIN_CLOSED):
        window.close()
        break
    if event == 'Adicionar':
        if values['auto_org'] == True:
            data = values['lista']
            # hora = datetime.datetime.strptime(data, '%H:%M')
            horarios_criados = []
            for i in range(0, len(tasks)):
                horarios_criados.append(tasks[i][1])
            if data in horarios_criados:
                sg.popup_ok('Já existe uma tarefa nesse horário.')
            else:

                task = [[counter, data, values['task']]]
                tasks += task
                tasks_organizada = []
                organiza_hora = []
                print(tasks)
                window['Tabela'].update(tasks)
                window['task'].update('')

                for i in range(0, len(tasks)):
                    a = tasks[i][1].split(':')
                    if len(a) == 2:
                        a_soma = int(a[0]) + int(a[1]) / 100
                        organiza_hora.append(a_soma)
                    else:
                        organiza_hora.append(a)
                print(organiza_hora)
                organiza_hora.sort()
                print(organiza_hora)
                for i in range(0, len(organiza_hora)):
                    for n in range(0, len(tasks)):
                        b = tasks[n][1].split(':')
                        b_soma = int(b[0]) + int(b[1]) / 100
                        if organiza_hora[i] == b_soma:
                            tasks_organizada.append(tasks[n])

                window['Tabela'].update(tasks_organizada)
                tasks = tasks_organizada
                window['task'].update('')
                counter += 1
        else:
            pass

    if event == 'Adicionar' and values['auto_org'] == False:
        horarios_criados = []
        data = values['lista']
        for i in range(0, len(tasks)):
            horarios_criados.append(tasks[i][1])
        if data in horarios_criados:
            sg.popup_ok('Já existe uma tarefa nesse horário.')
        else:

            # hora = datetime.datetime.strptime(data, '%H:%M')
            task = [[counter, data, values['task']]]
            tasks += task
            window['Tabela'].update(tasks)
            window['task'].update('')
            counter += 1
    elif event == 'deletar_tudo':
        opcao = sg.popup_yes_no('Você tem certeza que quer deletar tudo?', button_color='green', background_color='lightblue', text_color='black', title='Confirmação')
        if opcao == 'Yes':
            tasks = []
            window['Tabela'].update(tasks)
            counter = 1
        else:
            pass
    elif event == 'deletar':
        if values['Tabela']:
            index = values['Tabela'][0]
            del tasks[index]
            window['Tabela'].update(tasks)
    elif event == 'feito':
        if values['Tabela']:
            index = values['Tabela'][0]
            verifica = tasks[index][2].split()
            print(verifica)
            if verifica[-1] == '[Feito]':
                sg.popup_ok('Você já completou essa tarefa.')
            else:
                tasks[index][2] = tasks[index][2] + ' [Feito]'
                window['Tabela'].update(tasks)
    elif event == 'nao_feito':
        if values['Tabela']:
            index = values['Tabela'][0]
            verifica = tasks[index][2].split()
            print(verifica)
            if verifica[-1] == '[Feito]':
                verifica.pop()
                tasks[index][2] = ''
                for i in verifica:
                    tasks[index][2] = tasks[index][2] + ' ' + i
                window['Tabela'].update(tasks)
            else:
                pass
    elif event == 'topo':
        if values['Tabela']:
            index = values['Tabela']
            print(index)
            troca = tasks.pop(index[0])
            print(troca)
            tasks.insert(0, troca)
            window['Tabela'].update(tasks)
            window['task'].update('')
    elif event == 'mudar':
        if values['Tabela'] and values['novo']:
            index = values['Tabela']
            troca = tasks.pop(index[0])
            teste = int(values['novo'])
            tasks.insert(teste-1, troca)
            window['Tabela'].update(tasks)
            window['task'].update('')
    elif event == 'organizar':
        tasks_organizada = []
        organiza_hora = []


        for i in range(0, len(tasks)):
            a = tasks[i][1].split(':')
            if len(a) == 2:
                a_soma = int(a[0]) + int(a[1]) / 100
                organiza_hora.append(a_soma)

            else:
                organiza_hora.append(a[0])

        print(organiza_hora)
        organiza_hora.sort()
        print(organiza_hora)
        for i in range(0, len(organiza_hora)):
            for n in range(0, len(tasks)):
                b = tasks[n][1].split(':')
                if len(b) == 2:
                    b_soma = int(b[0]) + int(b[1])/100
                    if organiza_hora[i] == b_soma:
                        tasks_organizada.append(tasks[n])
                else:
                    if organiza_hora[i] == b[0]:
                        tasks_organizada.append(tasks[n])




        window['Tabela'].update(tasks_organizada)
        tasks = tasks_organizada
        window['task'].update('')
    print(values['Tabela'])
    window['tempo'].update(time.strftime('%H:%M'))
    tempo = time.strftime('%H:%M')

    for i in range(0, len(tasks)):
        if tempo == tasks[i][1]:
            # tray.notify('Notify', f'{tasks[i][2]}', fade_in_duration=10, display_duration_in_ms=1000, alpha=0.5)
            sg.popup_ok(f'{tasks[i][2]}', keep_on_top=True, font=('Any', 10))
            tasks[i][1] = tasks[i][1] + ' '
            window['Tabela'].update(tasks)


f = open('save.txt', 'w', newline='')
for i in range(0, len(tasks)):
    f.write(f'{tasks[i][0]},{tasks[i][1]},{tasks[i][2]}\n')
f.close()