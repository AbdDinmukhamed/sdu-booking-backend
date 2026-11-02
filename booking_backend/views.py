from django.http import JsonResponse

from .models import Booking, Room, Slot
    
def rooms(request):
    bookableRooms = Room.objects.filter(bookable = True)
    data = []
    
    for room in bookableRooms:
        data.append(room.toJSON())
        
    return JsonResponse(data, safe = False)

def roomDetail(request, room_id):
    room = Room.objects.filter(id = room_id, bookable = True).first()
    
    if room == None:
        return JsonResponse({"error": "Room not found"}, status = 404)
    
    return JsonResponse(room.toJSON())