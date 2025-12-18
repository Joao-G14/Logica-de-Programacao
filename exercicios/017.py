def classificar_nota(nota):
    if 0.0 <= nota <= 4.9:
        return "D"
    elif 5.0 <= nota <= 6.9:
        return "C"
    elif 7.0 <= nota <= 8.9:
        return "B"
    elif 9.0 <= nota <= 10.0:
        return "A"
    else:
        return None  # nota inválida
