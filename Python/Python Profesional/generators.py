from time import sleep

def fibonacciGenerator(_max: int):
    number_1 = 0
    number_2 = 1
    next_fb = 0
    while True:
        if next_fb == 0: 
            next_fb += 1
            yield 0
            continue

        next_fb = number_1 + number_2
        number_1, number_2 = number_2, next_fb

        if next_fb > _max: break
        yield next_fb

fb = fibonacciGenerator(21)
for n in fb:
    print(n)
    sleep(0.5)
