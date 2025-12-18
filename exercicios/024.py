cont2 = 0
cont = 0

while True:
    valor = int(input("Digite um número positivo (ou coloque um numero negativo para terminar): "))
    if valor < 0:  
         break

    else:
     cont += valor
     cont2 += 1
     
     
media = cont/cont2 
print(f"A media dos valores digitos é {media}")