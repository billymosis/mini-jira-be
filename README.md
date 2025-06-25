mkdir mini-jira-clone
cd mini-jira-clone
uv init
uv venv
source .venv/bin/activate
uv pip install django djangorestframework djangorestframework-simplejwt
django-admin startproject config .
