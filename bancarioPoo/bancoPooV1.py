#codigo ja corrigido pela video aula
#partes corrigidas marcada com comentario

from abc import ABC, abstractclassmethod, abstractproperty #soh importei o abc
from datetime import datetime #errei

#historico tambem foi errado, havia criado uma grande string como no projeto basico (copiado)
class Historico:
	def __init__(self):
		self.transacoes = []

	@property
	def transacoes(self):
		return self.transacoes

	def adicionarTransacoes(self, transacao):
		self.transacoes.append(
			{
				'tipo': transacao.__class__.__name__,
				'valor': transacao.valor,
				'data': datetime.now().strftime('%d-%m-%y %H:%M:%s'),
			}
		)



class Conta:  #errei, passei todos os argumentos e nao a estancia, ainda passei self tudo
	def __init__(self, numero, cliente):
		self.saldo = 0
		self.numero = numero
		self.agencia = '0001'
		self.cliente = cliente
		self.historico = Historico()


#nao usei nenhum decorador, esqueci de encapsular com o _
#escrevi apenas: saldo, novaConta, sacar, depositar (ainda nao havia entendido o modelo UML)
	@classmethod
	def novaConta(cls, cliente, numero):
		return cls(numero, cliente)


	@property
	def saldo(self):
		return self._saldo


	@property
	def numero(self):
		return self._numero


	@property
	def agencia(self):
		return self._agencia


	@property
	def cliente(self):
		return self._cliente


	@property
	def historico(self):
		return self._historico


#errei, nao estava completo apenas subtraindo do saldo se possivel
	def sacar(self, valor):
		self.saldo = saldo
		excedeuSaldo = valor > saldo


#removi todos os elifs que havia feito no projeto basico
#nao corrigi os prints
#corrigi os returns, havia feito um para cada if
		if excedeuSaldo:
			print('Operacao falhou, saldo insuficiente.')

		elif valor > 0:
			self._saldo -= valor
			print('Saque realizado com sucesso.')
			return True

		else:
			print('Operacao falhou, valor informado eh invalido')

		return False


#recebi primeiro as variaveis e depois fiz os ifs
	def depositar(self, valor):
		if valor > 0:
			self.saldo += valor
			print('Deposito realizado com sucesso.')

		else:
			print('Operacao falhou, valor informado eh invalido.')
			return False

		return True



#ainda nao entendia o UML, entao ja sabe criei apenas limite e limiteSaque
class ContaCorrente(Conta):
	def __init__(self, numero, cliente, limite=1000, limiteSaque=3):

		super().__init__(numero, cliente)
		self.limite = limite
		self.limiteSaque = limiteSaque

#for totalmente corrigido pelo gabarito (copiado)
	def sacar(self, valor):
		numeroSaques = len(
			[transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__]
		)

		excedeuLimite = valor > self.limite
		excedeuSaque = numeroSaques >= self.limiteSaque

		if excedeuLimite:
			print('Operacao falhou, limite insuficiente.')

		elif excedeuSaque:
			print('Operacao falhou, excedeu limite de saques')

		else:
			return super().sacar(valor)

		return False

#nao havia implementado esse metodo(copidado)
	def __str__(self):
		return f"""\
		agencia:\t{self.agencia}
		c/c:\t\t{self.numero}
		titular:\t{self.cliente.nome}
		"""



#errado tambem, criado apenas a classe com metodos
class Transacao(ABC):
	@property
	@abstractproperty
	def valor(self):
		pass

	@abstractclassmethod
	def registrar(self, conta):
		pass



#classe saque e deposito haviam sido criadas como metodo em transacoes
class Saque(Transacao):
	def __init__(self, valor):
		self._valor = valor

	@property
	def valor(self):
		return self._valor

	def registrar(self, conta):
		sucessoTransacao = conta.sacar(self.valor)

		if sucessoTransacao:
			conta.historico.adicionarTransacao(self)



class Deposito(Transacao):
	def __init__(self, valor):
		self._valor = valor

	@property
	def valor(self):
		return self._valor

	def registrar(self, conta):
		sucessoTransacao = conta.depositar(self.valor)

		if sucessoTransacao:
			conta.historico.adicionarTransacao(self)



class Cliente:
	def __init__(self, endereco,): #adicionei contas no paremetro
		self.endereco = endereco
		self.contas = []


	def realizarTransacao(self, conta, transacao): #errei
		transacao.registrar(conta)


	def adicionarConta(self, conta):
		self.contas.append(conta)



class PessoaFisica(Cliente):
	def __init__(self, cpf, nome, nascimento): #nao tinha reparado no date
		super().__init__(endereco) #nao havia passado o endereco
		self.cpf = cpf
		self.nome = nome
		self.nascimento = nascimento



"""
o salto entre as aulas de criar classes e metodos (animal, latir) para esse  projeto eh gigantesco
criei todas as classes e os argumentos corretamente alguns ateh alem do necessario, (confundi algumas classes achando que seriam metodos, como sacar depositar)
mas nao passei nem perto da complexidade do desfio, errei muitas passagens de argumento, returns e nao usei os decoradores de forma correta.
tambem nao conhecia a modelagem UML, entao criei cada tabela como classe os + como metodos os - como variaveis (argumentos), e as tabelas soltas achei q seriam metodos da classe transacao
acertei ao criar conta e cliente como abstratas e conta corrente e pessoa fisica como herdeiras
"""


