import uuid
from django.http import HttpResponse
from django.shortcuts import render, redirect
from iamusic.models import user_session

sessions = dict()

# Home page
def home(request):
    return render(request, 'index.html', {})

# Create new test session
def new(request):
    if request.method != "POST":
        return HttpResponse("/new should use POST method")
    
    session_id = str(uuid.uuid4())
    sessions[session_id] = user_session.UserSession()
    return redirect('/ask?session=%s' % (session_id,))

# Show existing test session
def ask(request):
    # Fetch session
    session_id = request.GET.get('session')
    if session_id is None or session_id not in sessions:
        return HttpResponse("Invalid session")
    session = sessions[session_id]
    if session.is_finished:
        return redirect('/results?session=%s' % (session_id,))

    # Respond
    return render(request, 'ask.html', {
        'session_id': session_id,
        'yt_shortcode': session.nextYtShortcode(),
        'completed_count': session.completed_count,
        'pred': session.getNextPrediction()
    })

# Submit preference
def submit(request):
    if request.method != "POST":
        return HttpResponse("/submit should use POST method")
    
    # Fetch session
    session_id = request.GET.get('session')
    if session_id is None or session_id not in sessions:
        return HttpResponse("Invalid session")
    session = sessions[session_id]
    if session.is_finished:
        return redirect('/results?session=%s' % (session_id,))

    # Fetch user preference
    preference = request.GET.get('preference')
    if preference != '0' and preference != '1':
        return HttpResponse("Invalid preference")

    # Set preference, fit model and generate next music
    session.setUserPreference(int(preference))
    session.fitUserModel()
    session.generateNextId()

    return redirect('/ask?session=%s' % (session_id,))

# Show existing test results
def results(request):
    # Fetch session
    session_id = request.GET.get('session')
    if session_id is None or session_id not in sessions:
        return HttpResponse("Invalid session")
    session = sessions[session_id]
    if not session.is_finished:
        return redirect('/ask?session=%s' % (session_id,))

    # Respond
    results = session.getResults()
    return render(request, 'results.html', {
        'completed_count': session.completed_count,
        'r_blues': round(results['blues'] * 100.0, 1),
        'r_classical': round(results['classical'] * 100.0, 1),
        'r_country': round(results['country'] * 100.0, 1),
        'r_disco': round(results['disco'] * 100.0, 1),
        'r_hiphop': round(results['hiphop'] * 100.0, 1),
        'r_jazz': round(results['jazz'] * 100.0, 1),
        'r_metal': round(results['metal'] * 100.0, 1),
        'r_pop': round(results['pop'] * 100.0, 1),
        'r_reggae': round(results['reggae'] * 100.0, 1),
        'r_rock': round(results['rock'] * 100.0, 1),
    })