from django.contrib import messages

from main.forms import AddVoteVariantForm
from main.models import VoteVariant


def process_add_vote_variant_form(request, voting_obj):
    add_vote_variant_form = AddVoteVariantForm(data=request.POST)
    if not add_vote_variant_form.is_valid():
        return add_vote_variant_form
    if voting_obj.type == 1:
        messages.add_message(request, messages.ERROR, 'Нельзя создать вариант голосования для дискретного голосования')
        return add_vote_variant_form
    VoteVariant.objects.create(voting=voting_obj,
                               description=add_vote_variant_form.cleaned_data['vote_variant_description'])
    return None


def collect_add_vote_variant_form():
    return AddVoteVariantForm()
