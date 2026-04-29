import json

def calculate_progress(tasks):
    try:
        total_tasks = len(tasks)
        if total_tasks == 0:
            return json.dumps({"percentage": 0})
        
        completed_tasks = sum(1 for task in tasks if task.get("status") == "completed")
        percentage = round((completed_tasks / total_tasks) * 100, 2)
        
        return json.dumps({"percentage": percentage})
    except Exception as e:
        return json.dumps({"percentage": 0, "error": str(e)})
