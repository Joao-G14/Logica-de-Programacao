valormaior = 0
valormenor= 11


for i in range(1,11):
   i = int(input("digite um valor: "))
   
   if i > valormaior:
       valormaior = i
       
   if i < valormenor:
       valormenor = i
       
print("o valor menor é:", valormenor)
print("o valor maior é: ", valormaior)       