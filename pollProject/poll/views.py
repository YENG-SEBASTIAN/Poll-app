from django.shortcuts import render
from django.http import HttpResponse
from .models import Poll
from .forms import CreatePollForm
from django.utils import timezone
from .utils import Utils


# Create your views here.
def index(request):
    return HttpResponse("HEY")

from django.shortcuts import render, redirect
from django.http import HttpResponse


def homeView(request):
    polls = Poll.objects.all()

    context = {
        'polls' : polls
    }
    return render(request, 'poll/home.html', context)

def createPoll(request):
    if request.method == 'POST':
        form = CreatePollForm(request.POST)

        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.verification_code = form_instance.generate_verification_code()
            form_instance.verification_code_expires = timezone.now() + timezone.timedelta(minutes=15)
            form_instance.save()

            email = form_instance['email']
            polls = Poll.objects.filter(email=email)
            context = {
                'polls' : polls
            }
            return render(request, 'poll/home.html', context)
    else:
        form = CreatePollForm()

    context = {'form' : form}
    return render(request, 'poll/create.html', context)

def resultsView(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    if timezone.now() > poll.verification_code_expires:
        address = poll.email
        code = poll.verification_code
        content = f"Use this code {code} to activate your session and continue"
        details = {"to_email":address, "text_content": content}
        Utils.send_message(details)
        return redirect("expired_session")
    
    context = {
        'poll' : poll
    }
    return render(request, 'poll/results.html', context)

def vote(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    if request.method == 'POST':

        selected_option = request.POST['poll']
        if selected_option == 'option1':
            poll.option_one_count += 1
        elif selected_option == 'option2':
            poll.option_two_count += 1
        elif selected_option == 'option3':
            poll.option_three_count += 1
        else:
            return HttpResponse(400, 'Invalid form option')
    
        poll.save()

        return redirect('resultsView', poll.id)

    context = {
        'poll' : poll
    }
    return render(request, 'poll/vote.html', context)


def activate_session(request):
    otp = request.POST['otp']
    poll = Poll.objects.get(verification_code=otp)
    if poll:
        poll.verification_code = poll.generate_verification_code()
        poll.verification_code_expires = timezone.now() + timezone.timedelta(minutes=15)
        poll.save()
        return redirect("vote", poll.id)
    return render(request, 'poll/expired.html')


def expired_session(request):
    return render(request, 'poll/expired.html')

def complete(request):
    return render(request, 'poll/complete.html')