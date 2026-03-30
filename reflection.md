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

Scheduler considered three constraints: priority, time and frequency. Priority was considered the most important constraint because it makes sense that a pet with high priority should always come first no matter the other constraints. Time came in second because frequency didn't matter much when it came to scheduling priority. 


**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

A trade off to selecting priority over time is that the scheduling list will no longer appear in chronological order which may be confusing to the user. That is exactly why there is a sort_by_time method to view it in chronological order.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

AI was best utilized when thinking about edge cases to use for our program. It thought up many edge cases that I was not able to think of and was able to architect a lot of tests very quickly to verify that the program is robust. 


**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One part where I did not accept AI was when I asked it to give me an alternate algorithm for the conflict detection method. The current configuration of that method uses a single passby with groupby from itertools, where as the suggested method used a dictionary which would need to search through all tasks and would lead to a performance loss. The best way to verify that AI suggestions for code was robust was to also ask it to make a test case in the test file which was most of the time a lot easier to understand. 

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

The main tests tested the mark_complete method, the incrementing of feeding_schedule, the sorting of tasks by time, seeing if marking tasks created a new task, and flagging conflicts. These tests were important to check because they were not edge cases and were the main functionality of our program. 

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am very confident that my scheduler works correctly because I tested a numerous amount of edge cases. If I did have to test more edge cases, I would see what happens when a pet that has two separate tasks have the same time. I think this would still flag the conflict in our program, but a test should be made. 

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am very satisfied with the robustness of our program. The many test cases mean that many edge cases should be handled and the program should be functional for most real world users. 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would redesign my methods in my scheduler to try and be simpler. There are many points in my methods that prioritized performance over readability and methods were used that were not necessary to implement. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I learned that AI is very capable of architecting code, but we must guide it with UML diagrams and testing cases to make sure that it goes in the correct direction. 