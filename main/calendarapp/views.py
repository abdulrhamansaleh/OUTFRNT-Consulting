from django.views.generic import ListView
from calendarapp.models import Event
from calendarapp.utils import Calendar
from calendarapp.forms import EventForm
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import timedelta, datetime, date
import calendar
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse


class AllEventsListView(ListView):
    """ All event list views """
    template_name = 'calendarapp/events_list.html'
    model = Event

    def get_queryset(self):
        return Event.objects.get_all_events(user=self.request.user)


class RunningEventsListView(ListView):
    """ Running events list view """
    template_name = 'calendarapp/events_list.html'
    model = Event

    def get_queryset(self):
        return Event.objects.get_running_events(user=self.request.user)


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


class CalendarView(LoginRequiredMixin, generic.ListView):
    login_url = 'accounts:signin'
    model = Event
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def create_event(request):
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        Event.objects.get_or_create(
            user=request.user,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time
        )
        return HttpResponseRedirect(reverse('calendarapp:calendar'))
    return render(request, 'tasks.html', {'form': form})


class CalendarViewNew(generic.View):
    login_url = 'accounts:signin'

    def get(self, request):
        forms = EventForm
        events = Event.objects.get_all_events(user=request.user)
        events_month = Event.objects.get_running_events(user=request.user)
        event_list = []
        for event in events:
            event_list.append({
                'title': event.title,
                'start': event.start_time.date().strftime("%Y-%m-%dT%H:%M:%S"),
                'end': event.end_time.date().strftime("%Y-%m-%dT%H:%M:%S"),
            })
        variables = {
            'form': forms,
            'events': event_list,
            'events_month': events_month
        }
        return render(request,'calendarapp/calendar.html', variables)

    def post(self, request):
        forms = EventForm(request.POST)
        if forms.is_valid():
            form = forms.save(commit=False)
            form.user = request.user
            form.save()
            return redirect('calendarapp:calendar')
        variables = {
            'form': forms
        }
        return render(request, 'calendarapp/calendar.html', variables)
