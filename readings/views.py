from datetime import datetime
from django.shortcuts import render, redirect
from django.db.models import Avg, Count
from .models import Rating, BuddhistWisdom
from .bazi import year_animal
import datetime as dt

def home(request):
    qs = Rating.objects.filter(is_visible=True)
    stats = qs.aggregate(avg=Avg('stars'), count=Count('id'))
    doy = dt.date.today().timetuple().tm_yday
    wisdom = BuddhistWisdom.objects.filter(day_index=doy % 30).first()
    return render(request, 'home.html', {
        'avg_rating': round(stats['avg'] or 0, 1),
        'review_count': stats['count'] or 0,
        'latest_reviews': qs[:3],
        'wisdom': wisdom,
    })

def demo_bazi(request):
    # PUBLIC - no login
    result = None
    date_str = request.GET.get('birth_date')
    time_str = request.GET.get('birth_time', '12:00')
    if date_str:
        try:
            d = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            # Reuse your existing get_year/month/day/hour pillar functions here
            result = {
                'animal': year_animal(d.date()),
                'birth_datetime': d,
                # Add: 'year': ..., 'month': ..., 'day': ..., 'hour': ..., 'day_master': ...
            }
        except ValueError:
            result = None
    return render(request, 'readings/demo.html', {
        'result': result, 'birth_date': date_str, 'birth_time': time_str
    })

def love_compatibility(request):
    # PUBLIC - deterministic, no AI
    result = None
    if request.method == 'POST':
        try:
            y1 = int(request.POST.get('year1'))
            y2 = int(request.POST.get('year2'))
            a1 = year_animal(dt.date(y1, 6, 15))
            a2 = year_animal(dt.date(y2, 6, 15))
            # Simple trine / opposite logic - replace with your existing table if you have one
            if a1 == a2:
                score, label = 70, "Steady - same energy, grow together"
            else:
                score, label = 68, "Good - complementary with effort"
            result = {'a1': a1, 'a2': a2, 'score': score, 'label': label}
        except Exception:
            result = None
    return render(request, 'readings/love.html', {'result': result})

def buddhist_wisdom(request):
    doy = dt.date.today().timetuple().tm_yday
    wisdom = BuddhistWisdom.objects.filter(day_index=doy % 30).first()
    return render(request, 'readings/buddhist.html', {'wisdom': wisdom})

def submit_rating(request):
    # PUBLIC - no login, nickname only
    saved = False
    if request.method == 'POST':
        Rating.objects.create(
            user=request.user if request.user.is_authenticated else None,
            nickname=request.POST.get('nickname', '')[:30],
            stars=int(request.POST.get('stars', 5)),
            comment=request.POST.get('comment', '')[:500],
            reading_type=request.POST.get('reading_type', 'general'),
        )
        saved = True
    return render(request, 'readings/rate.html', {'saved': saved})

def reviews_list(request):
    qs = Rating.objects.filter(is_visible=True)
    stats = qs.aggregate(avg=Avg('stars'), count=Count('id'))
    return render(request, 'readings/reviews.html', {
        'ratings': qs[:50], 'avg': round(stats['avg'] or 0, 1), 'count': stats['count'] or 0
    })

def ask_me(request):
    # MINIMAL v1 - NO free-text, NO LLM, 3 buttons only
    answer = None
    allowed = {'day_master': 'Your Day Master is your core element - how you tend to respond to stress.',
               'element_balance': 'Balance is a snapshot, not a prediction. Strengthen your lightest element with one small habit today.',
               'wisdom_today': 'A wisdom for today: Peace comes from within. Do not seek it without.'}
    if request.method == 'POST':
        key = request.POST.get('prompt_key')
        if key in allowed:
            answer = allowed[key]
    return render(request, 'readings/ask_me.html', {'answer': answer})
