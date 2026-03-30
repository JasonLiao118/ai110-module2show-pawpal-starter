import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import date, timedelta
from pawpal_system import FeedingTask, Pet, Owner, Scheduler


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


def make_scheduler():
    owner = Owner(name="Jordan", email="jordan@email.com")
    mochi = Pet(name="Mochi", species="dog", age=3)
    luna = Pet(name="Luna", species="cat", age=5)
    owner.add_pet(mochi)
    owner.add_pet(luna)
    return Scheduler(owner=owner, date=date.today()), mochi, luna


def test_sort_by_time_orders_chronologically():
    scheduler, mochi, _ = make_scheduler()
    mochi.add_feeding(FeedingTask(food_type="Evening meal", amount_cups=1.0, scheduled_time="18:00", priority="low",    frequency="daily"))
    mochi.add_feeding(FeedingTask(food_type="Dry kibble",   amount_cups=1.5, scheduled_time="07:00", priority="high",   frequency="daily"))
    mochi.add_feeding(FeedingTask(food_type="Wet food",     amount_cups=0.5, scheduled_time="12:00", priority="medium", frequency="daily"))

    sorted_tasks = scheduler.sort_by_time(scheduler.get_todays_tasks())
    times = [t.scheduled_time for t in sorted_tasks]
    assert times == sorted(times), f"Expected chronological order, got {times}"


def test_complete_task_creates_next_day_occurrence():
    scheduler, mochi, _ = make_scheduler()
    task = FeedingTask(food_type="Dry kibble", amount_cups=1.0, scheduled_time="08:00", priority="high", frequency="daily")
    mochi.add_feeding(task)

    next_task = scheduler.complete_task(task)

    assert task.completed is True
    assert next_task is not None
    assert next_task.scheduled_date == date.today() + timedelta(days=1)
    assert next_task in mochi.feeding_schedule


def test_detect_conflicts_flags_same_time():
    scheduler, mochi, luna = make_scheduler()
    mochi.add_feeding(FeedingTask(food_type="Dry kibble",     amount_cups=1.0, scheduled_time="08:00", priority="high", frequency="daily"))
    luna.add_feeding(FeedingTask(food_type="Hairball remedy", amount_cups=0.1, scheduled_time="08:00", priority="high", frequency="daily"))

    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]
    assert "Mochi" in conflicts[0]
    assert "Luna" in conflicts[0]


# ── Recurring task edge cases ─────────────────────────────────────────────────

def test_complete_weekly_task_creates_occurrence_seven_days_later():
    scheduler, mochi, _ = make_scheduler()
    task = FeedingTask(food_type="Tuna treat", amount_cups=0.25, scheduled_time="17:00", priority="low", frequency="weekly")
    mochi.add_feeding(task)

    next_task = scheduler.complete_task(task)

    assert next_task is not None
    assert next_task.scheduled_date == date.today() + timedelta(weeks=1)


def test_complete_once_task_does_not_create_new_task():
    scheduler, mochi, _ = make_scheduler()
    task = FeedingTask(food_type="Special treat", amount_cups=0.5, scheduled_time="10:00", priority="low", frequency="once")
    mochi.add_feeding(task)
    count_before = len(mochi.feeding_schedule)

    next_task = scheduler.complete_task(task)

    assert next_task is None
    assert len(mochi.feeding_schedule) == count_before


# ── Sorting edge cases ────────────────────────────────────────────────────────

def test_sort_by_time_empty_list_returns_empty():
    scheduler, _, _ = make_scheduler()
    assert scheduler.sort_by_time([]) == []


def test_build_schedule_empty_pet_returns_empty():
    scheduler, _, _ = make_scheduler()  # pets have no tasks
    assert scheduler.build_schedule() == []


def test_build_schedule_priority_order():
    scheduler, mochi, _ = make_scheduler()
    mochi.add_feeding(FeedingTask(food_type="Low task",    amount_cups=1.0, scheduled_time="07:00", priority="low",    frequency="daily"))
    mochi.add_feeding(FeedingTask(food_type="High task",   amount_cups=1.0, scheduled_time="08:00", priority="high",   frequency="daily"))
    mochi.add_feeding(FeedingTask(food_type="Medium task", amount_cups=1.0, scheduled_time="09:00", priority="medium", frequency="daily"))

    schedule = scheduler.build_schedule()
    priorities = [t.priority for t in schedule]

    assert priorities == ["high", "medium", "low"]


def test_sort_by_time_does_not_consider_priority():
    scheduler, mochi, _ = make_scheduler()
    mochi.add_feeding(FeedingTask(food_type="Low early",  amount_cups=1.0, scheduled_time="06:00", priority="low",  frequency="daily"))
    mochi.add_feeding(FeedingTask(food_type="High late",  amount_cups=1.0, scheduled_time="20:00", priority="high", frequency="daily"))

    sorted_tasks = scheduler.sort_by_time(scheduler.get_todays_tasks())

    assert sorted_tasks[0].scheduled_time == "06:00"
    assert sorted_tasks[1].scheduled_time == "20:00"


# ── Filter edge cases ─────────────────────────────────────────────────────────

def test_filter_tasks_unknown_pet_name_returns_empty():
    scheduler, mochi, _ = make_scheduler()
    mochi.add_feeding(make_task())

    result = scheduler.filter_tasks(pet_name="NonExistentPet")

    assert result == []


def test_filter_tasks_no_filters_returns_all():
    scheduler, mochi, luna = make_scheduler()
    mochi.add_feeding(make_task())
    luna.add_feeding(make_task())

    result = scheduler.filter_tasks()

    assert len(result) == 2


def test_filter_tasks_all_completed():
    scheduler, mochi, _ = make_scheduler()
    t1 = FeedingTask(food_type="Kibble", amount_cups=1.0, scheduled_time="08:00", priority="high", frequency="daily")
    t2 = FeedingTask(food_type="Snack",  amount_cups=0.5, scheduled_time="12:00", priority="low",  frequency="daily")
    mochi.add_feeding(t1)
    mochi.add_feeding(t2)
    t1.mark_complete()
    t2.mark_complete()

    pending = scheduler.filter_tasks(completed=False)

    assert pending == []


# ── Conflict detection edge cases ─────────────────────────────────────────────

def test_detect_conflicts_no_conflicts_returns_empty():
    scheduler, mochi, luna = make_scheduler()
    mochi.add_feeding(FeedingTask(food_type="Kibble", amount_cups=1.0, scheduled_time="08:00", priority="high", frequency="daily"))
    luna.add_feeding(FeedingTask(food_type="Kibble",  amount_cups=1.0, scheduled_time="09:00", priority="high", frequency="daily"))

    assert scheduler.detect_conflicts() == []


def test_detect_conflicts_three_tasks_same_time():
    scheduler, mochi, luna = make_scheduler()
    rex = Pet(name="Rex", species="dog", age=2)
    scheduler.owner.add_pet(rex)

    mochi.add_feeding(FeedingTask(food_type="Kibble",  amount_cups=1.0, scheduled_time="08:00", priority="high",   frequency="daily"))
    luna.add_feeding(FeedingTask(food_type="Wet food", amount_cups=0.5, scheduled_time="08:00", priority="medium", frequency="daily"))
    rex.add_feeding(FeedingTask(food_type="Snack",     amount_cups=0.5, scheduled_time="08:00", priority="low",    frequency="daily"))

    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "Mochi" in conflicts[0]
    assert "Luna" in conflicts[0]
    assert "Rex" in conflicts[0]
