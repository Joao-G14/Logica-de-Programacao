while True:
 valor1 = int(input("Insira um valor: "))
 valor2 = int(input("Insira um segundo valor: "))
 valor3 = int(input("Insira um terceiro valor: "))

 if valor1 and valor2 > valor3:
   print(f"A soma dos maiores valores é: {valor1 + valor2}")
 elif valor2 and valor3 > valor1:
    print(f"A soma dos maiores valores é: {valor2 + valor3}")
 elif valor1 and valor3 > valor2:
    print(f"A soma dos maiores valores é {valor1 + valor3}")   
    
 if valor1 == valor2 == valor3:   
  print("os valores sao iguais, digite novamente os valores!")
 else:
     break 
    