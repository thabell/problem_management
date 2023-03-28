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


# from django.utils import timezone
from datetime import timedelta, datetime

class Metric(models.Model):
    # created_at_culc = timezone.now
    created_at_culc = datetime.now()
    created_at = models.DateTimeField("Дата формирования отчета:", default=created_at_culc)
    print(created_at_culc)
    print(datetime.weekday(created_at_culc))  # день недели текущей даты
    date_start = datetime.fromordinal(datetime.toordinal(datetime.date(created_at_culc - timedelta(days=(7 + datetime.weekday(created_at_culc))))))
    print(date_start)  # полученный прошедший понедельник предыдущей недели от текущей даты в формате 2023-03-20 00:00:00 (в запросе включаются концы)
    print(datetime.weekday(date_start))  # день недели полученной даты (должен быть понедельник (0))
    date_stop = date_start + timedelta(days=7) - timedelta(seconds=1)
    print(date_stop)  # полученный следующий за секунду до понедельника от текущей даты в формате 2023-03-26 23:59:59 (в запросе включаются концы)
    
    print(Problem.objects.filter(completed_at__range=(date_start, date_stop)))
    num_solved_last_week_calc = Problem.objects.filter(completed_at__range=(date_start, date_stop)).count()
    num_solved_last_week = models.IntegerField("Решено на прошлой неделе",null=True, blank=True, default=num_solved_last_week_calc)
    print("Решено на прошлой неделе", num_solved_last_week_calc)

    num_unsolved_week_start_calc = (Problem.objects.filter(completed_at__isnull=False) & Problem.objects.filter(completed_at__gt=date_stop) & Problem.objects.filter(created_date__lte=date_stop)).count() + (Problem.objects.filter(completed_at__isnull=True) & Problem.objects.filter(created_date__lte=date_stop)).count()
    num_unsolved_week_start = models.IntegerField("Не решено на начало текущей недели",null=True, blank=True, default=num_unsolved_week_start_calc)
    print("Не решено на начало текущей недели", num_unsolved_week_start_calc)

    num_created_last_week_calc = Problem.objects.filter(created_date__range=(date_start, date_stop)).count()
    print("Создано на прошлой неделе", num_created_last_week_calc)
    num_created_last_week = models.IntegerField("Создано на прошлой неделе",null=True, blank=True, default=num_created_last_week_calc)
    
    unsolved_last_week_start_calc = (Problem.objects.filter(completed_at__isnull=False) & Problem.objects.filter(completed_at__gt=(date_start - timedelta(seconds=1))) & Problem.objects.filter(created_date__lt=(date_start - timedelta(seconds=1)))).count() + (Problem.objects.filter(completed_at__isnull=True) & Problem.objects.filter(created_date__lt=(date_start - timedelta(seconds=1)))).count()
    unsolved_last_week_start = models.IntegerField("Не решено на начало прошлой недели", null=True, blank=True, default=unsolved_last_week_start_calc)
    print("Не решено на начало прошлой недели", unsolved_last_week_start_calc)

    if unsolved_last_week_start_calc > 0:
        solved_last_week_ratio_calc = round((num_solved_last_week_calc / unsolved_last_week_start_calc * 100), 2)
    else:
        solved_last_week_ratio_calc = 100.00
    solved_last_week_ratio = models.FloatField("Процент решенных проблем за прошлую неделю от общего числа нерешенных на начало прошлой недели",null=True, blank=True, default=solved_last_week_ratio_calc)
    print("Процент решенных проблем за прошлую неделю от общего числа нерешенных на начало прошлой недели", solved_last_week_ratio_calc)

    from statistics import mean
    completion_times = []
    for problem in Problem.objects.filter(completed_at__range=(date_start, date_stop)):
        if problem.completed_at and problem.started_at:
            completion_times.append(problem.completed_at - problem.started_at)
    if completion_times:
        avg_solve_time_sec = mean([time.total_seconds() for time in completion_times])
        avg_solve_time_calc = timedelta(seconds=avg_solve_time_sec)
    else:
        avg_solve_time_calc = timedelta()
    avg_solve_time = models.DurationField("Среднее время решения задачи на прошлой неделе",null=True, blank=True, default=avg_solve_time_calc)
    print("Среднее время решения задачи на прошлой неделе", avg_solve_time_calc)
    
    reaction_times = []
    for problem in Problem.objects.filter(accepted_date__range=(date_start, date_stop)):
        if problem.accepted_date and problem.created_date:
            reaction_times.append(problem.accepted_date - problem.created_date)
    if reaction_times:
        avg_reaction_time_sec = mean([time.total_seconds() for time in reaction_times])
        avg_reaction_time_calc = timedelta(seconds=avg_reaction_time_sec)
    else:
        avg_reaction_time_calc = timedelta()
    avg_reaction_time = models.DurationField("Среднее время реакции на задачу на прошлой неделе",null=True, blank=True, default=avg_reaction_time_calc)
    print("Среднее время реакции на задачу на прошлой неделе", avg_reaction_time_calc)

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
        context['problems'] = Problem.objects.prefetch_related(Prefetch('comments', queryset=Comment.objects.all().order_by('created_date'))).order_by('-created_date')
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
        # context['metrics'] = Metric.objects.annotate(
        #     avg_solve_time_sec=Extract('avg_solve_time', 'second'),
        #     avg_reaction_time_sec=Extract('avg_reaction_time', 'second')
        #     ).order_by('created_at')
        context['metrics'] = Metric.objects.all().order_by('created_at')
        context['metrics_reverse'] = Metric.objects.all().order_by('-created_at')
        return context


