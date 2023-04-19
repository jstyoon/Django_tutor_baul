# user/views.py
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import UserModel

# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':
        return render(request, 'user/signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)
        bio = request.POST.get('bio', None)

        if password != password2:
            return render(request, 'user/signup.html')
        else:
            exist_user = UserModel.objects.filter(username=username)
            
            if exist_user: # 사용자가 존재하기 때문에 사용자를 저장하지 않고 회원가입 페이지를 다시 띄움
                return render(request, 'user/signup.html')
            else:
                new_user = UserModel()
                new_user.username = username
                new_user.password = password
                new_user.bio = bio
                new_user.save()
                return redirect('/sign-in')

            
           
            
                

def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        
        me = UserModel.objects.get(username=username)
        if me.password == password:
            request.session['user'] = me.username 
            return HttpResponse(me.username)
        else:
            return redirect('/login')
    elif request.method == 'GET':
        return render(request, 'user/signin.html')