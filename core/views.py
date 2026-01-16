from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
import csv
import json
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Sum, F, Q
from django.utils import timezone
from datetime import date, timedelta
from .models import InventoryTracker, Product, Sale
from .forms import RegisterForm, TrackerForm, ProductForm, SaleForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tracker_list')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('tracker_list')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def tracker_list(request):
    trackers = InventoryTracker.objects.filter(user=request.user)
    return render(request, 'core/trackers.html', {'trackers': trackers, 'limit': 5})

@login_required
def tracker_create(request):
    trackers_count = InventoryTracker.objects.filter(user=request.user).count()
    if trackers_count >= 5:
        messages.error(request, 'Tracker limit reached (max 5).')
        return redirect('tracker_list')
    if request.method == 'POST':
        form = TrackerForm(request.POST)
        if form.is_valid():
            t = form.save(commit=False)
            t.user = request.user
            t.save()
            return redirect('inventory', tracker_id=t.id)
    else:
        form = TrackerForm()
    return render(request, 'core/tracker_create.html', {'form': form})

def _get_tracker(request, tracker_id):
    return get_object_or_404(InventoryTracker, id=tracker_id, user=request.user)

#@login_required
#def inventory(request, tracker_id):
    #tracker = _get_tracker(request, tracker_id)
    #products = tracker.products.all()
    #search = request.GET.get("search", "")
    #products = Product.objects.all()
    #products = Product.objects.all()
    #paginator = Paginator(products, 50)  # 50 items per page
    #page_number = request.GET.get("page")
    #page_obj = paginator.get_page(page_number)
    #sort = request.GET.get("sort", "name")

    #if sort == "name":
        #products = products.order_by("name")
    #elif sort == "quantity":
        #products = products.order_by("-quantity")
    #elif sort == "price":
        #products = products.order_by("-price")
      
    
    #if search:
        #products = products.filter(
            #Q(name__icontains=search) |
            #Q(category__icontains=search) |
            #Q(barcode__icontains=search)
        #)

    #return render(request, 'core/inventory.html', {'tracker': tracker, 'products': products, "search": search, "page_obj": page_obj})

@login_required
def inventory(request, tracker_id):
    tracker = _get_tracker(request, tracker_id)

    products_qs = tracker.products.all()

    search = request.GET.get("search", "").strip()
    sort = request.GET.get("sort", "name")

    if search:
        products_qs = products_qs.filter(
            Q(name__icontains=search) |
            Q(category__icontains=search) |
            Q(barcode__icontains=search)
        )

    if sort == "name":
        products_qs = products_qs.order_by("name")
    elif sort == "quantity":
        products_qs = products_qs.order_by("-units_added")
    elif sort == "price":
        products_qs = products_qs.order_by("-price")
    else:
        products_qs = products_qs.order_by("name")

    paginator = Paginator(products_qs, 50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "tracker": tracker,
        "page_obj": page_obj,
        "search": search,
        "sort": sort,
        "base_currency": "KES",
    }
    return render(request, 'core/inventory.html', context)

@login_required
def add_product(request, tracker_id):
    tracker = _get_tracker(request, tracker_id)
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            p.tracker = tracker
            p.save()
            messages.success(request, 'Product added.')
            return redirect('inventory', tracker_id=tracker.id)
    else:
        form = ProductForm()
    return render(request, 'core/add_product.html', {'form': form, 'tracker': tracker})

#@login_required
#def update_product(request, pk):
    #product = Product.objects.get(id=pk)
    #if request.method == "POST":
        #product.name = request.POST["name"]
        #product.quantity = request.POST["quantity"]
        #product.save()
        #return redirect("inventory")
    #return render(request, "update_product.html", {"product": product})

@login_required
def update_product(request, pk):
    product = get_object_or_404(Product, id=pk)

    if request.method == "POST":
        product.name = request.POST.get("name", product.name)
        product.units_added = request.POST.get("units_added", product.units_added)
        product.price = request.POST.get("price", product.price)
        product.save()
        return redirect("inventory", tracker_id=product.tracker.id)

    return render(request, "core/update_product.html", {"product": product})


