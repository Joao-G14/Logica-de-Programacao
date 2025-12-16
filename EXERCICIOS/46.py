a = int(input("Digite o valor do primeiro lado do triangulo: "))
b = int(input("Digite o valor do segundo lado do triangulo: "))
c = int(input("Digite o valor do terceiro lado do triangulo: "))

if a == b == c:
    print("triangulo equilatero")
elif a == b != c:
    print("triangulo isosceles")
elif a != b != c:
    print("triangulo escaleno")
elif a < 0 or b < 0 or c < 0:
    print("vlores invalidos!")
else:
    print("valores invalidos!")
    
