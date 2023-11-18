import numpy as np

c = 3e8


class Nucleon:
    def __init__(self, mass, initial_position, initial_velocity):
        self.mass = mass
        self.position = np.array(initial_position, dtype=float)
        self.velocity = np.array(initial_velocity, dtype=float)
        self.gamma = 1 / np.sqrt(1 - np.linalg.norm(self.velocity) ** 2 / c ** 2)


class Simulation:
    def __init__(self, nucleon1, nucleon2, time_step):
        self.nucleon1 = nucleon1
        self.nucleon2 = nucleon2
        self.time_step = time_step
        self.nucleon1_positions_x = []
        self.nucleon1_positions_y = []
        self.nucleon2_positions_x = []
        self.nucleon2_positions_y = []


    def calculate_potential_energy(self):
        # Расчет потенциальной энергии между нуклонами (по потенциалу Юкавы)
        distance = np.linalg.norm(self.nucleon1.position - self.nucleon2.position)
        alpha = 1.0
        r0 = 1.0e-15
        return -alpha ** 2 / distance * np.exp(-distance / r0)

    def integrate(self, num_steps):
        # Интегрирование уравнений движения
        for _ in range(num_steps):
            force = self.calculate_force()
            acceleration_nucleon1 = 1 / (self.nucleon1.mass * self.nucleon1.gamma) * (force - (self.nucleon1.velocity / c**2)  * np.dot(self.nucleon1.velocity, force))
            acceleration_nucleon2 = -1 / (self.nucleon2.mass * self.nucleon2.gamma) * (force - (self.nucleon2.velocity / c ** 2) * np.dot(self.nucleon2.velocity, force))

            self.nucleon1.gamma = 1 / np.sqrt(1 - np.linalg.norm(self.nucleon1.velocity) ** 2 / c ** 2)
            self.nucleon2.gamma = 1 / np.sqrt(1 - np.linalg.norm(self.nucleon2.velocity) ** 2 / c ** 2)

            self.nucleon1.velocity += acceleration_nucleon1 * self.time_step
            self.nucleon2.velocity += acceleration_nucleon2 * self.time_step

            self.nucleon1.position += self.nucleon1.velocity * self.time_step
            self.nucleon2.position += self.nucleon2.velocity * self.time_step

            self.nucleon1_positions_x.append(self.nucleon1.position[0])  # Добавляем x-координату нуклона 1
            self.nucleon1_positions_y.append(self.nucleon1.position[1])  # Добавляем y-координату нуклона 1
            self.nucleon2_positions_x.append(self.nucleon2.position[0])  # Добавляем x-координату нуклона 2
            self.nucleon2_positions_y.append(self.nucleon2.position[1])  # Добавляем y-координату нуклона 2

    def get_nucleon1_positions(self): #getters
        return self.nucleon1_positions

    def get_nucleon2_positions(self):
        return self.nucleon2_positions

    def get_nucleon1_position(self):
        return self.nucleon1.position

    def get_nucleon2_position(self):
        return self.nucleon2.position

    def get_nucleon1_velocity(self):
        return self.nucleon1.velocity

    def get_nucleon2_velocity(self):
        return self.nucleon2.velocity

    def calculate_force(self):
        distance = np.linalg.norm(self.nucleon1.position - self.nucleon2.position)
        alpha = 8.926365e-15
        r0 = 1.4e-15 #check

        # Расчет силы
        force_magnitude = (alpha ** 2 / distance ** 2) * (1 + distance / r0) * np.exp(-distance / r0)

        # Направление силы
        direction = (self.nucleon2.position - self.nucleon1.position) / distance

        # Вычисление вектора силы
        force = force_magnitude * direction

        return force

