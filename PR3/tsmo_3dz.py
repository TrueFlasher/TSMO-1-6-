import math
import matplotlib.pyplot as plt
import numpy as np

def calculate_smo_exact(lambda_rate, mu_rate, num_channels):
    """Рассчитывает параметры СМО для заданного числа каналов."""
    if lambda_rate >= mu_rate * num_channels:
        raise ValueError("Система нестабильна: λ >= μ * количество каналов")

    rho = lambda_rate / mu_rate
    # Вероятность, что система свободна (p0)
    p0_inv = sum((rho**n / math.factorial(n)) for n in range(num_channels)) + \
             ((rho**num_channels / math.factorial(num_channels)) * (1 / (num_channels - rho)))
    p0 = 1 / p0_inv

    # Вероятность отказа (π)
    p_reject = (rho**num_channels / math.factorial(num_channels)) * (1 / (num_channels - rho)) * p0

    # Вероятность обслуживания (Q)
    Q = 1 - p_reject

    # Эффективная интенсивность
    lambda_eff = lambda_rate * Q

    # Коэффициент занятости каналов
    k_busy = lambda_eff / (num_channels * mu_rate)

    # Среднее число заявок в очереди
    L_queue = (rho**(num_channels + 1) / (math.factorial(num_channels) * (num_channels - rho)**2)) * p0

    # Среднее время ожидания
    W_queue = L_queue / lambda_eff

    # Среднее число заявок в системе
    L_system = L_queue + lambda_eff / mu_rate

    # Среднее время пребывания в системе
    W_system = W_queue + 1 / mu_rate

    return {
        "Свободная система (p0)": p0,
        "Вероятность отказа (π)": p_reject,
        "Вероятность обслуживания (Q)": Q,
        "Эффективная интенсивность (λ′)": lambda_eff,
        "Занятость каналов (k)": k_busy,
        "Среднее число заявок в очереди (L)": L_queue,
        "Среднее время ожидания (W)": W_queue,
        "Среднее число заявок в системе (L_system)": L_system,
        "Среднее время в системе (W_system)": W_system
    }

def plot_results_surface(lambda_rate, mu_rate, max_channels):
    """Визуализация результатов в 3D."""
    results = {
        "channels": [],
        "Q": [],
        "L": [],
        "W": [],
        "L_system": [],
        "k": [],
        "W_system": []
    }

    for num_channels in range(1, max_channels + 1):
        try:
            metrics = calculate_smo_exact(lambda_rate, mu_rate, num_channels)
            results["channels"].append(num_channels)
            results["Q"].append(metrics["Вероятность обслуживания (Q)"])
            results["L"].append(metrics["Среднее число заявок в очереди (L)"])
            results["W"].append(metrics["Среднее время ожидания (W)"])
            results["L_system"].append(metrics["Среднее число заявок в системе (L_system)"])
            results["k"].append(metrics["Занятость каналов (k)"])
            results["W_system"].append(metrics["Среднее время в системе (W_system)"])
        except ValueError:
            break

    # Построение графиков
    fig, axes = plt.subplots(2, 3, figsize=(18, 12), subplot_kw={'projection': '3d'})
    axes = axes.flatten()

    for idx, (key, title) in enumerate(zip(["Q", "L", "W", "L_system", "k", "W_system"],
                                           ["Вероятность обслуживания (Q)",
                                            "Среднее число заявок в очереди (L)",
                                            "Среднее время ожидания (W)",
                                            "Среднее число заявок в системе (L_system)",
                                            "Коэффициент занятости (k)",
                                            "Среднее время в системе (W_system)"])):
        ax = axes[idx]
        ax.plot(results["channels"], results[key], zs=0, zdir='z', label=key)
        ax.set_title(title, fontsize=12)
        ax.set_xlabel("Число каналов")
        ax.set_ylabel(title)

    plt.tight_layout()
    plt.show()

# Пример использования
lambda_rate = 2
mu_rate = 4
num_channels = 3

try:
    results = calculate_smo_exact(lambda_rate, mu_rate, num_channels)
    print("Результаты расчета для заданного количества каналов:")
    for key, value in results.items():
        print(f"{key}: {value:.4f}")
except ValueError as e:
    print(e)

plot_results_surface(lambda_rate, mu_rate, max_channels=10)
