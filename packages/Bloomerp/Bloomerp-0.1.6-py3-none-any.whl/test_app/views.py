from django.shortcuts import render
from bloomerp.utils.router import BloomerpRouter
from .models import Employee, Customer, BloomerpModel
from bloomerp.views.mixins import HtmxMixin
from django.views import View
from bloomerp.views.core import BloomerpBaseDetailView


router = BloomerpRouter()

# -----------------------------
# LIST VIEW ROUTE EXAMPLE
# -----------------------------
@router.bloomerp_route(
    path='send-emails', # path will become 
    name='Send Emails',
    description='Send email to {model}',
    route_type='list',
    url_name='send_emails', # url name will become employees_send_emails & customers_send_emails
    models=[Employee, Customer] # List of models for which the route will be created
)
class SendEmailsView(HtmxMixin, View):
    template_name = 'email_employees.html'
    model : BloomerpModel = None # Model will be passed through via the router

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        # Send emails business logic
        # ...

        return render(request, self.template_name, context)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # For example: get objects from model
        context['objects'] = self.model.objects.all()
        context['model'] = self.model
        return context


# -----------------------------
# DETAIL VIEW ROUTE EXAMPLE
# -----------------------------
@router.bloomerp_route(
    path='send-emails', 
    name='Send Email',
    description='Send email to object of {model} model',
    route_type='detail',
    url_name='send_email', 
    models=[Employee, Customer]
)
class SendEmailView(BloomerpBaseDetailView):
    template_name = 'send_email.html'
    model : BloomerpModel = None

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        # Send email business logic
        # ...

        return render(request, self.template_name, context)


# -----------------------------
# APP LEVEL ROUTE EXAMPLE
# -----------------------------
@router.bloomerp_route(
    path='custom-dashboard', # path will become /custom-dashboard
    name='Custom Dashboard',
    description='Custom dashboard created for the app',
    route_type='app',
    url_name='custom_dashboard', # url name will become custom_dashboard
)
class CustomDashboardView(HtmxMixin, View):
    template_name = 'custom_dashboard.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meaning_of_life'] = 42
        return context