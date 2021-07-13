import markdown2

from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, name):
    template = util.get_entry(name)
    if template:
        entry = markdown2.markdown(template)
    else:
        entry = "Error: The requested page was not found."

    return render(request, "encyclopedia/entry.html", {
        "entry": entry
    })


def search(request):
    form = Form(request.POST)
    template = util.get_entry(form.cleaned_data["q"])
    if template:
        entry = markdown2.markdown(template)
        url = "encyclopedia/entry.html"
    else:
        url = "encyclopedia/search.html"
        entries = util.list_entries()
        entry = [x for x in entries if x.rfind(name) != -1]

    return render(request, url, {
        "entry": entry
    })
