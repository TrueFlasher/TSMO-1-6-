import numpy as np
from sympy import symbols, Eq, solve
import matplotlib.pyplot as plt

def calculate_steady_state_probabilities(rate_params):
    """
    Рассчитывает предельные вероятности для заданных коэффициентов перехода.
    """
    # Извлечение параметров из словаря
    lambda_01 = rate_params['lambda_01']
    lambda_02 = rate_params['lambda_02']
    lambda_10 = rate_params['lambda_10']
    lambda_13 = rate_params['lambda_13']
    lambda_20 = rate_params['lambda_20']
    lambda_23 = rate_params['lambda_23']
    lambda_31 = rate_params['lambda_31']
    lambda_32 = rate_params['lambda_32']

    # Матрица коэффициентов для уравнений баланса
    transition_matrix = np.array([
        [lambda_01 + lambda_02, -lambda_10, -lambda_20, 0],
        [-lambda_01, lambda_10 + lambda_13, 0, -lambda_31],
        [-lambda_02, 0, lambda_20 + lambda_23, -lambda_32],
        [0, -lambda_13, -lambda_23, lambda_31 + lambda_32]
    ])

    # Добавление уравнения нормировки
    transition_matrix = np.vstack([transition_matrix, np.ones(4)])
    b = np.array([0, 0, 0, 0, 1])

    # Решение системы уравнений методом наименьших квадратов
    probabilities = np.linalg.solve(transition_matrix.T @ transition_matrix, transition_matrix.T @ b)

    return np.round(probabilities, 2)

def calculate_and_plot_income(rate_params):
    """
    Рассчитывает и отображает средний доход для исходных и скорректированных условий.
    """
    # Определение символов для решения системы уравнений
    p0, p1, p2, p3 = symbols('p0 p1 p2 p3')

    # Развёртка параметров
    lambda_01, lambda_02 = rate_params['lambda_01'], rate_params['lambda_02']
    lambda_10, lambda_13 = rate_params['lambda_10'], rate_params['lambda_13']
    lambda_20, lambda_23 = rate_params['lambda_20'], rate_params['lambda_23']
    lambda_31, lambda_32 = rate_params['lambda_31'], rate_params['lambda_32']

    # Уравнения баланса вероятностей
    equations = [
        Eq((lambda_01 + lambda_02) * p0, lambda_10 * p1 + lambda_20 * p2),
        Eq((lambda_10 + lambda_13) * p1, lambda_01 * p0 + lambda_31 * p3),
        Eq((lambda_20 + lambda_23) * p2, lambda_02 * p0 + lambda_32 * p3),
        Eq(p0 + p1 + p2 + p3, 1)
    ]

    # Решение системы уравнений
    solution = solve(equations, (p0, p1, p2, p3))
    rounded_solution = {var: round(val.evalf(), 2) for var, val in solution.items()}

    # Скорректированные параметры (увеличенное время ремонта)
    adjusted_params = {key: (val * 2 if '20' in key or '31' in key else val) for key, val in rate_params.items()}
    adjusted_equations = [
        Eq((adjusted_params['lambda_01'] + adjusted_params['lambda_02']) * p0, adjusted_params['lambda_10'] * p1 + adjusted_params['lambda_20'] * p2),
        Eq((adjusted_params['lambda_10'] + adjusted_params['lambda_13']) * p1, adjusted_params['lambda_01'] * p0 + adjusted_params['lambda_31'] * p3),
        Eq((adjusted_params['lambda_20'] + adjusted_params['lambda_23']) * p2, adjusted_params['lambda_02'] * p0 + adjusted_params['lambda_32'] * p3),
        Eq(p0 + p1 + p2 + p3, 1)
    ]

    adjusted_solution = solve(adjusted_equations, (p0, p1, p2, p3))
    adjusted_solution_rounded = {var: round(val.evalf(), 2) for var, val in adjusted_solution.items()}

    # Расчёт среднего дохода
    income_values = [10, 6]
    repair_costs = [4, 2]

    def compute_income(solution_probs, repair_multiplier=1):
        node1_working = solution_probs[p0] + solution_probs[p2]
        node2_working = solution_probs[p0] + solution_probs[p1]
        node1_repairing = solution_probs[p1] + solution_probs[p3]
        node2_repairing = solution_probs[p2] + solution_probs[p3]
        return round(
            node1_working * income_values[0] +
            node2_working * income_values[1] -
            node1_repairing * (repair_costs[0] * repair_multiplier) -
            node2_repairing * (repair_costs[1] * repair_multiplier), 2
        )

    original_income = compute_income(rounded_solution)
    adjusted_income = compute_income(adjusted_solution_rounded, repair_multiplier=2)

    # Вывод результатов и построение графика
    print(f"Средний доход (исходные параметры): {original_income}")
    print(f"Средний доход (скорректированные параметры): {adjusted_income}")

    plt.bar(['Исходные', 'Скорректированные'], [original_income, adjusted_income], color=['blue', 'green'])
    plt.title('Средний доход в разных условиях')
    plt.ylabel('Доход (ден. ед.)')
    plt.show()

# Основной блок
default_rates = {
    'lambda_01': 1, 'lambda_02': 2, 'lambda_10': 2, 'lambda_13': 2,
    'lambda_20': 3, 'lambda_23': 1, 'lambda_31': 3, 'lambda_32': 2
}


steady_state_probs = calculate_steady_state_probabilities(default_rates)
print("Предельные вероятности:", steady_state_probs)

calculate_and_plot_income(default_rates)
