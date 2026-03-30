from datetime import date
import streamlit as st
from pawpal_system import FeedingTask, Pet, Owner, Scheduler


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# ── Owner setup ───────────────────────────────────────────────────────────────
st.subheader("Owner Info")
owner_name = st.text_input("Owner name", value="Jordan")
owner_email = st.text_input("Owner email", value="jordan@email.com")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, email=owner_email)

# ── Add a Pet ─────────────────────────────────────────────────────────────────
st.divider()
st.subheader("Add a Pet")

pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
age = st.number_input("Age (years)", min_value=0, max_value=30, value=3)

if st.button("Add Pet"):
    new_pet = Pet(name=pet_name, species=species, age=age)
    st.session_state.owner.add_pet(new_pet)
    st.success(f"{pet_name} added to your pets!")

if st.session_state.owner.pets:
    st.table([{"Name": p.name, "Species": p.species, "Age": p.age}
              for p in st.session_state.owner.pets])
else:
    st.info("No pets yet. Add one above.")

# ── Schedule a Feeding Task ───────────────────────────────────────────────────
st.divider()
st.subheader("Schedule a Feeding Task")

pet_names = [p.name for p in st.session_state.owner.pets]

if pet_names:
    col1, col2 = st.columns(2)
    with col1:
        selected_pet = st.selectbox("Assign to pet", pet_names)
    with col2:
        food_type = st.text_input("Food type", value="Dry kibble")

    col3, col4, col5 = st.columns(3)
    with col3:
        amount = st.number_input("Amount (cups)", min_value=0.25, max_value=10.0, value=1.0, step=0.25)
    with col4:
        scheduled_time = st.time_input("Scheduled time")
    with col5:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    frequency = st.selectbox("Frequency", ["daily", "weekly", "once"])

    if st.button("Add Feeding Task"):
        task = FeedingTask(
            food_type=food_type,
            amount_cups=amount,
            scheduled_time=scheduled_time.strftime("%H:%M"),
            priority=priority,
            frequency=frequency,
            scheduled_date=date.today()
        )
        pet = next(p for p in st.session_state.owner.pets if p.name == selected_pet)
        pet.add_feeding(task)
        st.success(f"Feeding task '{food_type}' added for {selected_pet}!")
else:
    st.info("Add a pet first before scheduling tasks.")

# ── Today's Schedule ──────────────────────────────────────────────────────────
st.divider()
st.subheader("Today's Schedule")

sort_mode = st.radio("Sort by", ["Priority then time", "Time only"], horizontal=True)
filter_pet = st.selectbox("Filter by pet", ["All pets"] + pet_names)
filter_status = st.radio("Filter by status", ["All", "Pending only", "Completed only"], horizontal=True)

if st.button("Generate Schedule"):
    scheduler = Scheduler(owner=st.session_state.owner, date=date.today())

    # Conflict warnings
    conflicts = scheduler.detect_conflicts()
    for conflict in conflicts:
        st.warning(f"Schedule conflict: {conflict}")

    # Get and filter tasks
    pet_name_filter = None if filter_pet == "All pets" else filter_pet
    completed_filter = None
    if filter_status == "Pending only":
        completed_filter = False
    elif filter_status == "Completed only":
        completed_filter = True

    tasks = scheduler.filter_tasks(completed=completed_filter, pet_name=pet_name_filter)

    # Apply sort mode
    if sort_mode == "Time only":
        tasks = scheduler.sort_by_time(tasks)

    if not tasks:
        st.info("No tasks match your filters.")
    else:
        rows = []
        for task in tasks:
            pet = next((p for p in st.session_state.owner.pets if task in p.feeding_schedule), None)
            rows.append({
                "Pet": pet.name if pet else "Unknown",
                "Food": task.food_type,
                "Time": task.scheduled_time,
                "Amount (cups)": task.amount_cups,
                "Priority": task.priority,
                "Frequency": task.frequency,
                "Status": "Done" if task.completed else "Pending",
            })
        st.table(rows)
        st.success(f"{len(tasks)} task(s) scheduled for today.")
