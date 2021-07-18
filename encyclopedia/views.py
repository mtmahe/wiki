import markdown2
import os.path

from django.shortcuts import render, redirect
from django import forms
from django.forms import ModelForm, Textarea
from django.contrib import messages
from django.urls import reverse

from . import util



class NewEntryForm(forms.Form):
    help_text = "New entry goes here. Please use github markdown."
    title = forms.CharField(label="New Entry Title")
    entry = forms.CharField(label="", help_text="", widget=forms.Textarea)


class EditEntryForm(forms.Form):
    edit_entry = forms.CharField(label="", widget=forms.Textarea)


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
        "entry": entry,
        "name": name
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
            title = form.cleaned_data["title"]

            # check if title exists
            if util.get_entry(title) == None:
                util.save_entry(title, entry)
                entry = markdown2.markdown(entry)
                return render(request, "encyclopedia/entry.html", {
                    "entry": entry
                })

            else:
                messages.error(request, f'The title {title} already exists')
                
    return render(request, "encyclopedia/create.html", {
        "form": NewEntryForm()
    })


def edit(request, name):
    """ Edit a page. Overwrite old .md file of that name and go to the entry. """
    args = {}

    if request.method == "POST":
        form = EditEntryForm(request.POST)

        if form.is_valid():
            messages.debug(request, 'Form is valid.')
            entry = form.cleaned_data["edit_entry"]
            util.save_entry(name, entry)
            messages.success(request, 'Entry saved successfully.')
            entry = markdown2.markdown(entry)

            return redirect(reverse('entry', args=[name]))

        else:
            messages.error(request, 'Form invalid.')

    template = util.get_entry(name)

    if template:
        entry = template
    else:
        entry = ""
    return render(request, "encyclopedia/edit.html", {
        "name": name,
        "entry": entry,
        "form": EditEntryForm(initial={'edit_entry':entry})
    })


def error(request, error):
    """ display an error message """

    return render(request, "encyclopedia/error.html", {
        "error": error
    })
