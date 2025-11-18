from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Length

# Create your views here.
def index(request):
    search_term = request.GET.get('search')
    sort_term = request.GET.get('sort')
    btn_action = request.GET.get('btn_action')   # NEW

    movies = Movie.objects.all()

    # --- SEARCH BUTTON LOGIC ---
    if btn_action == "search" and search_term:
        movies = movies.filter(name__icontains=search_term)

    # --- FILTER BUTTON LOGIC ---
    if btn_action == "filter":
        if sort_term == 'reverse_alpha':
            movies = movies.order_by('-name')
        elif sort_term == 'length':
            movies = movies.annotate(name_length=Length('name')).order_by('name_length')
        elif sort_term == 'length_desc':
            movies = movies.annotate(name_length=Length('name')).order_by('-name_length')

    template_data = {
        'title': 'Movies',
        'movies': movies
    }

    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html', {
        'template_data' : template_data
    })
@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html',
            {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id,
        user=request.user)
    review.delete()
    return redirect('movies.show', id=id)