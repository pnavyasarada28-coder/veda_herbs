import os
import json
import urllib.request
import urllib.error
import re
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg, Count, Q
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Plant
from .forms import PlantForm

def home(request):
    total_plants = Plant.objects.count()
    
    # Total defined categories
    total_categories = len(Plant.CATEGORY_CHOICES)
    
    # Calculate categories counts from DB
    category_counts_query = Plant.objects.values('category').annotate(count=Count('id'))
    db_counts = {item['category']: item['count'] for item in category_counts_query}
    
    featured_plants = Plant.objects.filter(category__in=['sacred', 'immunity', 'skin'])[:3]
    trending_plants = Plant.objects.filter(category__in=['stress', 'heart', 'digestion', 'anti_inflammatory'])[:6]
    
    # We will estimate medicinal uses count by counting distinct "uses" or a solid default
    medicinal_uses_count = 18
    
    # Build category list with labels and counts for ALL 23 categories
    category_map = dict(Plant.CATEGORY_CHOICES)
    categories_data = []
    for cat_key, cat_label in Plant.CATEGORY_CHOICES:
        count = db_counts.get(cat_key, 0)
        categories_data.append({
            'key': cat_key,
            'label': cat_label,
            'count': count
        })

    # Render landing dashboard
    return render(request, 'home.html', {
        'total_plants': total_plants,
        'total_categories': total_categories,
        'featured_plants': featured_plants,
        'trending_plants': trending_plants,
        'medicinal_uses_count': medicinal_uses_count,
        'categories_list': categories_data,
    })

# Add plant (multi-step form wizard)
@login_required
def add_plant(request):
    if request.method == 'POST':
        form = PlantForm(request.POST)
        if form.is_valid():
            plant = form.save(commit=False)
            plant.is_user_added = True
            plant.save()
            return redirect('plant_list')
    else:
        form = PlantForm()

    return render(request, 'add_plant.html', {'form': form})

# Plant list with search + filter + AJAX support
def plant_list(request):
    plants = Plant.objects.all()

    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    dosha = request.GET.get('dosha', '').strip()

    # Search by multiple names
    if query:
        plants = plants.filter(
            Q(name__icontains=query) |
            Q(scientific_name__icontains=query) |
            Q(sanskrit_name__icontains=query) |
            Q(hindi_name__icontains=query) |
            Q(telugu_name__icontains=query) |
            Q(description__icontains=query) |
            Q(uses__icontains=query)
        )

    # Filter by category
    if category:
        plants = plants.filter(category=category)

    # Filter by Dosha Type (greater than 50 indicates high compatibility)
    if dosha:
        if dosha.lower() == 'vata':
            plants = plants.filter(dosha_vata__lt=40) # Balances Vata (lower score means pacifies it)
        elif dosha.lower() == 'pitta':
            plants = plants.filter(dosha_pitta__lt=40)
        elif dosha.lower() == 'kapha':
            plants = plants.filter(dosha_kapha__lt=40)



    # If it is an AJAX call, return JSON data for instant search
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('format') == 'json':
        category_map = dict(Plant.CATEGORY_CHOICES)
        plants_json = []
        for p in plants:
            plants_json.append({
                'id': p.id,
                'name': p.name,
                'scientific_name': p.scientific_name,
                'sanskrit_name': p.sanskrit_name or '',
                'hindi_name': p.hindi_name or '',
                'telugu_name': p.telugu_name or '',
                'description': p.description,
                'category_label': category_map.get(p.category, p.category),
                'image_url': p.image_url or 'https://images.unsplash.com/photo-1515150144380-bca9f1650ed9?auto=format&fit=crop&q=80&w=600',
            })
        return JsonResponse({'plants': plants_json})

    # Otherwise render normal template
    categories = [{'key': k, 'label': v} for k, v in Plant.CATEGORY_CHOICES]
    return render(request, 'plant_list.html', {
        'plants': plants,
        'categories': categories,
    })

# Plant detail page with related recommendations
def plant_detail(request, id):
    plant = get_object_or_404(Plant, id=id)
    
    # Related plants: same category or similar dosha profile, excluding current plant
    related = Plant.objects.filter(category=plant.category).exclude(id=plant.id)[:3]
    if related.count() < 3:
        # Fallback to general query if not enough in same category
        extra = Plant.objects.exclude(id=plant.id).exclude(id__in=[r.id for r in related])[:3 - related.count()]
        related = list(related) + list(extra)

    return render(request, 'plant_detail.html', {
        'plant': plant,
        'related_plants': related,
    })

# Favourites plant collection page
def favourites(request):
    all_plants = Plant.objects.all()
    return render(request, 'favourites.html', {
        'all_plants': all_plants,
    })


# Delete user-added plants
@login_required
def delete_plant(request, id):
    plant = get_object_or_404(Plant, id=id)
    
    # Check if the plant was added by a user
    if not plant.is_user_added:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("You can only delete plants that were manually added by users.")
        
    if request.method == 'POST':
        plant.delete()
        return redirect('plant_list')
        
    return redirect('plant_detail', id=id)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')