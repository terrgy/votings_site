from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from main.forms import AddForm, ComplaintsForm
from main.forms import RedactForm
from main.functions.edit_vote import collect_main_settings_form, collect_vote_variant_forms, \
    collect_add_vote_variant_form
from main.functions.edit_vote.utils import check_voting
from main.functions.edit_vote.vote_image import collect_image_upload_form
from main.functions.show_votes.votings_table import collect_votings_table, build_votings_table
from main.functions.submit_vote.time_utils import collect_full_time_block
from main.functions.submit_vote.variant_information import collect_variants_block
from main.models import VoteVariant, Folovers, MyFolovers
from main.models import Voting, User, VoteFact, Complaint


def index_page(request):
    context = {
        'vlad': User.objects.get(pk=3),
        'tin': User.objects.get(pk=4),
        'kirigaya': User.objects.get(pk=5),
        'ld': User.objects.get(pk=6),
        'sankea': User.objects.get(pk=7),
        'polomnik': User.objects.get(pk=8),
        'pers': User.objects.get(pk=9)
    }
    return render(request, 'pages/index.html', context)


def votings_list_page(request):
    voting_list = Voting.objects.filter(finished__gte=timezone.now(), is_active=1)
    context = collect_votings_table(request.user, voting_list)
    return render(request, 'pages/votings.html', context)


def voting_page(request, voting_id):
    voting_obj = get_object_or_404(Voting, pk=voting_id)

    context = {
        'voting': voting_obj,
        'is_favourite': False
    }

    context.update(collect_variants_block(request.user, voting_obj))

    if not context['is_ended']:
        context.update(collect_full_time_block(voting_obj.finished - timezone.now()))

    if request.user.is_authenticated:
        context['is_favourite'] = voting_obj.is_favourite(request.user)

    return render(request, 'pages/voting.html', context)


def e_handler403(request, exception):
    context = {'error_message': exception}
    return render(request, 'errors/error403.html', context, status=403)


@login_required
def edit_voting_page(request, voting_id):
    voting_obj = check_voting(request, voting_id)

    # add data to context
    context = {
        'voting': voting_obj,
        'main_settings_form': collect_main_settings_form(voting_obj),
        'vote_variant_forms': collect_vote_variant_forms(voting_obj),
        'image_upload_form': collect_image_upload_form()
    }
    if voting_obj.type != 1:
        context['add_vote_variant_form'] = collect_add_vote_variant_form()
    return render(request, 'pages/edit_voting.html', context)


@login_required()
def favorites_page(request, profile_id):
    user_now = get_object_or_404(User, pk=profile_id)
    voting_list = Voting.objects.filter(favouritevoting__author=user_now)
    context = collect_votings_table(user_now, voting_list, 'edit')
    return render(request, 'pages/favorites.html', context)


@login_required()
def history_page(request):
    vote_facts = request.user.votefact_set.all().order_by('created').reverse()
    favourite_votings = request.user.favouritevoting_set.all().order_by('created').reverse()
    events = []
    pointer1, pointer2 = [0] * 2
    while (pointer1 < len(vote_facts)) and (pointer2 < len(favourite_votings)):
        if vote_facts[pointer1].created > favourite_votings[pointer2].created:
            events.append({
                'type': 'vote',
                'voting': Voting.objects.filter(votevariant__votefactvariant__fact=vote_facts[pointer1]).distinct()[0],
                'time': vote_facts[pointer1].created
            })
            pointer1 += 1
        else:
            events.append({
                'type': 'favourite',
                'voting': favourite_votings[pointer2].voting,
                'time': favourite_votings[pointer2].created
            })
            pointer2 += 1
    while pointer1 < len(vote_facts):
        events.append({
            'type': 'vote',
            'voting': Voting.objects.filter(votevariant__votefactvariant__fact=vote_facts[pointer1]).distinct()[0],
            'time': vote_facts[pointer1].created
        })
        pointer1 += 1
    while pointer2 < len(favourite_votings):
        events.append({
            'type': 'favourite',
            'voting': favourite_votings[pointer2].voting,
            'time': favourite_votings[pointer2].created
        })
        pointer2 += 1
    context = {
        'events': events
    }
    return render(request, 'pages/history.html', context)


@login_required()
def my_votings_page(request, profile_id):
    user_now = get_object_or_404(User, pk=profile_id)
    voting_list = Voting.objects.filter(author=user_now)
    context = collect_votings_table(user_now, voting_list, 'edit')
    return render(request, 'pages/my_votings.html', context)


@login_required()
def add(request):
    context = {
        'add_voting_form': None
    }
    if request.method == "POST":
        form = AddForm(request.POST)
        if form.is_valid():
            voting_obj = form.save()
            if voting_obj.type == 1:
                # add Yes and No variants
                VoteVariant.objects.create(voting=voting_obj, description='Да')
                VoteVariant.objects.create(voting=voting_obj, description='Нет')
            return redirect('edit', voting_id=voting_obj.pk)
        else:
            context['add_voting_form'] = form
    else:
        context['add_voting_form'] = AddForm(initial={'author': request.user.id})
    return render(request, 'pages/add.html', context)


@login_required()
def AddComplaints(request, id):
    context = {
        'Complaints_voting_form': None
    }
    if request.method == "POST":
        form = ComplaintsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('votings')
        else:
            context['Complaints_voting_form'] = form
    else:
        context['Complaints_voting_form'] = ComplaintsForm(initial={
            'author': request.user.id,
            'status': 'Не просмотрено',
            'voting': id,
        },)
    return render(request, 'pages/AddComplaints.html', context)


