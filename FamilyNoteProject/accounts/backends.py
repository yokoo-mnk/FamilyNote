# from django.contrib.auth.backends import BaseBackend
# from django.contrib.auth import get_user_model

# class EmailBackend(BaseBackend):
#     def authenticate(self, request, email=None, password=None):
#         try:
#             user = get_user_model().objects.get(email=email)
#             if user.check_password(password):
#                 return user
#         except get_user_model().DoesNotExist:
#             return None