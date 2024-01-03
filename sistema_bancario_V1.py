# Sistema simples de banco, com 3 operações: depósito, saque e extrato, criado para seguir o curso Formação Python Developer, da DIO
# Por ser um sistema sistema, foram ignorados alguns problemas, como a falta de verificaçao de inputs, pois o objetivo era apenas criar
# uma estrutura básica de um sistema bancário
menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=>"""

saldo = 0
limite = 500.0
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu)
    if opcao.isalpha():
        opcao = opcao.lower()
    
    if opcao == "d":
        valor = float(input("Insira o valor do depósito: "))
        if valor <0:
            print("Valores negativos não são aceitos, operação inválida!")
        elif valor == 0:
            print("Depósito nulo, operação inválida!")
        else:
            saldo +=valor
            extrato += (f"Deposito: R${valor:.2f}\n")
            print("Deposito realizado com sucesso!")
    elif opcao == "s":
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

    elif opcao == "e":
        print("============EXTRATO============\n")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo Atual: {saldo:.2f}")
        print("===============================")

    elif opcao == "q":
        print("Obrigado por utilizar nosso sitema!")
        print("Saindo...")
        break
    else:
        print("Operacao inválida, por favor selecione novamente a operação desejada.")