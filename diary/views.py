from django.shortcuts import render, redirect

def index(request):
    # 로그인되어 있는 경우, 피드 페이지로
    if request.user.is_authenticated:
        return redirect("cal:CalendarView")
    
    # 로그인되어 있지 않은 경우, 로그인 페이지로
    else:
        return redirect("users:login")