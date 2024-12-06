def f(x):
    return x**2 + 3*x + 2


def derivative(f, x, h=1e-5):
    return (f(x + h) - f(x)) / h

x_value = 2

derivative_at_x = derivative(f, x_value)

print(f"The derivative of f(x) = x^2 + 3x + 2 at x = {x_value} is: {derivative_at_x}")
