from django.views.generic import ListView,CreateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Recipe
from .forms import RecipeForm

class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        
        if self.request.user.share_group:
            queryset = Recipe.objects.filter(user__share_group=self.request.user.share_group)
        else:
            queryset = Recipe.objects.filter(user=self.request.user)

        if query:
            queryset = queryset.filter(name__icontains=query)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context
    
class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/add_recipe.html'
    success_url = reverse_lazy('recipes:recipe_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)    

class RecipeDeleteView(DeleteView):
    model = Recipe
    template_name = 'recipe_delete.html'  # 使わないけど書く
    success_url = reverse_lazy('recipes:recipe_list')
