from wagtail.contrib.modeladmin.options import (ModelAdmin, modeladmin_register)
from home.models import Class, Priority, Problem, Comment, Metric


class ClassAdmin(ModelAdmin):
    model = Class
    base_url_path = 'classes' # customise the URL from default to admin/bookadmin
    menu_label = 'Классы проблем'  # ditch this to use verbose_name_plural from model
    menu_icon = 'cog'  # change as required
    menu_order = 000  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = True  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    add_to_admin_menu = True  # or False to exclude your model from the menu
    # list_display = ('id', 'deletion_mark', 'name')
    # list_filter = ('deletion_mark', 'name')
    # search_fields = ('name')

modeladmin_register(ClassAdmin)


class PriorityAdmin(ModelAdmin):
    model = Priority
    base_url_path = 'priorities' # customise the URL from default to admin/bookadmin
    menu_label = 'Приоритеты проблем'  # ditch this to use verbose_name_plural from model
    menu_icon = 'cog'  # change as required
    menu_order = 000  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = True  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    add_to_admin_menu = True  # or False to exclude your model from the menu
    # list_display = ('id', 'deletion_mark','name', 'superior', 'description', 'icon', 'job_instruction', 'positions_for_tasks')
    # list_filter = ('deletion_mark', 'superior', 'name')
    # search_fields = ('name', 'description')
    # inlines = [CertificateLinkInline,]  # TODO добавить инлайн соотношения с полями классификатора если возможно

modeladmin_register(PriorityAdmin)


class ProblemAdmin(ModelAdmin):
    model = Problem
    base_url_path = 'problems' # customise the URL from default to admin/bookadmin
    menu_label = 'Проблемы'  # ditch this to use verbose_name_plural from model
    menu_icon = 'cog'  # change as required
    menu_order = 000  # 000 being 1st place, 100 - 2nd)
    add_to_settings_menu = True  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    add_to_admin_menu = True  # or False to exclude your model from the menu
    # list_display = ('id', 'test')
    # list_display = ('id', 'deletion_mark','name', 'description', 'icon')
    # list_filter = ('deletion_mark', 'name')
    # search_fields = ('name', 'description')

# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(ProblemAdmin)


class CommentAdmin(ModelAdmin):
    model = Comment
    base_url_path = 'comments' # customise the URL from default to admin/bookadmin
    menu_label = 'Комментарии'  # ditch this to use verbose_name_plural from model
    menu_icon = 'cog'  # change as required
    menu_order = 000  # 000 being 1st place, 100 - 2nd)
    add_to_settings_menu = True  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    add_to_admin_menu = True  # or False to exclude your model from the menu
    # list_display = ('id', 'test')
    # list_display = ('id', 'deletion_mark','name', 'description', 'icon')
    # list_filter = ('deletion_mark', 'name')
    # search_fields = ('name', 'description')

# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(CommentAdmin)

class MetricAdmin(ModelAdmin):
    model = Metric
    base_url_path = 'metrics' # customise the URL from default to admin/bookadmin
    menu_label = 'Метрики'  # ditch this to use verbose_name_plural from model
    menu_icon = 'cog'  # change as required
    menu_order = 000  # 000 being 1st place, 100 - 2nd)
    add_to_settings_menu = True  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    add_to_admin_menu = True  # or False to exclude your model from the menu
    # list_display = ('id', 'test')
    # list_display = ('id', 'deletion_mark','name', 'description', 'icon')
    # list_filter = ('deletion_mark', 'name')
    # search_fields = ('name', 'description')

# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(MetricAdmin)
