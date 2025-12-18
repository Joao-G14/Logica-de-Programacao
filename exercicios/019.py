def classificar_idade(idade):
    if idade >= 5 and idade <= 7:
        return "Infantil A"
    elif idade >= 8 and idade <= 10:
        return "Infantil B"
    elif idade >= 11 and idade <= 13:
        return "Juvenil A"
    elif idade >= 14 and idade <= 17:
        return "Juvenil B"
    elif idade >= 18:
        return "Maiores de 18 anos(Adulto)"
    else:
        return None
    
while True:
    idade = int(input("Digite a idade do nadador: "))
    
    
    
    if classificar_idade(idade) is None:
        print("Idade invalida, digite a idade novamente!")
    else:
        break

print(f"Sua classificaça é: {classificar_idade(idade)}")
                
    