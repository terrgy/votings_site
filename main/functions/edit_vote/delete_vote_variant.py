from django.contrib import messages

from main.forms import DeleteVoteVariantForm
from main.functions.delete_variant import delete_all_vote_facts_related_to_variant
from main.models import VoteVariant


def process_delete_vote_variant_form(request, voting_obj):
    form = DeleteVoteVariantForm(data=request.POST)
    if not form.is_valid():
        return form
    if voting_obj.type == 1:
        messages.add_message(request, messages.ERROR, 'Нельзя удалять вариант голосования для дискретного голосования')
        return form
    variant_id = form.cleaned_data['vote_variant_delete_id']
    try:
        vote_variant = VoteVariant.objects.get(pk=variant_id, voting=voting_obj)
    except VoteVariant.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Такого варианта голосования не существует')
        return form
    delete_all_vote_facts_related_to_variant(vote_variant)
    vote_variant.delete()
    return None


def collect_delete_vote_variant_form(variant):
    data = {
        'vote_variant_delete_id': variant.pk
    }
    return DeleteVoteVariantForm(data=data)
