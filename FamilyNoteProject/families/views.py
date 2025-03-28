from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Family
from accounts.models import CustomUser


@login_required
def create_family(request):
    if request.method == "POST":
        family_name = request.POST.get("family_name")
        family = Family.objects.create(name=family_name)
        request.user.family = family
        request.user.save()
        return redirect("mypage")
    return render(request, "families/create_family.html")


@login_required
def invite_family(request):
    if not request.user.family:
        return redirect("create_family")
    return render(request, "families/invite_family.html", {"invite_code": request.user.family.invite_code})


@login_required
def join_family(request, invite_code):
    family = get_object_or_404(Family, invite_code=invite_code)
    request.user.family = family
    request.user.save()
    return redirect("mypage")