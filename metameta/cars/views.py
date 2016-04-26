from django.shortcuts import render

from .forms import BaseCarForm


def cars(request):
    if request.method == 'POST':
        form = BaseCarForm(data=request.POST)
    else:
        form = BaseCarForm()

    return render(request, 'cars/cars.html', {'form': form})