@login_required
def sell_product(request, tracker_id):
    tracker = _get_tracker(request, tracker_id)
    if request.method == 'POST':
        form = SaleForm(request.POST, tracker=tracker)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.tracker = tracker
            # Validate stock
            product = sale.product
            remaining = product.units_remaining
            if sale.quantity > remaining:
                messages.error(request, f'Not enough stock. Remaining: {remaining}')
            else:
                sale.save()
                messages.success(request, 'Sale recorded.')
                return redirect('sales_records', tracker_id=tracker.id)
    else:
        form = SaleForm(tracker=tracker)
    return render(request, 'core/sell_product.html', {'form': form, 'tracker': tracker})

#@login_required
#def sales_records(request, tracker_id):
    #tracker = _get_tracker(request, tracker_id)
    #sales = tracker.sales.select_related('product').all().order_by('-sold_date')
    #return render(request, 'core/sales_records.html', {'tracker': tracker, 'sales': sales})

@login_required
def sales_records(request, tracker_id):
    tracker = _get_tracker(request, tracker_id)
    sales_qs = tracker.sales.select_related('product').all()

    search = request.GET.get("search", "").strip()
    sort = request.GET.get("sort", "-sold_date")

    if search:
        sales_qs = sales_qs.filter(
            Q(product__name__icontains=search) |
            Q(product__category__icontains=search) |
            Q(product__barcode__icontains=search)
        )

    if sort == "name":
        sales_qs = sales_qs.order_by("product__name")
    elif sort == "category":
        sales_qs = sales_qs.order_by("product__category")
    elif sort == "date":
        sales_qs = sales_qs.order_by("-sold_date")
    elif sort == "price":
        sales_qs = sales_qs.order_by("-product__price")
    elif sort == "cost":
        sales_qs = sales_qs.order_by("-cost")
    else:
        sales_qs = sales_qs.order_by("-sold_date")

    paginator = Paginator(sales_qs, 50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "tracker": tracker,
        "page_obj": page_obj,
        "search": search,
        "sort": sort,
        "base_currency": "KES",
    }
    return render(request, 'core/sales_records.html', context)


#@login_required
#def dashboard(request, tracker_id):
    #tracker = _get_tracker(request, tracker_id)
    #sales = tracker.sales.select_related('product')

    # Sales per category (quantity)
    #category_data = list(
        #sales.values('product__category').annotate(total_qty=Sum('quantity'))
    #)

    # Sales per day (last 14 days)
    #today = date.today()
    #start = today - timedelta(days=13)
    #daily = []
    #for i in range(14):
        #d = start + timedelta(days=i)
        #qty = sales.filter(sold_date__date=d).aggregate(total=Sum('quantity'))['total'] or 0
        #daily.append({'date': d.strftime('%Y-%m-%d'), 'qty': qty})

    # Sales per week (last 8 weeks)
    #weekly = []
    #start_week = today - timedelta(weeks=7)
    #for w in range(8):
        #week_start = start_week + timedelta(weeks=w)
        #week_end = week_start + timedelta(days=6)
        #qty = sales.filter(sold_date__date__range=(week_start, week_end)).aggregate(total=Sum('quantity'))['total'] or 0
        #weekly.append({'label': f'W{week_start.isocalendar()[1]}', 'qty': qty})

    # Sales per month (current year)
    #monthly = []
    #for m in range(1, 13):
       # qty = sales.filter(sold_date__year=today.year, sold_date__month=m).aggregate(total=Sum('quantity'))['total'] or 0
       # monthly.append({'label': timezone.datetime(today.year, m, 1).strftime('%b'), 'qty': qty})


   # return render(request, 'core/dashboard.html', {
       # 'tracker': tracker,
       # 'category_data': category_data,
        #'daily': daily,
        #'weekly': weekly,
        #'monthly': monthly,
   # })