@login_required()
def complaint(request):
    context = {
        'complaint': Complaint.objects.filter(author=request.user)
    }
    return render(request, 'pages/My_complaint.html', context)


def user_profile(request, profile_id):
    user_now = get_object_or_404(User, pk=profile_id)

    my_votings = Voting.objects.filter(author=user_now)[:5]
    favourite_votings = Voting.objects.filter(favouritevoting__author=user_now)[:5]
    context = {
        'user_folovers': Folovers.objects.filter(to_user=user_now).count(),
        'user_folovers_table': Folovers.objects.filter(to_user=user_now)[:3],
        'folover': Folovers.objects.filter(folover=request.user.id, to_user=user_now).count,
        'user_facts': VoteFact.objects.filter(author=user_now).count(),
        'user_complaints': Complaint.objects.filter(author=user_now).count(),
        'user_variants_tr': VoteFact.objects.filter(
            votefactvariant__variant__voting__author=user_now).distinct().count(),
        'user_created': Voting.objects.filter(author=user_now).count(),
        'user': user_now,
        'my_votings_count': my_votings.count(),
        'favourite_votings_count': favourite_votings.count(),
        'my_votings_table': build_votings_table(request, my_votings, 'edit'),
        'favourite_votings_table': build_votings_table(request, favourite_votings, 'edit'),
        'username': user_now,
    }
    if request.method == 'POST':
        if request.POST.get('save') == 'True':
            form1 = Folovers()
            form1.folover = request.user.id
            form1.to_user = user_now
            form1.save()
            form2 = MyFolovers()
            form2.folover = request.user
            form2.to_user = user_now.id
            form2.save()
            return redirect('/profile/' + str(user_now.id))
        else:
            form1 = Folovers.objects.filter(folover=request.user.id, to_user=user_now)
            form1.delete()
            form2 = MyFolovers.objects.filter(folover=request.user, to_user=user_now.id)
            form2.delete()
            return redirect('/profile/' + str(user_now.id))
    return render(request, 'pages/profile.html', context)


@login_required()
def redact_profile(request, profile_id):
    user_now = get_object_or_404(User, pk=profile_id)
    user_n = User.objects.get(pk=profile_id)
    form = RedactForm()
    context = {
        'user_now': user_now,
        'form': None,
    }
    if request.method == "POST":
        form = RedactForm(request.POST)
        print(form.is_valid())
        username = request.POST.get('username', None)
        if not username is None:
            user_n.username = username
        else:
            user_n.username = user_now.username
        user_n.first_name = request.POST.get('first_name')
        user_n.last_name = request.POST.get('last_name')
        user_n.status = request.POST.get('status')

        user_n.save()
        return redirect('/profile/' + str(request.user.id))
    else:
        context['form'] = RedactForm(initial={
            'username': user_now.username,
            'first_name': user_now.first_name,
            'last_name': user_now.last_name,
            'status': user_now.status
        }, )
    context['image_upload_form'] = collect_image_upload_form()
    return render(request, 'pages/Redact_User_Profile.html', context)


@login_required()
def folover(request):
    context = {
        'folover': Folovers.objects.filter(folover=request.user.id)
    }
    if request.method == 'POST':
        user_now = get_object_or_404(User, pk=request.POST.get('user'))
        form1 = Folovers.objects.filter(folover=request.user.id, to_user=user_now)
        form1.delete()
        form2 = MyFolovers.objects.filter(folover=request.user, to_user=user_now.id)
        form2.delete()
    return render(request, 'pages/folover.html', context)


@login_required()
def folovers(request):
    context = {
        'folover': MyFolovers.objects.filter(to_user=request.user.id)
    }
    if request.POST == 'POST':
        if request.POST.get('save') == 'True':
            user_now = get_object_or_404(User, pk=request.POST.get('user'))
            form1 = Folovers()
            form1.folover = request.user.id
            form1.to_user = user_now
            form1.save()
            form2 = MyFolovers()
            form2.folover = request.user
            form2.to_user = user_now.id
            form2.save()
        else:
            user_now = get_object_or_404(User, pk=request.POST.get('user'))
            form1 = Folovers.objects.filter(folover=request.user.id, to_user=user_now)
            form1.delete()
            form2 = MyFolovers.objects.filter(folover=request.user, to_user=user_now.id)
            form2.delete()
    return render(request, 'pages/my_folover.html', context)


def ListUsers(request):
    context = {
        'user': User.objects.filter(is_active=True)
    }
    if request.POST == 'POST':
        if request.POST.get('save') == 'True':
            user_now = get_object_or_404(User, pk=request.POST.get('user'))
            form1 = Folovers()
            form1.folover = request.user.id
            form1.to_user = user_now
            form1.save()
            form2 = MyFolovers()
            form2.folover = request.user
            form2.to_user = user_now.id
            form2.save()
        else:
            user_now = get_object_or_404(User, pk=request.POST.get('user'))
            form1 = Folovers.objects.filter(folover=request.user.id, to_user=user_now)
            form1.delete()
            form2 = MyFolovers.objects.filter(folover=request.user, to_user=user_now.id)
            form2.delete()
    return render(request, 'pages/users.html', context)

def search_page(request):
    context = {}
    if request.method == 'POST':
        search = request.POST.get('search', None)
        if not search is None:
            obj_name = Voting.objects.filter(name__contains=search)
            obj_description = Voting.objects.filter(description__contains=search)
            context['votings'] = []
            for voting in obj_name:
                context['votings'].append(voting)
            for voting in obj_description:
                context['votings'].append(voting)
            print(context['votings'])
    return render(request, 'pages/search.html', context)
