from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from .models import Task
from .forms import TaskForm, NotesForm, TaskAsigneeForm
from django.db.models import F
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.contrib.auth.models import User
# Create your views here.

class DashboardView(ListView):
    """
    Class based view to display the dashboard page for a logged in user
    extends the generic ListView
    """
    model = Task
    template_name = 'tasks/dashboard.html'

    def get_queryset(self):
        """
        Applies all of the filters and search criteria to all of the assigned tasks
        QuerySet and returns the resulting QuerySet
        Output:
          my_tasks (QuerySet): A QuerySet of all tasks assigned to the current employee 
        """
        query = self.request.GET.get('query', "")
        status = self.request.GET.get('status', "")
        priority = self.request.GET.get('priority', "")
        
        my_tasks = Task.objects.filter(assigned_to = self.request.user.id).exclude(pk__in = self.get_overdue().values('pk')).order_by(F('deadline').asc(nulls_last = True))
        if query:
             my_tasks = my_tasks.filter(title__icontains = query)
        if status:
             my_tasks = my_tasks.filter(status = status)
        if priority:
             my_tasks = my_tasks.filter(priority = priority)
        return my_tasks

    def dispatch(self, request, *args, **kwargs):
        """
        Args:
          request (HttpRequest): The incoming HTTP request.
          *args: Positional arguments passed through to the parent method
          **kwargs: Keyword arguments passed through to the parent method
        Overrides the base dispatch method by adding the extra functionality
        of redirecting users to the log in page if they are not authenticated.
        Output:
          (HTTPResponse): Either redirects the user to the login page or returns the Dashboard Page
        """
        if not request.user.is_authenticated:
            return redirect('loginuser')
        return super().dispatch(request, *args, **kwargs)

    def get_overdue(self):
         """
         Helper method to get all tasks that are overdue meaning
         All tasks that are past their deadline and their status is not completed.
         """
         return Task.objects.filter(assigned_to = self.request.user.id, deadline__lt = timezone.now()).exclude(status = 'completed')
    
    def get_context_data(self, **kwargs):
        """
        Args:
          **kwargs: Keyword arguments passed through to the parent method
        Overrides the base get_context_data method by adding more data to the context dict
        adds the following:
          overdue_tasks(QuerySet) - of all of the overdue tasks of the currently logged in user
          users (QuerySet) - all of the users logged in the system
          to_do_count (Integer) - count of all tasks with status to do
          in_progress_count (Integer) - count of all tasks with status in progress
          completed_count (Integer) - count of all tasks with status completed
        Output:
          context (dictionary) all of the context sent to the template
        """
        context = super().get_context_data(**kwargs)
        context['overdue_tasks'] = self.get_overdue()
        context['users'] = User.objects.all()
        my_tasks = self.get_queryset()
        context['to_do_count'] = my_tasks.filter(status='to do').count()
        context['in_progress_count'] = my_tasks.filter(status='in progress').count()
        context['completed_count'] = my_tasks.filter(status='completed').count()
        
        return context

class CreatedByMeView(ListView):
     model = Task
     template_name = 'tasks/created_by_me.html'

     def get_queryset(self):
          """
          Gets the QuerySet with all of the tasks created by the current user
          Output:
            (QuerySet): All of the tasks where created_by = current_user
          """
          return Task.objects.filter(created_by = self.request.user.id).order_by(F('created_at').asc())

     def dispatch(self, request, *args, **kwargs):
          """
          Args:
            request (HttpRequest): The incoming HTTP request.
            *args: Positional arguments passed through to the parent method
            **kwargs: Keyword arguments passed through to the parent method
          Overrides the base dispatch method by adding the extra functionality
          of redirecting users to the log in page if they are not authenticated.
          Output:
            (HTTPResponse): Either redirects the user to the login page or returns the Dashboard Page
          """
          if not request.user.is_authenticated:
              return redirect('loginuser')
          return super().dispatch(request, *args, **kwargs)

class CreateTaskView(CreateView):
    """
    Class based view to add new records to the Tasks table
    """
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('dashboard')
    template_name = 'tasks/create_task.html'

    def form_valid(self, form):
        """
        Args:
          form (Form): The form recieved in the request sent with all of the data inside
        Fills the field created_by with the currently logged in user
        passes the form through to the parent method.
        Output:
          HttpResponse: Returns the user to the success_url
        """
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
            """
            Args:
              request (HttpRequest): The incoming HTTP request.
              *args: Positional arguments passed through to the parent method
              **kwargs: Keyword arguments passed through to the parent method
            Overrides the base dispatch method by adding the extra functionality
            of redirecting users to the log in page if they are not authenticated.
            Output:
              (HTTPResponse): Either redirects the user to the login page or returns the Dashboard Page
            """
            if not request.user.is_authenticated:
                return redirect('loginuser')
            return super().dispatch(request, *args, **kwargs)

