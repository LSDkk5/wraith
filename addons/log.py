from datetime import datetime

def log_action(actionType, action):
    with open(f'logs/{datetime.now().strftime("%Y-%m-%d")}.log', 'a+') as logs:
        logs.write(f"{datetime.now().strftime('[ %H:%M:%S ]')}:  [main/{actionType}]: {action}\n")
