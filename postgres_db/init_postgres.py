import csv
import time
import psycopg2
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Prospect, Country, Region, CountryRegion, UserIncludedLocation, UserExcludedLocation  # Assuming your models are in models.py

# PostgreSQL connection URL
DATABASE_URL = "postgresql://admin:admin_pass@postgres:5432/SampleadDB"


def wait_for_postgres():
    '''
    The function waits to the DB to be ready to set all schemas and data.
    :return:
    '''
    max_retries = 10  # Maximum retries before failing
    retries = 0
    while retries < max_retries:
        try:
            # Try to establish a connection
            conn = psycopg2.connect(DATABASE_URL)
            conn.close()
            print("PostgreSQL is ready!")
            return
        except psycopg2.OperationalError as e:
            retries += 1
            print(f"Waiting for PostgreSQL to be ready... Attempt {retries}/{max_retries}")
            time.sleep(5)  # Sleep for 5 seconds before retrying

    print("PostgreSQL failed to start in the expected time!")
    raise Exception("Could not connect to PostgreSQL within the retry limit.")


# Initialize the database models (tables)
def init_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    print("Database models initialized.")


# Load data from JSON files into the database
def load_data():
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Load country-to-region data from JSON
    with open('/app/db_data/country-to-regions-mapping.json') as f:
        country_data = json.load(f)
        for country_code, regions in country_data.items():
            country = session.query(Country).filter_by(name=country_code).first()
            if not country:
                country = Country(name=country_code)
                session.add(country)

            for region_name in regions:
                region = session.query(Region).filter_by(name=region_name).first()
                if not region:
                    region = Region(name=region_name)
                    session.add(region)

                # Create relationship between country and region
                country_region = CountryRegion(country=country, region=region)
                session.add(country_region)
        session.commit()
        print('Country regions data inserted.')

    # Load user location data from JSON
    with open('/app/db_data/users-locations-settings.json') as f:
        user_data = json.load(f)
        for user_id, location_data in user_data.items():
            user = User(user_id=user_id)
            session.add(user)
            for location in location_data.get("location_include", []):
                if location:
                    user_location = UserIncludedLocation(user=user, location=location)
                    session.add(user_location)
            # handle cases where exclude list is None
            location_exclude = location_data.get("location_exclude")
            if location_exclude is not None:  # Only iterate if it's not None
                for location in location_exclude:
                    user_location = UserExcludedLocation(user=user, location=location)
                    session.add(user_location)
            else:
                # Handle the case when location_exclude is None (just in case)
                print(f"User {user_id} has no location exclusions.")
        session.commit()
        print('User location data inserted.')

    # Load prospects data from CSV
    with open('/app/db_data/prospects.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        # Loop through the CSV and insert records into the Prospect table
        for row in reader:
            # Extract row data
            user_id = row.get("user_id").strip()
            prospect_id = row.get("prospect_id", "").strip()
            company_country = row.get("company_country", "").strip()
            company_state = row.get("company_state", "").strip()

            # Skip if any required field is missing or invalid
            if not user_id or not prospect_id or not company_country or not company_state:
                continue  # Skip this row if data is invalid

            # Create Prospect object
            prospect = Prospect(
                user_id=user_id,
                prospect_id=prospect_id,
                company_country=company_country,
                company_state=company_state
            )

            # Add the prospect to the session
            session.add(prospect)
        # Commit the session to the database to persist changes
        session.commit()
        print('Prospects data inserted.')

    print("ALL data loaded into database.")

    # Close the session when done
    session.close()


def main():
    wait_for_postgres()  # Wait for PostgreSQL to be ready
    init_db()  # Initialize models (tables)
    load_data()  # Load data from JSON files


if __name__ == "__main__":
    main()
