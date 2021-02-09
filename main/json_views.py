from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import get_messages
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.templatetags.static import static

from main.functions.edit_vote import process_main_settings_form, collect_main_settings_form, collect_vote_variant_forms, \
    process_save_vote_variant_form, process_delete_vote_variant_form
from main.functions.edit_vote.add_vote_variant import collect_add_vote_variant_form, process_add_vote_variant_form
from main.functions.edit_vote.utils import check_methods, check_forms_for_errors, check_voting, add_is_invalid_class, \
    get_base_json_context, get_first_error, forms_are_equal, has_errors, check_user
from main.functions.edit_vote.vote_image import collect_image_upload_form, process_image_upload_form
from main.functions.submit_vote import process_add_favourite, process_delete_favourite, process_vote_form
from main.functions.submit_vote.cancel_vote import process_cancel_vote
from main.functions.submit_vote.variant_information import collect_variants_block
from main.models import Voting


@login_required()
def edit_main_settings(request, voting_id):
    if not check_methods(request):
        return redirect('edit', voting_id=voting_id)
    voting_obj = check_voting(request, voting_id)

    context = {}
    # process request
    processed_form = process_main_settings_form(request, voting_obj)
    # collect other forms
    if processed_form:
        add_is_invalid_class(processed_form)
        context['main_settings_form'] = processed_form
    else:
        context['main_settings_form'] = collect_main_settings_form(voting_obj)
    # add related forms
    context['vote_variant_forms'] = collect_vote_variant_forms(voting_obj)
    if voting_obj.type != 1:
        context['add_vote_variant_form'] = collect_add_vote_variant_form()
    context.update(get_base_json_context(request, voting_obj))
    json_dict = {
        'main_settings_form': render_to_string('forms/main_settings.html', context, request),
        'vote_variant_forms': render_to_string('forms/vote_variant.html', context, request),
        'add_vote_variant_form': render_to_string('forms/add_vote_variant.html', context, request)
    }
    if check_forms_for_errors(context):
        json_dict['status'] = 'error'
    else:
        json_dict['status'] = 'ok'
        messages.add_message(request, messages.SUCCESS, 'Успешно сохранено')
    json_dict['messages'] = render_to_string('base/messages.html', context)
    return JsonResponse(json_dict)


@login_required()
def add_vote_variant(request, voting_id):
    if not check_methods(request):
        return redirect('edit', voting_id=voting_id)
    voting_obj = check_voting(request, voting_id)

    context = {}
    # process request
    processed_form = process_add_vote_variant_form(request, voting_obj)
    # collect other forms
    if processed_form:
        if (voting_obj.type == 1) and processed_form.errors:
            messages.add_message(request, messages.ERROR, get_first_error(processed_form))
        else:
            add_is_invalid_class(processed_form)
            context['add_vote_variant_form'] = processed_form
    else:
        if voting_obj.type != 1:
            context['add_vote_variant_form'] = collect_add_vote_variant_form()
    # add related forms
    context['vote_variant_forms'] = collect_vote_variant_forms(voting_obj)
    context.update(get_base_json_context(request, voting_obj))
    json_dict = {
        'vote_variant_forms': render_to_string('forms/vote_variant.html', context, request),
        'add_vote_variant_form': render_to_string('forms/add_vote_variant.html', context, request),
        'messages': render_to_string('base/messages.html', context)
    }
    if check_forms_for_errors(context):
        json_dict['status'] = 'error'
    else:
        json_dict['status'] = 'ok'
    return JsonResponse(json_dict)


@login_required()
def save_vote_variant(request, voting_id):
    if not check_methods(request):
        return redirect('edit', voting_id=voting_id)
    voting_obj = check_voting(request, voting_id)

    context = {}
    # process request
    processed_form = process_save_vote_variant_form(request, voting_obj)
    # collect other forms
    collected_vote_variant_forms = collect_vote_variant_forms(voting_obj)
    if processed_form:
        add_is_invalid_class(processed_form)
        is_found = False
        for i in range(len(collected_vote_variant_forms)):
            if forms_are_equal(collected_vote_variant_forms[i]['save'], processed_form, 'vote_variant_save_id'):
                collected_vote_variant_forms[i]['save'] = processed_form
                is_found = True
                break
        if not is_found and processed_form.errors:
            messages.add_message(request, messages.ERROR, get_first_error(processed_form))
    context['vote_variant_forms'] = collected_vote_variant_forms
    context.update(get_base_json_context(request, voting_obj))
    json_dict = {
        'vote_variant_forms': render_to_string('forms/vote_variant.html', context, request),
        'messages': render_to_string('base/messages.html', context)
    }
    if check_forms_for_errors(context):
        json_dict['status'] = 'error'
    else:
        json_dict['status'] = 'ok'
    return JsonResponse(json_dict)


