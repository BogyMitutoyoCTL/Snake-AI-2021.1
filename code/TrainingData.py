import sys
from datetime import datetime


class TrainingData:
    def __init__(self, verbose=True):
        self.best_score: int = 0
        self.worst_score: int = sys.maxsize
        self.epoch: int = 0
        self.max_epochs: int = 0
        self.max_number_of_steps: int = 0
        self.number_of_steps_walked: int = 0
        self.best_steps_walked: int = 0
        self.total_steps_walked: int = 0
        self.last_score: int = sys.maxsize
        self.verbose = verbose
        self.epsilon = 0
        self.create_time = datetime.now()
        self.total_food_eaten = 0

    def next_epoch(self):
        self.worst_score = min(self.last_score, self.worst_score)
        self.last_score = 3
        self.number_of_steps_walked = 0
        self.epoch += 1

    def steps_exceeded(self) -> bool:
        return self.number_of_steps_walked > self.max_number_of_steps

    def walk_step(self):
        self.number_of_steps_walked += 1
        self.total_steps_walked += 1
        if self.number_of_steps_walked > self.best_steps_walked:
            self.best_steps_walked = self.number_of_steps_walked
            if self.verbose:
                now = self._formatted_now()
                print(f"{now} - New record for number of steps walked: {self.best_steps_walked} in Epoche {self.epoch}")

    @staticmethod
    def _formatted_now():
        return datetime.now().strftime("%H:%M:%S")

    def __str__(self):
        description = f"{self._formatted_now()} training result -----------------------\n"
        description += f"Trainierte Epochen: {self.epoch}/{self.max_epochs}\n"
        description += f"Max. gelaufene Steps in einer Runde: {self.best_steps_walked}\n"
        description += f"Summe aller gelaufenen Schritte:     {self.total_steps_walked}\n"
        description += f"Bestes Ergebnis (Länge der Schlange): {self.best_score}\n"
        description += f"Schlechtestes Ergebnis (Länge der Schlange): {self.worst_score}\n"
        description += f"Gesamtmenge gegessen: {self.total_food_eaten}\n"
        now = datetime.now()
        duration = int((now - self.create_time).total_seconds())
        description += f"Zeit seit Erstellung des Objekts: {duration} s"
        return description

    def score(self, snake_length: int) -> None:
        self.last_score = snake_length
        self.total_food_eaten += 1
        if self.verbose:
            if self.last_score > self.best_score:
                print(f"{self._formatted_now()}  Score {self.last_score} in Epoche {self.epoch}")
        self.best_score = max(snake_length, self.best_score)


