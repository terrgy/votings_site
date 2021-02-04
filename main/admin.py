from django.contrib import admin

from .models import Voting, VoteFact, FavouriteVoting, VoteFactVariant, VoteVariant, User, UserSettings, Complaint, \
    Folovers, MyFolovers

admin.site.register(Voting)
admin.site.register(VoteFact)
admin.site.register(FavouriteVoting)
admin.site.register(VoteFactVariant)
admin.site.register(VoteVariant)
admin.site.register(User)
admin.site.register(UserSettings)
admin.site.register(Complaint)
admin.site.register(Folovers)
admin.site.register(MyFolovers)
