from django.shortcuts import render, redirect
from .models import TweetModel, TweetComment
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    user = request.user.is_authenticated
    if user:
        return redirect('/tweet')
    else:
        return redirect('/sign-in')
    
def tweet(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            all_tweet = TweetModel.objects.all().order_by('-created_at') #역순 정렬
            return render(request, 'tweet/home.html', {'tweet': all_tweet}) #딕셔너리 키값 tweet
        else:
            return redirect('/sign-in')
        
    elif request.method == 'POST':
        # 장고에서는 요청에 자동적으로 인증을 추가합니다. 아래처럼 작성하면 현재 요청이 누구에게서 요청 된 것인지 확인 할 수 있습니다.
        user = request.user # 로그인 한 user 전체 불러오기
        my_tweet = TweetModel() # 글쓰기 모델 가져오기
        my_tweet.author = user  # 모델에 사용자 저장
        # html에서 id와 name이 'my-content'입니다. 아래처럼 작성하면 POST 형식으로 요청 한 데이터를 id와 name을 가지고 올 수 있습니다.
        my_tweet.content = request.POST.get('my-content', '')
        my_tweet.save()
        return redirect('/tweet')
        
@login_required
def delete_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    my_tweet.delete()
    return redirect('/tweet')


@login_required # 상세보기 
def detail_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    tweet_comment = TweetComment.objects.filter(tweet_id=id).order_by('-created_at')
    return render(request,'tweet/tweet_detail.html',{'tweet':my_tweet,'comment':tweet_comment})


@login_required # 댓글달기
def write_comment(request, id):
    if request.method == 'POST':
        comment = request.POST.get("comment","")
        current_tweet = TweetModel.objects.get(id=id)

        TC = TweetComment()
        TC.comment = comment
        TC.author = request.user
        TC.tweet = current_tweet
        TC.save()
        
        return redirect('/tweet/'+str(id))
    
@login_required # 댓글삭제
def delete_comment(request, id):
    comment = TweetComment.objects.get(id=id)
    current_tweet = comment.tweet.id
    comment.delete()
    return redirect('/tweet/'+str(current_tweet))
