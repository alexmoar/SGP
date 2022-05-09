from projects.models import Project


class WriterController:
    @staticmethod
    def update_categories(project: Project, categories: list, is_updated: bool):
        """"""
        categories_old = list(project.category.all().only('id').values_list('id', flat=True))
        print("categories_old: ", categories_old)
        print("categories: ", categories)
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

        message = ''
        if is_updated:
            project.save()
            message = 'Proyecto actualizado'

        return message, project.id
