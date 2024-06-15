import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
# specific to this view
from django.views.generic import ListView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView

from .models import Blog,Technology
import datetime
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.views import APIView
from blog.serializers import BlogSerializer
from rest_framework.response import Response
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect


class BlogListView(ListView):
    queryset = Blog.published.all()
    template_name = 'blogs/blog_list.html' 
    ordering = ['-published_at']
    paginate_by = 10
    slug_url_kwarg= 'slug'
    context_object_name = 'blogs'


    def get_queryset(self):
        self.queryset = self.queryset.filter(primary_technology__slug=self.kwargs.get('slug'))
        if 'days' in self.request.GET:
            today = datetime.date.today()
            days = today - datetime.timedelta(days=int(self.request.GET.get('days')))
            self.queryset = self.queryset.filter(published_at__gte=days)
           
        return self.queryset
            

    def get_context_data(self, *args, object_list=None, **kwargs):
        
        today = datetime.date.today()
        context_data= super().get_context_data(object_list=self.queryset,*args,**kwargs)
        slug_data = self.kwargs.get('slug')
        current_year = datetime.datetime.now().year
        blog_count=self.object_list.count()
        context_data['page_title'] = f"{slug_data} Blogs"
        context_data['tech_slug'] = slug_data
        context_data['str'] = slug_data
        context_data['title']= f"{blog_count} Best {slug_data} blogs to Read in {current_year}"
        context_data['today'] =self.object_list.filter(published_at__gte=today)
        if 'days' in self.request.GET: 
            temp = render_to_string("blogs/_partial_list2.html", {"data": object_list})
           
            return JsonResponse({'data': temp })
        return context_data 


class BlogAPIView(APIView):
    queryset = Blog.published.all()
    serializer_class= BlogSerializer
    template_name = 'blogs/blog_list.html'

    def get_queryset(self):
        self.queryset = self.queryset.filter(primary_technology__slug=self.kwargs.get('slug'))
        if 'days' in self.request.GET:
            
            today = datetime.date.today()
            days = today - datetime.timedelta(days=int(self.request.GET.get('days')))
            
            self.queryset = self.queryset.filter(published_at__gte=days)
           
        return self.queryset
            

    def get(self, request, object_list=None, **kwargs):
        object_list= self.get_queryset()
        today = datetime.date.today()
        items = object_list.filter(primary_technology__slug=self.kwargs.get('slug'))
        if 'days' in self.request.GET: 
            temp = render_to_string("blogs/_partial_list2.html", {"data": items})
            return JsonResponse({'data': temp })
        return items 


class TechStackListView(ListView):
    queryset = Technology.objects.all()
    template_name = 'blogs/listing_page.html'
    context_object_name = 'techs'
    paginate_by = 41
    model= Technology
    success_url = reverse_lazy('blog_list')

    def get_context_data(self, *,object_list=None ,**kwargs):
        context_data = super().get_context_data(**kwargs)
     
        return context_data

#   blog search
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        
        keyword = self.request.GET.get('keyword')
        if keyword:
            return queryset.filter(name__icontains = keyword)
        return queryset



@method_decorator(login_required, name='dispatch')
class BlogCreateView(CreateView):
    model = Blog
    template_name = 'blogs/blog_form.html'

    fields = ['title', 'sub_title', 'url', 'primary_technology','related_technology', 'video','image','contents']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


# @method_decorator(login_required, name='dispatch')
class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blogs/blog_detail.html'
    context_object_name = 'blogs'
    fields = ['title', 'contents', 'image', 'video', 'url']


@method_decorator(login_required, name='dispatch')
class BlogUpdateView(UpdateView):
    model = Blog
    slug_url_kwarg = 'slug'
    template_name = 'blogs/blog_update.html'
    context_object_name = 'blogs'
    fields = ['title', 'primary_technology','image', 'video', 'url', 'contents',]
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        blog = self.get_object()
        if self.request.user == blog.author:
            return True
        return False
        

    def get_success_url(self):
        return reverse_lazy('tech_list')
        # return reverse_lazy('blog:blog_list', kwargs={'slug': self.slug})


@method_decorator(login_required, name='dispatch')
class BlogDeleteView(DeleteView):
    model = Blog
    template_name = 'blogs/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:blog_list') 

@login_required
def LikeView(request):
    if request.POST.get('action')=='post':
        result=''
        id = str(request.POST.get('postid'))
        blog = get_object_or_404(Blog , id = id)
    
        if blog.likes.filter(id=request.user.id).exists():
           blog.likes.remove(request.user)
           blog.like_count-=1
           result=blog.like_count
           blog.save()
        else:
           blog.likes.add(request.user)
           blog.like_count+=1
           result=blog.like_count
           blog.save()
    return JsonResponse({'result':result})
    