from datetime import datetime, timedelta

now = datetime.utcnow()
print(now)

print(timedelta(seconds=3600))

print(now + timedelta(seconds=3600))