@login_required
def dashboard(request, tracker_id):
    tracker = _get_tracker(request, tracker_id)
    sales = tracker.sales.select_related('product')

    # Per category: qty + income
    category_data = list(
        sales.values('product__category').annotate(
            total_qty=Sum('quantity'),
            total_income=Sum(F('quantity') * F('product__price'))
        )
    )
    # Convert Decimal to float for JSON serialization
    for item in category_data:
        item['total_income'] = float(item['total_income'])

    today = date.today()
    # Last 14 days qty + income
    daily = []
    start = today - timedelta(days=13)
    for i in range(14):
        d = start + timedelta(days=i)
        day_sales = sales.filter(sold_date__date=d)
        qty = day_sales.aggregate(total=Sum('quantity'))['total'] or 0
        income = day_sales.aggregate(
            total=Sum(F('quantity') * F('product__price'))
        )['total'] or 0
        daily.append({'date': d.strftime('%Y-%m-%d'), 'qty': qty, 'income': float(income)})

    # Last 8 weeks qty + income
    weekly = []
    start_week = today - timedelta(weeks=7)
    for w in range(8):
        week_start = start_week + timedelta(weeks=w)
        week_end = week_start + timedelta(days=6)
        week_sales = sales.filter(sold_date__date__range=(week_start, week_end))
        qty = week_sales.aggregate(total=Sum('quantity'))['total'] or 0
        income = week_sales.aggregate(
            total=Sum(F('quantity') * F('product__price'))
        )['total'] or 0
        weekly.append({
            'label': f'W{week_start.isocalendar()[1]}',
            'qty': qty,
            'income': float(income)
        })

    # Current year, per month qty + income
    monthly = []
    for m in range(1, 13):
        month_sales = sales.filter(sold_date__year=today.year, sold_date__month=m)
        qty = month_sales.aggregate(total=Sum('quantity'))['total'] or 0
        income = month_sales.aggregate(
            total=Sum(F('quantity') * F('product__price'))
        )['total'] or 0
        monthly.append({
            'label': timezone.datetime(today.year, m, 1).strftime('%b'),
            'qty': qty,
            'income': float(income)
        })

    context = {
        'tracker': tracker,
        'category_data': category_data,
        'daily': daily,
        'weekly': weekly,
        'monthly': monthly,
        'base_currency': 'KES',
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def autocomplete_products(request, tracker_id):
    tracker = _get_tracker(request, tracker_id)
    term = request.GET.get("term", "").strip()
    qs = tracker.products.all()
    if term:
        qs = qs.filter(name__icontains=term)
    names = list(qs.values_list("name", flat=True)[:10])
    return JsonResponse(names, safe=False)


@login_required
def export_inventory_csv(request, tracker_id):
    tracker = _get_tracker(request, tracker_id)
    products = tracker.products.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventory.csv"'

    writer = csv.writer(response)
    writer.writerow(['Product Id', 'Name', 'Category', 'Added Date', 'Price', 'Units Added', 'Total Earnings'])
    for p in products:
        writer.writerow([p.product_id, p.name, p.category, p.added_date, p.price, p.units_added, p.total_earnings_if_all_sold])

    return response

@login_required
def export_sales_csv(request, tracker_id):
    tracker = _get_tracker(request, tracker_id)
    sales = tracker.sales.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales.csv"'

    writer = csv.writer(response)
    writer.writerow(['Product Id', 'Name', 'Category', 'Sold Date', 'Price', 'Units Sold', 'Cost'])
    for s in sales:
        writer.writerow([s.product.product_id, s.product.name, s.product.category, s.sold_date, s.product.price, s.quantity, s.cost])

    return response

def about(request):
    return render(request, "about.html")
    
def privacy(request):
    return render(request, "privacy.html")
def terms(request):
    return render(request, "terms.html")
    
def home(request):
        if request.user.is_authenticated:
            return redirect('tracker_list')# send logged-in users to their inventories 
        return render(request, 'core/home.html')#show landing page to guests

def get_product_by_barcode(request, barcode):
    try:
        p = Product.objects.get(barcode=barcode)
        return JsonResponse({
            "found": True,
            "name": p.name,
            "category": p.category,
            "quantity": p.quantity
        })
    except Product.DoesNotExist:
        return JsonResponse({"found": False})

def print_barcode(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, "print_barcode.html", {"product": product})
