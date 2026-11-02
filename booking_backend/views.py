from django.http import JsonResponse

from .models import Booking, Room, Slot
    
def rooms(request):
    bookableRooms = Room.objects.filter(bookable = True)
    data = []
    
    for room in bookableRooms:
        data.append(room.toJSON())
        
    return JsonResponse(data, safe = False)