from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Poll
from .forms import CreatePollForm
from django.utils import timezone
from .utils import Utils
from django.http import HttpResponse
from rest_framework.decorators import api_view
from .serializers import PollSerializer


#view to diaplay all polls
@api_view(["GET"])
def homeView(request):
    polls = Poll.objects.all()

    context = {
        'polls' : polls
    }
    return render(request, 'poll/home.html', context)


#creating a poll view
def createPoll(request):
    if request.method == 'POST':
        form = CreatePollForm(request.POST)

        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.verification_code = form_instance.generate_verification_code()
            form_instance.verification_code_expires = timezone.now() + timezone.timedelta(minutes=600)
            form_instance.save()

            polls = Poll.objects.all()
            email = form_instance.email
            if polls:
                #get created poll
                created_poll = Poll.objects.get(email=email)
                serializer = PollSerializer(created_poll)
                id = serializer.data['id']
                scheme = request.scheme
                hostname = request.get_host()
                absolute_url_with_hostname = f"{scheme}://{hostname}/vote/{id}/"
                #send poll link to PC through their emails
                subject = "Poll link"
                content = f"Please use this link to cast your vote on the poll app {absolute_url_with_hostname}"
                details = {"subject":subject, "to_email":email, "text_content": content}
                Utils.send_message(details)
            context = {
                'polls' : polls
            }
            return render(request, 'poll/home.html', context)
    else:
        form = CreatePollForm()

    context = {'form' : form}
    return render(request, 'poll/create.html', context)


#results view
def resultsView(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    if timezone.now() > poll.verification_code_expires:
        subject = "One Time Pin"
        address = poll.email
        code = poll.verification_code
        content = f"Please use this code {code} to activate your session and continue"
        details = {"subject":subject, "to_email":address, "text_content": content}
        Utils.send_message(details)
        return redirect("expired_session")
    
    context = {
        'poll' : poll
    }
    return render(request, 'poll/results.html', context)


#view for casting vote
def vote(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    if poll.isOpen == False:
        return redirect("complete", poll.id)

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
    if request.method == "POST":
        otp = request.POST['otp']
        poll = Poll.objects.get(verification_code=otp)
        if poll:
            poll.verification_code = poll.generate_verification_code()
            poll.verification_code_expires = timezone.now() + timezone.timedelta(minutes=600)
            poll.save()
            return redirect("resultsView", poll.id)
    return render(request, 'poll/expired.html')


#view to return expired template for user to enter OTP code
def expired_session(request):
    return render(request, 'poll/expired.html')

#view to return open poll template for user to enter OTP code
def openPollTemplate(request):
    return render(request, 'poll/openPoll.html')


#vote complete view
@api_view(["GET"])
def complete(request, poll_id):
    poll = Poll.objects.get(id=poll_id)
    return render(request, 'poll/complete.html')

#view to open poll again
def openPollView(request):
    if request.method == "POST":
        otp = request.POST['otp']
        poll = Poll.objects.get(verification_code=otp)
        if poll.verification_code ==  otp:
            poll.isOpen = True
            poll.verification_code = poll.generate_verification_code()
            poll.verification_code_expires = timezone.now() + timezone.timedelta(minutes=600)
            poll.save()
            return redirect("homeView")
    return render(request, 'poll/openPoll.html')

#view to send otp code to reopen poll
def sendOpenPollCode(request, poll_id):
    poll = Poll.objects.get(id=poll_id)
    if poll.isOpen == False:
        subject = "Open poll verification"
        address = poll.email
        code = poll.verification_code
        content = f"Please use this code {code} to verify your identity"
        details = {"subject":subject, "to_email":address, "text_content": content}
        Utils.send_message(details)
        return redirect("openPollTemplate")
    return render(request, 'poll/openPoll.html')


#view to end poll and send link to user
def endPoll(request, poll_id):
    poll = Poll.objects.get(id=poll_id)
    if poll:
        poll.isOpen = False
        poll.save()
        poll_results = Poll.objects.get(email=poll.email)
        serializer = PollSerializer(poll_results)
        id = serializer.data['id']
        scheme = request.scheme
        hostname = request.get_host()
        absolute_url_with_hostname = f"{scheme}://{hostname}/resultsView/{id}/"
        #send poll link to PC through their emails
        subject = "View results"
        content = f"Please use this link to view the poll results {absolute_url_with_hostname}"
        details = {"subject":subject, "to_email":poll.email, "text_content": content}
        Utils.send_message(details)
        return redirect("homeView")
    return render(request, 'poll/complete.html')