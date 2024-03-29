from django.core.paginator import Paginator


def paginate(request, posts, NUMBER_OF_POSTS):
    paginator = Paginator(posts, NUMBER_OF_POSTS)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
