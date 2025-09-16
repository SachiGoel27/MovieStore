from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MovieRequest
from .forms import MovieRequestForm

@login_required
def requests_page(request):
    # Handle new request submission
    if request.method == "POST":
        form = MovieRequestForm(request.POST)
        if form.is_valid():
            movie_request = form.save(commit=False)
            movie_request.user = request.user
            movie_request.save()
            return redirect("requestsapp:requests_page")
    else:
        form = MovieRequestForm()

    # Fetch user’s requests
    user_requests = MovieRequest.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "requestsapp/requests_page.html", {
        "form": form,
        "user_requests": user_requests
    })


@login_required
def delete_request(request, request_id):
    movie_request = get_object_or_404(MovieRequest, id=request_id, user=request.user)
    movie_request.delete()
    return redirect("requestsapp:requests_page")

