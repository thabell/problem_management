from django.db import models
from wagtail.models import Page
from django.utils import timezone
from django.contrib.auth import get_user_model as USER_MODEL
from wagtail.fields import StreamField
from wagtail.blocks import TextBlock, RichTextBlock, BlockQuoteBlock, IntegerBlock, CharBlock, DateBlock, \
    PageChooserBlock, ListBlock, StreamBlock, RawHTMLBlock, URLBlock, StructBlock, BooleanBlock
from wagtail.images.blocks import ImageChooserBlock
from django.db.models import Prefetch
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField

class HomePage(Page):
    pass


class Class(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Класс проблем'
        verbose_name_plural = 'Классы проблем'


class Priority(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Приоритет проблем'
        verbose_name_plural = 'Приоритеты проблем'


class Problem(models.Model):
    STATUS_CHOICES = [
        ('Создано', 'Создано'),
        ('Принято в работу', 'Принято в работу'), 
        ('В работе', 'В работе'),
        ('Решено', 'Решено'),
    ]
    description = models.TextField()
    problem_class = models.ForeignKey(Class, null=True, blank=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(USER_MODEL(), related_name='authored_problems', null=True, blank=True, on_delete=models.SET_NULL)
    assignee = models.ForeignKey(USER_MODEL(), related_name='assigned_problems', null=True, blank=True, on_delete=models.SET_NULL)
    priority = models.ForeignKey(Priority, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Создано')
    created_date = models.DateTimeField(default=timezone.now)
    accepted_date = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    solution_result = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.description
    
    class Meta:
        verbose_name = 'Проблема'
        verbose_name_plural = 'Проблемы'


class Comment(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
    text = models.CharField(max_length=255)
    problem = models.ForeignKey(Problem, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(USER_MODEL(), related_name='authored_comments', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.author) + ":" + str(self.created_date)
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Metric(models.Model):
    created_at = models.DateTimeField(default=timezone.now)

    from django.utils import timezone
    from datetime import timedelta

    last_week = timezone.now() - timedelta(days=7)
    num_solved_last_week_calc = Problem.objects.filter(status='Решено', completed_at__gte=last_week).count()
    num_solved_last_week = models.IntegerField(null=True, blank=True, default=num_solved_last_week_calc)

    num_unsolved_now_calc = Problem.objects.exclude(status='Решено').count()
    num_unsolved_now = models.IntegerField(null=True, blank=True, default=num_unsolved_now_calc)

    num_created_last_week_calc = Problem.objects.filter(created_date__gte=last_week).count()
    num_created_last_week = models.IntegerField(null=True, blank=True, default=num_created_last_week_calc)
    
    unsolved_last_week = num_unsolved_now_calc - num_created_last_week_calc
    if unsolved_last_week > 0:
        solved_last_week_ratio_calc = round(num_solved_last_week_calc / unsolved_last_week, 2)
    else:
        solved_last_week_ratio_calc = 0.0

    solved_last_week_ratio = models.FloatField(null=True, blank=True, default=solved_last_week_ratio_calc)

    from statistics import mean
    completion_times = []
    for problem in Problem.objects.filter(status='Решено'):
        if problem.completed_at and problem.started_at:
            completion_times.append(problem.completed_at - problem.started_at)
    if completion_times:
        avg_solve_time_sec = mean([time.total_seconds() for time in completion_times])
        avg_solve_time_calc = timedelta(seconds=avg_solve_time_sec)
    else:
        avg_solve_time_calc = timedelta()
    avg_solve_time = models.DurationField(null=True, blank=True, default=avg_solve_time_calc)
    
    reaction_times = []
    for problem in Problem.objects.filter(status='Принято в работу'):
        if problem.accepted_date and problem.created_date:
            reaction_times.append(problem.accepted_date - problem.created_date)
    if reaction_times:
        avg_reaction_time_sec = mean([time.total_seconds() for time in reaction_times])
        avg_reaction_time_calc = timedelta(seconds=avg_reaction_time_sec)
    else:
        avg_reaction_time_calc = timedelta()
    avg_reaction_time = models.DurationField(null=True, blank=True, default=avg_reaction_time_calc)

    def __str__(self):
        return str(self.created_at)
    
    class Meta:
        verbose_name = 'Метрика'
        verbose_name_plural = 'Метрики'


class IndexPage(Page):

    class Meta:
        verbose_name = 'Главная страница'
        verbose_name_plural = 'Главные страницы'

    def get_context(self, request, **kwargs):
        context = super().get_context(request)
        context['users'] = USER_MODEL().objects.all()
        context['classes'] = Class.objects.all()
        context['priorities'] = Priority.objects.all()
        context['problems'] = Problem.objects.prefetch_related(Prefetch('comments', queryset=Comment.objects.all().order_by('created_date'))).order_by('created_date')
        # context['kitties'] = KittyPage.objects.all().live().filter(sold=False)
        # context['litter'] = context['kitties'].order_by('litter')[0].litter
        # context['images'] = Image.objects.filter(collection__name="Папа Леголас") \
        #                     | Image.objects.filter(collection__name="Мама Эльза") \
        #                     | Image.objects.filter(collection__name="Прайд D") \
        #                     | Image.objects.filter(collection__name="Прайд C") \
        #                     | Image.objects.filter(collection__name="Прайд A")
        # context['images'] = context['images'].order_by('collection__name')
        return context


class MetricListPage(Page):

    class Meta:
        verbose_name = 'Оценка эффективности'
        verbose_name_plural = 'Оценки эффективности'

    def get_context(self, request, **kwargs):
        context = super().get_context(request)
        context['metrics'] = Metric.objects.all().order_by('created_at')
        return context


from django.shortcuts import render

class MetricPage(Page):

    def serve(self, request):
        from home.forms import MetricForm

        if request.method == 'POST':
            form = MetricForm(request.POST)
            if form.is_valid():
                metric = form.save()
                print("check")
                return render(request, 'home/metric_list_page.html', {
                    'page': MetricListPage.objects.all().order_by('id')[0],
                    'metric': metric,
                })
        else:
            form = MetricForm()

        return render(request, 'home/metric_page.html', {
            'page': self,
            'form': form,
        })

    def __str__(self):
        return str(self.intro)
    
    class Meta:
        verbose_name = 'Страница метрики'
        verbose_name_plural = 'Страницы метрик'

# class ProblemFormPage(Page):
#     intro = RichTextField(blank=True, null=True)
#     thankyou_page_text = models.CharField(
#         max_length=255, help_text="Text to use for the 'thank you' page")

#     # Note that there's nothing here for specifying the actual form fields -
#     # those are still defined in forms.py. There's no benefit to making these
#     # editable within the Wagtail admin, since you'd need to make changes to
#     # the code to make them work anyway.

#     content_panels = Page.content_panels + [
#         FieldPanel('intro', classname="full"),
#         FieldPanel('thankyou_page_text'),
#     ]

#     def serve(self, request):
#         from home.forms import ProblemForm

#         if request.method == 'POST': # тут декомпозиция на создание/редактирование/удаление
#             form = ProblemForm(request.POST)
#             if form.is_valid():
#                 problem = form.save()
#                 return render(request, 'home/thankyou.html', {
#                     'page': self,
#                     'problem': problem,
#                 })
#         else: # тут декомпозиция на получение пустой формы или формы редактирования, то есть по id надо найти
#             form = ProblemForm()

#         return render(request, 'home/suggest.html', {
#             'page': self,
#             'form': form,
#         })