from django.shortcuts import render # type: ignore

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.urls import reverse_lazy # type: ignore
from django.views.generic import ListView, CreateView, UpdateView, DeleteView # type: ignore
from .models import Task
from .forms import TaskForm
from .optimizer import optimize_schedule

class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'scheduled_tasks'
    
    def get_queryset(self):
        # Get incomplete tasks
        incomplete_tasks = Task.objects.filter(completed=False).order_by('deadline')
        # Run the optimizer
        return optimize_schedule(incomplete_tasks)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['completed_tasks'] = Task.objects.filter(completed=True).order_by('-created_at')
        return context

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task-list')

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task-list')

class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('task-list')
    template_name = 'tasks/task_confirm_delete.html'

def complete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed = True
    task.save()
    return redirect('task-list')

def reopen_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed = False
    task.save()
    return redirect('task-list')