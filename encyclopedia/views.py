import random
import markdown2
import re
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util


def index(request):
	return render(request, "encyclopedia/index.html",{
    	"entries": util.list_entries()
    })

def TITLE(request,name):
	if name in util.list_entries():
		return render(request, "encyclopedia/Page1.html",{"name":markdown2.markdown(util.get_entry(name)), "title": name})
		
def search(request,):
	if request.method=="POST":
		query=request.POST.get("q")
		r=re.compile(f"\w*{query}+",re.IGNORECASE)
		matches=list(filter(r.match,util.list_entries()))
		if query.upper() in [entry.upper() for entry in util.list_entries()]:
			query_search = re.compile(query,re.IGNORECASE)
			match_list = list(filter(query_search.match , util.list_entries()))
			extracted_query= match_list[0]
			return HttpResponseRedirect(reverse("TITLE", args=(extracted_query,)))
		elif len(matches)>= 1:			
			return render(request, "encyclopedia/search.html",{"matches":matches,})
		else:
			return render(request,"encyclopedia/error.html")
		
def NewPage(request):
	if request.method == "POST":
		title=request.POST['title']
		content=request.POST['content']
		new_list = []
		for each_entry in util.list_entries():
			new_list.append(each_entry.upper())
		if title.strip().upper() not in new_list and content is not None:
			util.save_entry(title,content)
			return HttpResponseRedirect(reverse("index"))
		else:
			message="Page Already Exists!!!"
			return render (request,"encyclopedia/NewPage.html", {"message":message})
	return render(request, "encyclopedia/NewPage.html")


def EditPage(request,name):
	if request.method=="POST":
		content=request.POST.get("edit")
		if content is not False:
			util.save_entry(name,content)
			return HttpResponseRedirect(reverse("TITLE", args=(name,)))
	return render(request,"encyclopedia/EditPage.html",{"name":name, "content":util.get_entry(name)})
				
		
def Random(request):
	random.shuffle(util.list_entries())
	title=random.choice(util.list_entries())
	return HttpResponseRedirect(reverse("TITLE", args=(title,)))

	