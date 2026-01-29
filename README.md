# Webhook Repo

This repository contains a Flask application that receives GitHub webhook events from a separate action repository, processes them, stores minimal event data in MongoDB, and displays the activity on a simple UI.

## Features
- Receives GitHub webhook events (Push, Pull Request, Merge)
- Extracts only required fields from webhook payloads
- Stores events in MongoDB
- Displays repository activity on a UI that polls every 15 seconds

## Tech Stack
- Flask
- MongoDB
- GitHub Webhooks
- HTML & JavaScript

## Application Flow
1. A developer performs an action (push, pull request, merge) on the action repository.
2. GitHub sends a webhook event to this Flask application.
3. The application extracts minimal required data and stores it in MongoDB.
4. The UI polls the backend every 15 seconds to display the latest activity.

## Running the Application
1. Start MongoDB on `localhost:27017`
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
