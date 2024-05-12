from django import forms
from .models import User, Blog, Appointment
from django.db.models import Q
# from datetime import date, datetime, time, timedelta


class UserSignupForm(forms.ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder':'Type the username'
        })
        
        self.fields['password'].widget.attrs.update({
            'type':'password',
            'placeholder':'Type password'
        })
        self.fields['password_confirm'].widget.attrs.update({
            'placeholder':'confirm password'
        })
        self.fields['profile_picture'].widget.attrs.update({
            'placeholder':'Select the profile Picture'
        })
        self.fields['profile_type'].widget.attrs.update({
            'placeholder':'Select the profile type'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder':'xyz@example.com'
        })
        self.fields['address_line1'].widget.attrs.update({
            'placeholder':'Address Line 1'
        })
        self.fields['city'].widget.attrs.update({
            'placeholder':'City'
        })
        self.fields['pincode'].widget.attrs.update({
            'placeholder':'Pincode'
        })
        self.fields['first_name'].widget.attrs.update({
            'placeholder':'First Name'
        })
        self.fields['last_name'].widget.attrs.update({
            'placeholder':'Last Name'
        })
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'profile_type', 'profile_picture', 'username', 'email', 'password', 'password_confirm', 'address_line1', 'city', 'pincode']

class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = [ 'category', 'name', 'blog_picture', 'content','draft']






from .models import Appointment
# from datetime import time, timedelta, datetime
import datetime

from django.utils.timezone import now

class BookingForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['chosen_date', 'chosen_time','required_speciality']

    def __init__(self, doctor, paitent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.paitent = paitent
        self.doctor = doctor
        min_date = (now()+datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        max_date = (now()+datetime.timedelta(days=31)).strftime('%Y-%m-%d')
        self.fields['chosen_date'].widget = forms.DateInput(attrs={'type': 'date', 'id': 'id_chosen_date','min': min_date,'max':max_date})
        self.fields['chosen_date'].initial = min_date
        self.fields['chosen_time'].widget = forms.Select(choices=self.get_available_slots())

    def get_available_slots(self):
        chosen_date = self.data.get('chosen_date') or (datetime.date.today()+ datetime.timedelta(days=1))

        # Generate all slots for the working hours (9 am to 10 pm) with a 45-minute interval
        available_slots = []
        current_time = datetime.time(9, 0)  # Start with 9:00 AM
        end_time = datetime.time(22, 0)    # End at 10:00 PM

        while current_time < end_time:
            # available_slots.append(current_time)
            # current_time = datetime.datetime.combine(datetime.date.today(), current_time)
            # current_time += datetime.timedelta(minutes=45)
            # current_time = current_time.time()


            current_datetime = datetime.datetime.combine(datetime.date.today(), current_time)
            # slot = current_time  # Format as "9:00:00"
            available_slots.append(current_time)
    
            # Increment by timedelta
            current_datetime += datetime.timedelta(minutes=45)
            
            # Extract the time component
            current_time = current_datetime.time()
            

            if current_datetime.time() >= end_time:
                break


        # Fetch booked appointments for the chosen date
        # booked_appointments = Appointment.objects.filter(
        #     doctor=self.doctor,
        #     chosen_date=chosen_date
        # ).values_list('chosen_time', flat=True)
        booked_appointments = Appointment.objects.filter(
            Q(patient=self.paitent) | Q(doctor=self.doctor),
            chosen_date=chosen_date
        ).values_list('chosen_time', flat=True)
        print(booked_appointments)

        # Exclude booked slots from available slots
        available_slots = [(slot.strftime('%H:%M:%S'), slot.strftime('%H:%M:%S')) for slot in available_slots if slot not in booked_appointments]

        return available_slots
