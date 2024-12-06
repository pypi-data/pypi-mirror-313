from kerykeion import AstrologicalSubject
from kerykeion.utilities import get_houses_list, get_available_planets_list
from typing import Union
from kerykeion.kr_types.kr_models import AstrologicalSubjectModel
import json


class Report:
    """
    Create a report for a Kerykeion instance in JSON format.
    """

    def __init__(self, instance: Union[AstrologicalSubject, AstrologicalSubjectModel]):
        self.instance = instance

    def get_report_title(self) -> str:
        return f"Kerykeion report for {self.instance.name}"

    def get_data(self) -> dict:
        """
        Creates the main data section of the report.
        """
        return {
            "date": f"{self.instance.day}/{self.instance.month}/{self.instance.year}",
            "time": f"{self.instance.hour}:{self.instance.minute}",
            "location": f"{self.instance.city}, {self.instance.nation}",
            "longitude": self.instance.lng,
            "latitude": self.instance.lat,
        }

    def get_planets_data(self) -> list:
        """
        Creates the planets section of the report.
        """
        return [
            {
                "planet": planet.name,
                "sign": planet.sign,
                "position": round(float(planet.position), 2),
                "retrograde": planet.retrograde,
                "house": planet.house,
            }
            for planet in get_available_planets_list(self.instance)
        ]

    def get_houses_data(self) -> list:
        """
        Creates the houses section of the report.
        """
        return [
            {
                "house": house.name,
                "sign": house.sign,
                "position": round(float(house.position), 2),
            }
            for house in get_houses_list(self.instance)
        ]

    def get_full_report(self) -> dict:
        """
        Returns the full report in JSON format.
        """
        return {
            "title": self.get_report_title(),
            "data": self.get_data(),
            "planets": self.get_planets_data(),
            "houses": self.get_houses_data(),
        }

    def print_report(self) -> None:
        """
        Prints the JSON report.
        """
        print(json.dumps(self.get_full_report(), indent=4))


if __name__ == "__main__":
    from kerykeion.utilities import setup_logging
    setup_logging(level="debug")

    john = AstrologicalSubject("John", 1975, 10, 10, 21, 15, "Roma", "IT")
    report = Report(john)
    report.print_report()
