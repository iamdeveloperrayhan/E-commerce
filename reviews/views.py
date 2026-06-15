from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from products.models import Product
from accounts.models import CustomerProfile
from reviews.forms import ReviewForm


@login_required
def review_create(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    customer = get_object_or_404(CustomerProfile, user=request.user)
    if Review.objects.filter(customer=customer, product=product).exists():
        messages.error(request, 'You have already reviewed this product.')
        return redirect('product_detail', pk=product.id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.customer = customer
            review.product = product
            review.save()
            messages.success(request, 'Review submitted.')
            return redirect('product_detail', pk=product.id)
    else:
        form = ReviewForm()
    return render(request, 'reviews/review_form.html', {'form': form, 'product': product})


@login_required
def review_update(request, pk):
    customer = get_object_or_404(CustomerProfile, user=request.user)
    review = get_object_or_404(Review, pk=pk, customer=customer)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated.')
            return redirect('product_detail', pk=review.product.id)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'reviews/review_form.html', {'form': form, 'product': review.product})


@login_required
def review_delete(request, pk):
    customer = get_object_or_404(CustomerProfile, user=request.user)
    review = get_object_or_404(Review, pk=pk, customer=customer)
    if request.method == 'POST':
        product_id = review.product.id
        review.delete()
        messages.success(request, 'Review deleted.')
        return redirect('product_detail', pk=product_id)
    return render(request, 'reviews/review_confirm_delete.html', {'review': review})