from django.shortcuts import redirect, render

class MetricPage(Page):

    def serve(self, request):
        from home.forms import MetricForm

        if request.method == 'POST':
            if "reculc" in request.POST:
                form = MetricForm(request.POST)
                if form.is_valid():
                    created_at_culc = form.cleaned_data["created_at"]
                    print(created_at_culc)
                    print(datetime.weekday(created_at_culc))  # день недели текущей даты
                    date_start = datetime.fromordinal(datetime.toordinal(datetime.date(created_at_culc - timedelta(days=(7 + datetime.weekday(created_at_culc))))))
                    print(date_start)  # полученный прошедший понедельник предыдущей недели от текущей даты в формате 2023-03-20 00:00:00 (в запросе включаются концы)
                    print(datetime.weekday(date_start))  # день недели полученной даты (должен быть понедельник (0))
                    date_stop = date_start + timedelta(days=7) - timedelta(seconds=1)
                    print(date_stop)  # полученный следующий за секунду до понедельника от текущей даты в формате 2023-03-26 23:59:59 (в запросе включаются концы)
                    
                    print(Problem.objects.filter(completed_at__range=(date_start, date_stop)))
                    num_solved_last_week_calc = Problem.objects.filter(completed_at__range=(date_start, date_stop)).count()
                    # num_solved_last_week = models.IntegerField(null=True, blank=True, default=num_solved_last_week_calc)
                    print("Решено на прошлой неделе", num_solved_last_week_calc)

                    num_unsolved_week_start_calc = (Problem.objects.filter(completed_at__isnull=False) & Problem.objects.filter(completed_at__gt=date_stop) & Problem.objects.filter(created_date__lte=date_stop)).count() + (Problem.objects.filter(completed_at__isnull=True) & Problem.objects.filter(created_date__lte=date_stop)).count()
                    # num_unsolved_week_start = models.IntegerField(null=True, blank=True, default=num_unsolved_week_start_calc)
                    print("Не решено на начало текущей недели", num_unsolved_week_start_calc)

                    num_created_last_week_calc = Problem.objects.filter(created_date__range=(date_start, date_stop)).count()
                    print("Создано на прошлой неделе", num_created_last_week_calc)
                    # num_created_last_week = models.IntegerField(null=True, blank=True, default=num_created_last_week_calc)
                    
                    # unsolved_last_week_start_calc = num_unsolved_week_start_calc - num_solved_last_week_calc
                    unsolved_last_week_start_calc = (Problem.objects.filter(completed_at__isnull=False) & Problem.objects.filter(completed_at__gt=(date_start - timedelta(seconds=1))) & Problem.objects.filter(created_date__lt=(date_start - timedelta(seconds=1)))).count() + (Problem.objects.filter(completed_at__isnull=True) & Problem.objects.filter(created_date__lt=(date_start - timedelta(seconds=1)))).count()
                    # unsolved_last_week_start = models.IntegerField(null=True, blank=True, default=unsolved_last_week_start_calc)
                    print("Не решено на начало прошлой недели", unsolved_last_week_start_calc)

                    if unsolved_last_week_start_calc > 0:
                        solved_last_week_ratio_calc = round((num_solved_last_week_calc / unsolved_last_week_start_calc * 100), 2)
                    else:
                        solved_last_week_ratio_calc = 100.00
                    # solved_last_week_ratio = models.FloatField(null=True, blank=True, default=solved_last_week_ratio_calc)
                    print("Процент решенных проблем за прошлую неделю от общего числа нерешенных на начало прошлой недели", solved_last_week_ratio_calc)

                    from statistics import mean
                    completion_times = []
                    for problem in Problem.objects.filter(completed_at__range=(date_start, date_stop)):
                        if problem.completed_at and problem.started_at:
                            completion_times.append(problem.completed_at - problem.started_at)
                    if completion_times:
                        avg_solve_time_sec = mean([time.total_seconds() for time in completion_times])
                        avg_solve_time_calc = timedelta(seconds=avg_solve_time_sec)
                    else:
                        avg_solve_time_calc = timedelta()
                    # avg_solve_time = models.DurationField(null=True, blank=True, default=avg_solve_time_calc)
                    print("Среднее время решения задачи на прошлой неделе", avg_solve_time_calc)
                    
                    reaction_times = []
                    for problem in Problem.objects.filter(accepted_date__range=(date_start, date_stop)):
                        if problem.accepted_date and problem.created_date:
                            reaction_times.append(problem.accepted_date - problem.created_date)
                    if reaction_times:
                        avg_reaction_time_sec = mean([time.total_seconds() for time in reaction_times])
                        avg_reaction_time_calc = timedelta(seconds=avg_reaction_time_sec)
                    else:
                        avg_reaction_time_calc = timedelta()
                    # avg_reaction_time = models.DurationField(null=True, blank=True, default=avg_reaction_time_calc)
                    print("Среднее время реакции на задачу на прошлой неделе", avg_reaction_time_calc)

                    form = MetricForm(initial={
                        'created_at': created_at_culc,
                        'num_solved_last_week': num_solved_last_week_calc,
                        'num_unsolved_week_start': num_unsolved_week_start_calc,
                        'num_created_last_week': num_created_last_week_calc,
                        'unsolved_last_week_start': unsolved_last_week_start_calc,
                        'solved_last_week_ratio': solved_last_week_ratio_calc,
                        'avg_solve_time': avg_solve_time_calc,
                        'avg_reaction_time': avg_reaction_time_calc 
                        })
                    return render(request, 'home/metric_page.html', {
                        'page': self,
                        'form': form,
                    })
                    # TODO поправить отрисовку
            else:
                form = MetricForm(request.POST)
                if form.is_valid():
                    metric = form.save()
                    return redirect(MetricListPage.objects.all().order_by('id')[0].get_url())
                    # return render(request, 'home/metric_list_page.html', {
                    #     'page': MetricListPage.objects.all().order_by('id')[0],
                    #     'metrics': Metric.objects.all().order_by('-created_at'),
                    # })
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