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
        username = request.POST.get('username','') # 앞의 요소가 없다면 None 빈칸처리
        password = request.POST.get('password','')
        password2 = request.POST.get('password2','')
        bio = request.POST.get('bio','')
        
        if password != password2:
            # 패스워드가 같지 않다고 알람
            return render(request, 'user/signup.html', {'error':'패스워드를 확인해 주세요'})
        else: # 공백 알람
            if username == '' or password == '':
                return render(request, 'user/signup.html', {'error': '사용자이름과 비밀번호는 필수 값 입니다'})
            # 사용자 존재유무 확인
            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                return render(request, 'user/signup.html', {'error': '사용자가 존재합니다'})
            else:
                UserModel.objects.create_user(username=username, password=password, bio=bio)
                return redirect('/sign-in') # 회원가입 완료되면 로그인 페이지로 
# 로그인 뷰
def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        
        me = auth.authenticate(request, username=username, password=password)
        if me is not None:
            auth.login(request, me)
            return redirect('/')
        else: 
            return render(request, 'user/signin.html', {'error':'유저이름 혹은 패스워드를 확인 해 주세요'})
     
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
