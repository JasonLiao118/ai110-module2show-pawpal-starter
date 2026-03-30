from datetime import date
from pawpal_system import FeedingTask, Pet, Owner, Scheduler


# Create owner
jordan = Owner(name="Jordan", email="jordan@email.com")

# Create pets
mochi = Pet(name="Mochi", species="dog", age=3)
luna = Pet(name="Luna", species="cat", age=5)

# Add tasks to Mochi (dog)
mochi.add_feeding(FeedingTask(
    food_type="Dry kibble",
    amount_cups=1.5,
    scheduled_time="07:00",
    priority="high",
    frequency="daily"
))
mochi.add_feeding(FeedingTask(
    food_type="Wet food",
    amount_cups=0.5,
    scheduled_time="12:00",
    priority="medium",
    frequency="daily"
))

# Add tasks to Luna (cat)
luna.add_feeding(FeedingTask(
    food_type="Dry kibble",
    amount_cups=0.75,
    scheduled_time="08:30",
    priority="high",
    frequency="daily"
))
luna.add_feeding(FeedingTask(
    food_type="Tuna treat",
    amount_cups=0.25,
    scheduled_time="17:00",
    priority="low",
    frequency="weekly",
    scheduled_date=date.today()
))

# Register pets with owner
jordan.add_pet(mochi)
jordan.add_pet(luna)

# Build and display schedule
scheduler = Scheduler(owner=jordan, date=date.today())

print("=" * 40)
print("       TODAY'S SCHEDULE")
print(f"       {date.today().strftime('%A, %B %d %Y')}")
print("=" * 40)
print(scheduler.explain_plan())
