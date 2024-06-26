from django.shortcuts import render,redirect
from django.conf import settings
from .models import History
import requests
from django.contrib import messages


API_URL="https://api-inference.huggingface.co/models/slauw87/bart_summarisation"
HEADERS={"Authorization": f"BEARER {settings.HUGGINGFACE_API_TOKEN}"}


def summarize_text(prompt):
    try:
        payload={"inputs":prompt}
        response=requests.post(API_URL, headers=HEADERS, json=payload)
        summary = response.json()
        if isinstance(summary,list) and len(summary)>0:
            return summary[0].get('summary_text','No summary available')
        else:
            return 'Invalid response from API'
    except requests.exceptions.RequestException as e:
        return f'API request Failed:{e}'
    except KeyError:
        return 'Unexpected response from API'


def home(request):
    if request.method=='POST':
        prompt=request.POST.get('prompt')
        response=summarize_text(prompt)
        if "API request Failed" in response:
            messages.error(request,response)
        else:
            History.objects.create(prompt=prompt,response=response)
            return redirect('history')

    return render(request,'home.html')


def history(request):
    summaries=History.objects.all()
    return render(request, 'history.html',{'summaries':summaries})