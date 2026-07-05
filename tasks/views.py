from django.shortcuts import render,redirect,get_object_or_404
from .models import Task
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout 
from django.contrib.auth.decorators import login_required
from datetime import date
from django.core.paginator import Paginator

@login_required(login_url='/login/')
def home(request):

    if request.method == "POST":
        title = request.POST.get("title")
        due_date = request.POST.get("due_date")
        Task.objects.create(
            title=title,
            due_date=due_date,
            user=request.user
        )

        return redirect('home')
    tasks = Task.objects.filter(user=request.user)
    search_query = request.GET.get('search', '')

    if search_query:
        
        tasks = tasks.filter(title__icontains=search_query)
    today = date.today()

    sort = request.GET.get("sort", "")

    if sort == "newest":
        tasks = tasks.order_by("-id")

    elif sort == "oldest":
        tasks = tasks.order_by("id")

    elif sort == "due":
        tasks = tasks.order_by("due_date")

    elif sort == "az":
        tasks = tasks.order_by("title")

    elif sort == "za":
        tasks = tasks.order_by("-title")

    filter_type = request.GET.get("filter", "")

    if filter_type == "completed":
      tasks = tasks.filter(completed=True)

    elif filter_type == "pending":
     tasks = tasks.filter(completed=False)

    elif filter_type == "overdue":
      tasks = tasks.filter(
        completed=False,
        due_date__lt=date.today()
     )

    for task in tasks:
     if task.due_date:

        difference = (task.due_date - today).days

        if difference > 0:
            task.status = f"🟢 {difference} day(s) left"

        elif difference == 0:
            task.status = "🟡 Due Today"

        else:
            task.status = f"🔴 Overdue by {abs(difference)} day(s)"

     else:
        task.status = ""
       

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    pending_tasks = tasks.filter(completed=False).count()
    

    if total_tasks > 0:
      completion_percentage = int((completed_tasks / total_tasks) * 100)
    else:
      completion_percentage = 0  
    # paginator = Paginator(tasks, 5)
    # page_number = request.GET.get("page")
    # tasks = paginator.get_page(page_number)
    
    context = {
        'tasks': tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'completion_percentage': completion_percentage,
    } 

    return render(request, 'tasks/home.html', context)
@login_required(login_url='/login/')
def delete_task(request, id):
    task = task = get_object_or_404(Task,id=id,user=request.user)
    task.delete()

    return redirect('home')
@login_required(login_url='/login/')
def update(request , id):
    task = Task.objects.get(id=id)

    if request.method == "POST":
        data = request.POST
        due_date = data.get('due_date')
        title = data.get('title')
        task.title = title
        task.due_date = due_date
        task.save()
        
        return redirect('home')
    

    context = {'task': task}

    return render(request , 'tasks/update.html' , context)
@login_required(login_url='/login/')
def complete(request,id):
    task = get_object_or_404(Task, id=id)
    if task.completed == False:
        task.completed = True
    else:
        task.completed = False

    task.save()
    return redirect('home')        


def login_page(request):
    if request.method == "POST":
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request , 'Invalid username or Password!')
            return redirect('/login/')
        
        else:
            login(request,user)
            return redirect('home')
    return render(request , "tasks/login.html")    


def logout_page(request):
    logout(request)
    return redirect('/login/')

def register(request):
     
     if request.method == "POST":
         first_name = request.POST.get('first_name')
         last_name = request.POST.get('last_name')
         username = request.POST.get('username')
         password = request.POST.get('password')

         # Validate empty fields
         if not username or not password:
             context = {'error': 'Username and password are required!'}
             return render(request, "register.html", context)

         # Check if username already exists
         if User.objects.filter(username=username).exists():
             context = {'error': 'Username already exists!'}
             return render(request, "tasks/register.html", context)

         user = User.objects.create(
             first_name = first_name,
             last_name = last_name,
             username = username,
         )
         
         user.set_password(password)
         user.save()
         messages.success(request, 'Registration successful! You can now log in.')
         return redirect('/login/')

     return render(request , "tasks/register.html")

 