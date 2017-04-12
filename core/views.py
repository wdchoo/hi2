from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django.core.cache import cache

from .models import *

from django.db.models import Q


@login_required
def home(request):
    user = request.user
    #cache.set("keykey", "cached string", nx=False)

    profile = Profile.objects.filter(user=user)
    if profile:
        session = request.session
        if session.get("user" + str(user.id) + "_nickname", False):
            nickname = session["user" + str(user.id) + "_nickname"]
        else:
            session["user" + str(user.id) + "_nickname"] = profile[0].nickname
            nickname = session["user" + str(user.id) + "_nickname"]
        #request.session.set_expiry(15)

        return render(request, 'core/home_metcon.html', {'nickname': nickname})
    else:
        return render(request, 'registration/additional_info.html')


@login_required
def metcon(request):
    user = request.user
    profile = Profile.objects.filter(user=user)
    if profile:
        session = request.session
        if session.get("user" + str(user.id) + "_nickname", False):
            nickname = session["user" + str(user.id) + "_nickname"]
        else:
            session["user" + str(user.id) + "_nickname"] = profile[0].nickname
            nickname = profile[0].nickname 
        #request.session.set_expiry(15)

        wod = WOD.objects.get(name="metcon")
        rec = Record.objects.filter(profile=profile).filter(WOD_type=wod).filter(is_newest=True)
        if rec:
            met_minutes = rec[0].metcon_rec / 60
            met_seconds = rec[0].metcon_rec % 60
            return render(request, 'core/home_metcon.html', {'nickname': nickname, 'met_minutes': met_minutes, 'met_seconds': met_seconds})
        else:
            return render(request, 'core/home_metcon.html', {'nickname': nickname})

    else:
        return render(request, 'registration/additional_info.html')


