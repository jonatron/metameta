from django.shortcuts import render

from .forms import BaseCarForm, HondaForm, FirstCrazyForm, SecondCrazyForm, CustomMetaForm


def cars(request):
    if request.method == 'POST':
        form = HondaForm(data=request.POST)
    else:
        form = HondaForm()

    # if request.method == 'POST':
    #     form = FirstCrazyForm(data=request.POST)
    # else:
    #     form = FirstCrazyForm()

    # if request.method == 'POST':
    #     form = CustomMetaForm(data=request.POST)
    # else:
    #     form = CustomMetaForm()

    # if request.method == 'POST':
    #     form = SecondCrazyForm(data=request.POST)
    # else:
    #     form = SecondCrazyForm()

    # if request.method == 'POST':
    #     form = BaseCarForm(data=request.POST)
    # else:
    #     form = BaseCarForm()

    return render(request, 'cars/cars.html', {'form': form})
