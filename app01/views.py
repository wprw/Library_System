from django.shortcuts import render, redirect, reverse, HttpResponse
from app01 import models

# Create your views here.
'''
从数据库中查询用户名和密码；
将用户名和密码与前端得到的名字和密码进行比对；
如果比对成功则登录成功跳转到home页面；
如果比对不成功则返回一个登录失败页面，显示返回注册
'''

# print(type(models.User))
# print(type(models.User. ))
# print(type(models.User.objects.filter(pk=1).filter()))
from django.db.models.query import QuerySet
from django.db.models.manager import Manager
from django.db.models.base import ModelBase

def login(request):
    # print(request)
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        # user_list = models.User.objects.values('name','password')  # all()是取出所有对象
        # print(user_list)  # <QuerySet [{'name': 'wpr', 'password': '111'}, {'name': '', 'password': ''}, {'name': '万佩佩', 'password': '123'}]>
        if name and password:
            user_list=models.User.objects.values('name','password')
            # print(user_list)  # <QuerySet [{'name': 'wpr'}, {'name': ''}, {'name': '万佩佩'}, {'name': '万佩佩'}, {'name': '万佩佩'}]>
            for user in user_list:
                if name==user.get('name'):
                    if password==user.get('password'):
                        return redirect(reverse('home'))
                    else:
                        return HttpResponse('密码错啦！')
                    # else:
                    #     return HttpResponse('没有该用户，请返回注册！')
        else:
            error='请输入用户名和密码！'
            # return HttpResponse('请输入用户名和密码！')
    return render(request, 'login.html', locals())


'''
从数据库中查询出用户名；
将用户名和前端得到用户名进行比对；
如果姓名在数据库中则提示已经注册，请直接登录；
若不在则创建新的用户
'''
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        if name and password:
            username_list = models.User.objects.values('name')  # print(user_dic)  # <QuerySet [{'name': 'wpr'}, {'name': ''}, {'name': '万佩佩'}, {'name': '万佩佩'}, {'name': '万佩佩'}, {'name': '万佩佩'}, {'name': '万佩佩'}, {'name': '万佩佩'}]>
            for username in username_list:
                if name in username.get('name'):
                    # print(username.get('name'))
                    tip='用户已存在，请直接登录！'
                    # return HttpResponse('用户已存在，请直接登录！')
                else:
                    models.User.objects.create(name=name, password=password)
                    return redirect(reverse('login'))
        else:
            error='请输入用户名和密码！'
            # return HttpResponse('')
    return render(request, 'register.html',locals())


def home(request):
    return render(request, 'home.html')


def book_list(request):
    # 先查询出所有书籍，将内容渲染到前端
    book_list = models.Book.objects.all()
    return render(request, 'book_list.html', locals())


def add_book(request):
    if request.method == 'POST':
        print(request.method)
        title = request.POST.get('title')
        price = request.POST.get('price')
        # publish拿到的是出版社的id
        publish_id = request.POST.get('publish')
        publish_date = request.POST.get('date')
        authors = request.POST.getlist('authors')
        # 数据库新增数据
        book_obj = models.Book.objects.create(title=title, price=price, publish_id=publish_id,
                                              publish_time=publish_date)
        # 去书籍与作者的第三表手动创建关系
        book_obj.authors.add(*authors)
        # 跳转到图书的展示页面
        return redirect(reverse('book_list'))
    # 将出版社和作者数据全部传递给添加页面
    publish_list = models.Publish.objects.all()
    author_list = models.Author.objects.all()
    # get请求返回一个添加页面
    return render(request, 'add_book.html', locals())


def delete_book(request, delete_id):
    models.Book.objects.filter(pk=delete_id).delete()
    return redirect(reverse('book_list'))


def edit_book(request, edit_id):
    # 返回一个编辑页面，但是这个编辑页面需要将原来数据的信息展示出来
    edit_obj = models.Book.objects.filter(pk=edit_id).first()
    if request.method == 'POST':
        title = request.POST.get('title')
        price = request.POST.get('price')
        publish_date = request.POST.get('date')
        publish_id = request.POST.get('publish')
        authors = request.POST.getlist('authors')
        models.Book.objects.filter(pk=edit_id).update(title=title, price=price, publish_time=publish_date,
                                                      publish_id=publish_id)
        edit_obj.authors.set(authors)
        return redirect(reverse('book_list'))
    publish_list = models.Publish.objects.all()
    author_list = models.Author.objects.all()
    return render(request, 'edit_book.html', locals())


def author_list(request):
    author_list = models.Author.objects.all()
    # print(author_list)
    return render(request, 'author_list.html', locals())


def add_author(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        addr = request.POST.get('addr')
        print(addr)
        # authordetail_id = request.POST.get('authordetail')
        authordetail_obj = models.AuthorDetail.objects.create(phone=phone, addr=addr)
        # authordetail_obj = models.AuthorDetail.objects.filter(detail_obj.pk).first()
        models.Author.objects.create(name=name, age=age, authordetail_id=authordetail_obj.pk)
        return redirect(reverse('author_list'))
    return render(request, 'add_author.html', locals())


def delete_author(request, delete_id):
    models.Author.objects.filter(pk=delete_id).delete()
    return redirect(reverse('author_list'))


def edit_author(request, edit_id):
    # 先将所有信息找到
    edit_obj = models.Author.objects.filter(pk=edit_id).first()
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        models.Author.objects.filter(pk=edit_id).update(name=name, age=age)
        return redirect(reverse('author_list'))
    authordetail_list = models.AuthorDetail.objects.all()
    return render(request, 'edit_author.html', locals())


def author_detail(request, detail_id):
    author_obj = models.Author.objects.filter(pk=detail_id).first()
    authordetail_list = models.AuthorDetail.objects.filter(pk=author_obj.authordetail_id).all()
    # 查询作者的姓名
    # author_name= models.AuthorDetail.objects.values('author__name')
    return render(request, 'author_detail.html', locals())


def publish_list(request):
    publish_list = models.Publish.objects.all()
    return render(request, 'publish_list.html', locals())


def add_publish(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        addr = request.POST.get('addr')
        email = request.POST.get('email')
        publish_obj = models.Publish.objects.create(name=name, addr=addr, email=email)
        return redirect(reverse('publish_list'))
    return render(request, 'add_publish.html', locals())


def delete_publish(request, delete_id):
    models.Publish.objects.filter(pk=delete_id).delete()
    return redirect(reverse('publish_list'))


def edit_publish(request, edit_id):
    edit_obj = models.Publish.objects.filter(pk=edit_id).first()
    if request.method == 'POST':
        name = request.POST.get('name')
        addr = request.POST.get('addr')
        email = request.POST.get('email')
        models.Publish.objects.filter(pk=edit_id).update(name=name, addr=addr, email=email)
        return redirect(reverse('publish_list'))
    return render(request, 'edit_publish.html', locals())
