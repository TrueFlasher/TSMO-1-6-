import numpy as np
import matplotlib.pyplot as plt

def calculate_metrics(lambda_rate, m_values, t_ob_values):
    """Вычисляет ключевые метрики системы массового обслуживания."""
    mu_values = 1 / (t_ob_values / 60)
    M, T_ob = np.meshgrid(m_values, t_ob_values)
    Mu = 1 / (T_ob / 60)
    chi = lambda_rate / Mu

    P_otk = (chi ** (M + 1)) / np.sum([chi ** i for i in range(M.max() + 1)], axis=0)
    Q = 1 - P_otk
    A = Q * lambda_rate
    L = np.where(chi < 1, chi ** 2 / (1 - chi), np.nan)

    return M, T_ob, Q, A, L

def display_selected_metrics(m_values, t_ob_values, Q, A, L, selected_m, selected_t_ob):
    """Выводит выбранные метрики системы для заданных параметров."""
    m_idx = np.abs(m_values - selected_m).argmin()
    t_ob_idx = np.abs(t_ob_values - selected_t_ob).argmin()

    selected_Q = Q[t_ob_idx, m_idx]
    selected_A = A[t_ob_idx, m_idx]
    selected_L = L[t_ob_idx, m_idx]

    print(f"Для m = {selected_m}, t_об = {selected_t_ob} сек:")
    print(f"Относительная пропускная способность (Q): {selected_Q:.4f}")
    print(f"Абсолютная пропускная способность (A): {selected_A:.4f} заявок/мин")
    print(f"Средняя длина очереди (L): {selected_L:.4f}")

def plot_results(M, T_ob, Q, A, L):
    """Создает графики для визуализации ключевых метрик."""
    fig = plt.figure(figsize=(15, 10))

    ax1 = fig.add_subplot(131, projection='3d')
    ax1.plot_surface(M, T_ob, Q, cmap='viridis', edgecolor='k')
    ax1.set_title("Относительная пропускная способность (Q)")
    ax1.set_xlabel("m (места в очереди)")
    ax1.set_ylabel("t_об (секунды)")
    ax1.set_zlabel("Q")

    ax2 = fig.add_subplot(132, projection='3d')
    ax2.plot_surface(M, T_ob, A, cmap='plasma', edgecolor='k')
    ax2.set_title("Абсолютная пропускная способность (A)")
    ax2.set_xlabel("m (места в очереди)")
    ax2.set_ylabel("t_об (секунды)")
    ax2.set_zlabel("A")

    ax3 = fig.add_subplot(133, projection='3d')
    ax3.plot_surface(M, T_ob, L, cmap='coolwarm', edgecolor='k')
    ax3.set_title("Средняя длина очереди (L)")
    ax3.set_xlabel("m (места в очереди)")
    ax3.set_ylabel("t_об (секунды)")
    ax3.set_zlabel("L")

    plt.tight_layout()
    plt.show()

# Основной блок программы
lambda_rate = 4
m_values = np.arange(2, 101)
t_ob_values = np.linspace(10, 250, 100)

# Расчеты
M, T_ob, Q, A, L = calculate_metrics(lambda_rate, m_values, t_ob_values)

# Вывод метрик для выбранных параметров
selected_m = 10
selected_t_ob = 120
display_selected_metrics(m_values, t_ob_values, Q, A, L, selected_m, selected_t_ob)

# Построение графиков
plot_results(M, T_ob, Q, A, L)
