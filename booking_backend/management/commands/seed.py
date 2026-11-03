import datetime
from django.core.management.base import BaseCommand

from booking_backend.models import Booking, Room, Slot

exampleRooms = [
    {
    "name": "H102", 
    "building": "Main Building", 
    "floor": 1, 
    "capacity": 80, 
    "equipment": ["Projector", "Whiteboard"], 
    "description": "Standard classroom.", 
    "bookable": True
    },
    
    {
    "name": "F303", 
    "building": "Main Building", 
    "floor": 3, 
    "capacity": 30, 
    "equipment": ["Projector", "Whiteboard"], 
    "description": "Small classroom.", 
    "bookable": True
    },
    
    {
    "name": "I303", 
    "building": "Main Building", 
    "floor": 3, 
    "capacity": 30, 
    "equipment": ["Projector", "Whiteboard"],  
    "description": "Small far away room", 
    "bookable": True
    },
    
    {
    "name": "F204", 
    "building": "Main Building", 
    "floor": 2, 
    "capacity": 30, 
    "equipment": ["Projector", "Whiteboard"], 
    "description": "Small classroom.", 
    "bookable": True
    },
    
    {
    "name": "D218", 
    "building": "Main Building", 
    "floor": 2, 
    "capacity": 120, 
    "equipment": ["Projector", "Whiteboard", "Air conditioning"], 
    "description": "Large lecture bochka.", 
    "bookable": True
    },
    
    {
    "name": "G304", 
    "building": "Main Building", 
    "floor": 3, 
    "capacity": 100, 
    "equipment": ["Projector", "Whiteboard"], 
    "description": "Large classroom.", 
    "bookable": True
    },
    
    {
    "name": "G108", 
    "building": "Main Building", 
    "floor": 1, 
    "capacity": 24, 
    "equipment": ["Computers", "Projector", "Whiteboard"], 
    "description": "Computer classroom?", 
    "bookable": True
    },
    
]

exampleTime = [
    (datetime.time(9, 30), datetime.time(10, 20)),  
    (datetime.time(10, 30), datetime.time(11, 20)), 
    (datetime.time(11, 30), datetime.time(12, 20)), 
    (datetime.time(12, 30), datetime.time(13, 20))
    ]

class Command(BaseCommand):
    def handle(self, *args, **options):
        for model in (Booking, Slot, Room):
            model.objects.all().delete()
        
        rooms = []
        
        for room in exampleRooms:
            rooms.append(
                Room.objects.create(
                    name = room["name"], 
                    building = room["building"], 
                    floor = room["floor"], 
                    capacity = room["capacity"], 
                    equipment = room["equipment"], 
                    description = room["description"], 
                    bookable = room["bookable"])
                )
        
        day = datetime.date.today()

        for room in rooms:
            n = 0
            for start, end in exampleTime:
                n += 1
                Slot.objects.create(
                    id = f"{room.id}-{n}", 
                    room = room, 
                    start = datetime.datetime.combine(day, start), 
                    end = datetime.datetime.combine(day, end)
                )
        
        
        s1 = Slot.objects.get(id = f"{rooms[1].id}-1")
        s2 = Slot.objects.get(id = f"{rooms[2].id}-2")
        s3 = Slot.objects.get(id = f"{rooms[4].id}-3")
        
        Booking.objects.create(room = s1.room, slot = s1, userLogin = "240107001", status = Booking.CONFIRMED, requestReason = "we want to celebrate birthday of our friend, there will be 12 of us there")
        Booking.objects.create(room = s2.room, slot = s2, userLogin = "240107002", status = Booking.PENDING,requestReason = "we need to discuss future plans of our team project in person on site")
        Booking.objects.create(room = s3.room, slot = s3, userLogin = "240107003", status = Booking.PENDING, requestReason = "all the lecture halls are full, please help us we need to study")