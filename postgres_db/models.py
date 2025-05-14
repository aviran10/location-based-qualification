from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

# Create a base class for the models
Base = declarative_base()


# Country table
class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)  # Country name (e.g., US)

    # Relationship with country_regions (many-to-many via country_regions)
    country_regions = relationship('CountryRegion', back_populates="country")

    # Relationship with regions (many-to-many via country_regions)
    regions = relationship('Region', secondary='country_regions', back_populates="countries")

    def __repr__(self):
        return f"<Country(name={self.name})>"


# Region table
class Region(Base):
    __tablename__ = 'regions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)  # Region name (e.g., "APJ", "Oceania")

    # Relationship with country_regions (many-to-many via country_regions)
    country_regions = relationship('CountryRegion', back_populates="region")

    # Relationship with countries (many-to-many via country_regions)
    countries = relationship('Country', secondary='country_regions', back_populates="regions")

    def __repr__(self):
        return f"<Region(name={self.name})>"


# Country-Region table (join of country and region tables)
class CountryRegion(Base):
    __tablename__ = 'country_regions'

    country_id = Column(Integer, ForeignKey('countries.id'), primary_key=True)
    region_id = Column(Integer, ForeignKey('regions.id'), primary_key=True)

    # Relationships
    country = relationship('Country', back_populates="country_regions")
    region = relationship('Region', back_populates="country_regions")


# User table
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, unique=True, nullable=False)

    # Relationships
    included_locations = relationship('UserIncludedLocation', back_populates="user")
    excluded_locations = relationship('UserExcludedLocation', back_populates="user")

    # Relationship with Prospect (a user can have multiple prospects)
    prospects = relationship('Prospect', back_populates='user')

    def __repr__(self):
        return f"<User(user_id={self.user_id})>"


# User included location
class UserIncludedLocation(Base):
    __tablename__ = 'user_included_locations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    location = Column(String, nullable=False)

    # Relationship with User
    user = relationship('User', back_populates="included_locations")

    def __repr__(self):
        return f"<UserIncludedLocation(user_id={self.user_id}, location={self.location})>"


# User excluded locations
class UserExcludedLocation(Base):
    __tablename__ = 'user_excluded_locations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    location = Column(String, nullable=False)

    # Relationship with User
    user = relationship('User', back_populates="excluded_locations")

    def __repr__(self):
        return f"<UserExcludedLocation(user_id={self.user_id}, location={self.location})>"


# Prospect table
class Prospect(Base):
    __tablename__ = 'prospects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    prospect_id = Column(String, unique=True, nullable=False)
    user_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    company_country = Column(String, nullable=False)
    company_state = Column(String, nullable=False)

    # Relationship with User
    user = relationship('User', back_populates="prospects")

    def __repr__(self):
        return f"<Prospect(prospect_id={self.prospect_id}, company_country={self.company_country}, company_state={self.company_state})>"


# User-Prospect Result table
class UserProspectResult(Base):
    __tablename__ = 'user_prospect_results'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    prospect_id = Column(String, ForeignKey('prospects.prospect_id'), nullable=False)
    is_in_location = Column(Boolean, nullable=False)  # True or False
    checked_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship('User', backref='user_prospect_results')
    prospect = relationship('Prospect', backref='user_prospect_results')

    def __repr__(self):
        return f"<UserProspectResult(user_id={self.user_id}, prospect_id={self.prospect_id}, is_in_location={self.is_in_location}, checked_at={self.checked_at})>"

