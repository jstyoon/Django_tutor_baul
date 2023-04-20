from django.shortcuts import render, redirect # 저장이 된 다음 새로운 페이지 설정
from django.contrib.auth import get_user_model # 사용자가 데이터베이스 안에 있는지 검사하는 함수
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from .models import UserModel

# Create your views here.
# 회원가입 뷰
def sign_up_view(request): 
    if request.method == 'GET':
        user = request.user.is_authenticated # 로그인 된 상태인지 확인
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signup.html')
    
    elif request.method == 'POST':
        username = request.POST.get('username',None) # 앞의 요소가 없다면 None 빈칸처리
        password = request.POST.get('password',None)
        password2 = request.POST.get('password2',None)
        bio = request.POST.get('bio',None)
        
        if password != password2: # 패스워드가 같지 않다면 저장되지 않게 signup페이지를 다시 띄워줘 유저가 알아듣게끔 한다
            return render(request, 'user/signup.html')
        
        else:
            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                # 사용자가 존재하기 때문에 사용자를 저장하지 않고 signup페이지를 다시 띄움
                return render(request, 'user/signup.html')
            else:
                UserModel.objects.create_user(username=username, password=password, bio=bio)
                return redirect('/sign-in') # 회원가입 완료되면 로그인 페이지로 
# 로그인 뷰
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
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signin.html')
        
@login_required #로그인 되어야 접근가능
def logout(request):
    auth.logout(request)
    return redirect('/')

# user/views.py


@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'user/user_list.html', {'user_list': user_list})


@login_required
def user_follow(request, id):
    me = request.user # 로그인한 사용자
    click_user = UserModel.objects.get(id=id) # 팔로우누르려는사람(취소포함)
    if me in click_user.followee.all(): # 팔로우 된 전체 사용자 목록에 내가 있으면 취소
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user) # 없으면 추가
    return redirect('/user')
