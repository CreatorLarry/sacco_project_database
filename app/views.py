from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from app.app_forms import CustomerForm, DepositForm, LoginForm
from app.models import Customer, Deposit


# Create your views here.
def test(request):
    # save a customer. Commented line sice it has already been saved in database
    # c1 = Customer(first_name='Mary', last_name='Jane', email='mj@gmail.com', dob='2000-11-23', gender='Female',
    #               weight=62)
    # c1.save()
    #
    # c2 = Customer(first_name='John', last_name='Smith', email='johnsmith@gmail.com', dob='1997-06-13', gender='Male',
    #               weight=62)
    # c2.save()

    num_of_customers = Customer.objects.count()

    # fetching customers
    c1 = Customer.objects.get(id=1)  # select * from customers where id=1
    print(c1)

    # fetch deposits
    d1 = Deposit(amount=10000, status=True, customer=c1)
    d1.save()
    num_of_deposits = Deposit.objects.count()

    return HttpResponse(f"Current number of customers: {num_of_customers} & Current deposit: {num_of_deposits}")


@login_required  # decorator
def customers(request):
    data = Customer.objects.all().order_by(
        '-id').values()  # ORM-object relational marker select everything from customers
    # create a paginator
    paginator = Paginator(data, 15)
    page_number = request.GET.get('page', 1)
    try:
        paginated_data = paginator.page(page_number)
    except PageNotAnInteger | EmptyPage:
        paginated_data = paginator.page(1)

    return render(request, 'customers.html', {'data': paginated_data})


# render is to request
@login_required
def remove_customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)  # select everything from customer where id=7
    customer.delete()  # delete from customers where id=7
    messages.warning(request, f'Customer {customer.first_name} successfully deleted!')
    return redirect('customers')


@login_required
def customer_details(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    deposits = customer.deposits.all()
    total = Deposit.objects.filter(customer=customer).filter(status=True).aggregate(Sum('amount'))['amount__sum']
    return render(request, "details.html", {'customer': customer, 'deposits': deposits, 'total': total})


@login_required
def add_customers(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f"Customer {form.cleaned_data['first_name']} successfully added!")
            return redirect('customers')

    else:
        form = CustomerForm()
    return render(request, 'customer_form.html', context={"form": form})


@login_required
def update_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            messages.info(request, f"Customer {form.cleaned_data['first_name']} successfully updated!")
            return redirect('customers')

    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customer_update_form.html', context={"form": form})


@login_required
def search_customer(request):
    search_term = request.GET.get('search')
    data = Customer.objects.filter(
        Q(first_name__icontains=search_term) | Q(last_name__icontains=search_term) | Q(email__icontains=search_term))
    paginator = Paginator(data, 15)
    page_number = request.GET.get('page', 1)
    try:
        paginated_data = paginator.page(page_number)
    except PageNotAnInteger | EmptyPage:
        paginated_data = paginator.page(1)
    return render(request, "search.html", {'data': paginated_data})


@login_required
def deposit(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            depo = Deposit(amount=amount, status=True, customer=customer)
            depo.save()
            messages.success(request, 'Your deposit has been successfully updated')
            return redirect('customers')

    else:
        form = DepositForm()
    return render(request, 'deposit_form.html', {"form": form, "customer": customer})


def login_user(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, "login_form.html", {"form": form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)  # sessions # cookies
                return redirect('customers')
        messages.warning(request, 'Invalid username or password.')
        # return redirect(login_user)
        return render(request, "login_form.html", {"form": form})


@login_required
def logout_user(request):
    logout(request)
    return redirect('login')

# installing crispy forms
# pip install django-crispy-forms
# pip install crispy-bootstrap5
# pip install Pillow
