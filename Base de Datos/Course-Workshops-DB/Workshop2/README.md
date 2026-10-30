# Relational Algebra and ER Diagram

## Overview

This project is part of a workshop for **Databases Foundations** (Season 2024-III) at **Universidad Distrital Francisco José de Caldas**. It focuses on practicing relational algebra queries based on the design of an apartment management system database and creating an Entity-Relationship (ER) diagram to illustrate the relationships between entities in the database.

### Key Objectives:
1. **Relational Algebra Queries**: Write relational algebra expressions to extract meaningful information from the provided database tables. For each query, a result table is generated to validate the solution.
   
2. **Entity-Relationship Diagram**: Create an ER diagram showing the relationships between the tables used in the queries. This step helps to visualize the structure and relationships of the entities in the system.

## Files

1. **relational_algebra_queries.pdf**: This document contains the following relational algebra queries:
   - Queries based on apartment information (e.g., filtering apartments by area, rooms, and owners).
   - Queries based on owner data (e.g., filtering owners by age, number of children, and pets).
   - Queries based on reservation data (e.g., filtering reservations by date, apartment number, and common space).
   
2. **ER_diagram.png**: An entity-relationship diagram showing the structure of the database. The diagram includes the following entities:
   - **Apartment**: Represents the apartment details (number, block, area, owner, and rooms).
   - **Owner**: Represents the apartment owners (name, age, number of children, and pets).
   - **Reservations**: Represents reservation data (apartment number, owner, date, and common space).
   - **Public Services**: Represents public services available in the apartments (water, electricity, gas).

## Relational Algebra Queries

The following types of queries were written using relational algebra:

1. **Apartment Queries**:
   - Select apartments with an area greater than 50.
   - Select apartments with more than 2 rooms but fewer than 4.
   - Filter apartments based on the area between 40 and 70.
   - List apartments owned by people with "Van Halen" in their name.
   - Show apartments with an area greater than 60 and all available public services.

2. **Owner Queries**:
   - Select owners older than 50 years.
   - List owners with 1 to 3 children.
   - Filter owners based on age and the number of children and pets.
   
3. **Reservation Queries**:
   - Show reservations for the date 2020-01-01.
   - Select reservations made after a specific date and with certain criteria (e.g., pool, apartment number).
   - Show all reservations by reservation ID and common space.

## Entity-Relationship Diagram

The ER diagram provides a visual representation of how the entities are connected:

1. **Owner** has a one-to-many relationship with **Apartment** (a single owner can have multiple apartments).
2. **Apartment** has a one-to-many relationship with **Reservations** (an apartment can have multiple reservations).
3. **Owner** also has a one-to-many relationship with **Reservations** (a single owner can make multiple reservations).
4. **Apartment** and **PublicServices** have a many-to-many relationship (an apartment can have multiple services, and a service can be available to multiple apartments).

## How to Use

1. **Relational Algebra Queries**: You can use the queries provided in `relational_algebra_queries.pdf` to practice relational algebra operations on the provided database structure.
   
2. **ER Diagram**: The ER diagram (`ER_diagram.png`) helps you understand the relationships between the entities and how data is organized in this system.

3. **Database**: Although no actual database is provided, the relational algebra expressions and ER diagram offer a blueprint to implement the database schema and extract useful information.
