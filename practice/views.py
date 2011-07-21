from django.shortcuts import render
from models import *

def practice(request,phrase_set_id):
    phrase_set = PhraseSet.objects.get(id=int(phrase_set_id))
    phrases = phrase_set.phrases.all()

    # Post-quiz
    num = int(request.GET.get('num',1))
    if num > len(phrases):
        raise Exception('finished')

    last_one = num == len(phrases)

    # Grab relevant phrase
    phrase = phrases[num - 1]

    next_url = '?num=' + str(num + 1)
    return render(request,'practice.html',{
        'phrase_set':phrase_set,
        'last_one':last_one,
        'phrase':phrase,
        'next_url':next_url,
    })

def sets(request):
    phrase_sets = PhraseSet.objects.all()
    return render(request,'sets.html',{
        'phrase_sets':phrase_sets,
    })

def review(request):
    return render(request,'review.html',{})

