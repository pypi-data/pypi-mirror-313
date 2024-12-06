from django.db import models
from django.forms import ValidationError
from bloomerp.models.core import BloomerpModel, File
from bloomerp.models.fields import BloomerpFileField
from django.utils.translation import gettext as _

# Create your models here.
class Customer(BloomerpModel):
    name = models.CharField(max_length=255, help_text="The name of the customer")
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)

    string_search_fields = ['name']
    allow_string_search = True

    def __str__(self):
        return self.name

class Product(BloomerpModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to="products", blank=True, null=True)
    
    string_search_fields = ['name']
    allow_string_search = True

    def __str__(self):
        return self.name
    
class Order(BloomerpModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    products = models.ManyToManyField(Product)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="draft")
    notes = models.TextField(blank=True, null=True)
    
    string_search_fields = ['customer__name', 'status', 'notes', 'products__name']

    def __str__(self):
        return f"Order {self.id} by {self.customer.name}"

class Function(BloomerpModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    allow_string_search = True
    string_search_fields = ['name']

    def __str__(self):
        return self.name

class Equipment(BloomerpModel):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=255)

class Employee(BloomerpModel):
    first_name = models.CharField(max_length=255, help_text=_("The first name of the employee"))
    last_name = models.CharField(max_length=255, help_text=_("The last name of the employee"))
    email = models.EmailField()
    identification_document = BloomerpFileField( null=True, blank=True, allowed_extensions=['.jpg', '.png', '.jpeg'])
    manager = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, help_text=_("The manager of the employee"), related_name="direct_reports")
    functions = models.ManyToManyField(Function)
    equipment = models.ManyToManyField(Equipment)
    date_of_birth = models.DateField(blank=True, null=True)

    string_search_fields = ['first_name', 'last_name']
    allow_string_search = True

    def __str__(self):
        return self.first_name + " " + self.last_name

    def clean(self):
        errors = {}

        if self.manager == self:
            errors['manager'] = "Cannot be the same as the employee"
        

        if errors:
            raise ValidationError(errors)


class Accommodation(BloomerpModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = BloomerpFileField(allowed_extensions=['.jpg', '.png', '.jpeg'], null=True, blank=True)
    
    string_search_fields = ['name']

    def __str__(self):
        return self.name
    

class EmployeeOnAccommodation(BloomerpModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    
    string_search_fields = ['employee__first_name', 'employee__last_name', 'accommodation__name']

    def __str__(self):
        return f"{self.employee} on {self.accommodation.name}"
