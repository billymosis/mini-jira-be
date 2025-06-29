# MINI JIRA BE

A full-featured backend for a simplified Jira clone. Provides JWT-based auth, role-based access control, and REST APIs for projects, tasks, and analytics.

## Live demo

[https://api-mini-jira.billymosis.com/](https://api-mini-jira.billymosis.com/)

## Swagger Schema
[https://api-mini-jira.billymosis.com/api/schema/swagger-ui/](https://api-mini-jira.billymosis.com/api/schema/swagger-ui/)

## Redoc Schema
[https://api-mini-jira.billymosis.com/api/schema/swagger-ui/](https://api-mini-jira.billymosis.com/api/schema/redoc/)

## Seeded data from migrations

file: `apps/users/migrations/0002_auto_20250626_0706.py`
  - `admin:admin123`
  - `member1:member123`
  - `member2:member123`

to seed the database:
`python manage.py seed`

## Folder Structure

- `apps/users/` – Authentication, user profiles, roles
- `apps/projects/` – Project creation and listing
- `apps/tasks/` – Task CRUD and assignment
- `apps/analytics/` – Simple analytics endpoints

## Roles

Roles handled by using built in django groups
- **Admin**: Can create/edit/delete any project/task
- **Member**: Can create/edit/delete task

## Development

```bash
source .venv/bin/activate
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Docker Image Build

Live demo deployed with aws EC2

1. Docker build
```bash
docker build -t mini-jira-be .
```

2. Setup docker compose file for better developer experience
```yml
services:
  web:
    image: mini-jira-be:latest 
    restart: unless-stopped
    ports:
      - "80:8000"
    environment:
      - PYTHONUNBUFFERED=1
      - AWS_S3_ACCESS_KEY_ID=A********
      - AWS_S3_SECRET_ACCESS_KEY=WIX************
      - AWS_STORAGE_BUCKET_NAME=super-*********
      - AWS_S3_REGION_NAME=ap-southeast-1  # Optional
      - AWS_S3_SIGNATURE_VERSION=s3v4  # Optional
      - SECRET_KEY=b22***************
      - DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,13.229.114.236,api-mini-jira.billymosis.com
      - DJANGO_ALLOWED_ORIGINS=http://localhost,http://jira.billymosis.com,https://jira.billymosis.com,http://*.billymosis.com,https://*.billymosis.com
      - DEBUG=True
    volumes:
      - db_data:/app/db
      - ./staticfiles:/app/staticfiles

volumes:
  db_data:  # Named volume for SQLite database
```
3. docker compose pull
4. docker compose 

## Tech Stack
- UV
- Django
- Django rest framework
- Django simple jwt auth
- drf-spectacular (OPEN API SCHEMA)

## Features

- Task Management
- Project Management
- User Avatar Upload
- Basic Analytics
- Schema api/schema/swagger-ui/


### What can be improved
- Unit test
- Logging
- Enhance user auth

### Development work flow from scratch

1. mkdir mini-jira-clone  
2. cd mini-jira-clone  
3. uv init  
4. uv venv  
5. source .venv/bin/activate  
6. uv pip install django djangorestframework djangorestframework-simplejwt  
7. django-admin startproject config .  
8. cd apps  
9. uv run django-admin startapps tasks  
10. mkdir apps/tasks -p  
11. python manage.py startapp tasks apps/tasks  
12. python manage.py startapp users apps/users  
13. mkdir -p apps/projects  
14. python manage.py startapp projects apps/projects  
15. Seed groups, permissions and users  
16. python manage.py makemigrations users --empty  
17. python manage.py startapp analytics apps/analytics  
