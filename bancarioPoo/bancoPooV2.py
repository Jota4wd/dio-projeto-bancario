#versao feita sobre a versao1
#desafio extra tambem copiado da versao basica e adaptado
#codigo de validacao de usuario tambem implementado como funcao

import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime


class Historico:
	def __init__(self):
		self._transacoes = []

	@property
	def transacoes(self):
		return self._transacoes

	def adicionarTransacoes(self, transacao):
		self._transacoes.append(
			{
				'tipo': transacao.__class__.__name__,
				'valor': transacao.valor,
				'data': datetime.now().strftime('%d-%m-%y %H:%M:%s'),
			}
		)



class Conta:
	def __init__(self, numeroConta, cliente):
		self._saldo = 0
		self._Conta = numeroConta
		self._agencia = '0001'
		self._cliente = cliente
		self._historico = Historico()


	def __str__(self):
		return f"Agência: {self.agencia}, Conta: {self.numeroConta}, Titular: {self.cliente.nome}, Saldo: R${self.saldo:.2f}"


	@classmethod
	def novaConta(cls, cliente, numeroConta):
		return cls(numeroConta, cliente)


	@property
	def saldo(self):
		return self._saldo


	@property
	def numeroConta(self):
		return self._Conta


	@property
	def agencia(self):
		return self._agencia


	@property
	def cliente(self):
		return self._cliente


	@property
	def historico(self):
		return self._historico


	def sacar(self, valor):
		saldo = self.saldo
		excedeuSaldo = valor > saldo

		if excedeuSaldo:
			print('Operacao falhou, saldo insuficiente.')

		elif valor > 0:
			self._saldo -= valor
			print('Saque realizado com sucesso.')
			return True

		else:
			print('Operacao falhou, valor informado eh invalido')

		return False


	def depositar(self, valor):
		if valor > 0:
			self._saldo += valor
			print('Deposito realizado com sucesso.')

		else:
			print('Operacao falhou, valor informado eh invalido.')
			return False

		return True



class ContaCorrente(Conta):
	def __init__(self, numeroConta, cliente, limite=500, limiteSaque=3):

		super().__init__(numeroConta, cliente)
		self.limite = limite
		self.limiteSaque = limiteSaque


	def __str__(self):
		return f"""\agencia:\t{self.agencia}
					c/c:\t\t{self.numeroConta}
					titular\t{self.cliente.nome}
					"""


	def sacar(self, valor):
		numeroSaques = len(
			[transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__]
			)

		excedeuLimite = valor > self.limite
		excedeuSaque = numeroSaques >= self.limiteSaque

		if excedeuLimite:
			print('Operacao falhou, saque acima do limite.')

		elif excedeuSaque:
			print('Operacao falhou, excedeu limite de saques')

		else:
			return super().sacar(valor)

		return False



class Transacao(ABC):
	@property
	@abstractproperty
	def valor(self):
		pass

	@abstractclassmethod
	def registrar(self, conta):
		pass



class Saque(Transacao):
	def __init__(self, valor):
		self._valor = valor

	@property
	def valor(self):
		return self._valor

	def registrar(self, conta):
		sucessoTransacao = conta.sacar(self.valor)

		if sucessoTransacao:
			conta.historico.adicionarTransacoes(self)



class Deposito(Transacao):
	def __init__(self, valor):
		self._valor = valor

	@property
	def valor(self):
		return self._valor

	def registrar(self, conta):
		sucessoTransacao = conta.depositar(self.valor)

		if sucessoTransacao:
			conta.historico.adicionarTransacoes(self)



class Cliente:
	def __init__(self, endereco):
		self.endereco = endereco
		self.contas = []


	def realizarTransacao(self, conta, transacao):
		transacao.registrar(conta)


	def adicionarConta(self, conta):
		self.contas.append(conta)



class PessoaFisica(Cliente):
	def __init__(self, cpf, nome, nascimento, endereco):
		super().__init__(endereco)
		self.cpf = cpf
		self.nome = nome
		self.nascimento = nascimento
		
		
	def __str__(self):
		return f"Nome: {self.nome}, CPF: {self.cpf}, Nascimento: {self.nascimento}, Endereco: {self.endereco}"




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


