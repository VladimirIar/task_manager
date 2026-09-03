import time
from datetime import datetime

def send_notification(task_id: int, task_title: str):
  time.sleep(2)

  now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  with open("notifications.log", "a", encoding="utf-8") as f:
    f.write(f'[{now}] Уведомление: Создана задача #{task_id} - "{task_title}" \n')
