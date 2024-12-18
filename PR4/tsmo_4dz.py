import matplotlib.pyplot as plt

def get_input_with_default(prompt: str, default: float) -> float:
    """Получает ввод от пользователя с использованием значения по умолчанию."""
    user_input = input(prompt)
    return float(user_input) if user_input else default

def calculate_metrics(lambda_1, lambda_2, t_obsl_1, t_obsl_2):
    """Выполняет расчет метрик системы приоритезации."""
    mu_1 = 1 / t_obsl_1
    mu_2 = 1 / t_obsl_2

    y1 = lambda_1 / mu_1
    y2 = lambda_2 / mu_2
    y_total = y1 + y2

    t_och_1 = y1 / (mu_1 * (1 - y1))
    t_sist_1 = t_och_1 + t_obsl_1

    t_och_2 = (1 / mu_2) * (((mu_2 / mu_1) * (y1 / (1 - y_total)) + y_total) / (1 - y_total))
    t_sist_2 = t_och_2 + (1 / mu_2)

    return y1, y_total, t_och_1, t_sist_1, t_och_2, t_sist_2

def display_metrics(y1, y_total, t_och_1, t_sist_1, t_och_2, t_sist_2):
    """Выводит результаты расчета на экран."""
    print(f"\nКоэффициент загрузки первой очереди: {y1:.2f}")
    print(f"Общая загрузка системы: {y_total:.2f}")
    print(f"\nВремя ожидания в очереди (приоритет): {t_och_1:.2f} ч.")
    print(f"Полное время в системе (приоритет): {t_sist_1:.2f} ч.")
    print(f"\nВремя ожидания в очереди (без приоритета): {t_och_2:.2f} ч.")
    print(f"Полное время в системе (без приоритета): {t_sist_2:.2f} ч.")

def plot_comparison(t_och_1, t_sist_1, t_och_2, t_sist_2):
    """Создает столбчатую диаграмму для сравнения метрик."""
    labels = ['Очередь (приоритет)', 'Система (приоритет)', 'Очередь (без приоритета)', 'Система (без приоритета)']
    values = [t_och_1, t_sist_1, t_och_2, t_sist_2]
    plt.bar(labels, values, color=['blue', 'lightblue', 'orange', 'lightcoral'])
    plt.ylabel('Время (ч)')
    plt.title('Сравнение средних времен')
    plt.ylim(0, max(values) + 1)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

# Основной блок программы
lambda_1 = 0.1
lambda_2 = 0.2
t_obsl_1 = 1
t_obsl_2 = 2.5

# Расчет метрик
y1, y_total, t_och_1, t_sist_1, t_och_2, t_sist_2 = calculate_metrics(lambda_1, lambda_2, t_obsl_1, t_obsl_2)

# Отображение результатов
display_metrics(y1, y_total, t_och_1, t_sist_1, t_och_2, t_sist_2)

# Построение графика
plot_comparison(t_och_1, t_sist_1, t_och_2, t_sist_2)