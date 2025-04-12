from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from .models import Family
from django.urls import reverse

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
    
    invite_path = reverse("families:join_family", args=[family.invite_code])
    invite_url = request.build_absolute_uri(invite_path)
    return render(request, "families/invite_family.html", {"invite_url": invite_url})


def user_is_authenticated(user):
    return user.is_authenticated


@user_passes_test(user_is_authenticated, login_url='/accounts/login/?next={{ request.path }}')
def join_family(request, invite_code):
    family = get_object_or_404(Family, invite_code=invite_code)
    
    if request.user.family:
        return render(request, "families/join_family_error.html")
    
    if request.method == "POST":
        request.user.family = family
        request.user.save()
        return redirect("accounts:mypage")
    
    return render(request, "families/join_family.html", {"family": family})

def invite_register_redirect(request, invite_code):
    print("✅ invite_register_redirect に入りました！")  # ←これ追加！
    print("👉 invite_code:", invite_code)
    
    request.session['from_family_invite'] = True
    request.session['invite_code'] = str(invite_code)
    
    if request.user.is_authenticated:
        return redirect('families:join_family', invite_code=invite_code)
    else:
        login_url = reverse('accounts:login') + f'?next=/families/join/{invite_code}/'
        return redirect(login_url)

@login_required
def leave_family(request):
    if request.method == "POST":
        request.user.family = None
        request.user.save()
        return redirect("accounts:mypage")

    return render(request, "families/leave_family.html")