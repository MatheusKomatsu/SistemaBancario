#Sistema bancário com os conceitos de POO
from abc import (
    ABC, 
    abstractproperty
)
import datetime


class Conta():
    def __init__(self, _numero, _cliente) -> None:
        self._saldo = 0
        self._numero = _numero
        self._agencia = "0001"
        self._cliente = _cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
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
    
    def sacar (self, valor):
        if valor > self._saldo:
            print("Valor desejado é maior que o disponível na conta, operação inválida!")
        elif valor < 0:
            print("Valores negativos não são aceitos, operação inválida!")
        elif valor == 0:
            print("Saque nulo, operação inválida!")
        else:
            self._saldo -= valor
            print("Saque realizado com sucesso!")
            return True 
        return False 

    def depositar(self, valor):
        if valor < 0:
            print("Valores negativos não são aceitos, operação inválida!")
        elif valor == 0:
            print("Depósito nulo, operação inválida!")
        else:
            self._saldo += valor
            print("Deposito realizado com sucesso!")
            return True 
        return False

    def __str__(self) -> str:
        return f"Cliente: {self._cliente}, Numero: {self._numero}, Agência: {self._agencia}"


class ContaCorrente(Conta):
    def __init__(self, _numero, _cliente, _limite = 500, _limite_saques = 3) -> None:
        super().__init__( _numero, _cliente)
        self._limite = _limite
        self._limite_saques = _limite_saques

    @property
    def limite(self):
        return self._limite
    
    @property
    def limite_saques(self):
        return self._limite_saques
    
    def sacar (self, valor):
        numero_saques = 0
        for transacoes in self._historico._transacoes:
            if transacoes["Tipo"] == Saque.__name__:
                numero_saques += 1
        if numero_saques < self._limite_saques:
            if valor > self._limite:
                print("O valor máximo de saque é R$500.00, operação inválida!")
            if valor > self._saldo:
                print("Valor desejado é maior que o disponível na conta, operação inválida!")
            elif valor < 0:
                print("Valores negativos não são aceitos, operação inválida!")
            elif valor == 0:
                print("Saque nulo, operação inválida!")
            else:
                self._saldo -= valor
                print("Saque realizado com sucesso!")
                return True 
            
        else:
            print("Numero máximo de saques diários já atingido, não é possível prosseguir com a operação!")
        return False
    
    def __str__(self) -> str:
        return f"Numero: {self._numero}, Agência: {self._agencia}, Limite de Saque(valor): {self._limite}, \
Limite de Saque(quantidade): {self._limite_saques}"

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    
    def registrar(self, conta):
        pass
    
class Deposito(Transacao):
    def __init__(self, _valor) -> None:
        self._valor = _valor

    def registrar(self, conta):
        sucesso = conta.depositar(self._valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)
    
    @property
    def valor(self):
        return self._valor
      

class Saque(Transacao):
    def __init__(self, _valor):
        self._valor = _valor

    def registrar(self, conta):
        sucesso = conta.sacar(self._valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)

    @property
    def valor(self):
        return self._valor
        

class PessoaFisica():
    def __init__(self, _cpf, _nome, _data_nascimento) -> None:
        self._cpf = _cpf
        self._nome =  _nome
        self._data_nascimento = _data_nascimento
        
    @property
    def cpf(self):
        return self._cpf
    
    @property
    def nome(self):
        return self._nome
    
    def __str__(self) -> str:
        return f"CPF: {self._cpf}, Nome: {self._nome}, Data de nascimento: {self._data_nascimento}"


class Cliente(PessoaFisica):
    def __init__(self, _cpf, _nome, _data_nascimento, _endereco) -> None:
        super().__init__(_cpf, _nome, _data_nascimento)
        self._endereco = _endereco
        self._contas = []

    @property
    def contas(self):
        return self._contas

    @property
    def endereco(self):
        return self._endereco    

    def realizar_transacao (self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

    def __str__(self) -> str:
        return f"CPF: {self._cpf}, Nome: {self._nome}, Data de nascimento: {self._data_nascimento}, Endereço: {self._endereco}"


class Historico:
    def __init__(self) -> None:
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "Tipo": transacao.__class__.__name__,
                "Valor": transacao.valor,
                "Data": datetime.datetime.now(),
            }
        )


