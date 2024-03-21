from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2


from . import util

class SearchForm(forms.Form):
    keyword = forms.CharField(label="Search")

def search(request):
    keyword = request.GET.get('keyword', '')
    content = util.get_entry(keyword)
    partial_matches = util.search_entries(keyword)


    if content:
        
        return render (request, "encyclopedia/content.html", {
            "title": keyword,
            "content": markdown2.markdown(content, safe_mode=True)
        })
    else:
        return render (request, "encyclopedia/search.html", {
            "keyword": keyword,
            "entries": partial_matches
        })




def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })


def content(request, title):
    content = util.get_entry(title)
    if content:
        return render (request, "encyclopedia/content.html", {
            "title": title,
            "content": markdown2.markdown(content, safe_mode=True)
            
        })
    else:
        return render (request, "encyclopedia/content.html", {
            "title": title,
            "content": f"Error: '{title}' Not found",
            "hidden": "hidden"
        })

def random(request):
    title = util.random_entry()
    return HttpResponseRedirect(reverse('content', args=[title]))


    
class EditForm(forms.Form):
    filename = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea(attrs={'style': 'height: 300px;'}))

def edit(request, title):
    content = util.get_entry(title)
    form = EditForm(initial={
        'filename': title,
        'content': content
    })

    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            filename = form.cleaned_data["filename"]
            content = form.cleaned_data["content"]
            util.save_entry(filename, content)
            return HttpResponseRedirect(reverse('content', args=[title]))

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": form
    }) 
    
class AddForm(forms.Form):
    filename = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea(attrs={'style': 'height: 300px;'}))
    

def add(request):
    form = AddForm()

    if request.method == "POST":
        form = AddForm(request.POST)
        if form.is_valid():
            filename = form.cleaned_data["filename"]
            content = form.cleaned_data["content"]
            partial_matches = util.search_entries(filename)
            if partial_matches:
                return render(request, "encyclopedia/add.html", {
                    "message": "The entry already exists. Please add new entry.",
                    "form": form
                })  
            else:
                util.save_entry(filename,content)
                return HttpResponseRedirect(reverse('content', args=[filename]))
        else:
            return render(request, "encyclopedia/add.html", {
                "form": form
            })  

    return render(request, "encyclopedia/add.html", {
        "form": form
    })  








