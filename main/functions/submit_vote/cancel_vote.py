from django.contrib import messages

from main.models import VoteFact


def process_cancel_vote(request, voting_obj):
    if not voting_obj.is_voted(request.user):
        messages.add_message(request, messages.WARNING, 'Нечего отменять')
        return False
    VoteFact.objects.filter(author=request.user, votefactvariant__variant__voting=voting_obj).first().delete()
    return True
