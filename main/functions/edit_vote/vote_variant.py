from main.functions.edit_vote.delete_vote_variant import collect_delete_vote_variant_form
from main.functions.edit_vote.save_vote_variant import collect_save_vote_variant_form
from main.models import VoteVariant


def collect_vote_variant_forms(voting_obj):
    voting_variants = VoteVariant.objects.filter(voting=voting_obj)
    collected_forms = []
    for variant in voting_variants:
        forms_dict = {
            'save': collect_save_vote_variant_form(variant),
            'delete': collect_delete_vote_variant_form(variant),
            'info': variant
        }
        collected_forms.append(forms_dict)
    return collected_forms
