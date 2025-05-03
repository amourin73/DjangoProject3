from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from DjangoProject3.accounts.views import home, cart_view, register_view, custom_login_view
from DjangoProject3.trees.views_template import tree_list, create_tree, update_tree, delete_tree, view_cart, \
    add_to_cart, update_cart_quantity, clear_cart, rate_tree

urlpatterns = [
                  path('admin/', admin.site.urls),

                  # API endpoints
                  path('api/accounts/', include('DjangoProject3.accounts.urls')),
                  path('api/carts/', include('DjangoProject3.carts.urls')),
                  path('api/orders/', include('DjangoProject3.orders.urls')),
                  path('api/seasons/', include('DjangoProject3.seasons.urls')),
                  path('api/trees/', include('DjangoProject3.trees.urls')),

                  # Frontend views
                  path('', home, name='home'),
                  path('cart/', cart_view, name='cart'),
                  path('register/', register_view, name='register'),

                  # Auth endpoints - updated login
                  path('login/', custom_login_view, name='login'),
                  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
                  path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

                  # App includes
                  path('seasons/', include('DjangoProject3.seasons.urls')),
                  path('trees/', include([
                      path('', tree_list, name='tree_list'),
                      path('create/', create_tree, name='create_tree'),
                      path('update/<int:t_id>/', update_tree, name='update_tree'),
                      path('delete/<int:t_id>/', delete_tree, name='delete_tree'),
                      path('cart/', include([
                          path('', view_cart, name='view_cart'),
                          path('add/<int:t_id>/', add_to_cart, name='add_to_cart'),
                          path('update/<int:t_id>/<str:action>/', update_cart_quantity, name='update_cart'),
                          path('clear/', clear_cart, name='clear_cart'),
                      ])),
                      path('rate/', rate_tree, name='rate_tree'),
                  ])),
path('plant-guide/', include(('DjangoProject3.seasons.urls', 'seasons'), namespace='seasons')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)