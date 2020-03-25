from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ArticleColumn
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .forms import ArticleColumnForm
from django.views.decorators.http import require_POST

# Create your views here.


@login_required(login_url = '/account/login/')
@csrf_exempt #6
def article_column(request):
    # columns = ArticleColumn.objects.filter(user=request.user)
    # return render(request,"article/column/article_column.html",{"columns":columns}
    if request.method == "GET":
        columns = ArticleColumn.objects.filter(user=request.user)
        column_from = ArticleColumnForm()
        return render(request,"article/column/article_column.html",{"columns":columns,"column_form":column_from})
    if request.method == "POST":
        column_name = request.POST['column']
        columns = ArticleColumn.objects.filter(user_id=request.user.id,column=column_name)#7
        if columns:
            return HttpResponse('2')
        else:
            ArticleColumn.objects.create(user=request.user,column=column_name)
            return HttpResponse('1')


@login_required(login_url = '/account/login')
@require_POST
@csrf_exempt
def rename_article_column(request):
    column_name = request.POST["column_name"]
    column_id = request.POST['column_id']
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.column = column_name #重新赋值
        line.save()
        return HttpResponse("1")
    except:
        return HttpResponse("0")