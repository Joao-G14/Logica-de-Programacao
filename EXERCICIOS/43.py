peso = float(input("digite sue peso: "))
altura = float(input("digite sua altura: "))

IMC = peso / (altura**2)
while True:
 if IMC <= 18.5:
    print(f"voce esta abaixo do peso, seu Imc é {IMC}")
 elif IMC >= 18.6 and IMC <= 24.9:
     print(f"peso ideal, Parabens!! seu Imc é {IMC}")
 elif IMC >= 25.0 and IMC <= 29.9:
     print(f"Levemente acima do peso, seu Imc é {IMC}")
 elif IMC >= 30.0 and IMC <= 34.9:
    print(f"Obesidade grau 1, seu Imc é {IMC}")
 elif IMC >= 35.0 and IMC <= 39.9:
    print(f"Obesidade grau 2, seu Imc é {IMC}")
 elif IMC <= 0:
    print("valor do IMC invalido")
 else:
    print("obesidade grau 3(Mórbida)")
 break
    
 