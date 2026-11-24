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
    def getData(self):
        return [self.Id,self.bookingId,self.occuredAt]
        


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
            return True

class BookingService(Publisher):
    def create(self,request):
        return EventBookingCreated(request.id)
     
class StaffService(Consumer):
    def __init__(self):
        self.proccessedEvents = []
    def handle_event(self,event_type,data = None):
        if data[0] in self.proccessedEvents:
            print("CONSUMER: Event was already published, aborting")
            return
        auditRepository = Booking(id = data[1], room = Slot.objects.get(id = f"{data[1]}-1").room, slot = Slot.objects.get(id = f"{data[1]}-1"), userLogin = "test", status = Booking.PENDING)
        auditRepository.save()
        self.proccessedEvents.append(data[0])
        