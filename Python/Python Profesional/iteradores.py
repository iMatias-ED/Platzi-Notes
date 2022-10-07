from time import sleep

class FibonacciIterator:
    def __init__(self, max: int):
        self._max = max

    def __iter__(self):
        self.number_1: int = 0
        self.number_2: int = 1
        self.next_fb: int = 0

        return self;

    def __next__(self) -> int:
        if self.next_fb == 0: 
            self.next_fb += 1 
            return 0;

        self.next_fb = self.number_1 + self.number_2
        self.number_1, self.number_2 = self.number_2, self.next_fb

        if self.next_fb > self._max: raise StopIteration
        return self.next_fb

fibonacci_numbers = FibonacciIterator(21)
for number in fibonacci_numbers:
    print(number)
    sleep(0.5)
