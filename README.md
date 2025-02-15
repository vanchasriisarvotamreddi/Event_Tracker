# Event Tracker website

## Overview

Event Tracker is a web-based platform designed to streamline the management of college events. It enables organizers to schedule events, manage registrations, track participant attendance, and generate certificates automatically using Django.

## Features

### For Organizers
- Create, modify, and manage events
- Track participants and manage event details
- Mark attendance for registered participants
- Automatically generate and distribute event certificates

### For Students
- View and enroll in college events
- Download certificates once issued
- Manage event participation history

### Additional Features
- Centralized event tracking
- Digital certificate distribution via email
- Secure login for students and event organizers

## Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL
- **Other Tools**:
  - PIL (Python Imaging Library) for certificate generation
  - Cloudinary for image management
  - SMTP for email integration

## System Requirements

### Hardware:
- **RAM**: Minimum 4GB
- **Processor**: Intel i3 or higher
- **Storage**: Minimum 10GB

### Software:
- Python 3.x
- Django (Latest Stable Version)
- PostgreSQL
- VS Code (or any preferred IDE)

## Installation Guide

### Step 1: Clone the Repository
git clone https://github.com/your-username/event-tracker.git
cd event-tracker
text

### Step 2: Set Up a Virtual Environment
For Linux/Mac:
python -m venv venv
source venv/bin/activate
text
For Windows:
python -m venv venv
venv\Scripts\activate
text

### Step 3: Install Dependencies
pip install -r requirements.txt
text

### Step 4: Configure the Database
Open `settings.py` and update the database settings with your PostgreSQL credentials:
DATABASES = {
'default': {
'ENGINE': 'django.db.backends.postgresql',
'NAME': 'your_database_name',
'USER': 'your_database_user',
'PASSWORD': 'your_database_password',
'HOST': 'localhost',
'PORT': '5432',
}
}
text

### Step 5: Run Database Migrations
python manage.py makemigrations
python manage.py migrate
text

### Step 6: Create a Superuser (Admin Access)
python manage.py createsuperuser
text
Follow the prompts to set up the superuser.

### Step 7: Start the Server
python manage.py runserver
text

### Step 8: Access the Application
Open your browser and navigate to: `http://127.0.0.1:8000/`

## How to Use

### Admin
- Create and manage event organizers
- Oversee system operations and user activities

### Event Organizers
- Add and manage events
- Track participants and mark attendance
- Generate and distribute certificates

### Students
- Browse available events and register
- Download event certificates from their dashboard
