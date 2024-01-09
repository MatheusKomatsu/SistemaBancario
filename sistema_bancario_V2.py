# Sistema simples de banco, com 3 operações: depósito, saque e extrato, criado para seguir o curso Formação Python Developer, da DIO
# Por ser um sistema sistema, foram ignorados alguns problemas, como a falta de verificaçao de inputs, pois o objetivo era apenas criar
# uma estrutura básica de um sistema bancário
def depositar(saldo,extrato,/):
    valor = float(input("Insira o valor do depósito: "))
    if valor <0:
        print("Valores negativos não são aceitos, operação inválida!")
    elif valor == 0:
        print("Depósito nulo, operação inválida!")
    else:
        saldo +=valor
        extrato += (f"Deposito: R${valor:.2f}\n")
        print("Deposito realizado com sucesso!")
    return saldo, extrato
def sacar (*,saldo, extrato,limite,numero_saques, LIMITE_SAQUES):
    if numero_saques < LIMITE_SAQUES:
        valor = float(input("Por favor, insira a quantia desejada para o saque: "))
        if valor > limite:
            print("O valor máximo de saque é R$500.00, operação inválida!")
        elif valor > saldo:
            print("Valor desejado é maior que o disponível na conta, operação inválida!")
        elif valor < 0:
            print("Valores negativos não são aceitos, operação inválida!")
        elif valor == 0:
            print("Saque nulo, operação inválida!")
        else:
            saldo -= valor
            numero_saques += 1
            extrato += (f"Saque: R${valor:.2f}\n")
            print("Saque realizado com sucesso!") 
    else:
        print("Numero máximo de saques diários já atingido, não é possível prosseguir com a operação!")
    return saldo, extrato, numero_saques
def gerar_extrato(saldo,/,*,extrato):
    print("============EXTRATO============\n")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo Atual: {saldo:.2f}")
    print("===============================")
def criar_usuario(usuarios):
    cpf = input("Insira seu CPF:")
    if exibir_usuario(usuarios,cpf):
        print("Cpf já registrado no sistema, operação inválida!")
        return
    nome = input("Insira seu nome: ")
    data_nascimento = input("Insira a data de nascimento, no formato (dd-mm-aaaa): ")
    logradouro, numero, bairro, cidade, estado = input("Insira seu endereço, na ordem ->logradouro, numero, bairro, cidade e sigla do estado: ").split()
    endereco = (f"{logradouro}, {numero} - {bairro} - {cidade}/{estado}")
    usuario = {"cpf": cpf, "nome": nome, "data_nascimento": data_nascimento, "endereco":endereco}
    usuarios.append(usuario)
    print ("Usuário criado com sucesso!")
def exibir_usuario(usuarios,cpf_novo):
    for usuario in usuarios:    
        if usuario["cpf"] == cpf_novo:
            return usuario
    return None
def criar_conta(contas,usuarios):
    numero = len(contas) + 1 
    agencia = "0001"
    cpf = input("Insira seu cpf: ")
    usuario = exibir_usuario(usuarios,cpf)
    if not usuario:
        print("Usuario não registrado, operação inválida!")
        return
    conta = {"numero":numero, "agencia":agencia,"usuario": usuario}
    contas.append(conta)
    print("Conta registrada com sucesso!")
def listar_contas(contas):
    print("=========CONTAS=========")
    for conta in contas:
        listagem = f'''
Agência: {conta["agencia"]}
Número: {conta["numero"]}
Usuário: {conta["usuario"]["nome"]}
        '''
        print(listagem)
    print("========================")
def listar_usuarios(usuarios):
    print("========USUÁRIOS========")
    for usuario in usuarios:
        listagem = f'''
CPF: {usuario["cpf"]}
Nome: {usuario["nome"]}
Data de nascimento: {usuario["data_nascimento"]}
Endereço: {usuario["endereco"]}
        '''
        print(listagem)
    print("========================")



menu = """
==========MENU==========
[d] Depositar
[s] Sacar
[e] Extrato
[u] Criar Usuário
[c] Criar Conta
[lu] Listas Usuários
[lc] Listar Contas
[q] Sair
========================
=>"""

saldo = 0
limite = 500.0
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
usuarios = []
contas = []


while True:
    opcao = input(menu)
    if opcao.isalpha():
        opcao = opcao.lower()
    
    if opcao == "d":
        saldo, extrato = depositar(saldo, extrato)
    elif opcao == "s":
        saldo,extrato, numero_saques = sacar(saldo = saldo, extrato = extrato, limite = limite, numero_saques= numero_saques, LIMITE_SAQUES= LIMITE_SAQUES)
    elif opcao == "e":
        gerar_extrato(saldo, extrato=extrato)
    elif opcao == "u":
        criar_usuario(usuarios)
    elif opcao == "c":
        criar_conta(contas, usuarios)
    elif opcao == "lu":
        listar_usuarios(usuarios)
    elif opcao == "lc":
        listar_contas(contas)
    elif opcao == "q":
        print("Obrigado por utilizar nosso sitema!")
        print("Saindo...")
        break
    else:
        print("Operacao inválida, por favor selecione novamente a operação desejada.")