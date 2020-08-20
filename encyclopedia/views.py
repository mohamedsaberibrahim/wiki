from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
import random

from . import util
import markdown2

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry", max_length=30)
    content = forms.CharField(label="Content", widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entryPage(request, title):
    for entryName in util.list_entries():
        if title.lower() == entryName.lower():
            entryAsHtml = markdown2.markdown(util.get_entry(title))
            return render(request, "encyclopedia/entry.html", {
            "title": entryName,
            "content": entryAsHtml
    })
    else:
        return render(request, "encyclopedia/error.html", {
                "error": f"No such entry named {title}"
            })

def search(request):
    if request.method == "POST":
        keyword = request.POST["q"]
        matchedEnteries = []

        for entryName in util.list_entries():

            if keyword.lower() in entryName.lower():
                matchedEnteries.append(entryName)

        if len(matchedEnteries) == 1:
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=(matchedEnteries[0],)))
        else:
            return render(request, "encyclopedia/searchresults.html", {
                    "entries": matchedEnteries
                })
        
    return HttpResponseRedirect(reverse("encyclopedia:index"))

def add(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"].capitalize()
            content = form.cleaned_data["content"]

            for entryName in util.list_entries():
                if title.lower() == entryName.lower():
                    form.add_error('title', forms.ValidationError(
                        ('Already there is an entry named: %(value)s'),
                        code='invalid',
                        params={'value': entryName},
                    ))
                    return render(request, "encyclopedia/add.html", {
                        "form": form
                    })
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=(title,)))
        else:
            return render(request, "encyclopedia/add.html", {
                "form": form
            })
    return render(request, "encyclopedia/add.html", { 
        "form": NewEntryForm()
    })

def randomPage(request):
    enteries = util.list_entries()
    entryIndex = random.randint(0, len(enteries) - 1)
    return HttpResponseRedirect(reverse("encyclopedia:entry", args=(enteries[entryIndex],)))

def editPage(request, title):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=(title,)))
    entryAsMarkdown = util.get_entry(title)
    form = NewEntryForm(initial={"title": title, "content": entryAsMarkdown})
    form.fields['title'].widget.attrs['readonly'] = True
    return render(request, "encyclopedia/edit.html", { 
        "form": form,
        "title": title
    })
