from django.shortcuts import render
# from django.http import HttpResponse
from django.http import HttpResponseRedirect
from polls.models import *
from django.core.mail import get_connection, send_mail
from django.conf import settings
from polls.forms import RegistrationForm
from django.contrib.auth import authenticate, login
from django.core.cache import cache
cache.clear()

permission_list = []


def register(request):
    for p in range(16, 500):
        permission_list.append(p)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = User.objects.create_user(
                username=username,
                password=password,
                email=form.cleaned_data['email'],
                is_staff=True
            )
            for perm in range(16, 500):
                try:
                    user.user_permissions.add(perm)
                except:
                    pass
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/admin/')
    else:
        form = RegistrationForm()

    return render(request, 'admin/registration.html', {'form': form})


def build_survey(request, survey_id):
    survey = Survey.objects.get(pk=survey_id)
    name = ''
    if request.method == 'POST':
        new_visitor = Visitor.objects.create(survey=survey, user=survey.user)
        data = Dicty.objects.create(name=new_visitor.pk)
        print('request.POST: ', request.POST)
        for key in request.POST:
            if key != 'csrfmiddlewaretoken':
                poll = Poll.objects.get(pk=key)

                if poll.poll_type == 'multi':
                    charchoices = CharChoice.objects.filter(
                        pk__in=request.POST.getlist(key))
                    new_visitor.choices.add(*charchoices)
                    KeyVal.objects.create(
                        container=data,
                        key=poll.group.name,
                        value=str([choice.group.name for choice in charchoices]))
                    new_visitor.collected_data = data
                    new_visitor.save()

                elif poll.poll_type == 'one':
                    choice = CharChoice.objects.get(
                        pk=request.POST[key])
                    new_visitor.choices.add(choice)
                    KeyVal.objects.create(
                        container=data,
                        key=poll.group.name,
                        value=choice.group.name)
                    new_visitor.collected_data = data
                    new_visitor.save()

                else:
                    choice, create = CharChoice.objects.get_or_create(
                        choice_text=request.POST[key],
                        poll=poll,
                        created_by_visitor=True,
                        user=survey.user)
                    new_visitor.choices.add(choice)
                    KeyVal.objects.create(
                        container=data,
                        key=poll.group.name,
                        value=choice)
                    new_visitor.collected_data = data
                    new_visitor.save()

                for survey_attr in survey.surveyattribute_set.all():
                    if poll in survey_attr.polls.all():
                        if survey_attr.attr_type == 'summarize':
                            survey_attr.summarize(int(choice.choice_text))

                        if survey_attr.attr_type == 'count':
                            survey_attr.count(poll, choice)

                if poll.poll_type == 'email_now':
                    email = choice.choice_text

                if poll.poll_type == 'first_name':
                    name = choice.choice_text
        try:
            split_body = survey.welcome_letter.body.split('//')
            body = ''
            for part in split_body:
                if part == 'first_name':
                    part = name
                body += part

            send_mail(
                survey.welcome_letter.subject,
                body,
                survey.user.preferences['email_settings__email_host_user'],
                [email],
                connection=get_connection(
                    host=survey.user.preferences['email_settings__comment_notifications_enabled'],
                    port=survey.user.preferences['email_settings__email_port'],
                    password=survey.user.preferences['email_settings__email_password'],
                    username=survey.user.preferences['email_settings__email_host_user'],
                    use_tls=survey.user.preferences['email_settings__enable_TSL']),
                fail_silently=False)
            message = ''

            if survey.notify:
                send_mail(
                    'submit notification',
                    message,
                    survey.user.preferences['email_settings__email_host_user'],
                    [survey.user.email],
                    html_message=new_visitor.print_visitor(),
                    connection=get_connection(
                        host=survey.user.preferences['email_settings__comment_notifications_enabled'],
                        port=survey.user.preferences['email_settings__email_port'],
                        password=survey.user.preferences['email_settings__email_password'],
                        username=survey.user.preferences['email_settings__email_host_user'],
                        use_tls=survey.user.preferences['email_settings__enable_TSL']),
                    fail_silently=False)
        except:
            print('email address not valid')
        return HttpResponseRedirect("/thankyou/")

    polls = Poll.objects.filter(survey=survey, first_level=True)
    context = {'survey': survey,
               'polls': polls}
    return render(request, 'polls/index.html', context)


def thankyou(request):
    return render(request, 'polls/thankyou.html')


def send_newsletter_view(request):
    pass


def build_fixture(request):
    for choice in CharChoice.objects.filter(created_by_visitor=False):
        if not choice.group:
            choice.group = ChoiceGroup.objects.create(name=choice.choice_text)
    for poll in Poll.objects.all():
        if not poll.group:
            poll.group = PollGroup.objects.create(name=poll.question)
    return HttpResponseRedirect("/thankyou/")
