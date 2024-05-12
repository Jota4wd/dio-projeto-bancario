menu = '''


[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

>>>:   '''

saldo = 0
valor_limite_saque = 500
extrato = ''
quantidade_saques = 0
SAQUES_DIARIOS = 3

while True:

    opcao = input(menu)

    if opcao == 'd':
        valor = float(input('Informe o valor do deposito: '))

        if valor > 0:
            saldo += valor
            extrato += f'Deposito: R$ {valor:.2f}\n'

        else:
            print('Operaçao falhou! O valor informado eh invalido.')

    elif opcao == 's':
        valor = float(input('Informe o valor do saque: '))

        saldo_insuficiente = valor > saldo

        limite_saque = valor > valor_limite_saque

        limite_diario = quantidade_saques >= SAQUES_DIARIOS

        if saldo_insuficiente:
            print('Operaçao falhou! Voce nao possui saldo suficiente.')

        elif limite_saque:
            print('Operaçao falhou! O valor do saque excede o limite.')

        elif limite_diario:
            print('Operaçao falhou! Numero maximo de saques excedido.')

        elif valor > 0:
            saldo -= valor
            extrato += f'Saque: R$ {valor:.2f}\n'
            quantidade_saques += 1

        else:
            print('Operaçao falhou! O valor informado eh invalido.')

    elif opcao == 'e':

        titulo = '  EXTRATO  '
        decorador = '#'

        print(titulo.center(40,'#'))
        print('Nao foram realizadas movimentaçoes.' if not extrato else extrato)
        print(f'\nSaldo: R$ {saldo:.2f}')
        print(decorador.center(40,'#'))

    elif opcao == 'q':
        break

    else:
        print('operaçao invalida, por favor selecione novamente a operaçao desejada.')
