import numpy as np
import sympy as sp

class RootFinder:
    def __init__(self, function):
        self.function = function

    def bisection(self, a, b, tol=1e-5):
        y_a = self.function(a)
        y_b = self.function(b)

        if not y_a * y_b < 0:
            print(f"Нарушены условия разных знаков точек для интервала [{a}, {b}]")
            return None, 0  # Возвращаем 0 итераций

        iterations = 0  # Счетчик итераций
        while (b - a) / 2 > tol:  # Условие остановки по ширине интервала
            c = a + (b - a) / 2
            y_c = self.function(c)
            iterations += 1  # Увеличиваем счетчик итераций

            if y_c == 0:  # Если найден точный корень
                return c, iterations
            elif y_c * y_a < 0:  # Корень находится между a и c
                b = c
                y_b = y_c
            else:  # Корень находится между c и b
                a = c
                y_a = y_c

        return (a + b) / 2, iterations  # Возвращаем среднюю точку и количество итераций

    def find_intervals(self, start, end, step):
        intervals = []
        x = start
        prev_y = self.function(start)

        while x < end:
            x += step
            current_y = self.function(x)
            if prev_y * current_y < 0:  # Если функция меняет знак
                intervals.append((x - step, x))  # Добавляем интервал
            prev_y = current_y

        return intervals

    def find_all_roots(self, start, end, step, tol):
        intervals = self.find_intervals(start, end, step)
        roots = []
        total_iterations = 0  # Счетчик для общего числа итераций

        if not intervals:
            print(f"В заданном диапазоне [{start}, {end}] не найдено подходящих интервалов для поиска корней.")
            return roots, total_iterations

        for a, b in intervals:
            root, iterations = self.bisection(a, b, tol)
            if root is not None:
                roots.append(root)
                total_iterations += iterations  # Суммируем итерации

        return roots, total_iterations

# Функция для преобразования строкового ввода в callable функцию
def create_function(func_str):
    x = sp.symbols('x')
    func_expr = sp.sympify(func_str)
    return sp.lambdify(x, func_expr)

# Ввод функции и отрезка пользователем
func_input = input("Введите функцию от x (например, x**3 - 6*x**2 + 11*x - 6): ")
start = float(input("Введите начало отрезка для поиска корней: "))
end = float(input("Введите конец отрезка для поиска корней: "))

# Создаем функцию из введенной строки
f = create_function(func_input)

root_finder = RootFinder(f)

# Изменяем шаг и tol для наблюдения за количеством итераций
steps = [0.001, 0.0001]
tols = [1e-1, 1e-5, 1e-10, 1e-15]
true_roots = np.array([1, 2, 3])

for step in steps:
    for tol in tols:
        roots, total_iterations = root_finder.find_all_roots(start, end, step, tol)

        # Вычисляем СКО
        if roots:
            differences = true_roots - np.array(roots)
            std_dev = np.std(differences)
            print(
                f"Шаг: {step}, Точность: {tol} => Найденные корни: {roots}, Итерации: {total_iterations}, СКО: {std_dev}")
        else:
            print(f"Шаг: {step}, Точность: {tol} => Корни не найдены.")