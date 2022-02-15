from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.dateparse import parse_date

from .forms import *
from .models import *

# Create your views here.
def info(request):
	if request.method== 'POST':
		form = AvailabilityCheckForm(request.POST)
		if form.is_valid():
			date_in = form.cleaned_data['entry_date']
			date_out= form.cleaned_data['exit_date']

			rooms_available = Room.objects.exclude(reservation__entry_date__range=[date_in , date_out]).exclude(reservation__exit_date__range=[ date_in, date_out])
			print(rooms_available)
			context={
				'form': AvailabilityCheckForm(),
				'rooms':rooms_available,
				'dateIN':date_in,
				'dateOUT': date_out
			}
			return render(request, 'info.html', context )
	else:
		context= {
			'form': AvailabilityCheckForm(),
			'rooms': Room.objects.all()
		}

		return render(request, 'info.html', context )

def reservation(request, date_in, date_out, room_id):
	room = Room.objects.get(id=room_id)
	date_in = parse_date(date_in)
	date_out = parse_date(date_out)
	nights = (date_out - date_in).days
	total_price =  nights * room.price
	context={
		'date1':date_in,
		'date2':date_out,
		'nights':nights,
		'price':total_price,
		'room':room
	}
	if request.method == 'POST':
		new_reservation = Reservation(entry_date=date_in,
									  exit_date=date_out,
									  user=request.user,
									  room=room)
		new_reservation.save()
		messages.success(request, 'Booking done')
		return redirect('info')
	return render(request, 'reservation.html', context)



def login_(request):
	if request.method =='POST':
		print('in post')
		#get the user data
		username = request.POST['username']
		password = request.POST['password']
		print(username)
		#check if the user exists
		user = authenticate(username=username, password=password)
		print(user)
		if user is not None:
			login(request, user=user)
			messages.success(request, 'You are now log in') 
			return redirect('info')
		else :
			messages.error(request, 'Wrong credentials, try again')
			return redirect('login')

	return render(request, 'login.html')


def logout_(request):
	logout(request)
	return redirect('info')

