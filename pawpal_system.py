from datetime import date


class FeedingTask:
    def __init__(self, food_type: str, amount_cups: float, scheduled_time: str, priority: str):
        self.food_type = food_type
        self.amount_cups = amount_cups
        self.scheduled_time = scheduled_time
        self.priority = priority
        self.completed = False

    def mark_complete(self):
        pass

    def is_today(self) -> bool:
        pass


class Pet:
    def __init__(self, name: str, species: str, age: int):
        self.name = name
        self.species = species
        self.age = age
        self.feeding_schedule: list[FeedingTask] = []

    def add_feeding(self, task: FeedingTask) -> None:
        pass

    def get_feedings_for_today(self) -> list[FeedingTask]:
        pass


class Owner:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_todays_tasks(self) -> list[FeedingTask]:
        pass


class Scheduler:
    def __init__(self, owner: Owner, date: date):
        self.owner = owner
        self.date = date

    def build_schedule(self) -> list[FeedingTask]:
        pass

    def get_todays_tasks(self) -> list[FeedingTask]:
        pass

    def explain_plan(self) -> str:
        pass
