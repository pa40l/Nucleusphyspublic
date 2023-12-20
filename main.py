import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from nucleus import Nucleon, Simulation
MASS_1=1.67e-27
MASS_2=1.67e-27
INITIAL_POSITION_1="0.0, 0.0"
INITIAL_VELOCITY_1="1e7, 1e-15"
INITIAL_POSITION_2="0.6e-14, 1e-15"
INITIAL_VELOCITY_2="-1e7, 1e-15"
TIME_STEP=1e-25
NUMBER_OF_STEPS=6000
class NuclearSimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Релятивистская динамика")
        self.root.geometry("1060x500")

        # Переменные для ввода данных
        self.mass_proton = tk.DoubleVar(value=MASS_1)
        self.mass_neutron = tk.DoubleVar(value=MASS_2)
        self.initial_position_nucleon1 = tk.StringVar(value=INITIAL_POSITION_1)
        self.initial_velocity_nucleon1 = tk.StringVar(value=INITIAL_VELOCITY_1)
        self.initial_position_nucleon2 = tk.StringVar(value=INITIAL_POSITION_2)
        self.initial_velocity_nucleon2 = tk.StringVar(value=INITIAL_VELOCITY_2)
        self.time_step = tk.DoubleVar(value=TIME_STEP)
        self.num_steps = tk.IntVar(value=NUMBER_OF_STEPS)

        # Размещение элементов GUI
        self.create_input_widgets()
        self.create_plot_widget()

    def create_input_widgets(self):
        input_frame = ttk.Frame(self.root, padding="10")
        input_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Создание меток и полей для ввода данных
        ttk.Label(input_frame, text="Масса протона:").grid(column=0, row=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.mass_proton).grid(column=1, row=0, sticky=tk.W)

        ttk.Label(input_frame, text="Масса нейтрона:").grid(column=0, row=1, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.mass_neutron).grid(column=1, row=1, sticky=tk.W)

        ttk.Label(input_frame, text="Нач. координаты нуклона 1:").grid(column=0, row=2, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.initial_position_nucleon1).grid(column=1, row=2, sticky=tk.W)

        ttk.Label(input_frame, text="Нач. скорость нуклона 1:").grid(column=0, row=3, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.initial_velocity_nucleon1).grid(column=1, row=3, sticky=tk.W)

        ttk.Label(input_frame, text="Нач. координаты нуклона 2:").grid(column=0, row=4, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.initial_position_nucleon2).grid(column=1, row=4, sticky=tk.W)

        ttk.Label(input_frame, text="Нач. скорость нуклона 2:").grid(column=0, row=5, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.initial_velocity_nucleon2).grid(column=1, row=5, sticky=tk.W)

        ttk.Label(input_frame, text="Шаг по времени:").grid(column=0, row=6, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.time_step).grid(column=1, row=6, sticky=tk.W)

        ttk.Label(input_frame, text="Количество врем. шагов:").grid(column=0, row=7, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.num_steps).grid(column=1, row=7, sticky=tk.W)

        # Кнопка для запуска симуляции
        ttk.Button(input_frame, text="Запустить симуляцию", command=self.run_simulation).grid(column=0, row=8, columnspan=2, pady=10)

    def create_plot_widget(self):
        plot_frame = ttk.Frame(self.root, padding="10")
        plot_frame.grid(column=3, row=0)

        # Создание виджета для отображения графика
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=plot_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.draw()

    def run_simulation(self):
        # Получение данных от пользователя
        mass_proton = self.mass_proton.get()
        mass_neutron = self.mass_neutron.get()
        initial_position_nucleon1 = [float(q) for q in self.initial_position_nucleon1.get().split(",")]
        initial_velocity_nucleon1 = [float(v) for v in self.initial_velocity_nucleon1.get().split(",")]
        initial_position_nucleon2 = [float(q) for q in self.initial_position_nucleon2.get().split(",")]
        initial_velocity_nucleon2 = [float(v) for v in self.initial_velocity_nucleon2.get().split(",")]
        time_step = self.time_step.get()
        num_steps = self.num_steps.get()

        # Инициализация нуклонов
        nucleon1 = Nucleon(mass_proton, initial_position_nucleon1, initial_velocity_nucleon1)
        nucleon2 = Nucleon(mass_neutron, initial_position_nucleon2, initial_velocity_nucleon2)

        # Инициализация симуляции
        simulation = Simulation(nucleon1, nucleon2, time_step)

        # Интеграция уравнений движения
        simulation.integrate(num_steps)

        # Отображение графика
        self.ax.clear()
        self.ax.plot(simulation.nucleon1_positions_x, simulation.nucleon1_positions_y, label='Нуклон 1')
        self.ax.plot(simulation.nucleon2_positions_x, simulation.nucleon2_positions_y, label='Нуклон 2')
        self.ax.set_title('Движение нуклонов')
        self.ax.set_xlabel('X-координата')
        self.ax.set_ylabel('Y-координата')
        self.ax.legend()
        self.canvas.draw()


# if __name__ == "__main__":
root = tk.Tk()
app = NuclearSimulationApp(root)
root.mainloop()



