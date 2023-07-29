import random
import uuid


class Schema:
    """
    This class defines the Schema class which has a method
    to generate random schema names.
    """

    @staticmethod
    def generate_schema_name(university_name):
        return f"{university_name.replace(' ', '').upper()}{random.randint(100, 999)}"

    @staticmethod
    def generate_uuid():
        return uuid.uuid4()
