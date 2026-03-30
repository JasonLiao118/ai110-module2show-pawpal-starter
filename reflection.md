# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My UML design consists of 4 classes, the owner which manages pets, pets which have a feeding schedule, and a scheduler that manages the owner. The owner is able to add a pet to its list, and get todays tasks. The pet is able to add a feeding task and get feeding tasks for the day. The feeding task is able to be marked complete or check if a feeding is today. The scheduler is able to build the schedule, get all tasks for the day, and explain the plan for the schedule.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Three changes were made during implementation into the class. The first issue was that both the owner and scheduler had get_todays_task so I just removed it for the owner and left it for the scheduler. The second issue was that feedingtask method has no date field so I added a parameter in the constructor for the scheduled date. The final issue was that the AI was unsure of the difference between buildschedule and gettodaystasks and I told AI that build schedule will handle most of the logic and the other method would just be a getter.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
