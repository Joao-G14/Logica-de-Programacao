
codigodeusuario = int(input("Digite o Codigo de Usuario: "))

while codigodeusuario != 1234:
    print("Codigo de Usuario Invalido")
    codigodeusuario = int(input("Digite o Codigo de Usuario: "))
    
if codigodeusuario == 1234:
    senha = int(input("Digite a Senha: "))

while senha != 9999:
    print("Senha incorreta.")
    senha = int(input("Digite a Senha: "))
    
    if senha == 9999:
        print("Acesso Liberado!")
    
                