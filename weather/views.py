import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm
# Create your views here.
def index(request):
	api_key = 'YOUR_API_KEY'
	weather_data=[]
	form=None
	message=''
	if api_key == "YOUR_API_KEY":
		message="Please add your api key"
	else :
		url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid='+api_key
		# print(response.text);
		form =CityForm(request.POST or None)
		if form.is_valid():
			print(request.POST['name'])
			city = request.POST['name']
			response=requests.get(url.format(city)).json()
			print(response)
			if response['cod'] != '404':
				form.save()
			else :
				message=response['message']
		cities=City.objects.all()
		for city in cities:
			response=requests.get(url.format(city)).json()
			city_weather={
				'city' : city.name,
		        'temperature' : response['main']['temp'],
		        'description' : response['weather'][0]['description'],
				'icon' : response['weather'][0]['icon'],
			}
			weather_data.append(city_weather)

	context={
		'data':weather_data,
		'form':form,
		'message':message
	}
	print(message)
	return render(request,'weather/weather.html',context)