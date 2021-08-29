import numpy as np
import matplotlib.pyplot as plt
import sympy
import random

x, y, z = sympy.symbols('x y z')
sympy.init_printing(use_unicode=True)
equation = (sympy.sin(10 * sympy.pi * x) / (2 * x)) + (x - 1) ** 4
diff = sympy.diff(equation, x)

eq = lambda t: equation.subs(x,t).evalf()
df = lambda t: diff.subs(x,t).evalf()

def plot(xdata, title):
    z = np.arange(0.5, 2.5, 0.01)
    
    def f(z):
        y = (np.sin(10 * np.pi * z) / (2 * z)) + (z - 1) ** 4
        return y

    ydata = []
    for d in xdata:
        ydata.append(equation.subs(x,d).evalf())

    startX = xdata.pop(0)
    startY = ydata.pop(0)
    endX = xdata.pop(-1)
    endY = ydata.pop(-1)

    # Create the plot
    plt.plot(z,f(z),label = 'y = (sin(10 * pi * x) / (2 * x)) + (x - 1) ** 4')
    plt.scatter(xdata,ydata,label = 'way')
    plt.scatter(startX,startY,label = 'start', c = "red")
    plt.scatter(endX,endY,label = 'end', c = "green")

    plt.title(title)
    plt.legend()

    plt.show()

def hillClimbing(start):
    current = start
    rate = 0.001
    precision = 0.0001
    points = []

    while (True):
        points.append(current)
        gradient = df(current)
        if (abs(gradient) <= precision):
            return points
        elif (gradient > 0):
            current -= rate * abs(gradient)
        elif(gradient < 0):
            current += rate * abs(gradient)
        
        print("x: ", current, "m: ", gradient)

def iterative(n):
    points = []
    i = 0
    minimum = 1000000
    best = []
    while (i < n):
        point = random.uniform(0.5, 2.5)
        if (point not in points):
            points.append(point)
            results = hillClimbing(point)
            y = eq(results[-1])
            if (y < minimum):
                minimum = y
                best = results[:]
            i += 1
            plot(results, "iterate: {}".format(i))
    return best

def simulatedAnnealing(start):
    domain = (0.5,2.5)
    jump = 0.1
    schedule = 64
    acceptance = 0.8
    current = start
    rate = 0.001
    precision = 0.0001
    points = []

    while (True):
        rand = random.randint(0, 100)

        points.append(current)
        gradient = df(current)

        if (abs(gradient) <= precision):
            return points
        elif (gradient > 0):
            if (rand > schedule):
                current -= rate * abs(gradient)
            else:
                tmp = current + jump
                if (tmp > domain[1]):
                    current = domain[1]
                else:
                    current = tmp

        elif(gradient < 0):
            if (rand > schedule):
                current += rate * abs(gradient)
            else:
                tmp = current - jump
                if (tmp < domain[0]):
                    current = domain[0]
                else:
                    current = tmp

        schedule *= acceptance
        
        print("x: ", current, "m: ", gradient)



data = hillClimbing(random.uniform(0.5, 2.5))
plot(data, "Hill Climbing")

data = iterative(10)
plot(data, "iterative final result")

data = simulatedAnnealing(random.uniform(0.5, 2.5))
plot(data, "simulated annealing")