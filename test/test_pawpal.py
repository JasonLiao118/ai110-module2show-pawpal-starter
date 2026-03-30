import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import FeedingTask, Pet


def make_task():
    return FeedingTask(
        food_type="Dry kibble",
        amount_cups=1.0,
        scheduled_time="08:00",
        priority="high",
        frequency="daily"
    )


def test_mark_complete_changes_status():
    task = make_task()
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_feeding_increases_task_count():
    pet = Pet(name="Mochi", species="dog", age=3)
    assert len(pet.feeding_schedule) == 0
    pet.add_feeding(make_task())
    assert len(pet.feeding_schedule) == 1
    pet.add_feeding(make_task())
    assert len(pet.feeding_schedule) == 2
