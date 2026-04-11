from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Project
from .forms import ProjectForm

def projects(request):
    projects = Project.objects.filter(owner=request.user)

    return render(request, "portfolio/projects.html", {
        "projects": projects
    })

def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()

            return redirect("user_projects", username=request.user.username)

    else:
        form = ProjectForm()

    return render(request, "portfolio/create_project.html", {"form": form})

def delete_project(request, id):
    project = get_object_or_404(Project, id=id)

    if project.owner != request.user:
        return redirect("projects")

    project.delete()

    return redirect("user_projects", username=request.user.username)

def user_projects(request, username):
    user = User.objects.get(username=username)
    projects = Project.objects.filter(owner=user)

    return render(request, "portfolio/user_projects.html", {
        "projects": projects,
        "profile_user": user
    })