litros = int(input("Digite quantos litros: "))
combustivel = input("Digite o tipo de combustivel: ")

total = 0

if combustivel == "Alcool":
    total = litros * 2.20

    if litros <= 20:
        total -= 0.3
    else:
        total -= 0.4
        
if combustivel == "Gasolina":
    total = litros * 3.30

    if litros <= 20:
        total -= 0.6
    else:
        total -= 0.5

print(f"o total a pagar é {total}R$")
