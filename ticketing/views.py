from typing import Any
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import VMTemplates
from .models import RequestEntry, Comment

from django.shortcuts import redirect
from . import guacamole

# Create your views here.

def guacamole_render(request) : 
    return render(request, "ticketing/guacamole.html")

def guacamole_submit(request) : 
    if request.method == "POST":

        data = request.POST
        username = data.get("username")
        password = data.get("password")
        guacamole.create_user(username, password)
        return redirect("home")
    return redirect("home")

class IndexView(generic.ListView):
    template_name = "ticketing/tsg_home.html"
    context_object_name = "request_list"

    def get_queryset(self):
        queryset = RequestEntry.objects.select_related("requester", "template").values(
            "status",
            "requester__first_name",
            "requester__last_name",
            "cores",
            "ram",
            "has_internet",
            "id",
            "template__vm_name"
        )
        #.order_by('-requestDate')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context['request_list'])
        return context
class DetailView(generic.DetailView):
    model = RequestEntry
    template_name = "ticketing/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        # Fetch the RequestEntry object
        request_entry = get_object_or_404(RequestEntry, pk=pk)

        # Get the details you need from the request_entry
        request_entry_details = RequestEntry.objects.select_related("requester", "template").values(
            "status",
            "requester__first_name",
            "requester__last_name",
            "cores",
            "ram",
            "storage",
            "has_internet",
            "id",
            "template__vm_name",
            "use_case",
            "date_needed",
            'expiration_date',
            "other_config",
            "vm_count",
            "template__storage"
        ).get(pk=pk)

        if request_entry_details.get('storage') == 0.0:
            request_entry_details['storage'] = request_entry_details.get('template__storage')

        # Fetch the comments related to the request_entry
        comments = Comment.objects.filter(request_entry=request_entry).order_by('-date_time')
        context['request_entry'] = {
            'details': request_entry_details,
            'comments' : comments
        }
        print(context)
        return context

class RequestForm(forms.ModelForm):
    class Meta:
        model = RequestEntry
        fields = ['requester']

class RequestFormView(generic.edit.FormView):
    template_name = "ticketing/new-form.html"
    form_class = RequestForm

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        vmtemplate_list = VMTemplates.objects.all().values_list('id', 'vm_name')
        context['vmtemplate_list'] = list(vmtemplate_list)
        #print(context)
        return context
    
def new_form_submit(request):

    # TODO: authenticate if valid user(logged in & faculty/tsg)
    
    if request.method == "POST":
        # get data
        # requester = get_object_or_404(User, username=request.user)
        requester = 1
        data = request.POST
        template_id = data.get("template_id")
        cores = data.get("cores")
        ram = data.get("ram")
        storage = data.get("storage")
        has_internet = data.get("has_internet") == 'true'
        use_case = data.get("use_case")
        date_needed = data.get ('date_needed')
        expiration_date = data.get('expiration_date')
        other_config = data.get("other_configs")
        vm_count = data.get("vm_count")
        
        vmTemplateID = VMTemplates.objects.get(id = template_id)
        print("-----------------------")
        print(data)

        # TODO: data verification

        # create request object
        #print (vmTemplateID, requester)
        new_request = RequestEntry(
            requester = requester,
            template = vmTemplateID,
            cores = cores,
            ram = ram,
            storage = storage,
            has_internet = has_internet,
            use_case = use_case,
            other_config = other_config,
            vm_count = vm_count,
            date_needed = date_needed,
            expiration_date = expiration_date
            # status = RequestEntry.Status.PENDING,
        )
        new_request.save()

    return HttpResponseRedirect(reverse("ticketing:index"))