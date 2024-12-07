# Frolic Event Management System

An **Event Management System** built with Flask, providing role-based interaction for Participants, Coordinators, Organizers, Branch Admins, and Admins. Frolic is open-source, free, and actively under development. While the prototype is functional, many essential features are still being developed, making this project a great starting point for managing events with a robust web application.

---

## Usage

### Prerequisites
It is recommended to create a virtual environment before installing and running the package to avoid dependency conflicts. You can set up a virtual environment using the following commands:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Install and Run

1. Install the package:
   ```bash
   pip install frolic-webserver
   ```

2. Mock the data:
   ```bash
   frolic mock
   ```

3. Start the server:
   ```bash
   frolic run
   ```

---


Use `frolic --help` to read the man page of `frolic` command.

Optionally, create a file named `.flaskenv` in current working directory to specify common options as below:
```
PROFILE=Development
FLASK_RUN_DEBUG=True
FLASK_RUN_PORT=8090
FLASK_RUN_HOST=0.0.0.0
```


## Features

- **Role-based interaction:**
  - **Participant**: Register and view events.
  - **Coordinator**: Assist in managing event operations.
  - **Organizer**: Plan and manage events.
  - **Branchadmin**: Oversee branch-specific events and operations.
  - **Admin**: Full control over the event management system.

- **Open Source & Free:** Available for contributions and usage without any cost.

- **Actively Developed:** While the prototype is ready, ongoing work ensures frequent updates and new features.