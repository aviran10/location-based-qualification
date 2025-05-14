# Prospect Matching Project

## Overview
This project aims to match user prospects based on location and other attributes, providing an efficient way to evaluate and store matched results.

## Setup

1. Clone the repository:
git clone <repository-url>
cd <project-directory>


### 2. Ensure Docker is running
- Make sure Docker is installed and running on your machine. You can check this by running:
  ```
  docker --version
  ```
- Use Docker Compose to set up the required services (like the database). To start the services, run:
  ```
  docker-compose build
  ```


  
## Database Schema
This project uses the following key tables:
- `users`: Stores user details.
- `prospects`: Contains prospect data.
- `user_included_locations`: Stores locations included for each user.
- `user_excluded_locations`: Stores locations excluded for each user.
- `user_prospect_results`: Contains the results of the matching process.

## Running the Match Process
The match process filters prospects based on user locations (included and excluded). After matching, the results are saved in the `user_prospect_results` table.

## Notes
- Ensure the database is properly set up and populated before running the matching process.
- The project uses SQLAlchemy for ORM-based interactions with the PostgreSQL database.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


