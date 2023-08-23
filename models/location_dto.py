import datetime


class LocationDto:
    id: int = None
    name: str = None
    date_created: datetime = None
    
    def __init__(self, location):

        self.id = location[0]
        self.name = location[1]
        self.date_created = location[2]