def gerar_extrato(clientes):
    cpf = input("Insira seu CPF:")
    cliente = exibir_clientes(clientes,cpf)
    if not cliente:
        print("Cliente não registrado no sistema, operação inválida!")
        return

    print("============EXTRATO============\n")
    for conta in cliente.contas:
        for transacao in conta.historico.transacoes: 
            for key, value in transacao.items():
                print(f"{key}: {value} ", sep = ' ')
            print()
        print(f"Saldo Atual: {conta.saldo:.2f}\n")
    print("===============================")


def registrar_cliente(clientes):
    cpf = input("Insira seu CPF:")
    if exibir_clientes(clientes,cpf):
        print("Cpf já registrado no sistema, operação inválida!")
        return
    nome = input("Insira seu nome: ")
    data_nascimento = input("Insira a data de nascimento, no formato (dd-mm-aaaa): ")
    logradouro, numero, bairro, cidade, estado = input(
"Insira seu endereço, na ordem -> logradouro numero bairro cidade sigla do estado: "
    ).split()
    endereco = (f"{logradouro}, {numero} - {bairro} - {cidade}/{estado}")
    cliente = Cliente(cpf,nome,data_nascimento,endereco)
    clientes.append(cliente)
    print ("Cliente registrado com sucesso!")


def exibir_clientes(clientes, cpf_novo):
    for cliente in clientes:    
        if cliente.cpf == cpf_novo:
            return cliente
    return None


def criar_conta(clientes):
    cpf = input("Insira seu cpf: ")
    for cliente in clientes:
        cliente = exibir_clientes(clientes, cpf)
        if cliente:
            numero = len(cliente.contas) + 1
            conta = ContaCorrente(numero, cliente)
            cliente.adicionar_conta(conta)
            print("Conta registrada com sucesso!")
            return True

    print("Cliente não registrado, operação inválida!")
    return False

    
def listar_contas(clientes):
    print("=========CONTAS=========")
    for cliente in clientes:
        for conta in cliente.contas:
            print(conta)
    print("========================")


def listar_clientes(clientes):
    print("========CLIENTES========")
    for cliente in clientes:
        print(cliente)
    print("========================")


def verificacao_cliente_conta(clientes):
    cpf = input("Insira o cpf do cliente: ")
    cliente = exibir_clientes(clientes, cpf)

    if not cliente:
        print("Cliente não consta no sistema, operação inválida!")
        return None, None
    
    conta = exibir_conta_cliente(cliente)
    if not conta:
        return None, None
    return cliente, conta


def depositar(clientes):
    cliente, conta = verificacao_cliente_conta(clientes)
    if not cliente:
        return False
    
    valor = float(input("Insira o valor do depósito: "))
    transacao = Deposito(valor)

    cliente.realizar_transacao(conta,transacao)
    return True


def sacar(clientes):
    cliente, conta = verificacao_cliente_conta(clientes)
    if not cliente:
        return False
        
    valor = float(input("Insira o valor do saque: "))
    transacao = Saque(valor)

    cliente.realizar_transacao(conta,transacao)
    return True


def exibir_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não tem contas, operação inválida!")
        return False
    return cliente.contas[0]


def menu():
    mensagem = """
==========MENU==========
[d] Depositar
[s] Sacar
[e] Extrato
[r] Registrar Cliente
[c] Criar Conta
[l] Listar Clientes
[t] Listar Contas
[q] Sair
========================
    =>\n"""
    return input(mensagem)


def main():
    clientes = []

    while True:
        opcao = menu()
        if opcao.isalpha():
            opcao = opcao.lower()
        if opcao == "d":
            depositar(clientes)
        elif opcao == "s":
            sacar(clientes)
        elif opcao == "e":
             gerar_extrato(clientes)
        elif opcao == "r":
            registrar_cliente(clientes)
        elif opcao == "c":
            criar_conta(clientes)
        elif opcao == "l":
            listar_clientes(clientes)
        elif opcao == "t":
            listar_contas(clientes)
        elif opcao == "q":
            print("Obrigado por utilizar nosso sitema!")
            print("Saindo...")
            break
        else:
            print("Operacao inválida, por favor selecione novamente a operação desejada.")
main()