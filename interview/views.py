from django.shortcuts import render,redirect
from .models import Candidate,Interviewer,Interview,Feedback
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User ,Group


def home(request):
    candidates = Candidate.objects.all()
    interviewers=Interviewer.objects.all()
    interviews=Interview.objects.all()

    return render(request, 'home.html', {'candidates': candidates,'interviewers':interviewers, 'interviews':interviews})
@login_required
def dashboard(request):
    candidate_count=Candidate.objects.count()
    interview_count=Interview.objects.count()
    interviewer_count=Interviewer.objects.count()
    return render(request,'dashboard.html',{'candidate_count':candidate_count,'interview_count':interview_count,'interviewer_count':interviewer_count})

def schedule_interview(request):
    candidates = Candidate.objects.all()
    interviewers = Interviewer.objects.all()

    if request.method == 'POST':
        candidate_id = request.POST['candidate']
        interviewer_id = request.POST['interviewer']
        interview_date = request.POST['interview_date']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        mode = request.POST['mode']
        meeting_link=request.POST.get('meeting_link', '')
        existing_interview=Interview.objects.filter(interviewer_id=interviewer_id,
                                                    interview_date=interview_date,
                                                    start_time__lt=end_time,
                                                    end_time__gt=start_time).exists()
        
        if existing_interview:
            return render(request,'schedule.html',{'candidates': candidates,
                    'interviewers': interviewers, 'error':'Interviewer is already busy at this time.'})

        Interview.objects.create(
            candidate_id=candidate_id,
            interviewer_id=interviewer_id,
            interview_date=interview_date,
            start_time=start_time,
            end_time=end_time,
            mode=mode,
            meeting_link=meeting_link
        )
        return redirect('/dashboard/')

    return render(request,'schedule.html',{'candidates': candidates,
                        'interviewers': interviewers})
@login_required
def interviewer_dashboard(request):
    interviewer = Interviewer.objects.get(user=request.user)
    interviews = Interview.objects.filter( interviewer=interviewer)

    return render(request, 'interviewer_dashboard.html', {'interviews': interviews})


def feedback (request,interview_id):
    interview=Interview.objects.get(id=interview_id)
    if request.method == 'POST':
        Feedback.objects.create(
                        interview=interview,
                        technical_rating=request.POST['technical_rating'],
                        communication_rating=request.POST['communication_rating'],
                        problem_solving_rating=request.POST['problem_solving_rating'],
                        overall_rating=request.POST['overall_rating'],
                        recommendation=request.POST['recommendation'],
                        comments=request.POST['comments']
                    )
        interview.status='Completed'
        interview.save()
    return render(request,'feedback.html',{'interview':interview})

@login_required
def candidate_dashboard(request):
    print("logged in user",request.user)
    interviews=Interview.objects.filter(candidate__user=request.user)
    return render(request,'candidate_dashboard.html',{'interviews':interviews})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            if user.groups.filter(name='HR').exists():
                return redirect('/dashboard/')

            elif user.groups.filter(name='Interviewer').exists():
                return redirect('/interviewer/')

            elif user.groups.filter(name='Candidate').exists():
                return redirect('/')

            return redirect('/')

        else:
            return render(
                request,
                'login.html',
                {'error': 'Invalid username or password'}
            )

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('/')

def interviewer_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['name']
        email = request.POST['email']
        department = request.POST['department']

        user = User.objects.create_user(
            username=username,
            password=password
        )
        group=Group.objects.get(name='Interviewer')
        user.groups.add(group)

        Interviewer.objects.create(
            user=user,
            name=name,
            email=email,
            department=department
        )
        return redirect('login')
    return render(request, 'interviewer_register.html')

def candidate_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['name']
        email = request.POST['email']
        phone=request.POST['phone']
        department = request.POST['department']
        user = User.objects.create_user(
            username=username,
            password=password
        )
        # Add user to Candidate group
        group = Group.objects.get(name='Candidate')
        user.groups.add(group)

        Candidate.objects.create(
            user=user,
            name=name,
            email=email,
            phone=phone,
            department=department
        )
        return redirect('login')
    return render(request, 'candidate_register.html')

@login_required
def interviewer_list(request):
    interviewers = Interviewer.objects.all()
    is_hr = request.user.groups.filter(name='HR').exists()
    return render(request, 'interviewer_list.html', {
        'interviewers': interviewers,
        'is_hr': is_hr
    })
@login_required
def result(request):
    feedbacks = Feedback.objects.filter(
        interview__candidate__user=request.user
    )

    return render(request, 'result.html', {
        'feedbacks': feedbacks
    })
def logout_view(request):
    logout(request)
    return redirect('home')

def how_it_works(request):
    return render(request,'how_it_works.html')
def about(request):
    return render(request,'about.html')
def help(request):
    return render(request,'help.html')