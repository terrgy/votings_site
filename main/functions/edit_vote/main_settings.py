from django.utils import timezone

from main.forms import VotingMainSettingsForm
from main.functions.delete_variant import delete_vote_variant
from main.models import VoteVariant


def process_main_settings_form(request, voting_obj):
    form = VotingMainSettingsForm(data=request.POST)
    if not form.is_valid():
        return form
    new_voting_type = int(form.cleaned_data['voting_type'])
    voting_obj.name = form.cleaned_data['voting_title']
    voting_obj.description = form.cleaned_data['voting_description']
    voting_obj.finished = form.cleaned_data['voting_finish_time']
    voting_obj.is_active = form.cleaned_data['voting_is_active']
    # process voting type changing
    if (voting_obj.type != 1) and (new_voting_type == 1):
        # delete all variants
        for variant in VoteVariant.objects.filter(voting=voting_obj):
            delete_vote_variant(variant)
        # add Yes and No variants
        VoteVariant.objects.create(voting=voting_obj, description='Да')
        VoteVariant.objects.create(voting=voting_obj, description='Нет')
    voting_obj.type = new_voting_type
    voting_obj.save()
    return None


def collect_main_settings_form(voting_obj):
    data = {
        'voting_title': voting_obj.name,
        'voting_description': voting_obj.description,
        'voting_type': VotingMainSettingsForm.TYPE_CHOICES[int(voting_obj.type) - 1],
        'voting_finish_time': timezone.localtime(voting_obj.finished),
        'voting_is_active': voting_obj.is_active,
        'request': 'get'
    }
    return VotingMainSettingsForm(data=data)
