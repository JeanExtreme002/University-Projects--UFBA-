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

    Returns the size of the area and the generated points [out, in].
    """
    
    results = [0, 0]  # total of (not_valid_points, valid_points)
    samples = [([], []), ([], [])]
    
    for sample in range(n_samples):
        x = random.randint(0, width)
        y = random.randint(0, height)
        
        if area.check(x,y):
            samples[1][0].append(x)
            samples[1][1].append(y)
            results[1] += 1
        else:
            samples[0][0].append(x)
            samples[0][1].append(y)
            results[0] += 1

    total = results[0] + results[1]
    total_area = width * height
    
    return total_area * (results[1] / total), samples


if __name__ == "__main__":
    from matplotlib import pyplot as plt
    import numpy as np

    # Bounds of the area.
    screen = 200, 200
    f1 = lambda x, y: math.sin(x/50)*50 + 50 >= y
    f2 = lambda x, y: math.sin(x/50)*50 * -1 + 50 <= y

    # Functions to draw on matplotlib.
    f_1 = lambda x: np.sin(x/50)*50 + 50
    f_2 = lambda x: np.sin(x/50)*50 * -1 + 50

    # Number of samples.
    n_samples = 10 ** 6

    # Creating area...
    area = Area()
    area.add_bound(f1)
    area.add_bound(f2)

    # Calculating...
    area, samples = monte_carlo_method(area, *screen, n_samples)
    print("Area =", area)

    # Plotting...
    x = np.linspace(0, screen[0], screen[0])
    
    plt.plot(x, f_1(x), color='black')
    plt.plot(x, f_2(x), color='black')

    plt.scatter(samples[0][0], samples[0][1], color = 'orange')
    plt.scatter(samples[1][0], samples[1][1], color = 'green')
    
    plt.show()
