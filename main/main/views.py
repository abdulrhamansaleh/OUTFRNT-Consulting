# django imports
from django.shortcuts import render
from django.shortcuts import redirect

# authenticate imports
from django.contrib.auth.decorators import login_required

# data-model imports
from calendarapp.models import Event

@login_required(login_url = '/signin/')
def DashBoardView(request):
    user = request.user 
    if user.is_client:
        events = Event.objects.get_all_events(user=request.user)
        running_events = Event.objects.get_running_events(user=request.user)
        latest_events = Event.objects.filter(
            user=request.user
        ).order_by('-id')[:10]
        variables = {
                'total_event': events.count(),
                'running_events': running_events,
                'latest_events': latest_events
            }
        return render(request, 'calendarapp/dashboard.html', variables)
    else:
        return redirect('accounts:home')