@login_required
def gymnastics(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    session = request.session
    nickname = session["user" + str(user.id) + "_nickname"]
    wod = WOD.objects.get(name="gymnastics")
    rec = Record.objects.filter(profile=profile).filter(WOD_type=wod).filter(is_newest=True)
    
    if rec:
        gymnastics_reps = rec[0].gymnastics_rec
        return render(request, 'core/home_gymnastics.html', {'nickname': nickname, 'gymnastics_reps': gymnastics_reps})
    else:
        return render(request, 'core/home_gymnastics.html', {'nickname': nickname})


@login_required
def weightlifting(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    session = request.session
    nickname = session["user" + str(user.id) + "_nickname"]
    wod = WOD.objects.get(name="weightlifting")
    rec = Record.objects.filter(profile=profile).filter(WOD_type=wod).filter(is_newest=True)

    if rec:
        weightlifting_kg = rec[0].weightlifting_rec
        return render(request, 'core/home_weightlifting.html', {'nickname': nickname, 'weightlifting_kg': weightlifting_kg})
    else:
        return render(request, 'core/home_weightlifting.html', {'nickname': nickname})

      

    return render(request, 'core/home_weightlifting.html', {'nickname': nickname})


@login_required
def input_additional_info(request):
    user = request.user

    if request.method == "POST":
        form = request.POST
        if Profile.objects.filter(nickname=form['nickname']):
            return HttpResponseForbidden('nickname already exists')

        profile = Profile.objects.create(
            user=user,
            nickname=form['nickname'],
            age=form['age'],
            weight=form['weight'],
            gender=True if form['gender'] == "1" else False,
            gym=Gym.objects.get(name=form['gym'])
        )
        profile.save()

        return render(request, 'core/home_metcon.html')


@csrf_exempt
def get_metcon_ranking(request):
    html = ""
    wod = WOD.objects.get(name='metcon')
    ranking_list = Record.objects.filter(WOD_type=wod).filter(is_newest=True).order_by('metcon_rec')
    for rank in ranking_list:
        html += "<p>" + rank.profile.nickname + "</p>"
    return HttpResponse(html)

@csrf_exempt
def get_gymnastics_ranking(request):
    html = ""
    wod = WOD.objects.get(name='gymnastics')
    ranking_list = Record.objects.filter(WOD_type=wod).filter(is_newest=True).order_by('-gymnastics_rec')
    for rank in ranking_list:
        html += "<p>" + rank.profile.nickname + "</p>"
    return HttpResponse(html)

@csrf_exempt
def get_weightlifting_ranking(request):
    html = ""
    wod = WOD.objects.get(name='weightlifting')
    ranking_list = Record.objects.filter(WOD_type=wod).filter(is_newest=True).order_by('-weightlifting_rec')
    for rank in ranking_list:
        html += "<p>" + rank.profile.nickname + "</p>"
    return HttpResponse(html)


@login_required
def mypage(request):
    user = request.user
    session = request.session
    nickname = session.get("user" + str(user.id) + "_nickname", False)
    return render(request, 'core/mypage.html', {'nickname': nickname})


@login_required
def change_info(request):
    user = request.user
    if request.method == 'GET':
        ex_nickname = Profile.objects.get(user=user).nickname
        return render(request, 'registration/change_info.html', {'ex_nickname': ex_nickname})

    elif request.method == 'POST':
        form = request.POST
        if Profile.objects.filter(~Q(user=user)).filter(nickname=form['nickname']):
            return HttpResponseForbidden('nickname already exists')

        profile = Profile.objects.get(user=user)
        profile.nickname = form['nickname']
        profile.age = form['age']
        profile.weight = form['weight']
        profile.gender = True if form['gender'] == "1" else False,
        profile.gym = Gym.objects.get(name=form['gym'])
        profile.save()

        session = request.session
        session["user" + str(user.id) + "_nickname"] = profile.nickname

        return render(request, 'core/mypage.html', {'nickname': profile.nickname})


@login_required
def input(request):
    if request.method == 'POST':
        user = request.user
        profile = Profile.objects.get(user=user)
        form = request.POST
        session = request.session
        nickname = session["user" + str(user.id) + "_nickname"]

        if form.get('met_minutes', False):
            print('metcon input!')
            wod = WOD.objects.get(name='metcon')
            all_seconds = int(form['met_minutes']) * 60 + int(form['met_seconds'])
            rec = Record.objects.filter(profile=profile).filter(WOD_type=wod).filter(is_newest=True)
            if rec:
                ex_rec = rec[0]
                ex_rec.is_newest = False
                ex_rec.save()
            new_rec = Record.objects.create(
                profile=profile,
                WOD_type=wod,
                metcon_rec=all_seconds
            )
            new_rec.save()
            return render(request, 'core/home_metcon.html', {'nickname': nickname, 'met_minutes': form['met_minutes'], 'met_seconds': form['met_seconds']})

        elif form.get('gymnastics_reps', False):
            print('gymnastics input!')
            wod = WOD.objects.get(name='gymnastics')
            rec = Record.objects.filter(profile=profile).filter(WOD_type=wod).filter(is_newest=True)
            if rec:
                ex_rec = rec[0]
                ex_rec.is_newest = False
                ex_rec.save()
            new_rec = Record.objects.create(
                profile=profile,
                WOD_type=wod,
                gymnastics_rec=int(form['gymnastics_reps'])
            )
            new_rec.save()
            return render(request, 'core/home_gymnastics.html', {'nickname': nickname, 'gymnastics_reps': form['gymnastics_reps']})

        elif form.get('weightlifting_kg', False):
            print('weightlifting input!')
            wod = WOD.objects.get(name='weightlifting')
            rec = Record.objects.filter(profile=profile).filter(WOD_type=wod).filter(is_newest=True)
            if rec:
                ex_rec = rec[0]
                ex_rec.is_newest = False
                ex_rec.save()
            new_rec = Record.objects.create(
                profile=profile,
                WOD_type=wod,
                weightlifting_rec=int(form['weightlifting_kg'])
            )
            new_rec.save()
            return render(request, 'core/home_weightlifting.html', {'nickname': nickname})

        else:
            return HttpResponse('input invalid')

    else:
        HttpResponseForbidden('allowed only via POST')
