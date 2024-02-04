import math
import random


class Area:
    
    __bounds = list()
    
    def add_bound(self, function):
        """
        Receives a function that returns a boolean, indicating
        that a point (x, y) is valid or not.
        """
        self.__bounds.append(function)

    def check(self, x, y):
        """
        Check if a point (x, y) is inside the area.
        """
        for function in self.__bounds:
            if not function(x, y):
                return False
        return True


def monte_carlo_method(area, width, height, n_samples = 10**6):
    """
    Calculate the size of an area by applying the Monte Carlo method.
    """
    
    results = [0, 0]  # total of (not_valid_points, valid_points)

    for sample in range(n_samples):
        x = random.randint(0, width)
        y = random.randint(0, height)

        results[int(area.check(x, y))] += 1

    total = results[0] + results[1]
    total_area = width * height
    
    return total_area * (results[1] / total)
    

if __name__ == "__main__":
    screen = 200, 200

    f1 = lambda x, y: math.sin(x/50)*50 + 50 >= y
    f2 = lambda x, y: math.sin(x/50)*50 * -1 + 50 <= y

    area = Area()
    area.add_bound(f1)
    area.add_bound(f2)

    n_samples = 10 ** 6

    print("Testing...")

    print("Area =", monte_carlo_method(area, *screen, n_samples))
