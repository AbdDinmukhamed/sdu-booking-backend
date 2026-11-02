from django.core.management.base import BaseCommand

from booking_backend.models import Booking, Room, Slot

exampleRooms = [
    {"name": "H102", "building": "Main Building", "floor": 1, "capacity": 80, "equipment": ["Projector", "Whiteboard"], "description": "Standard classroom.", "bookable": True},
    {"name": "F303", "building": "Main Building", "floor": 3, "capacity": 30, "equipment": ["Projector", "Whiteboard"], "description": "Small classroom.", "bookable": True},
    {"name": "I303", "building": "Main Building", "floor": 3, "capacity": 30, "equipment": ["Projector", "Whiteboard"],  "description": "Small far away room", "bookable": False},
    {"name": "F204", "building": "Main Building", "floor": 2, "capacity": 30, "equipment": ["Projector", "Whiteboard"], "description": "Small classroom.", "bookable": True},
    {"name": "D218", "building": "Main Building", "floor": 2, "capacity": 120, "equipment": ["Projector", "Whiteboard", "Air conditioning"], "description": "Large lecture bochka.", "bookable": False},
    {"name": "G304", "building": "Main Building", "floor": 3, "capacity": 100, "equipment": ["Projector", "Whiteboard"], "description": "Large classroom.", "bookable": True},
    {"name": "G108", "building": "Main Building", "floor": 1, "capacity": 24, "equipment": ["Computers", "Projector", "Whiteboard"], "description": "Computer classroom?", "bookable": True},
]

class Command(BaseCommand):
    def handle(self, *args, **options):
        for model in (Booking, Slot, Room):
            model.objects.all().delete()
        
        rooms = []
        
        for room in exampleRooms:
            rooms.append(Room.objects.create(name = room["name"], building = room["building"], floor = room["floor"], capacity = room["capacity"], equipment = room["equipment"], description = room["description"], bookable = room["bookable"]))
        