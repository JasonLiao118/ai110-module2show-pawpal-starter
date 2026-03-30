from datetime import date
from pawpal_system import FeedingTask, Pet, Owner, Scheduler


# Create owner
jordan = Owner(name="Jordan", email="jordan@email.com")

# Create pets
mochi = Pet(name="Mochi", species="dog", age=3)
luna = Pet(name="Luna", species="cat", age=5)

# Add tasks OUT OF ORDER intentionally
mochi.add_feeding(FeedingTask(food_type="Wet food",     amount_cups=0.5,  scheduled_time="12:00", priority="medium", frequency="daily"))
mochi.add_feeding(FeedingTask(food_type="Dry kibble",   amount_cups=1.5,  scheduled_time="07:00", priority="high",   frequency="daily"))
mochi.add_feeding(FeedingTask(food_type="Evening meal", amount_cups=1.0,  scheduled_time="18:30", priority="low",    frequency="daily"))

luna.add_feeding(FeedingTask(food_type="Tuna treat",      amount_cups=0.25, scheduled_time="17:00", priority="low",    frequency="weekly", scheduled_date=date.today()))
luna.add_feeding(FeedingTask(food_type="Dry kibble",      amount_cups=0.75, scheduled_time="08:30", priority="high",   frequency="daily"))
luna.add_feeding(FeedingTask(food_type="Afternoon snack", amount_cups=0.5,  scheduled_time="13:45", priority="medium", frequency="daily"))
# Intentional conflict: Luna and Mochi both have a task at 12:00
luna.add_feeding(FeedingTask(food_type="Hairball remedy", amount_cups=0.1,  scheduled_time="12:00", priority="high",   frequency="daily"))

# Mark one task complete to test filtering
mochi.feeding_schedule[1].mark_complete()  # Mochi's 07:00 dry kibble is done

# Register pets
jordan.add_pet(mochi)
jordan.add_pet(luna)

scheduler = Scheduler(owner=jordan, date=date.today())

# ── Today's full schedule (priority + time sorted) ────────────────────────────
print("=" * 45)
print("  TODAY'S SCHEDULE (priority then time)")
print("=" * 45)
print(scheduler.explain_plan())

# ── Sorted by time only ───────────────────────────────────────────────────────
print("\n" + "=" * 45)
print("  SORTED BY TIME")
print("=" * 45)
for t in scheduler.sort_by_time(scheduler.get_todays_tasks()):
    print(f"  {t.scheduled_time}  {t.food_type} ({t.priority})")

# ── Filter: pending tasks only ────────────────────────────────────────────────
print("\n" + "=" * 45)
print("  PENDING TASKS ONLY")
print("=" * 45)
for t in scheduler.filter_tasks(completed=False):
    print(f"  {t.food_type} at {t.scheduled_time} — pending")

# ── Filter: completed tasks only ──────────────────────────────────────────────
print("\n" + "=" * 45)
print("  COMPLETED TASKS ONLY")
print("=" * 45)
for t in scheduler.filter_tasks(completed=True):
    print(f"  {t.food_type} at {t.scheduled_time} — done")

# ── Filter: Mochi's tasks only ────────────────────────────────────────────────
print("\n" + "=" * 45)
print("  MOCHI'S TASKS ONLY")
print("=" * 45)
for t in scheduler.filter_tasks(pet_name="Mochi"):
    print(f"  {t.food_type} at {t.scheduled_time} ({t.priority})")

# ── Filter: Luna's pending tasks ──────────────────────────────────────────────
print("\n" + "=" * 45)
print("  LUNA'S PENDING TASKS")
print("=" * 45)
for t in scheduler.filter_tasks(completed=False, pet_name="Luna"):
    print(f"  {t.food_type} at {t.scheduled_time} ({t.priority})")
print("=" * 45)

# ── Conflict detection ────────────────────────────────────────────────────────
print("\n" + "=" * 45)
print("  CONFLICT DETECTION")
print("=" * 45)
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"  WARNING: {warning}")
else:
    print("  No conflicts found.")
print("=" * 45)
