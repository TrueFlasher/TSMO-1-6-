import numpy as np
import matplotlib.pyplot as plt
import math

def calculate_probabilities(lambda_rate, t_podg, t_obsl, n):
    """Вычисляет вероятности состояний и ключевые метрики системы."""
    phi = 1 / t_podg
    mu = 1 / t_obsl
    mu_total = (mu * phi) / (mu + phi)
    y = lambda_rate / mu_total

    p_0 = 1 / sum(y**k / math.factorial(k) for k in range(n + 1))
    probabilities = [y**k / math.factorial(k) * p_0 for k in range(n + 1)]

    p_reject = probabilities[-1] * y / n
    Q = 1 - p_reject
    A = lambda_rate * Q
    k_busy = A / mu_total

    return probabilities, p_reject, Q, A, k_busy

def display_results(probabilities, p_reject, Q, A, k_busy):
    """Выводит результаты расчетов на экран."""
    print(f"Вероятности состояний: {probabilities}")
    print(f"Вероятность отказа Pотк: {p_reject:.2f}")
    print(f"Коэффициент использования Q: {Q:.2f}")
    print(f"Абсолютная пропускная способность A: {A:.2f}")
    print(f"Среднее число занятых каналов: {k_busy:.2f}")

def plot_metrics(probabilities, Q, A, n):
    """Создает графики для визуализации вероятностей и метрик."""
    x = np.arange(0, n + 1)
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.bar(x, probabilities, color='blue', alpha=0.7)
    plt.xlabel("Количество занятых каналов")
    plt.ylabel("Вероятность")
    plt.title("Распределение вероятностей состояний")

    plt.subplot(1, 2, 2)
    metrics = ["Q", "A"]
    values = [Q, A]
    plt.bar(metrics, values, color=['green', 'orange'], alpha=0.7)
    plt.title("Эффективность системы")
    plt.ylabel("Значение")

    plt.tight_layout()
    plt.show()

# Основной блок программы
lambda_rate = 0.2
t_podg = 0.5
t_obsl = 2.0
n = 3

# Расчеты
probabilities, p_reject, Q, A, k_busy = calculate_probabilities(lambda_rate, t_podg, t_obsl, n)

# Вывод результатов
display_results(probabilities, p_reject, Q, A, k_busy)

# Построение графиков
plot_metrics(probabilities, Q, A, n)