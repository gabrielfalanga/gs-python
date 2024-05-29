import os
import datetime as dt


def identificar_tipo_chamado():
    'Pede para o usuário selecionar o tipo de denúncia e o retorna.'
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
    mapa_meses = {
        1: 'jan', 2: 'fev', 3: 'mar', 4: 'abr', 5: 'mai', 
        6: 'jun', 7: 'jul', 8: 'ago', 9: 'set', 10: 'out',
        11: 'nov', 12: 'dez'
        }

    data_atual = dt.datetime.today()

    dia = data_atual.day
    mes = mapa_meses[data_atual.month]
    ano = data_atual.year

    return f'{dia} {mes} {ano}'


def solicitar_estado_e_cidade():
    estados_cidades = {
        'BA': ['Ilhéus', 'Porto Seguro', 'Salvador'],
        'RJ': ['Arraial do Cabo', 'Búzios', 'Paraty'],
        'SP': ['Caraguatatuba', 'Santos', 'Praia Grande']
    }

    estado_selecionado = input('\nDigite a sigla do estado (BA, RJ ou SP)\n> ').upper()

    if estado_selecionado in estados_cidades:
        print('Digite o número correspondente à cidade')
        for i, cidade in enumerate(estados_cidades[estado_selecionado]):
            print(f'{i+1}. {cidade}')
        try:
            n_cidade_escolhida = int(input('> ')) - 1
            cidade_selecionada = estados_cidades[estado_selecionado][n_cidade_escolhida]
            return estado_selecionado, cidade_selecionada
        except:
            print('Digite somente o número correspondente à cidade.')
    else:
        print('Estado inválido. Tente novamente.')


def solicitar_cidade(estado):
    print('\nEscolha a cidade\n')
    while True:
        if estado == 'BA':
            cidade = input('(I)lhéus\n(P)orto Seguro\n(S)alvador').upper()[0]
        elif estado == 'RJ':
            cidade = input('(A)rraial do Cabo\n(B)úzios\n(P)araty').upper()[0]
        elif estado == 'SP':
            cidade = input('(C)araguatatuba\n(S)antos\n(P)raia Grande').upper()[0]


def verificar_ultimo_id(chamados):
    ultimo_id = int(chamados[-1]['id'])
    return ultimo_id


def identificar_ultimo_id():
    with open('chamados.csv', 'r', encoding='utf-8') as csv_chamados:
        linha = '-'
        while linha != '':
            linha = csv_chamados.readline()
            if linha != '':
                colunas = linha.split(',')
                ultimo_id_encontrado = colunas[0]

        return int(ultimo_id_encontrado)


def enviar_chamado_para_csv(chamado_novo):
    c = chamado_novo
    with open('chamados.csv', 'a', encoding='utf-8') as csv_chamados:
        csv_chamados.write(f"\n{c['id']},{c['tipo']},{c['estado']},{c['cidade']},{c['bairro']},{c['rua']},{c['data']},{c['hora']},{c['descricao']}")


def limpar_console():
    'Limpa o console, independente do sistema operacional.'
    # Verifica o sistema operacional
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:                # Unix/Linux/MacOS
        os.system('clear')


menu_tipos_denuncia = '''
Selecione o tipo do chamado

(A)nimal em perigo
(P)esca ilegal
(D)escarte inadequado de lixo/material tóxico

> '''


# Iniciando o chamado do usuário
print('Vamos realizar seu chamado.')

ultimo_id = identificar_ultimo_id()
id_chamado = ultimo_id + 1
tipo = identificar_tipo_chamado()
descricao = input('Descreva a situação\n> ').strip().capitalize().replace(',', ';')
estado, cidade = solicitar_estado_e_cidade()
bairro = input('Digite o bairro mais próximo\n> ').title().strip()
rua = input('Digite a rua e, se possível, o número mais próximos\n> ').title().strip().replace(',', ';')
data = identificar_data_atual()
hora = dt.datetime.now().strftime('%H:%M')

chamado = {
    "id": id_chamado,
    "tipo": tipo,
    "estado": estado,
    "cidade": cidade, 
    "bairro": bairro, 
    "rua": rua,
    "data": data,
    "hora": hora,
    "descricao": descricao
}

enviar_chamado_para_csv(chamado)

print('\nSeu chamado foi finalizado com sucesso e já será analisado e encaminhado para as autoridades competentes.')

print(f'''\
-----------------------------
      TICKET DO CHAMADO
-----------------------------

Número: {id_chamado}     
Tipo: {tipo}
Descrição: {descricao}
Local: {cidade} - {estado} | {rua}

{data}  |  {hora}

Obrigado pela colaboração!''')