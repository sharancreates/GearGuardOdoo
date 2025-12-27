# GearGuard 🛡️

**A smarter way to track equipment maintenance.**

I built **GearGuard** because managing equipment repairs with spreadsheets or paper tickets is a nightmare. This is a full-stack web application designed to help maintenance teams track breakdowns, schedule preventive maintenance, and manage their inventory without the headache.

It’s built on **Flask** (Python) and uses a custom-styled interface that’s clean, responsive, and easy to look at all day.


## Key Features

Here are the parts of the app I'm most proud of:

* **The Kanban Board:** This is the heart of the app. You can drag and drop repair tickets from `New` → `In Progress` → `Repaired`. It gives you an instant visual of how busy the team is.
* **"Smart" Request Forms:** When you select a machine (like "Drill Press 01"), the system automatically knows which team (Mechanics) and which technician is responsible for it. It fills those fields in for you.
* **Preventive Calendar:** Not everything is a breakdown. You can schedule future maintenance checks, and they show up on a dedicated calendar view so they aren't forgotten.
* **The "Scrap" Logic:** If a machine is beyond repair, dragging the card to the **Scrap** column doesn't just close the ticket—it actually updates the inventory database to mark that machine as dead/decommissioned so nobody tries to assign work to it again.
* **Dashboard Analytics:** A quick overview of active requests, workload distribution, and recent activity right when you log in.

## The Tech Stack

I chose this stack for speed and reliability:

* **Backend:** Python 3 & Flask (Lightweight and fast)
* **Database:** SQLite with SQLAlchemy ORM (Easy to set up)
* **Frontend:** Jinja2 templates with **custom CSS** (No heavy frameworks like React, just clean HTML/CSS and vanilla JS).
* **Auth:** Flask-Login for secure user sessions.


## How to Run It

I've included a `seed.py` script so you don't have to manually enter data to test it out.

**1. Clone the repo and set up your environment:**

```bash
# Set up a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install the requirements
pip install Flask Flask-SQLAlchemy Flask-Login

```

**2. Initialize the Database:**
I wrote a seeding script that wipes the DB and fills it with dummy teams, users, and machines so you can click around immediately.

```bash
python seed.py

```

*You should see a message saying "SEEDING COMPLETE".*

**3. Launch the App:**

```bash
python app.py

```

Then just open your browser to `http://127.0.0.1:5000`.

---

## Login Info

Since the database is seeded with dummy data, you can use these accounts to test the permissions:

* **Manager Account:** `manager@gearguard.com` / `password123`
* **Technician Account:** `john@gearguard.com` / `password123`


## How the Code is Organized

I tried to keep the folder structure clean by separating the logic into "Blueprints":

* `app.py`: The main entry point.
* `routes/`: Where the logic lives.
* `maintenance_routes.py`: Handles the Kanban board and ticket logic.
* `equipment_routes.py`: Handles the inventory list and forms.
* `api_routes.py`: Returns JSON data for the calendar and auto-fill features.


* `static/css/`: Custom styling. I have separate files for the `dashboard.css`, `equipment.css`, and `kanban.css` to keep things modular.
* `templates/`: The HTML files. I use a `base.html` layout so I don't have to rewrite the navbar on every page.


* Email notifications when a ticket is assigned to you.
* A mobile-friendly view for technicians working on the shop floor.
* Upload functionality so technicians can attach photos of the broken parts.
