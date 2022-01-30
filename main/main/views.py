from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from calendarapp.models import Event

@login_required(login_url = 'accounts/signin.html')
def DashBoardView(request):
    user = request.user 
    # check if user is allowed to view the site
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
    
    # if user is not the right permission return them home
    else:
        return redirect('accounts:home')
