from django.contrib import messages

from main.models import FavouriteVoting


def process_add_favourite(request, voting) -> bool:
    if voting.is_favourite(request.user):
        messages.add_message(request, messages.WARNING, 'Голосование уже находится в избранном')
        return False
    FavouriteVoting.objects.create(author=request.user, voting=voting)
    return True


def process_delete_favourite(request, voting) -> bool:
    try:
        FavouriteVoting.objects.get(author=request.user, voting=voting).delete()
    except FavouriteVoting.DoesNotExist:
        messages.add_message(request, messages.WARNING, 'Голосование не находится в избранном')
        return False
    return True
