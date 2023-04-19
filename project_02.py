# proejct_02.py에 게시글을 저장하는 class를 만들려고 합니다. 
# 클래스 안에 들어갈 변수는(id, title, author, content) 으로 
# 모두 빈 문자열로 저장하고, 게시글 한 개를 저장해 보세요!

class Post:
    # 클래스 안에 들어갈 변수는 
    # ( id, title, author, content)이고 모두 빈 문자열로 저장
    id = ''
    title = ''
    author = ''
    content = ''

post = Post()
post.id = '1'
post.title = '제목'
post.author = '유저'
post.content = '나불나불 게시글 입니다'

print(post)
print("id ", post.id)
print("title ", post.title)
print("author ", post.author)
print("content ", post.content)
