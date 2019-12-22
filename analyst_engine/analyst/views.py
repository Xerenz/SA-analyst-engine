from django.shortcuts import render
from .forms import MalwareForm
from .models import Malware
from .scraper import simple_search

# dummy data to test views

malwares = {
    "Trojan.SH.KERBERDS.A" : 
    {
        "Infection Channel": "Downloaded from the Internet",
        "PLATFORM": "Linux",
        "OVERALL RISK RATING": "LOW",
        "DAMAGE POTENTIAL": "MEDIUM",
        "DISTRIBUTION POTENTIAL": "LOW",
        "REPORTED INFECTION": "LOW",
        "INFORMATION EXPOSURE": "LOW",
        "Threat Type": " Trojan",
        "Destructiveness": " No",
        "Encrypted": " No",
        "In the wild": " Yes"
    },

    "Trojan.JS.KOVCOREG.A" : 
    {
        "Infection Channel": "Dropped by other malware, Downloaded from the Internet",
        "PLATFORM": "Windows",
        "OVERALL RISK RATING": "LOW",
        "DAMAGE POTENTIAL": "MEDIUM",
        "DISTRIBUTION POTENTIAL": "LOW",
        "REPORTED INFECTION": "LOW",
        "INFORMATION EXPOSURE": "LOW",
        "Threat Type": " Trojan",
        "Destructiveness": " No",
        "Encrypted": " Yes",
        "In the wild": " Yes"
    },

    "Rootkit.Linux.SKIDMAP.A" : 
    {
        "File Size": "272,665  bytes",
        "PLATFORM": "Linux",
        "OVERALL RISK RATING": "LOW",
        "DAMAGE POTENTIAL": "HIGH",
        "DISTRIBUTION POTENTIAL": "LOW",
        "REPORTED INFECTION": "LOW",
        "INFORMATION EXPOSURE": "LOW",
        "Threat Type": " Rootkit",
        "Destructiveness": " No",
        "Encrypted": " No",
        "In the wild": " Yes"
    },

    "Coinminer.Win64.MALXMR.TIAOODBZ" : 
    {
        "Infection Channel": "Downloaded from the Internet",
        "PLATFORM": "Windows",
        "OVERALL RISK RATING": "LOW",
        "DAMAGE POTENTIAL": "MEDIUM",
        "DISTRIBUTION POTENTIAL": "LOW",
        "REPORTED INFECTION": "LOW",
        "INFORMATION EXPOSURE": "LOW",
        "Threat Type": " Coinminer",
        "Destructiveness": " No",
        "Encrypted": "",
        "In the wild": " Yes",
        "ALIASES": "HEUR:RiskTool.Win32.Generic (Kaspersky)"
    },

    "Backdoor.Linux.BASHLITE.SMJC2" : 
    {
        "Infection Channel": "Dropped by other malware, Downloaded from the Internet",
        "PLATFORM": "Linux",
        "OVERALL RISK RATING": "LOW",
        "DAMAGE POTENTIAL": "MEDIUM",
        "DISTRIBUTION POTENTIAL": "LOW",
        "REPORTED INFECTION": "LOW",
        "INFORMATION EXPOSURE": "LOW",
        "Threat Type": " Backdoor",
        "Destructiveness": " No",
        "Encrypted": " No",
        "In the wild": " Yes",
        "ALIASES": "HEUR:Backdoor.Linux.Mirai.h (Kaspersky), Backdoor:Linux/DemonBot.YA!MTB (Microsoft)"
    },

    "ELF_SETAG.SM" : 
    {
        "Infection Channel": "Via vulnerability(ies), Downloaded from the Internet, Dropped by other malware",
        "PLATFORM": "Linux",
        "OVERALL RISK RATING": "LOW",
        "DAMAGE POTENTIAL": "LOW",
        "DISTRIBUTION POTENTIAL": "HIGH",
        "REPORTED INFECTION": "LOW",
        "INFORMATION EXPOSURE": "MEDIUM",
        "Threat Type": " Backdoor",
        "Destructiveness": " No",
        "Encrypted": " No",
        "In the wild": " Yes",
        "ALIASES": "Backdoor:Linux/Setag.A(Microsoft)"
    },
}

# Create your views here.
def index(request):
    
    return render(request, 'analyst/index.html')

def search(request):
    print('search called')
    query = request.GET.get("query")
    print(query)
    malware = Malware.objects.filter(name__contains=query)
    if not malware:
        # scrape data
        malware_data = simple_search(query)
        malware = {'name': query, 'data': malware_data}

    print(malware)
    return render(request, 'analyst/malware.html', {"malware" : malware})

def update(request):
    if request.POST:
        print(request.POST)

        form = MalwareForm(request.POST)

        form.save()

    return render(request, 'analyst/index.html')
