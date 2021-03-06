from django.contrib import admin
from adminsortable.admin import\
    NonSortableParentAdmin, SortableStackedInline, SortableTabularInline
from polls.models import Survey, Poll, CharChoice,\
    SurveyAttribute, Elmail, PollGroup, Visitor, ChoiceGroup
from django.utils.html import format_html
from django.conf.urls import *
from django.shortcuts import render
from dynamic_preferences.admin import *
from polls.forms import CustomPreferenceForm
from image_cropping import ImageCroppingMixin
# from polls.customadminclview import changelist_view as customclview


class CustomPreferenceAdmin(UserPreferenceAdmin):
    form = CustomPreferenceForm
    changelist_form = CustomPreferenceForm
    list_display_links = None
    actions = None
    list_display = ('verbose_name', 'help_text', 'raw_value')

    def get_queryset(self, request):
        qs = super(CustomPreferenceAdmin, self).get_queryset(request)
        return qs.filter(instance=request.user)

    def has_delete_permission(request, obj=None):
        return False

    def has_add_permission(request, obj=None):
        return False


class EmailAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'body',)
    exclude = ('user',)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super(EmailAdmin, self).get_queryset(request)
        return qs.filter(user=request.user)


class ChoiceSortableTabularInline(SortableStackedInline):

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "nested":
            kwargs["queryset"] = Poll.objects.filter(user=request.user)
        return super(ChoiceSortableTabularInline, self).formfield_for_manytomany(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "group":
            kwargs["queryset"] = ChoiceGroup.objects.filter(user=request.user)
        return super(ChoiceSortableTabularInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

    model = CharChoice
    exclude = ['created_by_visitor', 'user']
    filter_horizontal = ('nested',)
    extra = 0

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super(ChoiceSortableTabularInline, self).get_queryset(request)
        return qs.filter(created_by_visitor=False, user=request.user)


class PollTabularInline(SortableTabularInline):
    model = Poll
    show_change_link = True
    fields = ('poll_type', 'question', 'group', 'first_level', 'include_in_raport',
              'include_in_details', 'ghost',)
    extra = 0

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super(PollTabularInline, self).get_queryset(request)
        try:
            survey = qs[0].survey
            if survey.hide_ghost:
                qs = qs.filter(ghost=False, user=request.user)
        except:
            pass
        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "group":
            kwargs["queryset"] = PollGroup.objects.filter(user=request.user)
        return super(PollTabularInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


class SurveyAttributeTabularInline(SortableTabularInline):
    model = SurveyAttribute
    fields = ['name', 'dicti', 'attr_type', 'polls']
    readonly_fields = ['dicti']
    filter_horizontal = ('polls',)
    extra = 0

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "polls":
            kwargs["queryset"] = Poll.objects.filter(user=request.user)
        return super(SurveyAttributeTabularInline, self).formfield_for_manytomany(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super(SurveyAttributeTabularInline, self).get_queryset(request)
        return qs.filter(user=request.user)


class SurveyAdmin(ImageCroppingMixin, NonSortableParentAdmin):
    review_template = 'admin/polls/survey/report.html'

    readonly_fields = ('created', 'url',)

    fieldsets = (
        (None,
            {
                'fields':
                    ('title', 'description', 'created', 'url', 'notify',
                        ('welcome_letter', 'newsletter', 'hide_ghost'),)
            }),
        ('Rendering options',
            {
                'classes': ('collapse',),
                'fields':
                    (
                        ('header_size', 'header_color'),
                        ('description_size', 'description_color'),
                        ('question_size', 'question_color'),
                        ('choice_size', 'choice_color'),
                        ('choice_indent', 'nested_indent'),
                        'background_color', 'font',
                        ('logo', 'logo_height'),
                        ('cropping'),
                        ('left_margin', 'top_margin'),
                )}))

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super(SurveyAdmin, self).get_queryset(request)
        return qs.filter(user=request.user)

    def update_fixtures(self, obj):
        return format_html('<a href="/build/">Build!</a>')

    def get_urls(self):
        urls = super(SurveyAdmin, self).get_urls()
        my_urls = [url(r'report/$', self.report), ]
        return my_urls + urls

    def report(self, request, *args, **kwargs):
        visitors = Visitor.objects.filter(user=request.user)
        sum_dict = {}

        included_poll_groups = [poll.group.name for poll in Poll.objects.filter(include_in_raport=True)]
        for visitor in visitors:
            for keyval in visitor.collected_data.keyval_set.all():
                if keyval.key in included_poll_groups:
                    if keyval.key not in sum_dict.keys():
                        sum_dict[keyval.key] = {}
                    for choice in keyval.listify():
                        if choice not in sum_dict[keyval.key].keys():
                            sum_dict[keyval.key][choice] = 0
                        sum_dict[keyval.key][choice] += 1

        for survey_attr in SurveyAttribute.objects.filter(include_in_raport=True):
            sum_dict[survey_attr.name] = {}

            for keyval in survey_attr.dicti.keyval_set.all():
                sum_dict[survey_attr.name][keyval.key] = keyval.value

        context = {
            "sum_dict": sum_dict,
            "title": "Report",
            "opts": self.model._meta,
        }
        return render(request, self.review_template, context)

    inlines = [
        SurveyAttributeTabularInline,
        PollTabularInline]

    def save_formset(self, request, form, formset, change):
        formset.save()
        for f in formset.forms:
            obj = f.instance
            print('obj', obj)
            obj.user = request.user
            try:
                if not obj.group:
                    obj.group, create = PollGroup.objects.get_or_create(
                        name=obj.question,
                        user=obj.user)
            except AttributeError:
                pass
            obj.save()

    class Media:
        extend = False
        js = ["/static/jquery-3.1.1.js",
              "/static/jquery-ui.min.js",
              "/static/admin/js/custom_inlines.js"
              ]
        css = {'all': ("/static/admin/css/custom-admin.css",)}


class PollAdmin(NonSortableParentAdmin):
    model = Poll
    exclude = ('user',)
    inlines = [ChoiceSortableTabularInline]
    list_display = ('group', 'question', 'poll_type')

    def save_model(self, request, obj, form, change):
        if not obj.group:
            obj.group, create = ChoiceGroup.objects.get_or_create(
                name=obj.question,
                user=obj.user)
        obj.user = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super(PollAdmin, self).get_queryset(request)
        return qs.filter(user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "group":
            kwargs["queryset"] = PollGroup.objects.filter(user=request.user)
        if db_field.name == 'survey':
            kwargs["queryset"] = Survey.objects.filter(user=request.user)
        return super(PollAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def save_formset(self, request, form, formset, change):
        formset.save()
        for f in formset.forms:
            obj = f.instance
            print('obj', obj)
            obj.user = request.user
            if not obj.group:
                obj.group, create = ChoiceGroup.objects.get_or_create(
                    name=obj.choice_text,
                    user=obj.user)
            obj.save()

    model = Poll
    exclude = ('user',)
    inlines = [ChoiceSortableTabularInline]
    list_display = ('group', 'question', 'poll_type')


class SurveyAttributeAdmin(NonSortableParentAdmin):
    list_display = ('name', 'tab',)
    model = SurveyAttribute

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super(SurveyAttributeAdmin, self).get_queryset(request)
        return qs.filter(user=request.user)

    def tab(self, obj):
        try:
            return format_html(obj.dicti.dict_table())
        except:
            return 'still empty'


class ChoiceGroupAdmin(admin.ModelAdmin):
    exclude = ('user',)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super(ChoiceGroupAdmin, self).get_queryset(request)
        return qs.filter(user=request.user)


class PollGroupAdmin(admin.ModelAdmin):
    exclude = ('user',)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super(PollGroupAdmin, self).get_queryset(request)
        return qs.filter(user=request.user)


class VisitorAdmin(admin.ModelAdmin):

    def changelist_view(self, request):
        response = super(VisitorAdmin, self).changelist_view(request)
        visitors = Visitor.objects.filter(user=request.user).order_by('-filled')
        response.context_data.update({'visitors': visitors})
        return response


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Poll, PollAdmin)
admin.site.register(PollGroup, PollGroupAdmin)
admin.site.register(ChoiceGroup, ChoiceGroupAdmin)
admin.site.register(Elmail, EmailAdmin)
admin.site.register(Visitor, VisitorAdmin)
admin.site.register(SurveyAttribute, SurveyAttributeAdmin)
admin.site.unregister(GlobalPreferenceModel)
admin.site.unregister(UserPreferenceModel)
admin.site.register(UserPreferenceModel, CustomPreferenceAdmin)
# admin.site.register(SurveyPreferenceModel, SurveyPreferenceAdmin)

admin.site.site_title = 'Survey Administration'
admin.site.index_title = 'Manage Your Surveys'
admin.site.site_header = 'Survey Administration'
admin.site.index_template = 'admin/custom-index.html'
admin.site.login_template = 'admin/custom-login.html'
