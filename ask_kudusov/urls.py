"""ask_kudusov URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from ask import views

urlpatterns = [
    # url(r'^/?', foo),
    url(r'^ask/', views.ask, name='ask'),
    url(r'^login', views.login, name='login'),
    url(r'^signup', views.signup, name='signup'),
    url(r'^$', views.index, name='index'),
    url(r'^hot/', views.hot, name='hot'),
    url(r'^tag/python/', views.tag_python, name='tag_python'),
    url(r'^tag/(?P<tag_name>[A-Za-z0-9+-]+)/', views.tag_python, name='tag_python'),
    url(r'^question/(?P<question_id>\d+)/', views.single_question, name='single_question'),
    # url(r'ask/', include('ask.urls')),

    url(r'^admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
