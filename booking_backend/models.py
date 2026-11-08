from django.db import models


class Login(models.Model):
    login = models.CharField(max_length = 9)
    result = models.IntegerField()
    role = models.CharField(max_length = 20)
    name = models.CharField(max_length = 64)
    
    def toJSON(self):
        return {
            "result": self.result,
            "login": self.login,
            "role": self.role,
            "name": self.name,
        }

class Room(models.Model):
    name = models.CharField(max_length = 16)
    building = models.CharField(max_length = 64)
    floor = models.IntegerField()
    capacity = models.IntegerField()
    equipment = models.JSONField(default = list, blank = True)
    description = models.CharField(max_length = 64, blank = True)
    bookable = models.BooleanField(default = True)
    
    def __str__(self):
        return self.name
    
    def toJSON(self):
        return {
            "id": self.id,
            "name": self.name,
            "building": self.building,
            "floor": self.floor,
            "capacity": self.capacity,
            "equipment": self.equipment,
            "description": self.description,
        }



class Slot(models.Model):
    id = models.CharField(max_length = 16, primary_key = True)
    room = models.ForeignKey(Room, on_delete = models.CASCADE, related_name = "slots")
    start = models.DateTimeField()
    end = models.DateTimeField()
    
    def __str__(self):
        return f"{self.room.name} {self.start}"
        
    def available(self):
        return self.room.bookable
    
    def toJSON(self):
        return {
            "id": self.id,
            "start": self.start.strftime("%Y-%m-%dT%H:%M"),
            "end": self.end.strftime("%Y-%m-%dT%H:%M"),
            "available": self.available(),
        }


class Booking(models.Model):
    PENDING, CONFIRMED, REJECTED, CANCELLED = "pending", "confirmed", "rejected", "cancelled"
    STATUSES = [(PENDING, PENDING), (CONFIRMED, CONFIRMED), (REJECTED, REJECTED), (CANCELLED, CANCELLED)]
    
    room = models.ForeignKey(Room, on_delete = models.CASCADE, related_name = "bookings")
    slot = models.ForeignKey(Slot, on_delete = models.CASCADE, related_name = "bookings")
    status = models.CharField(max_length = 10, choices = STATUSES, default = PENDING)
    requestReason = models.CharField(max_length = 500, blank = True, default = "")
    userLogin = models.CharField(max_length = 64)
    
    def toJSON(self):
        return {
            "id": self.id,
            "roomId": self.room.id,
            "roomName": self.room.name,
            "start": self.slot.start.strftime("%Y-%m-%dT%H:%M"),
            "end": self.slot.end.strftime("%Y-%m-%dT%H:%M"),
            #"requestReason" : self.requestReason,
            "status": self.status,
        }
    