carros = int(input("Numero de Carros vendidos: "))
total = int(input("Valor total de vendas: "))
salario = int(input("Salario Fixo: "))
comissao = int(input("Comissão por carro: "))

comissaototal = (carros * comissao) + (0.05 * total)
salariofinal = salario + comissaototal

print(f"Salario final:{salariofinal}")