class DetailTaskView(DetailView):
    model = Task
    template_name = 'tasks/view_task.html'

    def get_context_data(self, **kwargs):
         """
         Args:
           **kwargs: Keyword arguments passed through to the parent method
         Overrides the base get_context_data method by adding more data to the context dict
         adds the following:
           notes_form the form for the notes attached to the current task
           notes (Note.model): All the notes for a task
         Output:
           context (dictionary) all of the context sent to the template
         """
         context =  super().get_context_data(**kwargs)  
         context['notes_form'] = NotesForm()
         context['notes'] = self.object.task_notes.all()
         return context
    
    def get_object(self, queryset= None):
         """
         Args:
            queryset (QuerySet, optional): QuerySet to look the task up in.
            if queryset = None then it defaults to the views own queryset.

         Gets the task and if the assignee is not the current user raises an exception
         otherwise returns the task

         Output:
           task (Task): task chosen by the user
           
         """
         task = super().get_object(queryset)
         if task.assigned_to != self.request.user:
              raise PermissionDenied
         return task

    def post(self, request, *args, **kwargs):
         """
         Args:
           request (HttpRequest): The incoming HTTP request.
           *args: Positional arguments passed through to the parent method
           **kwargs: Keyword arguments passed through to the parent method
         Handles the post requests to the DetailTaskView page.
         Output:
           redirects the user to the view_task after a completed form
         """
         self.object = self.get_object()
         form = NotesForm(request.POST)
         if form.is_valid():
              note = form.save(commit= False)
              note.on_task = self.object
              note.by_user = request.user
              note.save()
              return redirect('view_task', pk = self.object.pk)
         

class UpdateTaskView(UpdateView):
    model = Task
    template_name = 'tasks/edit_task.html'
    
    def get_success_url(self):
        """
        sets the success url to view_task with pk = self.object.pk
        if a task is updated user is sent back to the view task page of that same task
        """
        return reverse_lazy('view_task', kwargs = {'pk': self.object.pk})

    def get_object(self, queryset = None):
        """
        Args:
           queryset (QuerySet, optional): QuerySet to look the task up in.
           if queryset = None then it defaults to the views own queryset.

        Gets the task and if the assignee or the creaator is not the current user raises an exception
        otherwise returns the task.

        Output:
          task (Task): task chosen by the user
       
        """
        task = super().get_object(queryset)
        if self.request.user.id not in (task.created_by.id, task.assigned_to.id):
             raise PermissionDenied
        return task
    
    def get_form_class(self):
        """
        Method that swaps between forms if the user that sent the request created the task.
        """
        if self.request.user.id == self.object.created_by.id:
            return TaskForm
        return TaskAsigneeForm
            

class DeleteTaskView(DeleteView):
     model = Task
     template_name = 'tasks/delete_task.html'
     success_url = reverse_lazy('dashboard')

     def dispatch(self, request, *args, **kwargs):
         """
         Args:
           request (HttpRequest): The incoming HTTP request.
           *args: Positional arguments passed through to the parent method
           **kwargs: Keyword arguments passed through to the parent method
         Overrides the base dispatch method by adding the extra functionality
         of redirecting users to the log in page if they are not authenticated.
         Output:
           (HTTPResponse): Either redirects the user to the login page or returns the Dashboard Page
         """
         if not request.user.is_authenticated:
             return redirect('loginuser')
         return super().dispatch(request, *args, **kwargs)

class AllTasksView(ListView):
     model = Task
     template_name = 'tasks/all_tasks.html'
 
     def get_context_data(self, **kwargs):
          """
          Args:
            **kwargs: Keyword arguments passed through to the parent method
          Overrides the base get_context_data method by adding more data to the context dict
          adds the following:
            users (User) = all users registered in the systen
          Output:
            context (dictionary) all of the context sent to the template
          """
          context = super().get_context_data(**kwargs)
          context['users'] = User.objects.all()
          return context
     def get_queryset(self):
          priority = self.request.GET.get('priority','')
          status = self.request.GET.get('status', '')
          assignee = self.request.GET.get('assignee','')
          tasks = Task.objects.all()
          if priority:
               tasks = tasks.filter(priority=priority)
          if status:
               tasks = tasks.filter(status = status)
          if assignee:
               tasks = tasks.filter(assigned_to =assignee)
          return tasks

     def dispatch(self, request, *args, **kwargs):
          """
          Args:
            request (HttpRequest): The incoming HTTP request.
            *args: Positional arguments passed through to the parent method
            **kwargs: Keyword arguments passed through to the parent method
          Overrides the base dispatch method by adding the extra functionality
          of redirecting users to the log in page if they are not authenticated.
          Output:
            (HTTPResponse): Either redirects the user to the login page or returns the Dashboard Page
          """
          if not request.user.is_authenticated:
              return redirect('loginuser')
          return super().dispatch(request, *args, **kwargs)