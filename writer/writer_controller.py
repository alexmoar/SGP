from projects.models import Project, Question


class WriterController:
    @staticmethod
    def update_categories(project: Project, categories: list, is_updated: bool):
        """"""
        categories_old = list(project.category.all().only('id').values_list('id', flat=True))
        for c in categories_old:
            if not str(c) in categories:
                project.category.remove(c)
                is_updated = True
            else:
                categories.remove(str(c))

        for c in categories:
            project.category.add(c)
            is_updated = True

        return is_updated

    @classmethod
    def update_project(cls, id_project: int, data: dict):
        """"""
        title = data.get('title')
        description = data.get('description')
        status = data.get('status')
        project = Project.objects.get(id=id_project)
        is_updated = False
        if project.title != title:
            project.title = title
            is_updated = True
        if project.status != status:
            project.status = status
            is_updated = True
        if project.description != description:
            project.description = description
            is_updated = True

        is_updated = cls.update_categories(project, data.get('categories'), is_updated)

        if is_updated:
            project.save()
            message = 'Proyecto actualizado'
            alert = 'success'
        else:
            message = 'No tenemos información para actualizar'
            alert = 'warning'

        return message, alert, project.id

    @classmethod
    def update_questions(cls, data, request):
        """Update questions items project"""
        query = Question.objects.get(
            id=int(data.get('id')),
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

        return query

    @classmethod
    def delete_question(cls, data, request):
        query = Question.objects.get(
            id=int(data.get('id')),
            project__author_id=request.user.id
        )
        query.delete()
        return query
