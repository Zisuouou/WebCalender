from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, timedelta, date
from django.views import generic
from django.utils.safestring import mark_safe
import calendar
from django.contrib.auth import authenticate, login, logout
from django.utils.timezone import make_aware

from cal.forms import EventForm
from users.forms import * 
from .models import * 
from .utils import Calendar
from .forms import EventForm
from .models import EventModel
from dateutil import parser

# Create your views here.

# generic.ListView 클래스를 상속받아, class_contents 모델을 이용하여 DB에서 달력에 보여줄 이벤트들을 가져옴
class CalendarView(generic.ListView):
    model = class_contents
    template_name = 'cal/calendar.html'

    # get_context_data() 데이터를 가져오는 함수
    # 현재 달력에 보여줄 년도와 월 정보를 가져오고 Calendar 클래스의 인스턴스를 생성
    # **kwargs는 부모 클래스에서 전달된 인자를 받아오는 용도로 사용
    # **kwargs를 사용하여 기존의 context 데이터를 유지하면서 새로운 데이터를 추가하거나 변경할수 있음
    def get_context_data(self, **kwargs):
        # 클래스 내부에 get_context_data() 메서드를 추가하여 이전/다음 달을 가져오는 과정 구현
        context = super().get_context_data(**kwargs)
        
        selected_datetime = self.get_selected_date()

        cal = Calendar(selected_datetime.year, selected_datetime.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(selected_datetime)
        context['next_month'] = next_month(selected_datetime)

        form = EventForm()
        context["form"] = form 
        events = EventModel.objects.filter(edate__gte=selected_datetime, edate__lt=selected_datetime + timedelta(days=1))

        context['events'] = events

        return context


    def get_selected_date(self):
        # URL에서 전달된 날짜를 가져옵니다.
        req_day = self.request.GET.get('day', None)
        # 가져온 날짜를 파싱하여 datetime 객체로 변환합니다.
        if req_day: 
            year, month, day = (int(x) for x in req_day.split('-'))
            selected_datetime = datetime(year, month, day)  # selected_datetime 변수 정의
            return selected_datetime
        else:
            return datetime.today().date()

        # selected_date_str = selected_date.strftime('%Y-%m-%d')

        # selected_datetime = parser.parse(selected_date_str)

        # return selected_datetime
    
    def post(self, request, *args, **kwargs):
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cal:calendar')  
        else:
            return render(request, 'cal/calendar.html', {'form': form})


# get_daye()는 URL에서 전달된 년도와 월 정보를 추출하여, datatime 객체로 변환하는 함수
# 위에서 선언한 get_context_data() 내에서 호출    

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    a = 'day=' + str(prev_month.year) + '-' + str(prev_month.month) + '-' + str(prev_month.day)
    return a

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    a = 'day=' + str(next_month.year) + '-' + str(next_month.month) + '-' + str(next_month.day)
    return a

def post_detail(request):
    return render(request, 'cal/post_detail.html')

def index(request):
    if request.user.is_authenticated:
        return redirect("cal:calendar")
    
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            # username과 password 값을 가져와 변수에 할당
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            # username, password 에 해당하는 사용자가 있는지 검사
            user = authenticate(username=username, password=password)

            # 해당 사용자가 존재한다면
            if user:
                # 로그인 처리 후, 피드페이지로 redirect
                login(request, user)
                return redirect("cal:calendar")
            # 사용자가 없다면 form에 에러 추가
            else: 
                form.add_error(None, "입력한 자격증명에 해당하는 사용자가 없습니다(이걸 틀리네 낄낄)")

        # 실패한 경우 다시 LoginForm 을 사용한 로그 페이지 렌더링
        context = {"form" : form}

    else:
        # LoginForm 인스턴스를 생성
        form = LoginForm()

        # 생성한 LoginForm 인스턴스를 템플릿에 "form" 이라는 키로 전달
        context = {
            "form" : form,
        }
    return render(request, 'cal/index.html', context)

