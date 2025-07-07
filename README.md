# Is it In Yet? - Real-Time Restock & Deal Alert System

**Is it In Yet?** is a powerful, automated web service that monitors e-commerce product pages and sends real-time alerts to users the moment an item is restocked or goes on sale. Built with a robust Python backend and a clean, user-friendly interface.
## Project Vision

The core problem this service solves is **scarcity and opportunity**. High-demand products (GPUs, limited-edition sneakers, concert tickets, etc.) sell out in seconds. Manually checking for restocks is tedious and ineffective. "Is it In Yet?" automates this process, giving users a competitive advantage by notifying them instantly of availability.

This repository is structured to be a showcase of modern web application development practices, including a scalable application structure, background task processing, secure user authentication, and integration with third-party APIs for payments and notifications.

## Core Features (MVP)

* **Secure User Authentication:** Users can create an account and log in securely. Passwords are fully hashed.
* **Alert Management Dashboard:** A clean dashboard where authenticated users can add, view, and delete product alerts.
* **Real-Time Notifications:** Users receive an email notification the moment a tracked product's status changes from "Out of Stock" to "In Stock".
* **Dynamic Web Scraper:** A robust backend scraper capable of parsing product pages from major e-commerce sites.

## Planned Premium Features

* **Multi-Channel Notifications:** Alerts via SMS and Discord webhooks.
* **Faster Polling Rates:** Premium users' alerts are checked more frequently.
* **Advanced Alert Conditions:** Alerts for price drops below a certain threshold.
* **Subscription Management:** Seamless monthly subscriptions handled by Stripe.

## Tech Stack

This project leverages a modern, scalable Python-based tech stack:

* **Backend:** Python 3
* **Web Framework:** Flask
* **Database:** PostgreSQL (production), SQLite (development) with SQLAlchemy ORM
* **Background Tasks:** Celery with Redis as the message broker
* **Web Scraping:** Playwright
* **User Authentication:** Flask-Login for session management
* **Payments:** Stripe for recurring subscriptions
* **Deployment:** Docker, with plans for Heroku or a similar PaaS

---

### `requirements.txt`

This file lists all the Python packages our project will depend on. This allows anyone (including you on a different machine) to install the exact same environment.

```text
# Core Flask and Web Components
Flask
Flask-SQLAlchemy
Flask-Migrate
Flask-Login
Flask-WTF
python-dotenv

# Background Task Processing
celery
redis

# Web Scraping
playwright

# Utilities
gunicorn # For production deployment
psycopg2-binary # For PostgreSQL
