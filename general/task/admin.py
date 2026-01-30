from django.contrib import admin
from .models import Team, Task, TaskMember, TeamMember

admin.site.register(Team)
admin.site.register(Task)
admin.site.register(TeamMember)
admin.site.register(TaskMember)