def depositar(clientes):
	cpf = input('informe o cpf do cliente: ')
	cliente = filtrarCliente(cpf, clientes)
	
	if not cliente:
		print('cliente nao cadastrado')
		return

	valor = float(input('valor do deposito: '))
	
	transacao = Deposito(valor)
	
	conta = recuperarContaCliente(cliente)
	
	if not conta:
		return
		
	cliente.realizarTransacao(conta, transacao)

        
def sacar(clientes):
	cpf = input('cpf do cliente: ')
	cliente = filtrarCliente(cpf, clientes)

	if not cliente:
		print('cliente nao cadastrado')
		return

	valor = float(input('valor do saque: '))
	transacao = Saque(valor)

	conta = recuperarContaCliente(cliente)
	if not conta:
		return

	cliente.realizarTransacao(conta, transacao)


def exibirExtrato(clientes):
	cpf = input('cpf do cliente: ')
	cliente = filtrarCliente(cpf, clientes)

	if not cliente:
		print('cliente nao cadastrado')
		return

	conta = recuperarContaCliente(cliente)
	if not conta:
		return

	titulo = '  EXTRATO  '
	decorador = '#'

	print(titulo.center(40,'#'))
	transacoes = conta.historico.transacoes

	extrato = ''

	if not transacoes:
		extrato = 'sem movimentacao'

	else:
		for transacao in transacoes:
			extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"

	print(extrato)
	print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
	print(decorador.center(40,'#'))

def cadastrarCliente(clientes):
	cpf = input('Informe o CPF: ')
	cliente = filtrarCliente(cpf, clientes)
    
	if cliente:
		print('usuario ja eh correntista')
		return

	nome = input('Escreva o nome completo: ')
	nascimento = input('Informe a data de nascimento (dd-mm-aaaa): ')
	endereco = input('Informe o endereço (logradouro, nro - bairro -  cidade/sigla estado): ')

	cliente = PessoaFisica(nome=nome, nascimento=nascimento, cpf=cpf, endereco=endereco)
	clientes.append(cliente)
	print('\n\nCliente cadastrado com sucesso')


def cadastrarConta(numeroConta, clientes, contas):
	cpf = input('Informe o cpf do correntista: ')
	cliente = filtrarCliente(cpf, clientes)


	if not cliente:
		print('Usuario ainda nao cadastrado')
		return

	conta = ContaCorrente.novaConta(cliente=cliente, numeroConta=numeroConta)
	contas.append(conta)
	cliente.contas.append(conta)

	print('conta aberta com sucesso')


def filtrarCliente(cpf, clientes):
	clientesFiltrados = [cliente for cliente in clientes if cliente.cpf == cpf]
	return clientesFiltrados[0] if clientesFiltrados else None


def recuperarContaCliente(cliente):
	if not cliente.contas:
		print('cliente nao cadastrado')
		return

	return cliente.contas[0]


def main():
    clientes = []
    contas = []
    

    while True:
        opcao = menu()

        if opcao == 'cu':
            cadastrarCliente(clientes)

        elif opcao == 'cc':
            numeroConta = len(contas) + 1

            cadastrarConta(numeroConta, clientes, contas)

        # menus ocultos para verificar clientes e contas
        elif opcao == 'pu':
            for cliente in clientes:
                print(cliente)

        elif opcao == 'pc':
            for conta in contas:
                print(conta)

        elif opcao == 'd':
            depositar(clientes)

        elif opcao == 's':
            sacar(clientes)

        elif opcao == 'e':
            exibirExtrato(clientes)

        elif opcao == 'q':
            break

        else:
            print('operacao invalida, por favor selecione novamente a operacao desejada.')

main()


# deixando registrado mais uma vez que:
# o salto eh gigantesco, mesmo estudando o codigo por um tempo
# ainda estou um pouco perdido de oq eh oq
# principalmente com argumentos e methodos
