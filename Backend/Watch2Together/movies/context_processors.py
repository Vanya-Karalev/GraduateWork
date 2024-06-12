from movies.models import Film


def films_processor(request):
    films = Film.objects.all()
    return {'films': films}
