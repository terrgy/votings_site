from django.template.loader import render_to_string
from django.utils import timezone

from main.functions.submit_vote.time_utils import collect_strict_time_block


def collect_votings_table(user, votings_list, additional_field='complain'):
    collected_list = []
    for voting in votings_list:
        voting_dict = {
            'pk': voting.pk,
            'name': voting.name,
            'description': voting.description,
            'author': voting.author,
            'is_ended': voting.finished < timezone.now()
        }
        if user.is_authenticated:
            voting_dict['is_favourite'] = voting.is_favourite(user)
        if not voting_dict['is_ended']:
            voting_dict.update(collect_strict_time_block(voting.finished - timezone.now()))
        collected_list.append(voting_dict)
    return {
        'votings_list': collected_list,
        'additional_field': additional_field
    }


def build_votings_table(request, votings_list, additional_field='complain'):
    context = collect_votings_table(request.user, votings_list, additional_field)
    return render_to_string('blocks/votings_table.html', context, request)
