# Task Manager

## Table of Contents

- [Overview](#overview)
- [Technology Stack](#technology-stack)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Example](#example)

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
- Multilingual Support.

## Installation

### Direct Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/snegirevdv/Task-Manager.git
   ```

2. Change the directory:

   ```sh
   cd Task_Manager
   ```

3. Create a `.env` file with the necessary environment variables and update the .env file with your configuration:

   ```sh
   touch .env
   ```

4. Install the dependencies and initialize the database:

   ```sh
   make build
   ```

5. Run the application:
   ```sh
   make start
   ```

### Using Docker Compose

1. Download the `docker-compose.production.yml` file:

   ```sh
   curl -O https://raw.githubusercontent.com/snegirevdv/Task-Manager/main/docker-compose.production.yml
   ```

2. Create a `.env` file with the necessary environment variables and update the .env file with your configuration:

   ```sh
   touch .env
   ```

3. Start the application using the production Docker Compose file. The application should now be running at `http://localhost:8001`:

   ```sh
   docker-compose -f docker-compose.production.yml up
   ```

## Usage

After setting up the project, the application will be available at http://127.0.0.1:8001/.
Register a new user, log in, and start managing your tasks.

## Example

[https://task-manager.snegirev.dev/](https://task-manager.snegirev.dev)
