from django.contrib.messages import get_messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from main.models import Voting, User


def has_errors(form):
    return form.errors and len(form.errors)


def get_first_error(form):
    return str(form.errors[next(iter(form.errors))][0])


def forms_are_equal(form1, form2, id_key):
    return str(form1.data.get(id_key, '+')) == str(form2.data.get(id_key, '-'))


def check_forms_for_errors(context):
    if context.get('main_settings_form') and has_errors(context['main_settings_form']):
        return True
    if context.get('vote_variant_forms'):
        for forms_dict in context['vote_variant_forms']:
            if has_errors(forms_dict['save']) or has_errors(forms_dict['delete']):
                return True
    if context.get('add_vote_variant_form') and has_errors(context['add_vote_variant_form']):
        return True
    return False


def check_methods(request):
    if request.method == 'GET':
        return False
    if request.method != 'POST':
        raise PermissionDenied()
    return True


def check_voting(request, voting_id):
    voting_obj = get_object_or_404(Voting, pk=voting_id)
    if voting_obj.author != request.user:
        raise PermissionDenied('У Вас нет доступа к редактированию этого голосования')
    return voting_obj


def check_user(request, profile_id):
    user_obj = get_object_or_404(User, pk=profile_id)
    if user_obj != request.user:
        raise PermissionDenied('У Вас нет доступа к редактированию этого пользователя')
    return user_obj


def add_is_invalid_class(form):
    if form.errors:
        for error in form.errors:
            try:
                form.fields[error].widget.attrs['class'] = \
                    form.fields[error].widget.attrs['class'] + ' is-invalid'
            except KeyError:
                pass


def get_base_json_context(request, voting_obj):
    return {
        'voting': voting_obj,
        'messages': get_messages(request)
    }
