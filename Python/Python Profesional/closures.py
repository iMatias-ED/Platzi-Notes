def word_multiplier(word: str):
    def multiply(n: int):
        return word * n

    return multiply

hola = word_multiplier("hola")

print(hola(5))