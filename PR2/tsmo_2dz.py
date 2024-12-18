import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Исходные данные
lambda_rate = 2.4  # Интенсивность потока клиентов
mu_rate = 3.0       # Интенсивность обслуживания
work_duration = 6   # Рабочие часы мастера

# Расчеты для одного мастера
load_intensity = lambda_rate / mu_rate
idle_probability = 1 - load_intensity
average_queue_length = (load_intensity**2) / (1 - load_intensity)
average_queue_time = average_queue_length / lambda_rate
average_system_time = average_queue_time + (1 / mu_rate)

active_hours = load_intensity * work_duration
clients_handled = active_hours * mu_rate
gross_revenue_per_master = clients_handled * 60
net_income_per_master = gross_revenue_per_master * 0.3

# Общие расчеты для двух мастеров
gross_revenue_parlor = gross_revenue_per_master * 2
net_income_parlor = net_income_per_master * 2

# Вывод результатов
print("Результаты для одного мастера:")
print(f"Нагрузка мастера (ρ): {load_intensity:.2f}")
print(f"Вероятность простоя мастера (P0): {idle_probability:.2f}")
print(f"Среднее число клиентов в очереди (L_queue): {average_queue_length:.2f}")
print(f"Среднее время ожидания в очереди (T_queue): {average_queue_time:.2f} минут")
print(f"Среднее время пребывания клиентов в системе (T_system): {average_system_time:.2f} минут")
print(f"Рабочее время мастера: {active_hours:.2f} ч")
print(f"Обслуженные клиенты: {clients_handled:.2f}")
print(f"Общая выручка мастера: {gross_revenue_per_master:.2f} руб")
print(f"Чистый доход мастера: {net_income_per_master:.2f} руб")

print("\nРезультаты для парикмахерской (два мастера):")
print(f"Общая выручка парикмахерской: {gross_revenue_parlor:.2f} руб")
print(f"Суммарный чистый доход мастеров: {net_income_parlor:.2f} руб")

# Построение графиков
lambda_vals = np.linspace(1.5, 3.5, 50)
mu_vals = np.linspace(2.5, 4.5, 50)
lambda_mesh, mu_mesh = np.meshgrid(lambda_vals, mu_vals)

rho_mesh = lambda_mesh / mu_mesh
rho_mesh[rho_mesh >= 1] = np.nan

queue_lengths = (rho_mesh**2) / (1 - rho_mesh)
queue_times = queue_lengths / lambda_mesh
system_times = queue_times + (1 / mu_mesh)

# Создание одного окна с несколькими графиками
fig = plt.figure(figsize=(15, 12))

# График интенсивности нагрузки
ax1 = fig.add_subplot(221, projection='3d')
ax1.plot_surface(lambda_mesh, mu_mesh, rho_mesh, cmap='viridis', edgecolor='none')
ax1.set_title('(ρ)', fontsize=14)
ax1.set_xlabel('(клиентов/ч)', fontsize=12)
ax1.set_ylabel('(клиентов/ч)', fontsize=12)
ax1.set_zlabel('ρ (нагрузка)', fontsize=12)

# График средней длины очереди
ax2 = fig.add_subplot(222, projection='3d')
ax2.plot_surface(lambda_mesh, mu_mesh, queue_lengths, cmap='plasma', edgecolor='none')
ax2.set_title('(L_queue)', fontsize=14)
ax2.set_xlabel('(клиентов/ч)', fontsize=12)
ax2.set_ylabel('(клиентов/ч)', fontsize=12)
ax2.set_zlabel('L_queue (клиенты)', fontsize=12)

# График среднего времени ожидания
ax3 = fig.add_subplot(223, projection='3d')
ax3.plot_surface(lambda_mesh, mu_mesh, queue_times, cmap='coolwarm', edgecolor='none')
ax3.set_title('(T_queue)', fontsize=14)
ax3.set_xlabel('(клиентов/ч)', fontsize=12)
ax3.set_ylabel('(клиентов/ч)', fontsize=12)
ax3.set_zlabel('T_queue (мин)', fontsize=12)

# График среднего времени пребывания
ax4 = fig.add_subplot(224, projection='3d')
ax4.plot_surface(lambda_mesh, mu_mesh, system_times, cmap='inferno', edgecolor='none')
ax4.set_title('(T_system)', fontsize=14)
ax4.set_xlabel('(клиентов/ч)', fontsize=12)
ax4.set_ylabel('(клиентов/ч)', fontsize=12)
ax4.set_zlabel('T_system (мин)', fontsize=12)

plt.tight_layout()
plt.show()
