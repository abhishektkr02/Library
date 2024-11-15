from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib import auth
from .import forms,models
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from datetime import datetime,timedelta,date
from django.core.mail import EmailMessage



def home_view(request):

    return render(request,'index.html')
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'adminclick.html')
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'studentclick.html')
def adminsignup_view(request):
    form=forms.AdminSignUpForm()
    if request.method=='POST':
        form=forms.AdminSignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group=Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request,'adminsignup.html',{'form':form})
def studentsignup_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()
            my_student_group=Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('studentlogin')
    return render(request,'studentsignup.html',context=mydict)
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def afterlogin_view(request):
    if is_admin(request.user):
        return render(request,'adminafterlogin.html')
    else:
        return render(request,'studentafterlogin.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def addbook_view(request):
    form=forms.BookForm()
    if request.method=='POST':
        form=forms.BookForm(request.POST)
        if form.is_valid():
            user=form.save()
            return render(request,'bookadded.html')
    return render(request,'addbook.html',{'form':form})

class CustomLogoutView(LogoutView):
    next_page=reverse_lazy('home')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewbook_view(request):
    books=models.Book.objects.all()
    return render(request,'viewbook.html',{'books':books})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def issuebook_view(request):
    form=forms.IssuedBookForm()
    if request.method=='POST':
        form=forms.IssuedBookForm(request.POST)
        print(form)
        if form.is_valid():
            ib=models.IssuedBook()
            ib.enrollment=request.POST.get('enrollment2')
            ib.isbn=request.POST.get('isbn2')
            ib.save()
            return render(request,'bookissued.html')
    return render(request,'issuebook.html',{'form':form})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewissuedbook_view(request):
    issuedbooks=models.IssuedBook.objects.all()
    print(issuedbooks)
    li=[]
    for ib in issuedbooks:
        isudate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        days=(date.today()-ib.issuedate)
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10
        books=list(models.Book.objects.filter(isbn=ib.isbn))
        print(books)
        students=list(models.StudentExtra.objects.filter(enrollment=ib.enrollment))
        i=0
        for l in books:
            t=(students[i].get_name,students[i].enrollment,books[i].name,books[i].author,isudate,expdate,fine)
            i=i+1
            li.append(t)
    return render(request,'viewissuedbook.html',{'li':li})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewstudent_view(request):
    students=models.StudentExtra.objects.all()
    return render(request,'viewstudent.html',{'students':students})

@login_required(login_url='studentlogin')
def viewissuedbookbystudent_view(request):
    student=models.StudentExtra.objects.filter(user_id=request.user.id)
    issuedbook=models.IssuedBook.objects.filter(enrollment=student[0].enrollment)
    li=[]
    li2=[]
    for ib in issuedbook:
        books=models.Book.objects.filter(isbn=ib.isbn)
        for book in books:
            t=(request.user,student[0].enrollment,student[0].branch,book.name,book.author)
            li.append(t)
        isudate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        days=(date.today()-ib.issuedate)
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10
        t=(isudate,expdate,fine)
        li2.append(t)
    return render(request,'viewissuedbookbystudent.html',{'li':li,'li2':li2})

def aboutus_view(request):
    return render(request,'aboutus.html')
def contactus_view(request):
    cont=forms.ContactusForm()
    if request.method=='POST':
        cont=forms.ContactusForm(request.POST)
        if cont.is_valid():
            email=cont.cleaned_data['Email']
            name=cont.cleaned_data['Name']
            message=cont.cleaned_data['Message']
            EmailMessage('contact form submission from{}'.format(name),'form',['abhishektkr2002tkr@gmail.com'],[],reply_to=[email]).send()
            return render(request,'contactussuccess.html')
    return render(request,'contactus.html',{'form':cont})
def aboutus_view(request):
    return render(request,'aboutus.html')