@login_required()
def delete_vote_variant(request, voting_id):
    if not check_methods(request):
        return redirect('edit', voting_id=voting_id)
    voting_obj = check_voting(request, voting_id)

    context = {}
    # process request
    processed_form = process_delete_vote_variant_form(request, voting_obj)
    # collect other forms
    collected_vote_variant_forms = collect_vote_variant_forms(voting_obj)
    if processed_form:
        add_is_invalid_class(processed_form)
        is_found = False
        for i in range(len(collected_vote_variant_forms)):
            if forms_are_equal(collected_vote_variant_forms[i]['delete'], processed_form, 'vote_variant_delete_id'):
                collected_vote_variant_forms[i]['delete'] = processed_form
                is_found = True
                break
        if not is_found and processed_form.errors:
            messages.add_message(request, messages.ERROR, get_first_error(processed_form))
    context['vote_variant_forms'] = collected_vote_variant_forms
    context.update(get_base_json_context(request, voting_obj))
    json_dict = {
        'vote_variant_forms': render_to_string('forms/vote_variant.html', context, request),
        'messages': render_to_string('base/messages.html', context)
    }
    if check_forms_for_errors(context):
        json_dict['status'] = 'error'
    else:
        json_dict['status'] = 'ok'
    return JsonResponse(json_dict)


@login_required()
def reload_edit_forms(request, voting_id):
    if not check_methods(request):
        return redirect('edit', voting_id=voting_id)
    voting_obj = check_voting(request, voting_id)

    context = {
        'main_settings_form': collect_main_settings_form(voting_obj),
        'vote_variant_forms': collect_vote_variant_forms(voting_obj),
        'add_vote_variant_form': collect_add_vote_variant_form(),
        'image_upload_form': collect_image_upload_form()
    }
    context.update(get_base_json_context(request, voting_obj))
    json_dict = {
        'main_settings_form': render_to_string('forms/main_settings.html', context, request),
        'vote_variant_forms': render_to_string('forms/vote_variant.html', context, request),
        'add_vote_variant_form': render_to_string('forms/add_vote_variant.html', context, request),
        'image_upload_form': render_to_string('forms/image_upload_form.html', context, request),
        'messages': render_to_string('base/messages.html', context),
        'status': 'ok'
    }
    return JsonResponse(json_dict)


@login_required()
def add_favourite(request, voting_id):
    if not check_methods(request):
        return redirect('voting', voting_id=voting_id)
    voting_obj = get_object_or_404(Voting, pk=voting_id)

    is_ok = process_add_favourite(request, voting_obj)
    context = get_base_json_context(request, voting_obj)
    if is_ok:
        json_dict = {
            'status': 'ok',
            'html': render_to_string('blocks/delete_favourite_img.html', context)
        }
    else:
        json_dict = {
            'status': 'error',
            'html': render_to_string('blocks/add_favourite_img.html', context)
        }
    json_dict['messages'] = render_to_string('base/messages.html', context)
    return JsonResponse(json_dict)


@login_required()
def delete_favourite(request, voting_id):
    if not check_methods(request):
        return redirect('voting', voting_id=voting_id)
    voting_obj = get_object_or_404(Voting, pk=voting_id)

    is_ok = process_delete_favourite(request, voting_obj)
    context = get_base_json_context(request, voting_obj)
    if is_ok:
        json_dict = {
            'status': 'ok',
            'html': render_to_string('blocks/add_favourite_img.html', context)
        }
    else:
        json_dict = {
            'status': 'error',
            'html': render_to_string('blocks/delete_favourite_img.html', context)
        }
    json_dict['messages'] = render_to_string('base/messages.html', context)
    return JsonResponse(json_dict)


