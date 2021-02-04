from django.contrib import messages

from main.forms import SaveVoteVariantForm
from main.functions.delete_variant import delete_all_vote_facts_related_to_variant
from main.models import VoteVariant


def process_save_vote_variant_form(request, voting_obj):
    form = SaveVoteVariantForm(data=request.POST)
    if not form.is_valid():
        return form
    variant_id = form.cleaned_data['vote_variant_save_id']
    try:
        vote_variant = VoteVariant.objects.get(pk=variant_id, voting=voting_obj)
    except VoteVariant.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Такого варианта голосования не существует')
        return form
    if vote_variant.description != form.cleaned_data['vote_variant_new_description']:
        delete_all_vote_facts_related_to_variant(vote_variant)
        vote_variant.description = form.cleaned_data['vote_variant_new_description']
        vote_variant.save()
    return None


def collect_save_vote_variant_form(variant):
    data = {
        'vote_variant_new_description': variant.description,
        'vote_variant_save_id': variant.pk
    }
    return SaveVoteVariantForm(data=data)
