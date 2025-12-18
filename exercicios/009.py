numerocliente =int(input("Digite o numero da conta do cliente: "))
saldo = float(input("Digite o seu saldo: "))
debito = float(input("Dgite o se Debito: "))
credito = float(input("Digite o seu Credito: "))

saldoAtual = saldo-debito+credito

if saldoAtual >= 0:
    print("Saldo Positivo!")
else:
    print("Saldo negativo!")