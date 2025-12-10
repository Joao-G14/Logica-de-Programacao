custo = int(input("Custo de Fabrica: "))

percentualDistribuidor = 28
percentualImpostos = 45

custoFinal = custo * (1 + percentualDistribuidor/100 + percentualImpostos)

print(f"Custo final do consumidor:{custoFinal}")

