from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django.core.cache import cache

from .models import *

from random import randint
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView

from django.db.models import Q


@login_required
def home(request):
    user = request.user
    #cache.set("keykey", "cached string", nx=False)

    if Profile.objects.filter(user=user):
        return render(request, 'core/home.html')
    else:
        return render(request, 'registration/additional_info.html')


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

        return render(request, 'core/home.html')


@csrf_exempt
def get_ranking(request):
    html = ""
    wod = WOD.objects.get(name='metcon')
    metcon_ranking_list = Record.objects.filter(WOD_type=wod).filter(is_newest=True).order_by('metcon_rec')
    for rank in metcon_ranking_list:
        html += "<p>" + rank.profile.nickname + "</p>"
    return HttpResponse(html)


@login_required
def mypage(request):
    return render(request, 'core/mypage.html')


@login_required
def change_info(request):

    if request.method == 'GET':
        ex_nickname = Profile.objects.get(user=request.user).nickname
        return render(request, 'registration/change_info.html', {'ex_nickname': ex_nickname})

    elif request.method == 'POST':
        form = request.POST
        if Profile.objects.filter(~Q(user=request.user)).filter(nickname=form['nickname']):
            return HttpResponseForbidden('nickname already exists')

        profile = Profile.objects.get(user=request.user)
        profile.nickname = form['nickname']
        profile.age = form['age']
        profile.weight = form['weight']
        profile.gender = True if form['gender'] == "1" else False,
        profile.gym = Gym.objects.get(name=form['gym'])
        profile.save()

        return render(request, 'core/mypage.html')


@login_required
def input(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        form = request.POST

        if form.get('met_minutes', False):
            wod = WOD.objects.get(name='metcon')
            all_seconds = int(form['met_minutes']) * 60 + int(form['met_seconds'])
            rec = Record.objects.filter(profile=profile).filter(WOD_type=wod).filter(is_newest=True)
            if rec:
                ex_rec = rec[0]
                ex_rec.is_newest = False
                ex_rec.save()
            new_rec = Record.objects.create(
                profile=profile,
                WOD_type=WOD.objects.get(name='metcon'),
                metcon_rec=all_seconds
            )
            new_rec.save()
            return render(request, 'core/home.html')

        elif form.get('gym_reps', False):
            wod = WOD.objects.get(name='gymnastics')
            rec = Record.objects.filter(profile=profile).filter(WOD_type=wod).filter(is_newest=True)
            if rec:
                ex_rec = rec[0]
                ex_rec.is_newest = False
                ex_rec.save()
            new_rec = Record.objects.create(
                profile=profile,
                WOD_type=WOD.objects.get(name='gymnastics'),
                metcon_rec=int(form['gym_reps'])
            )
            new_rec.save()
            return render(request, 'core/home.html')

        elif form.get('weight_kg', False):
            wod = WOD.objects.get(name='weightlifting')
            rec = Record.objects.filter(profile=profile).filter(WOD_type=wod).filter(is_newest=True)
            if rec:
                ex_rec = rec[0]
                ex_rec.is_newest = False
                ex_rec.save()
            new_rec = Record.objects.create(
                profile=profile,
                WOD_type=WOD.objects.get(name='weightlifting'),
                metcon_rec=int(form['weight_kg'])
            )
            new_rec.save()
            return render(request, 'core/home.html')

        else:
            return HttpResponse('input invalid')

    else:
        HttpResponseForbidden('allowed only via POST')