valor = float(input("Digite o valor do produto: "))
pagamento = int(input(f"formas de pagamento:\n1 = A vista no dinheiro ou Pix (recebe 15% de desconto)\n2 = A Vista no cartão de crédito (recebe 10% de descont)\n3 = Parcelado no cartão em duas vezes (preço normal do produto sem juros)\n4 = Parcelado no cartão em três vezes ou mais (preço normal do produto mais juros de 10%)\nDigite sua forma de pagamento: "))
total = 0

if pagamento == 1:
    total = valor - (0.15 * valor)
elif pagamento == 2:
    total = valor - (0.10 * valor)
elif pagamento == 3:
    total = valor
elif pagamento == 4:
    total = valor + (0.10 * valor)
else:
    print("Valor invalido")
    
    
print(f"o total a pagar é: {total}R$")