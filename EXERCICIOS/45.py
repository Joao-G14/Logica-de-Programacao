nome = input("Digite seu noeme: ") 
idade = int(input("Digite sua idade: "))

if idade >= 18:
    print(f"seu nome é {nome} e voce é maior de idade")
elif idade <= 0:
    print("idade invalida")
else:
    print(f"seu nome é {nome} e voce é menor de idade")