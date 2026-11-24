from abc import ABC, abstractmethod
import random
from datetime import datetime

from .models import Booking, Room, Slot, Login


class EventBus(ABC):
    @abstractmethod
    def add(self, event_type,subscriber):
        pass
    @abstractmethod
    def publish(self,event_type,data):
        pass

class Consumer(ABC):
    @abstractmethod
    def handle_event(self,event_type,data):
        pass

class Publisher(ABC):
    @abstractmethod
    def create(self,id):
        pass


class EventBookingCreated():
    def __init__(self,bookingId):
        self.Id = random.randint(0,99999)
        self.bookingId = bookingId
        self.occuredAt = datetime.now()
        self.type = "BookingCreated"
        


class EventBus(EventBus):
    def __init__(self):
        self.subscribers = {}
    def add(self,event_type,subscriber):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(subscriber)
    def publish(self,event_type,data=None):
        if event_type in self.subscribers:
            for subscriber in self.subscribers[event_type]:
                subscriber.handle_event(event_type, data)

class BookingService(Publisher):
    def create(self,request):
        return EventBookingCreated(request.id)
     
class StaffService(Consumer):
    def __init__(self):
        self.bookingRepo = [] #for simplicity our Booking repo will be separate from real SQL db
    def handle_event(self,event_type,data = None):
        self.bookingRepo.append([data])
     
if __name__ == "__main__":
    myEventBus = EventBus()
    myBookingService = BookingService()
    myStaffService = StaffService()
    
    booking = myBookingService.create(Room.objects[0].id)
    myEventBus.add("BookingCreated",myStaffService)