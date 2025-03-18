from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from .models import UsuarioJogos, Regional, UsuarioRegional
from django.contrib import messages
from .forms import UsuarioJogosForm, RegionalForm, UsuarioRegionalForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import  DeleteView
from django.utils.decorators import method_decorator
from .utils import PERFIL_CHOICES, TIPO_REGIONAL_CHOICES
import re


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name="dispatch")
class UsuarioJogosListView(ListView):
    model = UsuarioJogos
    paginate_by = 10
    template_name = "usuario/list.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return UsuarioJogos.objects.filter(nome__icontains=query).order_by('nome')
        else:
            return UsuarioJogos.objects.all().order_by('nome')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['create_url'] = reverse('create_usuario')
        return context
    

@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name="dispatch")
class UsuarioJogosDetailView(TemplateView):
    template_name = "usuario/usuario.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = get_object_or_404(UsuarioJogos, id=self.kwargs['id'])
        context['usuario'] = usuario
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name="dispatch")
class UsuarioJogosFormView(View):
    form_class = UsuarioJogosForm
    template_name = "usuario/form.html"

    def get(self, request, id=None):
        if id:
            usuario = get_object_or_404(UsuarioJogos, id=id)
            form = self.form_class(instance=usuario)
            titulo = 'Editar Usuário'
        else:
            form = self.form_class()
            titulo = 'Cadastro de Usuário'

        return render(request, self.template_name, {"form": form, "titulo": titulo})
    
    def post(self, request, id=None):
        data = request.POST.copy()
        cpf = re.sub(r'\D', '', request.POST.get('cpf'))
        telefone = re.sub(r'\D', '', request.POST.get('telefone'))

        data["cpf"] = cpf
        data["telefone"] = telefone

        if id:
            usuario = get_object_or_404(UsuarioJogos, id=id)
            form = self.form_class(data, instance=usuario)
            msg = 'Usuário atualizado com sucesso'
        else:
            form = self.form_class(data)
            msg = 'Usuário cadastrado com sucesso'

        if form.is_valid():
            form.save()
            messages.success(request, msg)
            return redirect('/')
        else:
            messages.error(request, form.errors)

        return render(request, self.template_name, {"form": form})
    
    
@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name="dispatch")
class UsuarioJogosDeleteView(DeleteView):
    model = UsuarioJogos
    pk_url_kwarg = "id"

    def get_success_url(self):
        messages.success(self.request, "Usuário deletado com sucesso")
        return reverse_lazy('list_usuarios')


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name="dispatch")
class RegionalListView(ListView):
    model = Regional
    paginate_by = 10
    template_name = "regional/list.html"  

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Regional.objects.filter(nome__icontains=query).order_by('nome')
        else:
            return Regional.objects.all().order_by('nome')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context

@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name="dispatch")
class RegionalDetailView(TemplateView):
    template_name = "regional/regional.html" 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        regional = get_object_or_404(Regional, id=self.kwargs['id'])
        context['regional'] = regional
        return context

@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name="dispatch")
class RegionalFormView(View):
    form_class = RegionalForm
    template_name = "regional/form.html"  

    def get(self, request, id=None):
        if id:
            regional = get_object_or_404(Regional, id=id)
            form = self.form_class(instance=regional)
        else:
            form = self.form_class()

        return render(request, self.template_name, {"form": form})

    def post(self, request, id=None):
        if id:
            regional = get_object_or_404(Regional, id=id)
            form = self.form_class(request.POST, instance=regional)
            msg = 'Regional atualizada com sucesso!'
        else:
            form = self.form_class(request.POST)
            msg = 'Regional criada com sucesso!'

        if form.is_valid():
            form.save()
            messages.success(request, msg)
            return redirect('list_regional')
        else:
            messages.error(request, form.errors)

        return render(request, self.template_name, {"form": form})

@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name="dispatch")
class RegionalDeleteView(DeleteView):
    model = Regional
    pk_url_kwarg = "id"
    def get_success_url(self):
        messages.success(self.request, "Regional deletada com sucesso")
        return reverse_lazy('list_regional')


#Crud Usuario Regional

@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name="dispatch")
class UsuarioRegionalListView(ListView):
    model = UsuarioRegional
    paginate_by = 10
    template_name = "usuario_regional/list.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return UsuarioRegional.objects.filter(usuario__icontains=query).order_by('usuario')
        else:
            return UsuarioRegional.objects.all().order_by('usuario')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['regional'] = get_object_or_404(Regional, id=self.kwargs['id'])
        return context    
    

@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name="dispatch")
class UsuarioRegionalDetailView(TemplateView):
    template_name = "usuario_regional/regional.html" 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario_regional = get_object_or_404(UsuarioRegional, id=self.kwargs['id'])
        context['usuario_regional'] = usuario_regional
        return context

@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name="dispatch")
class UsuarioRegionalFormView(TemplateView):
    form_class = UsuarioRegionalForm
    template_name = "usuario_regional/form.html"

    def get(self, request, id, usuario_regional_id=None):
        regional = get_object_or_404(Regional, id=id)
        if usuario_regional_id:
            usuario_regional = get_object_or_404(UsuarioRegional, id=usuario_regional_id, regional=regional)
            form = self.form_class(instance=usuario_regional)
        else:
            form = self.form_class()
        return render(request, self.template_name, {"form": form, "regional": regional})

    def post(self, request, id=None):
        if id:
            usuario_regional = get_object_or_404(UsuarioRegional, id=id)
            form = self.form_class(request.POST, instance=usuario_regional)
            msg = 'Usuário Regional atualizado com sucesso!'
        else:
            form = self.form_class(request.POST)
            msg = 'Usuário Regional criado com sucesso!'
        
        if form.is_valid():
            form.save()
            messages.success(request, msg)
            return redirect('list_usuario_regional', id=request.POST.get('regional_id')) 
        else:
            messages.error(request, form.errors)

        return render(request, self.template_name, {"form": form})
        
@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name="dispatch")
class UsuarioRegionalDeleteView(DeleteView):
    model = UsuarioRegional
    pk_url_kwarg = "id"
    def get_success_url(self):
        messages.success(self.request, "Usuario Regional deletado com sucesso")
        return reverse_lazy('list_usuario_regional')

