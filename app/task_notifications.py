import time

def send_notification(task_id: int, task_title: str):
  time.sleep(2)
  with open("notifications.log", "a", encoding="utf-8") as f:
    f.write(f'Уведомление: Создана задача #{task_id} - "{task_title}" \n')
