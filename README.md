# Worklife Python Technical test

This project serves as a technical test for middle-senior backend developers in Python. This repository shows my approach to solve the case after joining the backend team as a junior. 

It makes use of FastAPI (and Pydantic), SQLAlchemy (orm), alembic (migrations).
It also uses PostgreSQL as database and poetry for dependency management.

## Overview

You are building an employee vacation handling system to manage leave.

Employees belong to teams. There can be many teams. One employee can belong to only one team.

Employee vacations can be of two types:
* Unpaid leave
* Paid leave

A vacation has:
* A type of vacation (as explained above)
* A start date
* An end date

### Notes

For this project:
* There is no half-day leaves, only complete days.
* There is no employee balance.
* Employees work a typical work week of 5/7 with weekends being on Saturday-Sunday

## The project

You need to create an API to help manage vacations including:
* Models and relationships for the various entities
* Features logic (see below)
* API Endpoints

Your API should be able to handle **at least** the following features:
* Create employees
* Create, update and delete vacations
* Search for employees on vacation given various parameters
* When creating or updating a vacation, if it overlaps (or is contiguous to) another one, merge them into one.
Only works with vacations of the same type, else it will fail (overlaps with another type of vacation).

The current boilerplate should serve as a base to start with.
Feel free to upgrade / downgrade it as you see fit.

#### Bonus features
If you have the time/will, you can implement any (or all) of those features:
* Search employees and vacations by employee name/identifier
* Searching should also return the number of vacation days for each employee (given the search parameters).
* Compare two employees and return the days they will be both on vacation
* Implement a balance, decreasing as an employee takes paid vacations

## Requirements

* docker
* poetry (optional, if you want to add libs)
* make (optional)

## Usage

Depending on your docker and docker-compose setup you might need to use

`docker-compose up -d` or `docker compose up -d`

Once the container run, you should be able to access the docs at http://localhost:880/docs

To create and migrate the database with the migration already added:

First use `make create-db`

Then use `make migrate-db`

If you make modifications/additions to models and want to auto generate migrations you can use. 
Don't forget to migrate the database afterwards.

`make autogenerate-migration revision_message='"your_message"'`
