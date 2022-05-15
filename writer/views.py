import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from authentication.models import UserInformation
from core.models import Category
from projects.models import Project, Question
from writer.writer_controller import WriterController


class UserProfileView(LoginRequiredMixin, View):
    template_name = "writer/profile.html"

    def get(self, request, *args, **kwargs):
        user = UserInformation.objects.get(user_id=request.user.id)
        return render(request, self.template_name, {
            'user': user,
        })

    def post(self, request, *args, **kwargs):
        try:
            user_info = UserInformation.objects.get(user=request.user)
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            identification = request.POST.get('identification')
            cellphone = request.POST.get('cellphone')
            terms_conditions = request.POST.get('terms_conditions')
            biography = request.POST.get('biography')

            user_info.biography = biography
            user_info.identification = identification
            user_info.cellphone = cellphone
            user_info.save()

            user = user_info.user
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            messages.info(request, "Información personal actualizada")
            return redirect(reverse_lazy('writer:profile'))
        except Exception as e:
            messages.error(request, "Tenemos un error al intentar guardar tu información. "
                                    "Por favor verifica que los campos estén completos")
            return redirect(reverse_lazy('writer:profile'))


class ProjectsDashboardView(LoginRequiredMixin, View):
    template_name = "writer/projects_dashboard.html"

    def get(self, request, *args, **kwargs):
        user = UserInformation.objects.get(user_id=request.user.id)
        qualified = Project.objects.filter(status=Project.QUALIFIED).count()
        send = Project.objects.filter(status=Project.SEND).count()
        for_correction = Project.objects.filter(
            Q(status=Project.FOR_CORRECTION) | Q(status=Project.DRAFT) | Q(status=Project.CREATED)
        ).count()
        in_correction = Project.objects.filter(status=Project.IN_CORRECTION).count()
        total_projects = Project.objects.all().count()
        return render(request, self.template_name, {
            'user': user,
            'qualified': qualified,
            'send': send,
            'for_correction': for_correction,
            'in_correction': in_correction,
            'total_projects': total_projects,
        })


class ProjectsEditView(LoginRequiredMixin, View):
    template_name = "writer/project_edit.html"

    def get(self, request, *args, **kwargs):
        user = UserInformation.objects.get(user_id=request.user.id)
        project = Project.objects.get(id=kwargs.get('id'), author_id=request.user.id)
        categories_project = [{'id': cat.id, 'name': cat.name} for cat in project.category.only('id', 'name')]
        categories = Category.objects.all()
        return render(request, self.template_name, {
            'user': user,
            'project': project,
            'categories_project': categories_project,
            'categories': categories,
            'count_items': Question.objects.filter(
                project_id=kwargs.get('id'),
                project__author_id=request.user.id
            ).count()
        })

    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        query = Project.objects.get(
            id=data.get('id'),
            author_id=request.user.id
        )
        query.delete()
        return JsonResponse(status=200, data={'id': query.id, 'message': 'Proyecto eliminado'})


class ProjectQuestionsView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        query = Question.objects.filter(
            project_id=kwargs.get('id'),
            project__author_id=request.user.id
        ).only('id', 'title')
        questions = [{'id': q.id, 'title': q.title} for q in query]
        return JsonResponse(status=200, data={'questions': questions})


class ProjectDescriptionQuestionView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        query = Question.objects.get(
            id=kwargs.get('id'),
            project__author_id=request.user.id
        )
        return JsonResponse(status=200, data={'id': query.id, 'title': query.title, 'answer': query.answer})

    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        query = Question.objects.get(
            id=data.get('id'),
            project__author_id=request.user.id
        )
        query.delete()
        return JsonResponse(status=200, data={'id': query.id, 'message': 'Item eliminado'})

    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        query = Question.objects.get(
            id=data.get('id'),
            project__author_id=request.user.id
        )
        is_changed = False
        if query.title != data.get('title'):
            query.title = data.get('title')
            is_changed = True
        if query.answer != data.get('answer'):
            query.answer = data.get('answer')
            is_changed = True

        if is_changed:
            query.save()

        return JsonResponse(status=200,
                            data={'item': {'id': query.id, 'title': query.title},
                                  'message': 'Item actualizado exitosamente'})


class AddProjectView(LoginRequiredMixin, View):
    template_name = "writer/project_add.html"

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        return render(request, self.template_name, {'categories': categories})

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        categories = Category.objects.filter(id__in=data['categories']).only('id').values_list('id', flat=True)
        project = Project.objects.create(
            author=request.user,
            title=data['title'],
            description=data['description'],
            status=Project.CREATED,
            created_by=request.user.id
        )
        for c in categories:
            project.category.add(c)

        return JsonResponse(status=200, data={'id': project.id})

    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        id_project = data.get('id', None)
        if not id_project:
            return JsonResponse(status=400, data={'message': 'Id proyecto no identificado'})

        message, project_id = WriterController.update_project(id_project, data)

        return JsonResponse(
            status=200,
            data={
                'message': message,
                'id': project_id
            }
        )


class AddQuestionsProjectView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        id_project = data.get('id_project', None)
        if not id_project:
            return JsonResponse(status=400, data={'message': 'Id proyecto no identificado'})

        questions = list()
        for q in data.get('questions', None):
            q = Question.objects.create(
                title=q.get('title'),
                answer=q.get('answer'),
                project_id=id_project
            )
            questions.append({
                'id': q.id,
                'title': q.title,
                'answer': q.answer
            })
        print(questions)
        return JsonResponse(status=200, data={'questions': questions, 'message': 'Item creado exitosamente'})
