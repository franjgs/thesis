from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render_to_response, redirect

from ratings.models import Story

def index(request):
    try:
        story = Story.objects.get(label = 0)
    except Story.DoesNotExist:
        return render_to_response("ratings/index.html", { 'error_message': 'No unlabeled stories left' })
    else:
        return render_to_response("ratings/index.html", { 'story': story })

def rate(request, story_id):
    story = get_object_or_404(pk = story_id)
    if request.POST['label']:
        story.label = int(request.POST['label'])
        story.save()
    return redirect('index')
