# # context_processors.py
# from django.contrib.auth.models import Group

# def is_admin(user):
#     return user.groups.filter(name='Admin').exists()

# def is_team_lead(user):
#     return user.groups.filter(name='Team_lead').exists()

# def is_team_member(user):
#     return user.groups.filter(name='Team_member').exists()

# def user_roles(request):
#     user = request.user
#     admin_status = is_admin(user)
#     team_lead_status = is_team_lead(user)
#     team_member_status = is_team_member(user)
#     return {
#         'admin_status': admin_status,
#         'team_lead_status': team_lead_status,
#         'team_member_status': team_member_status
#     }
