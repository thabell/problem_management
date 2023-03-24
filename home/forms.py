from django import forms

from home.models import Class, Priority, Problem, Comment, Metric


# class ProblemForm(forms.ModelForm):

#     class Meta:
#         model = Problem


# class CommentForm(forms.ModelForm):

#     class Meta:
#         model = Comment


class MetricForm(forms.ModelForm):

    class Meta:
        model = Metric
        fields = ['created_at', 'num_solved_last_week', 'num_unsolved_now', 'num_created_last_week', 'solved_last_week_ratio', 'avg_solve_time', 'avg_reaction_time']
