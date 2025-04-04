from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from .models import Family


User = get_user_model()


@login_required
def create_family(request):
    if request.method == "POST":
        family_name = request.POST.get("family.family_name")
        
        if not family_name:
            return JsonResponse({"success": False, "errors": "家族名が未入力です。"})
        
        family = Family.objects.create(family_name=family_name)
        family.members.add(request.user)
        request.user.family = family
        request.user.save()
        
    
        return JsonResponse({"success": True})
        
    return JsonResponse({"success": False, "errors": "Invalid request method"})


@login_required
def invite_family(request):
    family = request.user.family
    if not family:
        return redirect("accounts:mypage")
    
    invite_url = family.get_invite_url()
    return render(request, "families/invite_family.html", {"invite_url": invite_url})


def user_is_authenticated(user):
    return user.is_authenticated


@user_passes_test(user_is_authenticated, login_url='/accounts/accounts/login/?next={{ request.path }}')
def join_family(request, invite_code):
    family = get_object_or_404(Family, invite_code=invite_code)
    
    if request.user.family:
        return render(request, "families/join_family_error.html")
    
    if request.method == "POST":
        request.user.family = family
        request.user.save()
        return redirect("accounts:mypage")
    
    return render(request, "families/join_family.html", {"family": family})


@login_required
def leave_family(request):
    if request.method == "POST":
        request.user.family = None
        request.user.save()
        return redirect("accounts:mypage")
    
    return redirect("accounts:mypage")


@login_required
def confirm_leave_family(request):
    if request.method == "POST":
        request.user.family = None
        request.user.save()
        return redirect("accounts:mypage")

    return render(request, "families/confirm_leave_family.html")