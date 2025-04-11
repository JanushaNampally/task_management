import datetime
from django.utils import timezone
import pulp

def optimize_schedule(tasks, available_hours=8):
    if not tasks:
        return []

    now = timezone.now()

    # Calculate normalized deadline score
    deadline_scores = []
    for task in tasks:
        hours_until_deadline = max(0.1, (task.deadline - now).total_seconds() / 3600)
        deadline_score = 100 / hours_until_deadline
        deadline_scores.append(deadline_score)

    max_deadline_score = max(deadline_scores)
    normalized_deadlines = [score / max_deadline_score * 10 for score in deadline_scores]

    # Final weighted score
    scores = [
        0.6 * task.importance + 0.4 * norm_deadline
        for task, norm_deadline in zip(tasks, normalized_deadlines)
    ]

    # LP Problem
    prob = pulp.LpProblem("Task_Scheduling", pulp.LpMaximize)

    # Decision variables: 1 if task is scheduled, 0 otherwise
    x = [pulp.LpVariable(f"x{i}", cat="Binary") for i in range(len(tasks))]

    # Objective: maximize total score of selected tasks
    prob += pulp.lpSum([scores[i] * x[i] for i in range(len(tasks))]), "Total_Score"

    # Constraint: total hours ≤ available
    prob += pulp.lpSum([tasks[i].estimated_hours * x[i] for i in range(len(tasks))]) <= available_hours

    # Solve
    prob.solve()

    # Select and schedule tasks based on LP result
    scheduled_tasks = []
    start_time = now
    for i in range(len(tasks)):
        if x[i].varValue == 1:
            task = tasks[i]
            scheduled_tasks.append({
                'task': task,
                'start_time': start_time,
                'end_time': start_time + datetime.timedelta(hours=task.estimated_hours),
                'score': scores[i],
            })
            start_time += datetime.timedelta(hours=task.estimated_hours)

    return scheduled_tasks
