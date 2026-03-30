from datetime import date, timedelta
from itertools import groupby

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

    def next_occurrence(self) -> "FeedingTask | None":
        """Return a new FeedingTask for the next occurrence, or None if frequency is 'once'."""
        if self.frequency == "daily":
            next_date = self.scheduled_date + timedelta(days=1)
        elif self.frequency == "weekly":
            next_date = self.scheduled_date + timedelta(weeks=1)
        else:
            return None
        return FeedingTask(
            food_type=self.food_type,
            amount_cups=self.amount_cups,
            scheduled_time=self.scheduled_time,
            priority=self.priority,
            frequency=self.frequency,
            scheduled_date=next_date
        )

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

    def sort_by_time(self, tasks: list[FeedingTask]) -> list[FeedingTask]:
        """Sort a list of tasks by scheduled_time in ascending HH:MM order."""
        return sorted(tasks, key=lambda t: t.scheduled_time)

    def filter_tasks(self, completed: bool = None, pet_name: str = None) -> list[FeedingTask]:
        """Filter today's tasks by completion status, pet name, or both."""
        tasks = self.build_schedule()
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]
        if pet_name is not None:
            tasks = [t for t in tasks
                     if any(p.name == pet_name and t in p.feeding_schedule
                            for p in self.owner.pets)]
        return tasks

    def detect_conflicts(self) -> list[str]:
        """Return a list of warning messages for any tasks scheduled at the same time."""
        tasks = self.sort_by_time(self.build_schedule())
        warnings = []
        for time_slot, group in groupby(tasks, key=lambda t: t.scheduled_time):
            entries = list(group)
            if len(entries) > 1:
                labels = ", ".join(
                    f"{next(p.name for p in self.owner.pets if t in p.feeding_schedule)} ({t.food_type})"
                    for t in entries
                )
                warnings.append(f"Conflict at {time_slot}: {labels}")
        return warnings

    def complete_task(self, task: FeedingTask) -> FeedingTask | None:
        """Mark a task complete and add the next occurrence to its pet's schedule. Returns the new task or None."""
        task.mark_complete()
        next_task = task.next_occurrence()
        if next_task is not None:
            pet = next(
                (p for p in self.owner.pets if task in p.feeding_schedule),
                None
            )
            if pet is not None:
                pet.add_feeding(next_task)
        return next_task

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
