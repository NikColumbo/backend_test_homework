from dataclasses import asdict, dataclass
from typing import Dict, List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))

@dataclass #у родительского класса получилось применить, я рад))
class Training:
    action: int
    duration: int
    weight: int

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MINS_IN_HR = 60


    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
            )


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79
    LEN_STEP: float = 0.65


    def get_spent_calories(self) -> float:
        return (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
             + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
            / self.M_IN_KM * self.duration * self.MINS_IN_HR)

#@dataclass
# а вот тут уже начались проблемы, тк появляется параметр height
# NameError: name 'height' is not defined
class SportsWalking(Training): 
    #height: float
    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    """Тренировка: спортивная ходьба."""
    SEC_IN_HR: float = 3600 #Тут я ввел новую переменную
    CM_IN_M: int = 100
    LEN_STEP: float = 0.65
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_MULTIPLIER: float = 0.029

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        return (
            (self.CALORIES_WEIGHT_MULTIPLIER * self.weight
            + ((self.get_mean_speed() 
                * round(self.M_IN_KM/self.SEC_IN_HR,3)) ** 2 #а тут округлил через round
             / (self.height / self.CM_IN_M))
            * self.CALORIES_SPEED_MULTIPLIER * self.weight)
            * self.duration * self.MINS_IN_HR)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CALORIES_CORRECT_KONSTANT: float = 1.1
    CALORIES_SWIM_MULTIPLIER: float = 2

    def __init__(self, action: int, duration: float,
                 weight: float, length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.CALORIES_CORRECT_KONSTANT)
            * self.CALORIES_SWIM_MULTIPLIER * self.duration * self.weight)

# При попытке вынести словарь за пределы функции,
# выдает ошибку (TypeError: 'type' object is not subscriptable)
#TRAINING_NAMES: Dict[type[Training]] = {
#        'SWM': Swimming,
#        'RUN': Running,
#        'WLK': SportsWalking}

def read_package(workout_type: str, data: List[str]) -> Training:
    """Прочитать данные полученные от датчиков."""
    TRAINING_NAMES: Dict[type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
    if workout_type not in TRAINING_NAMES:
        raise ValueError(f'Тренировки типа {workout_type} не существует!')
    return TRAINING_NAMES[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
