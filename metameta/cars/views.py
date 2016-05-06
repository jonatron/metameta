from django.shortcuts import render

from .forms import BaseCarForm, FirstCrazyForm, SecondCrazyForm, CustomMetaForm


def cars(request):
    # import pdb; pdb.set_trace()
    if request.method == 'POST':
        form = CustomMetaForm(data=request.POST)
    else:
        form = CustomMetaForm()
    """
    if request.method == 'POST':
        form = SecondCrazyForm(data=request.POST)
    else:
        form = SecondCrazyForm()
    """

    """
    if request.method == 'POST':
        form = FirstCrazyForm(data=request.POST)
    else:
        form = FirstCrazyForm()
    """

    """
    if request.method == 'POST':
        form = BaseCarForm(data=request.POST)
    else:
        form = BaseCarForm()
    """

    return render(request, 'cars/cars.html', {'form': form})
