from django.shortcuts import render, redirect # 저장이 된 다음 새로운 페이지 설정
from .models import UserModel
from django.http import HttpResponse
from django.contrib.auth import get_user_model # 사용자가 데이터베이스 안에 있는지 검사하는 함수
from django.contrib import auth

# Create your views here.
def sign_up_view(request): # 회원 가입 실행 될 때
    if request.method == 'GET':
        return render(request, 'user/signup.html')
    
    elif request.method == 'POST':
        username = request.POST.get('username',None) # 앞의 요소가 없다면 None 빈칸처리
        password = request.POST.get('password',None)
        password2 = request.POST.get('password2',None)
        bio = request.POST.get('bio',None)
        
        if password != password2: # 패스워드가 같지 않다면 저장되지 않게 signup페이지를 다시 띄워줘 유저가 알아듣게끔 한다
            return render(request, 'user/signup.html')
        
        else: # 같다면 유저정보 저장
            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                return render(request, 'user/signup.html')
            else: # 사용자가 없을 경우 
                UserModel.objects.create_user(username=username, password=password, bio=bio)
                return redirect('/sign-in') # 회원가입 완료되면 redirect

def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username',None)
        password = request.POST.get('password',None)
        
        me = auth.authenticate(request, username=username, password=password)
        if me is not None:
            auth.login(request, me)
            return redirect('/')
        else: 
            return redirect('/sign-in')
     
    elif request.method == 'GET':
        return render(request, 'user/signin.html')
