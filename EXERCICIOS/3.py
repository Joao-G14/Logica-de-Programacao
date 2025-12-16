total = int(input("total de eleitore:"))
brancos = int(input("votos brancos: "))
nulos = int(input("votos nulos: "))
validos = int(input("votos validos: "))

percentualBrancos = (brancos * 100)/total
percentualNulos = (nulos * 100)/total
percentualValidos = (validos * 100)/total

print(f"Brancos: {percentualBrancos}%")
print(f"Nulos: {percentualNulos}%")
print(f"Validos: {percentualValidos}%")
