from django.shortcuts import render, get_object_or_404
from .models import Event
from django.core.paginator import Paginator
from core.models import Instructor


def event_list(request):
    events = Event.objects.all()
    
    paginator = Paginator(events, 6) 
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'event-grid.html', {'page_obj': page_obj})

    
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, "event-grid.html", {"event": event})
