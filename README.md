mkdir mini-jira-clone
cd mini-jira-clone
uv init
uv venv
source .venv/bin/activate
uv pip install django djangorestframework djangorestframework-simplejwt
django-admin startproject config .
cd apps
uv run django-admin startapps tasks
mkdir apps/tasks -p
python manage.py startapp tasks apps/tasks
python manage.py startapp users apps/users

```bash
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}' \
  http://localhost:8000/api/token/
{"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MDkzNzgzOSwiaWF0IjoxNzUwODUxNDM5LCJqdGkiOiJjZDBiNjVkMjMyZDg0OTEzOWM4MWFkZDc3M2Y4ODc0NiIsInVzZXJfaWQiOjF9.0j13hc3z1N2_WaGtAzTiXPgy3fI1eP_WbXsDuNNri4o","access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwODUxNzM5LCJpYXQiOjE3NTA4NTE0MzksImp0aSI6ImJiNDM2ZTg5MTlmZTQxN2JhOWQ4YzZhOWQ3YjI1MGUxIiwidXNlcl9pZCI6MX0.yWXD-GzTKXP9zJ6opYogL0hlPKhj7dIkPBqdsbIrSkI"}%
```

```bash
curl \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwOTIwMTU3LCJpYXQiOjE3NTA5MTk4NTcsImp0aSI6IjNiYjE2MzM0NTIwODQzNzg5ZWM5MTRmZjhiNzQ2ZTJlIiwidXNlcl9pZCI6ImM2OTM5ZDUxLWYzMGQtNDk4My05Y2FmLWFhZjk4MTFiOWUzMCJ9.tie8rvYwooVJXDkqT4cN9qkY_pndlgNIbYrTsBi2790" \
  http://localhost:8000/api/v1/hello-json
{"status":"request was permitted"}%
```

mkdir -p apps/projects
python manage.py startapp projects apps/projects

Seed groups, permissions and users
python manage.py makemigrations users --empty

admin token:
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxNTk0Mjg3LCJpYXQiOjE3NTA5ODk0ODcsImp0aSI6ImFkZmMxZDc5NDU4ZTRiNTJiNTkxODJlM2Q0NDVmZDk4IiwidXNlcl9pZCI6ImZhN2FmYmJiLTc3ZTItNDRkYy05MjkxLWZiM2RjNzgzYzdlMSJ9.AxQFvuP2XiOwr3nQ-5l7tM9kYWQ-EBHbspQyZeOgMVI

member1 token:
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxNTk0Mjk5LCJpYXQiOjE3NTA5ODk0OTksImp0aSI6IjllNWY5NmM2MDUxYzQ0MjliNDczYWM5ZWVjZDcwZjAwIiwidXNlcl9pZCI6IjI1ZmMzMzVmLTE1MjUtNDlkOS05MDQ4LWEwY2QwMzUyYWVjNiJ9.zCAQoVcZlH5da3m_UI5936n45xrd_X04oTx7KGKaPxA
