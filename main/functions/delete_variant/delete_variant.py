from main.models import VoteFactVariant


def delete_all_vote_facts_related_to_variant(vote_variant):
    for fact_variant in VoteFactVariant.objects.filter(variant=vote_variant):
        if VoteFactVariant.objects.filter(fact=fact_variant.fact).count() == 1:
            fact_variant.fact.delete()
        else:
            fact_variant.delete()


def delete_vote_variant(vote_variant):
    delete_all_vote_facts_related_to_variant(vote_variant)
    vote_variant.delete()
