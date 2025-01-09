from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import FoodStock, FeedingLog

def my_view(request):
    current_stock = FoodStock.objects.first()
    logs = FeedingLog.objects.all().order_by('-timestamp')  # Сортировка по времени (последние действия сверху)
    return render(request, 'food_tracker/index.html', {
        'current_stock': current_stock.quantity if current_stock else 0,
        'logs': logs
    })

def add_food(request):
    if request.method == 'POST':
        amount = float(request.POST.get('amount', 0))
        food_stock, created = FoodStock.objects.get_or_create(id=1)
        food_stock.quantity += amount
        food_stock.save()

        # Записываем лог
        FeedingLog.objects.create(action='add', amount=amount)

        return redirect('index')
    else:
        return render(request, 'food_tracker/add_food.html')

def feed_cat(request):
    if request.method == 'POST':
        amount = float(request.POST.get('amount', 0))
        food_stock, created = FoodStock.objects.get_or_create(id=1)
        if food_stock.quantity >= amount:
            food_stock.quantity -= amount
            food_stock.save()

            # Записываем лог
            FeedingLog.objects.create(action='feed', amount=amount)

            return redirect('index')
        else:
            return render(request, 'food_tracker/feed_cat.html', {'error': 'Not enough food'})
    else:
        return render(request, 'food_tracker/feed_cat.html')