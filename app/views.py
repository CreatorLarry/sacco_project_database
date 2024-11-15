from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect

from app.models import Customer, Deposit


# Create your views here.
def test(request):
    # save a customer. Commented line sice it has already been saved in data base
    c1 = Customer(first_name='Mary', last_name='Jane', email='mj@gmail.com', dob='2000-11-23', gender='Female',
                  weight=62)
    c1.save()

    c2 = Customer(first_name='John', last_name='Smith', email='johnsmith@gmail.com', dob='1997-06-13', gender='Male',
                  weight=62)
    c2.save()

    num_of_customers = Customer.objects.count()

    # fetching customers
    c1 = Customer.objects.get(id=1)  # select * from customers where id=1
    print(c1)

# fetch deposits
    d1 = Deposit(amount=10000, status=True, customer=c1)
    d1.save()
    num_of_deposits = Deposit.objects.count()

    return HttpResponse(f"Current number of customers: {num_of_customers} & Current deposit: {num_of_deposits}")


def customers(request):
    data = Customer.objects.all().order_by('id').values() # ORM-object relational marker select everything from customers
    # create a paginator
    paginator = Paginator(data, 8)
    page_number = request.GET.get('page', 1)
    try:
        paginated_data = paginator.page(page_number)
    except PageNotAnInteger | EmptyPage:
        paginated_data = paginator.page(1)

    return render(request, 'customers.html', {'data': paginated_data})
# render is to request
def remove_customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id) # select everything from customer where id=7
    customer.delete() # delete from customers where id=7
    return redirect('customers')


def customer_details(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    deposits = Deposit.objects.filter(customer_id=customer_id)
    return render(request, "details.html", {'deposits': deposits, 'customer': customer})