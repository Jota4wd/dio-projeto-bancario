def menu():
    menu = '''
    [cu] Cadastrar usuario
    [cc] Cadastrar conta
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair
    \n
    >>>:   
    '''

    return input(menu)


def depositar(valor, saldo, extrato, /):
        
        if valor > 0:
            saldo += valor
            extrato += f'Deposito: R$ {valor:.2f}\n'

        else:
            print('Operaçao falhou! O valor informado eh invalido.')

        return saldo, extrato

        
def sacar(*, valor, saldo, extrato, saque_maximo, quantidade_saques, saque_diario):
        saldo_insuficiente = valor > saldo
        limite_saque = valor > saque_maximo
        limite_diario = quantidade_saques >= saque_diario
        
        

        if saldo_insuficiente:
            print('Operaçao falhou! Voce nao possui saldo suficiente.')

        elif limite_saque:
            print('Operaçao falhou! O valor do saque excede o limite por saque.')

        elif limite_diario:
            print('Operaçao falhou! Numero maximo de saques diarios realizados.')

        elif valor > 0:
            saldo -= valor
            extrato += f'Saque: R$ {valor:.2f}\n'
            quantidade_saques += 1

        else:
            print('Operaçao falhou! O valor informado eh invalido.')

        return saldo, extrato, quantidade_saques


def exibir_extrato(saldo, /, *, extrato):
        extrato = extrato
        saldo = saldo
        titulo = '  EXTRATO  '
        decorador = '#'

        print(titulo.center(40,'#'))
        print('Nao foram realizadas movimentaçoes.' if not extrato else extrato)
        print(f'\nSaldo: R$ {saldo:.2f}')
        print(decorador.center(40,'#'))


def cadastrar_usuario(usuarios):
    cpf = input('Informe apenas os numeros do CPF: ')
    cadastrado = False
    incluir = {}

    for cliente in usuarios:
        if cpf in cliente.values():
            print('Usuario ja cadastrado!')
            cadastrado = True

            break

    if not cadastrado:
        incluir['cpf'] = cpf
        incluir['nome'] = input('Escreva o nome completo: ')
        incluir['nascimento'] = input('Informe a data de nascimento (dd-mm-aaaa): ')
        incluir['endereco'] = input('Informe o endereço (logradouro, nro - bairro -  cidade/sigla estado): ')

        print('\n\nUsuario cadastrado com sucesso')
        usuarios.append(incluir)


def cadastrar_conta(AGENCIA, guia_conta, usuarios, contas):
    cpf = input('Informe o cpf do correntista(apenas numeros): ')

    cadastrado = True
    incluir = {}

    for cliente in usuarios:
        if cpf not in cliente.values():
            print('Cpf informado ainda nao eh correntista!')

            cadastrado = False

            break

    if cadastrado:
        incluir['agencia'] = AGENCIA
        incluir['conta'] = guia_conta
        incluir['cpf'] = cpf

        print('\n\nConta cadastrada com sucesso sucesso')
        contas.append(incluir)


def main():
    SAQUES_DIARIOS = 3
    VALOR_MAXIMO_SAQUE = 500
    AGENCIA = '0001'

    saldo = 0
    extrato = ''
    quantidade_saques = 0
    usuarios = []
    contas = []
    guia_conta = 0

    while True:
        opcao = menu()

        if opcao == 'cu':
            cadastrar_usuario(usuarios)

        elif opcao == 'cc':
            guia_conta += 1

            cadastrar_conta(AGENCIA, guia_conta, usuarios, contas)

        # menus ocultos para verificar usuarios e contas
        elif opcao == 'pu':
            print(usuarios)

        elif opcao == 'pc':
            print(contas)

        elif opcao == 'd':
            valor = float(input('Informe o valor do deposito: '))
            saldo, extrato = depositar(valor, saldo, extrato)

        elif opcao == 's':
            valor = float(input('Informe o valor do saque: '))
            saldo, extrato, quantidade_saques = sacar(
                valor = valor,
                saldo = saldo,
                extrato = extrato,
                saque_maximo = VALOR_MAXIMO_SAQUE,
                quantidade_saques = quantidade_saques,
                saque_diario = SAQUES_DIARIOS)

        elif opcao == 'e':
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == 'q':
            break

        else:
            print('operaçao invalida, por favor selecione novamente a operaçao desejada.')

main()
