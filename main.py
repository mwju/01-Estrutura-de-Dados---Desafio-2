LIMITE_SAQUES = 3
AGENCIA = "0001"
LIMITE_DIARIO = 500
clientes = []
contas = []

def retira_sinais(texto):
    resultado = ''
    for caractere in texto:
        if caractere.isdigit():
            resultado += caractere
    return resultado

def menu_conta():
    tela = """
            Movimentação de Conta Corrente

                Selecione uma opção:
                [C]adastrar Cliente
                [I]ncluir Conta
                [P]osicionar Cliente/Conta
                [L]istar Contas

                [S]air
        => """
    return input(tela)

def menu_opcoes():
    tela = """
            Movimentação de Conta Corrente

                Selecione uma opção:
                [D]epositar
                [R]etirar
                [E]xtrato

                [V]oltar
        => """
    return input(tela)

def saldo_conta(conta):
    return sum(conta['extrato'])

def selecionar_cliente(cpf):
    for cliente in clientes:
        if retira_sinais(cliente['cpf']) == cpf:
            return cliente
    return None

def selecionar_conta(cpf, numero_conta):
    for conta in contas:
        if (conta['numero_conta'] == int(numero_conta)) and (conta['cliente']['cpf'] == cpf):
            return conta
    return None


def listar_contas():
    print("==========================================")
    print("Início da Listagem")
    for conta in contas:
        saldo = saldo_conta(conta)
        print(f"""
            Agência: {conta['agencia']}
            C/C: {conta['numero_conta']}
            Titular: {conta['cliente']['nome']}
            Saldo: {saldo}
        """)
    print("Fim da Listagem")
    print("==========================================")

def criar_conta(cliente,/):
    if cliente:
        numero_conta = len(contas) + 1
        conta = {"agencia": AGENCIA, "numero_conta": numero_conta, "cliente": cliente, "extrato": []}
        contas.append(conta)
        return conta
    else:
        print("Cliente não cadastrado!")

def solicitar_numero_conta():
    while True:
        numero_conta = input("Número da conta: ")
        if numero_conta.isdigit():
            return int(numero_conta)
        else:
            print("Por favor, insira apenas números inteiros para o número da conta.")

def depositar(conta):
    valor = float(input("Entre com o valor do depósito: "))
    if valor > 0:
        conta['extrato'].append(valor)
    else:
        print('Valor não pode ser negativo')

def retirar(*, numero_saques, conta):
    if numero_saques < LIMITE_SAQUES:
        valor = float(input("Entre com o valor de saque: "))
        if valor > LIMITE_DIARIO:
            print(f'Valor excede limite de saque. Limite: R$ {LIMITE_DIARIO}')
        elif valor < 0:
            print('Valor não pode ser negativo')        
        else:
            if valor <= saldo_conta(conta): 
                conta['extrato'].append(-valor)
                numero_saques += 1
            else:
                print(f'Saldo insuficiente para saque. Total em conta: R$ {saldo_conta(conta)}')
    else:
        print('Limite de saques diários atingido (Máximo 3)')
    return numero_saques

def lista_extrato(cpf, /, *, conta):
    if conta['extrato'] == []:
        print('Não foram realizadas movimentações!')
    else:
        print("==========================================")
        print(f"CPF: {cpf}")
        print(f"Agência: {conta['agencia']}")
        print(f"C/C: {conta['numero_conta']}")
        print(f"Titular: {conta['cliente']['nome']}")
        print("==========================================")
        print("Início Extrato")
        for item in conta['extrato']:
            if item >= 0:
                print(f'\tC R$ {item}')
            else:
                print(f'\tD R$ {item}')
        print("")
        print(f'\tSaldo: R$ {saldo_conta(conta)}')
    print("Fim Extrato")
    print("==========================================")

while True:
    opcao = menu_conta().upper()

    if opcao == 'C':
        cpf = input("CPF: ")
        nome = input("Nome: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
        clientes.append({"cpf": cpf, "nome": nome, "data_nascimento": data_nascimento, "endereco": endereco})
        print("Cliente cadastrado com sucesso!")

    elif opcao == 'I':
        cpf = input("CPF do cliente: ")
        cliente = selecionar_cliente(cpf)
        conta = criar_conta(cliente)
        if conta:
            print("Conta cadastrada com sucesso!")

    elif opcao == 'L':
        listar_contas()

    elif opcao == 'P':
        cpf = input("CPF do cliente: ")
        numero_conta = solicitar_numero_conta()
        conta = selecionar_conta(cpf, numero_conta)
        
        opcao_conta = ''
        numero_saques = 0
        while opcao_conta != 'V':
            opcao_conta = menu_opcoes().upper()
            if opcao_conta == 'D':
                depositar(conta)
            elif opcao_conta == 'R':
                numero_saques = retirar(numero_saques=numero_saques, conta=conta)
            elif opcao_conta == 'E':                
                lista_extrato(cpf, conta=conta)
            elif opcao_conta == 'V':
                break
            else:
                print("Opção inválida!")

    elif opcao == 'S':
        break

    else:
        print("Opção inválida!")
