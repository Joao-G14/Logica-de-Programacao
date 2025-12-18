horastrabalhadas = int(input("Horas trabalhadas: "))
salario = int(input("Salario por Hora: "))
regulares = 160

if horastrabalhadas <= regulares:
    total = horastrabalhadas * salario
else:
    extras = horastrabalhadas - regulares
    valorextra = salario * 1.5
    total = (regulares * salario) + (extras * valorextra)
    
print(f"Salario total: {total}")

