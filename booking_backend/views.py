from django.http import JsonResponse

from .models import Booking, Room, Slot, Login
from .sdu_api import *

#results: integer returning status of SDU response
#0: login and password is found, role is correct
#1: login or password is not correct
#2: role is not correct
def login(request):
    if request.method == "POST":
        result = 0
        username = request.POST.get("login")
        password = request.POST.get("password")
        role = request.POST.get("role")
        hasAccount = 0
        account = 0
        while account < len(TEST_USERS):
            if TEST_USERS[account]["login"] == username and TEST_USERS[account]["password"] == password:
                hasAccount = 1
                break
            account += 1
        if hasAccount == 0:
            result = 1
        if TEST_USERS[account]["role"] != role:
            result = 2
        response = Login.objects.create(result = result, login = username, role = role, name = TEST_USERS[account]["name"])
        
            
        return JsonResponse(response.toJSON())
    return JsonResponse({"error": "incorrect method, login awaits POST request"}, status = 404)



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
    
def roomSlots(request, room_id):
    if Room.objects.filter(id = room_id, bookable = True).exists() != True:
        return JsonResponse({"error": "Room not found"}, status = 404)
    
    slots = Slot.objects.filter(room_id = room_id)
    
    response = []
    for s in slots:
        response.append(s.toJSON())
    
    return JsonResponse(response, safe = False)


def bookings(request):
    if request.method == "GET":
        qs = Booking.objects.select_related("room", "slot")
        
        response = []
        for booking in qs:
            response.append(booking.toJSON())
            
        return JsonResponse(response, safe = False)