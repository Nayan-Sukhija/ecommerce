from django.shortcuts import redirect

def redirect_if_not_logged_in(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('user_login')  
        return view_func(request, *args, **kwargs)
    return wrapper

def redirect_if_not_admin(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser == True:
            return redirect('user_login')  
        return view_func(request, *args, **kwargs)
    return wrapper