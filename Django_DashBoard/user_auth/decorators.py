# user_auth/decorators.py
from functools import wraps
from django.shortcuts import redirect

def patient_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.profile_type == 'patient':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')  # Redirect to login if not authenticated or not a patient
    return _wrapped_view

def doctor_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.profile_type == 'doctor':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')  # Redirect to login if not authenticated or not a doctor
    return _wrapped_view
