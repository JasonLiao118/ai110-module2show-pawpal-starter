from datetime import date

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


class FeedingTask:
    def __init__(self, food_type: str, amount_cups: float, scheduled_time: str, priority: str, frequency: str = "daily", scheduled_date: date = None):
        """Initialize a feeding task with food details, schedule, and priority."""
        self.food_type = food_type
        self.amount_cups = amount_cups
        self.scheduled_time = scheduled_time
        self.priority = priority
        self.frequency = frequency  # "daily", "weekly", "once"
        self.completed = False
        self.scheduled_date = scheduled_date or date.today()

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def is_today(self) -> bool:
        """Return True if this task is scheduled to occur today based on its frequency."""
        today = date.today()
        if self.frequency == "daily":
            return True
        elif self.frequency == "weekly":
            return today.weekday() == self.scheduled_date.weekday()
        else:  # "once"
            return self.scheduled_date == today


class Pet:
    def __init__(self, name: str, species: str, age: int):
        """Initialize a pet with a name, species, age, and an empty feeding schedule."""
        self.name = name
        self.species = species
        self.age = age
        self.feeding_schedule: list[FeedingTask] = []

    def add_feeding(self, task: FeedingTask) -> None:
        """Add a feeding task to this pet's schedule."""
        self.feeding_schedule.append(task)

    def get_feedings_for_today(self) -> list[FeedingTask]:
        """Return all of this pet's feeding tasks that are scheduled for today."""
        return [task for task in self.feeding_schedule if task.is_today()]


class Owner:
    def __init__(self, name: str, email: str):
        """Initialize an owner with a name, email, and an empty list of pets."""
        self.name = name
        self.email = email
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)


class Scheduler:
    def __init__(self, owner: Owner, date: date):
        """Initialize the scheduler with an owner and the target date."""
        self.owner = owner
        self.date = date

    def build_schedule(self) -> list[FeedingTask]:
        """Collect and sort all of today's tasks across every pet by priority then time."""
        all_tasks = []
        for pet in self.owner.pets:
            all_tasks.extend(pet.get_feedings_for_today())
        return sorted(all_tasks, key=lambda t: (PRIORITY_ORDER.get(t.priority, 99), t.scheduled_time))

    def get_todays_tasks(self) -> list[FeedingTask]:
        """Return the fully built and sorted schedule for today."""
        return self.build_schedule()

    def explain_plan(self) -> str:
        """Return a human-readable summary of today's schedule with pet, time, priority, and status."""
        tasks = self.build_schedule()
        if not tasks:
            return "No tasks scheduled for today."

        lines = []
        for task in tasks:
            pet_name = next(
                (pet.name for pet in self.owner.pets if task in pet.feeding_schedule),
                "Unknown pet"
            )
            status = "done" if task.completed else "pending"
            lines.append(
                f"{pet_name}: {task.food_type} at {task.scheduled_time} ({task.priority} priority) [{status}]"
            )
        return "\n".join(lines)
