from django.shortcuts import render, redirect
from .forms import CategoryForm, ProductForm
from .models import Category, Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required(login_url='login')
# @allowed_users(allowed_roles=["student"])
def index(request):
    categories = Category.objects.all()
    products = Product.objects.filter(product_type="BOOKS")[:5]
    context = {
        "categories":categories,
        "products":products
    }

    return render(request,'main/index.html',context)

@login_required(login_url='login')
def category_list_view(request):
    categories = Category.objects.all()

    category_title = request.GET.get('title', None)

    selected_category = Category.objects.filter(title=category_title).first()
    # print(selected_category)

    selected_products = Product.objects.filter(category=selected_category)

    if category_title is not None :
        context = {
            "categories":categories,
            "selected_category":selected_category,
            "selected_products":selected_products
            }
    else:
        context = {
            "categories":categories,
            "selected_category": [],
            "selected_products": []
        }

    return render(request,'main/category_list.html',context)

@login_required(login_url='login')
def category_create_view(request):
    categories = Category.objects.all()
    form = CategoryForm()

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            category = form.cleaned_data['title']
            messages.success(request, category + " Has Been Added ")
            return redirect('main:category_list')
        else:
            messages.error(request,"Failed To Create Category")
        
    context = {
        "categories":categories,
        'form': form
        }

    return render(request,'main/category_new.html',context)

@login_required(login_url='login')
def product_create_view(request):
    categories = Category.objects.all()
    form = ProductForm()
    
    if request.method == "POST":
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            product = form.save()
            product_title = form.cleaned_data['title']
            user = request.user
            product.created_bY = user
            product.updated_bY = user
            product.save()
            messages.success(request, product_title + " Has Been Added ")
            return redirect('main:product_list')
        else:
            messages.error(request,"Failed To Add Product")
        
    context = {
        "categories":categories,
        'form': form}

    return render(request,'main/product_new.html',context)

@login_required(login_url='login')
def product_list_view(request): 
    categories = Category.objects.all()
    type = request.GET.get('type',None)
    if type is None:   
        all_products = Product.objects.all()
    else:
        all_products = Product.objects.filter(product_type__icontains=type)
    
    paginator = Paginator(all_products, 3) # 5 per page
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1) # If None Or None Character
    except EmptyPage: # If Page is more than the available pages 
        products = paginator.page(paginator.num_pages)
    
    context = {
        "categories":categories,
        "products":products
    }


    # if type is None:
    #     context = {
    #         "categories":categories,
    #         "products":products}
    # else:
    #     products = Product.objects.filter(product_type__icontains=type)
    #     context = {
    #         "categories":categories,
    #         "products":products}

    return render(request,'main/product_list.html',context)

@login_required(login_url='login')
def product_detail_view(request,pk): 
    categories = Category.objects.all()   
    product = Product.objects.get(id=pk)
    context = {
        "categories":categories,
        "product":product
    }

    return render(request,'main/product_detail.html',context)

@login_required(login_url='login')
def product_edit_view(request,pk): 
    categories = Category.objects.all()   
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)

    if request.method == "POST":
        form = ProductForm(request.POST,request.FILES,instance=product)
        if form.is_valid():
            product = form.save()
            product_title = form.cleaned_data['title']
            user = request.user
            product.updated_bY = user
            product.save()
            messages.success(request, product_title + " Has Been Edited ")
            return redirect('main:product_list')
        else:
            messages.error(request,"Failed To Edit Product")
    
    context = {
        "categories":categories,
        "product":product,
        "form":form
    }

    return render(request,'main/product_edit.html',context)

@login_required(login_url='login')
def product_delete_view(request,pk): 
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect('main:product_list')

