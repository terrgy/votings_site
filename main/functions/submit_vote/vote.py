from django.contrib import messages
from django.utils import timezone

from main.forms import MultiVariantVoteForm, SingleVariantVoteForm
from main.functions.edit_vote.utils import has_errors, get_first_error
from main.models import VoteFactVariant, VoteFact, VoteVariant


def process_vote_form(request, voting_obj):
    if voting_obj.finished < timezone.now():
        messages.add_message(request, messages.ERROR, 'Голосование окончено')
        return False
    vote_variants = voting_obj.votevariant_set.all()
    choices_arr = [(variant.pk, variant.description) for variant in vote_variants]
    if voting_obj.type in [1, 2]:
        if request.POST.getlist('vote_variants') and (len(request.POST.getlist('vote_variants')) > 1):
            messages.add_message(request, messages.ERROR, 'В данном голосовании можно выбрать только один вариант')
            return False
        vote_variant_form = SingleVariantVoteForm(data=request.POST, choices=choices_arr)
    else:
        vote_variant_form = MultiVariantVoteForm(data=request.POST, choices=choices_arr)
    if not vote_variant_form.is_valid():
        error_text = None
        if has_errors(vote_variant_form):
            messages.add_message(request, messages.ERROR, get_first_error(vote_variant_form))
        return False
    if voting_obj.is_voted(request.user):
        messages.add_message(request, messages.WARNING, 'Вы уже проголосовали')
        return False
    if voting_obj.type in [1, 2]:
        chosen_variants = [vote_variant_form.cleaned_data['vote_variants']]
    else:
        chosen_variants = vote_variant_form.cleaned_data['vote_variants']
    vote_fact = VoteFact.objects.create(author=request.user)
    for variant in chosen_variants:
        VoteFactVariant.objects.create(fact=vote_fact, variant=VoteVariant.objects.get(pk=variant))
    return True
