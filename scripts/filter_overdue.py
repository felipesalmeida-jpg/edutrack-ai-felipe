import json
from datetime import datetime

def filter_overdue(tasks):
    try:
        today = datetime.today().date()
        overdue = []
        
        for task in tasks:
            due_date = task.get("due_date")
            if due_date:
                try:
                    due = datetime.fromisoformat(str(due_date)).date()
                    if due < today and task.get("status") != "completed":
                        overdue.append(task)
                except Exception:
                    continue
        
        return json.dumps({"overdue_tasks": overdue, "total": len(overdue)})
    except Exception as e:
        return json.dumps({"overdue_tasks": [], "total": 0, "error": str(e)})
