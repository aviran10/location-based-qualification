from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, or_
from postgres_db.models import Base, User, Prospect, UserProspectResult, UserExcludedLocation, UserIncludedLocation, \
    Region, CountryRegion, Country

# Setup engine and session
DATABASE_URL = "postgresql://admin:admin_pass@postgres:5432/SampleadDB"
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def match_prospect_and_set_results():
    # Step 1: Retrieve all prospects from the database
    prospects = session.query(Prospect).all()

    # Step 2: Loop through each prospect and check the user's locations
    for prospect in prospects:
        user_id = prospect.user_id  # Assuming user_id is stored on the prospect record

        # Step 2.1: Get the included and excluded locations for the user
        location_include = {loc.location for loc in
                            session.query(UserIncludedLocation).filter_by(user_id=user_id).all()}
        location_exclude = {loc.location for loc in
                            session.query(UserExcludedLocation).filter_by(user_id=user_id).all()}

        company_country = prospect.company_country
        company_state = prospect.company_state

        # Step 3: Initialize match as False
        is_in_location = False

        # Step 3.1: Check if the company country is in the included locations
        if company_country in location_include:
            is_in_location = True

        # Step 3.2: If the country is the US, check if the combination of country-state is in the included locations
        elif company_country == "US" and f"{company_country}-{company_state}" in location_include:
            is_in_location = True

        # Step 3.3: If the company country is excluded, mark as False
        if company_country in location_exclude:
            is_in_location = False

        # Step 4: Store the result in the UserProspectResult table
        result = UserProspectResult(
            user_id=user_id,
            prospect_id=prospect.prospect_id,
            is_in_location=is_in_location,
            checked_at=datetime.utcnow()
        )
        session.add(result)

    # Step 5: Commit the results to the database
    session.commit()

    print("Matching completed and results stored.")


# Run the matching function
if __name__ == "__main__":
    match_prospect_and_set_results()
