import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from authentication.models import UserInformation
from core.models import Category
from evaluator.evaluator_controller import EvaluatorController
from evaluator.models import Evaluator
from projects.models import Score, Project, Question, FilesApp


class DashboardView(LoginRequiredMixin, View):
    template_name = "evaluator/dashboard.html"

    def get(self, request, *args, **kwargs):
        to_evaluate = Score.objects.filter(
            evaluator__user=request.user,
            project__status=Project.SEND,
            extra__isnull=True,
            question__isnull=True

        )
        return render(request, self.template_name, {'to_evaluate': to_evaluate})

    def post(self, request, *args, **kwargs):
        pass


class ProjectsQualifiedView(LoginRequiredMixin, View):
    template_name = "evaluator/project_qualified.html"

    def get(self, request, *args, **kwargs):
        id_project = kwargs.get('id_project')
        is_assigned = Score.objects.filter(
            evaluator__user=request.user,
            project__status=Project.SEND,
            project_id=id_project,
        ).exists()
        if not is_assigned:
            return redirect(reverse_lazy('evaluator:dashboard'))

        user = UserInformation.objects.get(user_id=request.user.id)
        project = Project.objects.get(id=kwargs.get('id_project'))
        categories_project = [{'id': cat.id, 'name': cat.name} for cat in project.category.only('id', 'name')]
        categories = Category.objects.all()
        return render(request, self.template_name, {
            'user': user,
            'project': project,
            'categories_project': categories_project,
            'categories': categories,
            'count_items': Question.objects.filter(
                project_id=id_project
            ).count()
        })


class ProjectQuestionsView(LoginRequiredMixin, View):

    def get_score(self, id_q):
        sc = Score.objects.filter(question_id=id_q).only('score').values('score').first()
        return int(sc.get('score')) if sc else 0

    def get(self, request, *args, **kwargs):
        query = Question.objects.filter(
            project_id=kwargs.get('id'),
        ).only('id', 'title')
        questions = [{'id': q.id, 'title': q.title, 'score': self.get_score(q.id)} for q in query]
        return JsonResponse(status=200, data={'questions': questions})

    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        print(data)
        score = data.get('score', 0)
        item_id = data.get('item_id', None)
        extra = data.get('extra', None)
        id_project = data.get('id_project', None)
        evaluator = Evaluator.objects.get(user=request.user)

        if extra:
            sc = Score.objects.filter(project_id=id_project, extra=extra).only('score').first()
        else:
            sc = Score.objects.filter(question_id=item_id).only('score').first()

        if sc and sc.score != score:
            sc.score = score
            sc.save()

        if not sc:
            print('=' * 30)
            print(float(score))
            sc = Score.objects.create(
                score=float(score),
                evaluator=evaluator,
                project_id=id_project,
                extra=extra
            )

            if not extra and item_id:
                sc.question_id = item_id
                sc.save()

        return JsonResponse(
            status=200,
            data={
                'item': {'id': sc.id, 'score': sc.score},
                'message': 'Calificación guardada exitosamente',
                'alert': 'success'
            }
        )


class ProjectDescriptionQuestionView(LoginRequiredMixin, View):

    def get_score(self, id_q):
        sc = Score.objects.filter(question_id=id_q).only('score').values('score').first()
        return int(sc.get('score')) if sc else 0

    def get(self, request, *args, **kwargs):
        query = Question.objects.get(
            id=kwargs.get('id'),
        )
        return JsonResponse(
            status=200,
            data={
                'id': query.id, 'title': query.title, 'answer': query.answer, 'score': self.get_score(query.id)
            }
        )


class ProjectScoresQuestionView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return JsonResponse(
            status=200,
            data=EvaluatorController.get_score_project(kwargs.get('id_project'))
        )
