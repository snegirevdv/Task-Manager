# Task Manager

[![Actions Status](https://github.com/snegirevdv/python-django-developer-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/snegirevdv/python-django-developer-project-52/actions)

## Table of Contents

- [Overview](#overview)
- [Technology Stack](#technology-stack)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Example](#example)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

Task Manager is a web application that helps manage tasks effectively. It supports creating, updating, and deleting tasks, user authentication and management.

## Technology Stack

- **Backend:** Django, Python
- **Frontend:** HTML, Bootstrap Framework, Django Templates
- **Database:** PostgreSQL
- **Tools:** Poetry, Git, GitHub Actions

## Features

- User Authentication: Sign up, sign in, and manage user profiles.
- Task Management: Create, update, delete, and view tasks.
- Labels: Use labels for better task organization.
- Statuses: Use task statuses to track progress.
- Filters: Filter tasks based on different parameters.
- Multilingual Support: Currently supports Russian localization.

## Installation

To install and run the project, follow these steps:

1. **Clone the repository:**

```sh
git clone https://github.com/snegirevdv/python-django-developer-project-52.git
cd python-django-developer-project-52
```

2. **Install dependencies:**
   You must have [Poetry](https://python-poetry.org/) installed.

```sh
poetry install
```

3. **Apply migrations:**

```sh
poetry run python manage.py migrate
```

4. **Run the development server:**

```sh
poetry run python manage.py runserver
```

## Usage

After setting up the project, the application will be available at 'http://127.0.0.1:8000/'.
Register a new user, log in, and start managing your tasks.

## Example

https://task-manager-09zt.onrender.com
