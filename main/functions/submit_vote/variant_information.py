from django.template.loader import render_to_string
from django.utils import timezone

from main.forms import MultiVariantVoteForm
from main.models import VoteFactVariant


def build_variant_progress_bar(variant_votes_count, total_votes_count):
    context = {
        'count': variant_votes_count
    }
    if total_votes_count:
        context['percentage'] = int(variant_votes_count / total_votes_count * 100)
    else:
        context['percentage'] = 0
    if context['percentage'] <= 10:
        context['class'] = 'bg-danger'
    elif context['percentage'] <= 20:
        context['class'] = 'bg-warning'
    elif context['percentage'] <= 60:
        context['class'] = 'bg-primary'
    elif context['percentage'] <= 90:
        context['class'] = 'bg-info'
    else:
        context['class'] = 'bg-success'
    return render_to_string('blocks/variant_progress_bar.html', context)


def collect_variants_information(variants, chosen_variants_ids):
    collected_array = []
    total_votes_count = 0
    for variant in variants:
        current_votes_count = VoteFactVariant.objects.filter(variant=variant).count()
        total_votes_count += current_votes_count
        variant_info = {
            'description': variant.description,
            'is_voted': variant.pk in chosen_variants_ids,
            'count': current_votes_count
        }
        collected_array.append(variant_info)
    for i in range(len(collected_array)):
        collected_array[i]['progress_bar'] = build_variant_progress_bar(collected_array[i]['count'], total_votes_count)
    return collected_array


def collect_not_voted_first_second_type(vote_variants):
    vote_variants_collected = []
    i = 0
    for variant in vote_variants:
        vote_variants_collected.append({
            'id': 'vote_single_button_{}'.format(i),
            'choice_label': variant.description,
            'tag': variant.pk
        })
    return {
        'vote_variants': vote_variants_collected
    }


def collect_not_voted_third_type(vote_variants):
    if not vote_variants:
        return {}
    choices = [(variant.pk, variant.description) for variant in vote_variants]
    return {
        'vote_variant_form': MultiVariantVoteForm(choices=choices)
    }


def collect_variants_block(user, voting_obj):
    context = {
        'is_voted': False,
        'is_ended': voting_obj.finished < timezone.now()
    }
    vote_variants = voting_obj.votevariant_set.all()
    chosen_variants_ids = set()
    if user.is_authenticated:
        chosen_variants_ids.update(voting_obj.get_chosen_variants_ids(user))
        context['is_voted'] = len(chosen_variants_ids) > 0
    if context['is_voted'] or not user.is_authenticated or context['is_ended']:
        context['variants'] = collect_variants_information(vote_variants, chosen_variants_ids)
    else:
        if voting_obj.type in [1, 2]:
            context.update(collect_not_voted_first_second_type(vote_variants))
        else:
            context.update(collect_not_voted_third_type(vote_variants))
    return context
