salario = int(input("Salario Atual: "))
reajuste = float(input("porcentualdereajuste: "))

novosalario = salario * (1 + reajuste/100)

print("Novo salario:",novosalario)