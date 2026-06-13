# Smallpost
A minimal post application built with Docker and Flask. 

## Description
Smallpost is a lightweight API that allows users to create and retrieve posts. It is designed to demonstrate a simple backend architecture using Flask and MySQL, fully containerized with Docker.

## Motivation
This is a personal project created to explore Docker and Flask in a practical way.
There are likely areas for improvement — feedback and suggestions are welcome!

## Tech Stack
- **Backend:** Flask v3.1.2 + Python v3.12
- **Database:** MySQL
- **Containerization:** Docker + Docker Compose

## Requirements
- Docker
- Docker Compose

## Getting Started
1.  Copy the `.env.example` file and rename it to `.env`.
2. Create a folder named `db/`
3. Inside it, create a file called `password.txt`
4. Add your database password to that file.

Then run:
```bash
docker compose up --build
```
Docker Compose will use the default configuration values defined in the .env file to start the application.