from sqlalchemy import create_engine, Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from schema_setup import Weather


Base = declarative_base()


class WeatherDataGateway:
    def __init__(self, db_path):
        self.engine = create_engine(db_path)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_data(self, date, sunshine_duration, location_id, daylight_duration):
        try:
            weather = Weather(
                date=date,
                sunshine_duration=sunshine_duration,
                location_id=location_id,
                daylight_duration=daylight_duration,
            )
            self.session.add(weather)
            self.session.commit()
            return weather.id
        except Exception as e:
            print("Error:", e)
            self.session.rollback()
            return None

    def get_all_weather_data(self):
        try:
            weather = self.session.query(Weather).all()
            return [
                {
                    "id": item.id,
                    "location_id": item.location_id,
                    "date": item.date,
                    "sunshine_duration": item.sunshine_duration,
                    "daylight_duration": item.daylight_duration,
                }
                for item in weather
            ]
        except Exception as e:
            print("Error:", e)
            self.session.rollback()
            return None

    def get_weather_data_by_location(self, location_id):
        try:
            weather = self.session.query(Weather).filter_by(location_id=location_id)
            return [
                {
                    "id": item.id,
                    "location_id": item.location_id,
                    "date": item.date,
                    "sunshine_duration": item.sunshine_duration,
                    "daylight_duration": item.daylight_duration,
                }
                for item in weather
            ]
        except Exception as e:
            print("Error:", e)
            self.session.rollback()
            return None