@login_required()
def cancel_vote(request, voting_id):
    if not check_methods(request):
        return redirect('voting', voting_id=voting_id)
    voting_obj = get_object_or_404(Voting, pk=voting_id)

    is_ok = process_cancel_vote(request, voting_obj)
    context = get_base_json_context(request, voting_obj)
    context.update(collect_variants_block(request.user, voting_obj))
    json_dict = {
        'variants_block-html': render_to_string('blocks/variants_block.html', context, request),
        'messages': render_to_string('base/messages.html', context)
    }
    if is_ok:
        json_dict['status'] = 'ok'
    else:
        json_dict['status'] = 'error'
    return JsonResponse(json_dict)


@login_required()
def vote(request, voting_id):
    if not check_methods(request):
        return redirect('voting', voting_id=voting_id)
    voting_obj = get_object_or_404(Voting, pk=voting_id)

    is_ok = process_vote_form(request, voting_obj)
    context = get_base_json_context(request, voting_obj)
    context.update(collect_variants_block(request.user, voting_obj))
    json_dict = {
        'variants_block-html': render_to_string('blocks/variants_block.html', context, request),
        'messages': render_to_string('base/messages.html', context)
    }
    if is_ok:
        json_dict['status'] = 'ok'
    else:
        json_dict['status'] = 'error'
    return JsonResponse(json_dict)


@login_required()
def vote_upload_image(request, voting_id):
    if not check_methods(request):
        return redirect('edit', voting_id=voting_id)
    voting_obj = check_voting(request, voting_id)

    image_form = process_image_upload_form(request)
    context = get_base_json_context(request, voting_obj)
    if has_errors(image_form):
        context['image_upload_form'] = image_form
        json_dict = {
            'image_upload_form-html': render_to_string('forms/image_upload_form.html', context, request),
            'status': 'error'
        }
    else:
        image_obj = image_form.save()
        if voting_obj.image:
            voting_obj.image.image.delete()
            voting_obj.image.delete()
        voting_obj.image = image_obj
        voting_obj.save()
        context['image_upload_form'] = collect_image_upload_form()
        messages.add_message(request, messages.SUCCESS, 'Изображение успешно загружено')
        json_dict = {
            'new_image_src': voting_obj.image.image.url,
            'image_upload_form-html': render_to_string('forms/image_upload_form.html', context, request),
            'status': 'ok'
        }
    json_dict['messages'] = render_to_string('base/messages.html', context)
    return JsonResponse(json_dict)


@login_required()
def profile_upload_image(request, profile_id):
    if not check_methods(request):
        return redirect('user_profile', profile_id=profile_id)
    user_obj = check_user(request, profile_id)

    image_form = process_image_upload_form(request)
    context = {
        'messages': get_messages(request)
    }
    if has_errors(image_form):
        context['image_upload_form'] = image_form
        json_dict = {
            'image_upload_form-html': render_to_string('forms/image_upload_form.html', context, request),
            'status': 'error'
        }
    else:
        image_obj = image_form.save()
        if user_obj.image:
            user_obj.image.image.delete()
            user_obj.image.delete()
        user_obj.image = image_obj
        user_obj.save()
        context['image_upload_form'] = collect_image_upload_form()
        messages.add_message(request, messages.SUCCESS, 'Изображение успешно загружено')
        json_dict = {
            'image_upload_form-html': render_to_string('forms/image_upload_form.html', context, request),
            'status': 'ok'
        }
    json_dict['messages'] = render_to_string('base/messages.html', context)
    return JsonResponse(json_dict)


@login_required()
def voting_delete_image(request, voting_id):
    if not check_methods(request):
        return redirect('edit', voting_id=voting_id)
    voting_obj = check_voting(request, voting_id)

    context = get_base_json_context(request, voting_obj)
    json_dict = {
        'new_image_src': static('img/non_voting_picture.png')
    }
    if not voting_obj.image:
        messages.add_message(request, messages.WARNING, 'Изображение отсутствует')
        json_dict['status'] = 'error'
    else:
        voting_obj.image.image.delete()
        voting_obj.image.delete()
        messages.add_message(request, messages.SUCCESS, 'Изображение успешно удалено')
        json_dict['status'] = 'ok'
    json_dict['messages'] = render_to_string('base/messages.html', context)
    return JsonResponse(json_dict)
