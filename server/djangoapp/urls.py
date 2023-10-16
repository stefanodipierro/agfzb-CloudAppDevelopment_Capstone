from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view
    path('static/', views.static_page_view, name='static_page'),
    path('about/', views.about_view, name='about'),


    # path for contact us view
    path('contact/', views.contact_view, name='contact'),

    # path for registration
    path('registration/', views.registration_request, name='registration'),

    # path for login
    path('login/', views.user_login, name='login'),


    # path for logout
    path('logout/', views.user_logout, name='logout'),


    # path for dealer reviews view
    path(route='', view=views.get_dealerships, name='index'),

    # path for add a review view
    path('api/dealership', views.all_dealerships),
    path('api/dealership?state=<str:state>', views.dealerships_by_state),
    path('api/review?dealerId=<int:dealer_id>', views.reviews_for_dealership),
    path('api/review', views.post_review),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)