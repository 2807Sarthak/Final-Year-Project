from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import UserSignupForm, BlogForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Blog, Category
from user_auth.decorators import patient_required, doctor_required
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# utility functions


def check_confirm_password(form):
    if form.cleaned_data['password'] != form.cleaned_data['password_confirm']:
        return True
    return False


def redirect_to_dashboard(user):
    if user.profile_type == 'Patient' or user.profile_type == 'patient':
        return 'patient_dashboard'
    elif user.profile_type == 'Doctor' or user.profile_type == 'doctor':
        return 'doctor_dashboard'

# all the urls


@login_required(login_url='login')
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    blogs = Blog.objects.filter(
        (Q(author=request.user) | Q(draft=False))
    )
    p = Paginator(blogs, 4)

    page_number = request.GET.get(
        'page') if request.GET.get('page') != None else '1'
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_number = '1'
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_number = p.num_pages
        page_obj = p.page(p.num_pages)

    categorys = Category.objects.all()
    context = {'blogs': blogs,
               'categorys': categorys,
               'page_obj': page_obj}
    return render(request, 'user_auth/index.html', context)


@login_required(login_url='login')
def category(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''


    blogs = Blog.objects.filter(
        Q(category__name=q) &
        (Q(author=request.user) | Q(draft=False))
    )

    p = Paginator(blogs, 4)

    page_number = request.GET.get(
        'page') if request.GET.get('page') != None else '1'
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_number = '1'
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_number = p.num_pages
        page_obj = p.page(p.num_pages)
    categorys = Category.objects.all()
    context = {'blogs': blogs, 'categorys': categorys,
               'page_obj': page_obj, 'q': q}
    return render(request, 'user_auth/Category.html', context)


@doctor_required
def self_blogs(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    blogs = Blog.objects.filter(
        Q(author__username=request.user)
    )
    p = Paginator(blogs, 4)

    page_number = request.GET.get(
        'page') if request.GET.get('page') != None else '1'
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_number = '1'
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_number = p.num_pages
        page_obj = p.page(p.num_pages)

    categorys = Category.objects.all()
    context = {'blogs': blogs, 'categorys': categorys,
               'page_obj': page_obj, 'q': q}
    return render(request, 'user_auth/self_blog.html', context)


def signup(request):

    if request.user.is_authenticated:
        dashboard_url = redirect_to_dashboard(request.user)
        return redirect(dashboard_url)
    if request.method == 'POST':
        form = UserSignupForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)

            # checking if the pass is same as confirm_pass
            if check_confirm_password(form):
                return render(request, 'user_auth/signup.html', {'form': form})

            password = form.cleaned_data['password']
            username = form.cleaned_data['username']

            user.set_password(password)
            user.save()
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('login')
        else:
            print(form.errors)
    else:

        form = UserSignupForm()
    return render(request, 'user_auth/signup.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        dashboard_url = redirect_to_dashboard(request.user)
        return redirect(dashboard_url)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            print(request.user.profile_picture,
                  type(request.user.profile_picture))
            return redirect('home')
    return render(request, 'user_auth/login.html')


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('login')


@patient_required
def patient_dashboard(request):
    user = request.user
    return render(request, 'user_auth/patient_dashboard.html', {'user': user})


@doctor_required
def doctor_dashboard(request):
    user = request.user
    return render(request, 'user_auth/doctor_dashboard.html', {'user': user})


def blog_detail(request, slug):
    blog = Blog.objects.get(pk=slug)

    context = {'blog': blog}
    return render(request, 'user_auth/blog.html', context)


@doctor_required
def create_blog(request):
    page = 'create'
    if request.method == 'POST':
        blog_category = request.POST.get('category')
        cate_old, created = Category.objects.get_or_create(name=blog_category)

        # Creating a new Blog instance
        blog = Blog.objects.create(
            author=request.user,
            name=request.POST.get('name'),
            category=cate_old,
            content=request.POST.get('content'),
            draft=request.POST.get('draft') == 'on'
        )

        # Handling blog_picture upload separately
        blog.blog_picture = request.FILES.get('blog_picture')
        blog.save()
        return redirect('blog_detail', slug=blog.id)
    else:
        form = BlogForm()
    categorys = Category.objects.all()  
    context = {'form': form, 'categorys': categorys, 'page': page}
    return render(request, 'user_auth/create_blog.html', context)


@doctor_required
def update_blog(request, slug):
    page = 'update'
    blog = Blog.objects.get(pk=slug)

    if request.user != blog.author:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        blog_category = request.POST.get('category')
        cate_old, created = Category.objects.get_or_create(name=blog_category)
        blog.name = request.POST.get('name')
        blog.category = cate_old
        blog.content = request.POST.get('content')
        blog.draft = request.POST.get('draft') == 'on'
        if request.FILES.get('blog_picture'):
            blog.blog_picture = request.FILES.get('blog_picture')
        blog.save()
        return redirect('blog_detail', slug=blog.id)
    else:
        form = BlogForm(instance=blog)

    categorys = Category.objects.all()
    context = {'form': form, 'blog': blog,
               'categorys': categorys, 'page': page}
    return render(request, 'user_auth/create_blog.html', context)

    

from google.oauth2 import service_account
from googleapiclient.discovery import build

def create_google_calendar_event(appointment):
    # Load OAuth 2.0 credentials
    credentials = service_account.Credentials.from_service_account_file(
        'user_auth/credentials.json',
        scopes=['https://www.googleapis.com/auth/calendar']
    )

    # Create a Google Calendar API service
    service = build('calendar', 'v3', credentials=credentials)
    
    event_end_datetime = datetime.datetime.combine(appointment.chosen_date, appointment.end_time)
    event_end_datetime_str = event_end_datetime.strftime('%Y-%m-%dT%H:%M:%S')

    event_start_datetime = datetime.datetime.combine(appointment.chosen_date, appointment.chosen_time)
    event_start_datetime_str = event_start_datetime.strftime('%Y-%m-%dT%H:%M:%S')
    # Define event details
    event = {
        'summary': f'Appointment with Dr {appointment.doctor.first_name} {appointment.doctor.last_name} and Patient {appointment.patient.first_name} {appointment.patient.last_name}',
        'description': 'Appointment with Dr. {}'.format(appointment.doctor),
        'start': {
            'dateTime': event_start_datetime_str,
            'timeZone': 'IST',
        },
        'end': {
            'dateTime': event_end_datetime_str,
            'timeZone': 'IST',
        }
        # 'attendees': [
        #     {'email': appointment.doctor.email},
        #     {'email': appointment.patient.email},
        # ],
    }

    # Create the event
    event = service.events().insert(calendarId='{Google API key}', body=event).execute()
    if event.get('id'):
        appointment.google_url = event.get("htmlLink")
        return False
    return True


from .forms import BookingForm
import datetime

def booking_view(request, slug):
    doctor = User.objects.get(id=slug)
    
    if request.method == 'POST' and request.user.profile_type == 'doctor':
        form = BookingForm(doctor,request.user, request.POST)
        if form.is_valid():
            
            chosen_date = form.cleaned_data['chosen_date']
            chosen_time = form.cleaned_data['chosen_time']

            booked_appointments = Appointment.objects.filter(
            doctor=doctor,
            chosen_date=chosen_date,
            chosen_time=chosen_time
            )
            slot_duration = datetime.datetime.strptime('00:45', '%H:%M')
            end_datetime = datetime.datetime.combine(chosen_date, chosen_time) + datetime.timedelta(minutes=45)
            end_time = end_datetime

            appointment = form.save(commit=False)
            appointment.doctor = request.user
            appointment.end_time = end_time.time()
            if booked_appointments:
                form = BookingForm(doctor)
                return render(request, 'booking', {'form': form, 'doctor': doctor})

    if request.method == 'POST' and request.user.profile_type == 'patient':        
            
            patient_docs = form.cleaned_data['patient_docs']
            patient_desc = form.cleaned_data['patient_desc']
            required_speciality = form.cleaned_data['required_speciality']

            appointment.patient = request.user
            appointment.patient_docs= patient_docs
            appointment.patient_desc = patient_desc
            appointment.required_speciality = required_speciality

            if create_google_calendar_event(appointment):
                form = BookingForm(doctor,request.user)

                return render(request, 'booking.html', {'form': form, 'doctor': doctor})
                
            appointment.save()
            
            # Redirect or show a success message
            return redirect( 'A_detail', slug = appointment.id)
    else:
        form = BookingForm(doctor,request.user)

    return render(request, 'booking.html', {'form': form , 'user':request.user})


from user_auth.models import User

@patient_required
def list_doctors(request):
    # Retrieve all doctors from the database
    doctors = User.objects.filter(profile_type='doctor')
    
    # Render a template with the list of doctors
    return render(request, 'list_doctors.html', {'doctors': doctors})


from .models import Appointment
from django.http import JsonResponse

def get_available_slots(request):
    selected_date = request.GET.get('date')  
    # print(request.GET.get('doctor_id'))
    doctor = User.objects.get(id=request.GET.get('doctor_id'))

    available_slots = calculate_available_slots(selected_date,doctor,request.user)
    return JsonResponse({'slots': available_slots})

def calculate_available_slots(selected_date, doctor,paitent):
        chosen_date = selected_date

        # Generate all slots for the working hours (9 am to 10 pm) with a 45-minute interval
        available_slots = []
        current_time = datetime.time(9, 0)  # Start with 9:00 AM
        end_time = datetime.time(22, 0)    # End at 10:00 PM

        while current_time < end_time:

            available_slots.append(current_time)
            current_time = datetime.datetime.combine(datetime.date.today(), current_time)
            current_time += datetime.timedelta(minutes=45)
            current_time = current_time.time()


        booked_appointments = Appointment.objects.filter(
            Q(patient=paitent) | Q(doctor=doctor),
            chosen_date=chosen_date
        ).values_list('chosen_time', flat=True)

        print(booked_appointments)
        # Exclude booked slots from available slots
        available_slots = [(slot) for slot in available_slots if slot not in booked_appointments]
        return available_slots


def A_detail(request,slug):
    appointment = Appointment.objects.get(id=slug)

    if request.user != appointment.doctor and request.user != appointment.patient:
        return HttpResponse('You are not allowed here')

    return render(request,'A_detail.html',{ 'appointment' : appointment})


@login_required(login_url='login')
def appointment(request):
    if request.user.profile_type == 'patient':
        appointments = Appointment.objects.filter(
            Q(patient=request.user)
        ).order_by('-id')[:30]
    
    else:
        appointments = Appointment.objects.filter(
            Q(doctor=request.user)
        ).order_by('-id')[:30]

    return render(request, 'list_appointments.html',{'appointments':appointments})

@login_required(login_url='login')
def filter_appointment(request):
    if request.user_profile_type =='doctor':
         appointments = Appointment.objects.filter(
            Q(required_speciality=request.user.speciality) AND Q(doctor=None)
        ).order_by('-id')[:30]