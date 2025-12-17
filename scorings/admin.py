from django.contrib import admin
from .models import ScoringCurrent, ScoringTop, ScoringAllTime, LevelCurrent

admin.site.register(ScoringCurrent)
admin.site.register(ScoringTop)
admin.site.register(ScoringAllTime)
admin.site.register(LevelCurrent)
