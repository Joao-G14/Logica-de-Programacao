while True:
 nota = float(input("Digite a nota do Aluno: "))

 if nota >= 0.0 and nota <= 4.9:
    print("Sua Media final é D!")
 elif nota >= 5.0 and nota <=6.9:
    print("Sua Media final é C!")
 elif nota >= 7.0 and nota <=8.9:
    print("Sua Media final é B!")
 elif nota >= 9.0 and nota <=10.0:
    print("Sua Media final é A!")    

 if nota < 0.0 or nota > 10.0:
    print("Nota invalida")
 else:
     break