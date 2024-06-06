import os
import datetime as dt


def identificar_tipo_chamado():
    '''
    Pede para o usuário selecionar o tipo de denúncia e o retorna.
    '''
    while True:
        opcao_denuncia = input(menu_tipos_denuncia).upper()[0]
        if opcao_denuncia == 'A':
            return 'Animal em perigo'
        elif opcao_denuncia == 'P':
            return 'Pesca ilegal'
        elif opcao_denuncia == 'D':
            return 'Descarte inadequado'
        else:
            print('Opção inválida. Por favor, selecione uma das opções do menu.')


def identificar_data_atual():
    '''
    Retorna data do sistema no formato: DD mes AAAA
    '''
    mapa_meses = {
        1: 'jan', 2: 'fev', 3: 'mar', 4: 'abr', 5: 'mai', 
        6: 'jun', 7: 'jul', 8: 'ago', 9: 'set', 10: 'out',
        11: 'nov', 12: 'dez'
        }

    data_atual = dt.datetime.today()

    dia = f'{data_atual.day:0>2}'
    mes = mapa_meses[data_atual.month]
    ano = data_atual.year

    return f'{dia} {mes} {ano}'


def solicitar_estado_e_cidade():
    '''
    Exibe as opções de estados e cidades e retorna o estado e a cidade que o usuário escolheu.
    '''
    estados_cidades = {
        'BA': ['Ilhéus', 'Porto Seguro', 'Salvador'],
        'RJ': ['Arraial do Cabo', 'Búzios', 'Paraty'],
        'SP': ['Caraguatatuba', 'Santos', 'Praia Grande']
    }

    verifica = False
    while verifica == False:
        estado_selecionado = input('\nDigite a sigla do estado (BA, RJ ou SP)\n> ').upper()[:2]
        # se o estado escolhido for válido
        if estado_selecionado in estados_cidades:
            verifica = True  # encerra o loop
        # se for inválido
        else:
            print('Digite uma sigla válida.')

    while True:
        print('\nDigite o número correspondente à cidade\n')
        # exibe e numera as cidades disponíveis do estado selecionado
        for i, cidade in enumerate(estados_cidades[estado_selecionado]):
            print(f'{i+1}. {cidade}')
        # se o número da opção digitado for válido, funciona
        try:
            n_cidade_escolhida = int(input('\n> ')) - 1
            # pega a cidade no dicionário 'estados_cidades'de acordo com a sigla do estado (chave) e o n° da cidade (índice da lista, que é o valor)
            cidade_selecionada = estados_cidades[estado_selecionado][n_cidade_escolhida]
            return estado_selecionado, cidade_selecionada
        # se for inválido, causa:  ValueError na primeira linha do try  ou  IndexError na segunda linha do try
        except:
            print('Digite somente o número correspondente à cidade.')


def gerar_id():
    '''
    Verifica o último ID do arquivo CSV e retorna o novo ID.\n
    Novo ID = Último ID + 1
    '''
    with open('chamados.csv', 'r', encoding='utf-8') as csv_chamados:
        linha = '-'
        # enquanto a linha lida não for vazia
        while linha != '':
            linha = csv_chamados.readline()
            if linha != '':
                # gera lista contendo cada um dos dados da linha em um índice
                colunas = linha.split(',')
                # pega o primeiro valor da lista (ID)
                ultimo_id_encontrado = colunas[0]

        novo_id = int(ultimo_id_encontrado) + 1
        return novo_id


def enviar_chamado_para_csv(chamado_novo):
    '''
    Recebe os dados do chamado em forma de lista e envia para chamados.csv.
    '''
    c = chamado_novo
    with open('chamados.csv', 'a', encoding='utf-8') as csv_chamados:
        # envia todos os dados da lista já no formato CSV
        csv_chamados.write(f"\n{c[0]},{c[1]},{c[2]},{c[3]},{c[4]},{c[5]},{c[6]},{c[7]},{c[8]}")


def limpar_console(texto=''):
    '''
    Limpa o console, independente do sistema operacional.\n
    Aceita o parâmetro "texto" que, se passado, é exibido no console após limpá-lo.
    '''
    # Verifica o sistema operacional
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:                # Unix/Linux/MacOS
        os.system('clear')

    if texto != '':
        print(texto)


menu_tipos_denuncia = '''
Selecione o tipo do chamado

(A)nimal em perigo
(P)esca ilegal
(D)escarte inadequado de lixo/material tóxico

> '''

txt_tela_chamado = '---------- TELA DE CHAMADO ----------'


### Iniciando o chamado do usuário
limpar_console(txt_tela_chamado)

# recebendo todos os dados do chamado
id_chamado = gerar_id()
tipo = identificar_tipo_chamado()
descricao = input('\nDescreva a situação\n> ').strip().capitalize().replace(',', ';')
limpar_console(txt_tela_chamado)
estado, cidade = solicitar_estado_e_cidade()
bairro = input('\nDigite o bairro mais próximo\n> ').title().strip().replace(',', ';')
rua = input('\nDigite a rua e, se possível, o número mais próximos\n> ').title().strip().replace(',', ';')
data = identificar_data_atual()
hora = dt.datetime.now().strftime('%H:%M')
limpar_console()

# criando chamado em forma de lista para usar a função abaixo 
chamado = [id_chamado, tipo, estado, cidade, bairro, rua, data, hora, descricao]
enviar_chamado_para_csv(chamado)

# finalizando chamado com ticket exibindo informações
print(f'''
Seu chamado foi finalizado com sucesso e já será 
analisado e encaminhado para as autoridades competentes.
      
-----------------------------
|     TICKET DO CHAMADO     |
-----------------------------

Número: {id_chamado}     
Tipo: {tipo}
Descrição: {descricao}
Local: {cidade} - {estado} | {rua}

{data}  |  {hora}
-----------------------------

Obrigado pela colaboração!''')