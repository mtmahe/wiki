import markdown2

from django.shortcuts import render
from django import forms

from . import util



class NewEntryForm(forms.Form):
    title = forms.CharField(label="New Entry Title")
    entry = forms.CharField(widget=forms.Textarea)


def index(request):
    """ Show a list of links to entries and a search bar. """

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, name):
    """ Render a page for the specific wiki entry. Give error if not found. """

    template = util.get_entry(name)
    if template:
        entry = markdown2.markdown(template)
    else:
        entry = "Error: The requested page was not found."

    return render(request, "encyclopedia/entry.html", {
        "entry": entry
    })


def search(request):
    """When search bar used, link to exact match entry page. If no exact match,
    provide list of entries that contain search parameter."""

    # Get value of GET variable with name "q", if doesn't exist return ""
    query = request.GET.get("q", "")

    # Check if search field empty
    if query == "":
        return render(request, "encyclopedia/search.html", {
            "query": query,
            "matches": ""
        })

    # Check if exact match
    entry = util.get_entry(query)
    if entry != None:
        entry = markdown2.markdown(entry)
        return render(request, "encyclopedia/entry.html", {
            "entry": entry
        })

    # Provide partial matches
    else:
        entries = util.list_entries()
        matches = [x for x in entries if x.rfind(query) != -1]
        return render(request, "encyclopedia/search.html", {
            "matches": matches,
            "query": query
        })


def create(request):
    """ Create a new entry. If entry name already exists give error message
    else, save the new entry as an .md file. """

    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            entry = form.cleaned_data["entry"]
            return render(request, "encyclopedia/create.html", {
                "form": NewEntryForm
            })

    else:
        return render(request, "encyclopedia/create.html", {
            "form": NewEntryForm()
        })
