Chatter

A Twitter-style news feed system: users sign up, post short messages, follow each other and read a home timeline.

Chatter is a learning project. It starts as a simple Django app and grows step by step to teach Docker, caching, queuing and microservices in practice.

New to those topics? Read docs/CONCEPTS.md first.

Contents
Tech stack
URLs
Getting started
VS Code setup
Everyday commands
Project layout
Roadmap
Troubleshooting

Tech stack
In use now
Area	Technology	Version	What it does here
Language	Python	3.13	Everything is written in it
Web framework	Django	6.1	Models, URL routing, admin, migrations
API	Django REST Framework	3.18	Builds the JSON REST API
Database	PostgreSQL	17	Stores users, posts, follows, likes
Database driver	psycopg	3.3	Lets Django talk to Postgres
Configuration	django-environ	0.14	Reads settings from the .env file
Containers	Docker + Docker Compose		Runs the app and database the same way everywhere
Package manager	uv		Installs and locks Python dependencies
Testing	pytest + pytest-django	9.1 / 4.14	Automated tests
Lint and format	Ruff	0.16	Code style checks and auto-formatting
CI	GitHub Actions		Runs lint and tests on every push
Editor	Visual Studio Code		Recommended extensions in .vscode/
Shortcuts	Make		make up, make test, and so on

Planned (added as the roadmap progresses)
Roadmap step	Technology	What it will do
Monolith MVP	djangorestframework-simplejwt	Login with JWT tokens
Monolith MVP	drf-spectacular	Auto-generated API docs (Swagger)
Caching	Redis + django-redis	Cache profiles, posts, counters and timelines
Queuing	Celery (+ Flower)	Background jobs, such as fanning a post out to followers
Microservices	Apache Kafka	Events between services (tweet.created, user.followed)
Microservices	Nginx or Traefik	API gateway in front of the services
Observability	OpenTelemetry, Prometheus, Grafana, Jaeger	Tracing, metrics and dashboards
Load testing	Locust	Measure the effect of caching and queuing

URLs
Available now

The app runs at http://localhost:8000 once docker compose up has started.

URL	Method	What it is
http://localhost:8000/health/	GET	Health check. Returns {"status": "ok"}
http://localhost:8000/admin/	GET	Django admin site (needs a superuser, see below)

Create an admin login with:

bash
docker compose exec web python manage.py createsuperuser

Postgres is reachable only from inside Docker, at db:5432. It is deliberately not exposed on your machine.

Getting started

You need Docker Desktop, Git, uv and VS Code installed (links above). Docker Desktop must be running before any docker command will work.

Open the chatter folder in VS Code, open the terminal (Ctrl+`) and run these one at a time:

bash
cp .env.example .env                               # 1. create your local settings file
docker compose up --build -d                       # 2. build the image, start web + db
docker compose exec web python manage.py migrate   # 3. create the database tables
docker compose exec web pytest                     # 4. run the tests (expect "2 passed")

Then open http://localhost:8000/health/ and you should see {"status": "ok"}.

Step 2 takes a few minutes the first time because Docker downloads Python and Postgres. After that it takes seconds.

VS Code setup
When VS Code asks to install the recommended extensions, accept.
Run uv sync in the terminal. This creates a .venv folder so VS Code can autocomplete Django code. (The app itself still runs in Docker.)
Cmd+Shift+P → Python: Select Interpreter → pick .venv.

Files are formatted automatically on save.

Run tests with make test, not the VS Code Testing panel: the database is only reachable from inside Docker.

Everyday commands
Command	What it does
make up	Build and start everything
make down	Stop everything (data is kept)
make logs	Watch the Django logs
make migrate	Apply database migrations
make test	Run the tests
make lint	Check code style
make fmt	Auto-format code
make shell	Python shell with Django loaded
make reset	Stop everything and delete the database

To add a dependency:

bash
uv add <package>
docker compose up --build -d    # rebuild so the container has it too
Project layout
chatter/
├── config/               Django project: settings, URL routing
├── tests/                pytest tests
├── docs/CONCEPTS.md      Plain-English guide to Docker, cache, queue
├── manage.py             Django's command-line tool
├── Dockerfile            Recipe for the app image
├── docker-compose.yml    Which containers run together (web + db)
├── pyproject.toml        Dependencies and tool settings
├── uv.lock               Exact dependency versions (commit this)
├── .env.example          Template for your local .env
├── Makefile              Command shortcuts
└── .github/workflows/    CI: runs lint + tests on every push

Troubleshooting
Problem	Fix
Cannot connect to the Docker daemon	Start Docker Desktop and wait for it to finish loading
port is already allocated	Something else uses port 8000. Stop it, or change "8000:8000" to "8001:8000" in docker-compose.yml
env file .env not found	Run cp .env.example .env
Added a package but get ModuleNotFoundError	Rebuild: make up
Want a clean slate	make reset, then make up and make migrate