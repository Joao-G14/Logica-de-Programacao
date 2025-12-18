while True: 
 homem1 = int(input("Escreva a idade de um homem: "))
 homem2 = int(input("Escreva uma idade diferente de outro homem:"))
 mulher1 =int(input("Escreva a idade de uma mulher: "))
 mulher2= int(input("Escreva uma idade diferente de outra mulher:"))

 if homem1 < homem2 and mulher1 < mulher2:
    print(f"Essa é a soma da idade do homem mais velho com a mulher mais nova: {homem2 + mulher1}")
    print(f"Essa é a soma de idade do homem mais novo com a mulher mais velha: {homem1+ mulher2}")
 elif homem1 > homem2 and mulher1 > mulher2:
    print(f"Essa é a soma da idade do homem mais velho com a mulher mais nova: {homem1 + mulher2}")
    print(f"Essa é a soma de idade do homem mais novo com a mulher mais velha: {homem2+ mulher1}")
 elif homem1 < homem2 and mulher1 > mulher2:
    print(f"Essa é a soma da idade do homem mais velho com a mulher mais nova: {homem2 + mulher2}")
    print(f"Essa é a soma de idade do homem mais novo com a mulher mais velha: {homem1+ mulher1}")   
 elif homem1 > homem2 and mulher1 < mulher2:
    print(f"Essa é a soma da idade do homem mais velho com a mulher mais nova: {homem1 + mulher1}")
    print(f"Essa é a soma de idade do homem mais novo com a mulher mais velha: {homem2+ mulher2}")     
    
 if homem1 == homem2 or mulher1 == mulher2:
     print("Idade Invalida, escreva Idades diferentes!")
 else:
     break   
 
    

