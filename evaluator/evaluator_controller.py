from django.db.models import Sum

from projects.models import FilesApp, Score


class EvaluatorController:
    @staticmethod
    def get_score_project(project_id: int):
        scores = Score.objects.filter(
            project_id=project_id,
        ).only('score', 'extra')

        score_g = scores.filter(extra=Score.GENERAL).first()
        score_g = int(score_g.score) if score_g else 0

        score_f = scores.filter(extra=Score.FILES).first()
        score_f = int(score_f.score) if score_f else 0

        items = scores.exclude(extra__isnull=False).exclude(question__isnull=True)
        print('items:::::::: ', items)
        is_files = FilesApp.objects.filter(project_id=project_id).exists()
        total = items.count() + 1
        if is_files:
            total += 1

        sum_items = items.aggregate(Sum('score')) if items else {}
        s_t = sum_items.get('score__sum') if sum_items else 0
        score_t = round(((s_t + score_f + score_g) / total), 2)
        score_i = round((s_t / items.count()), 2) if items else 0

        return {
            'score_t': score_t,
            'score_g': score_g,
            'score_i': score_i,
            'score_f': score_f,
        }
