from django.shortcuts import render, get_object_or_404, redirect
from .models import UsuarioJogos
from django.contrib import messages
from .forms import UsuarioJogosForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.paginator import Paginator
from django.views import View
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from .utils import PERFIL_CHOICES
import re

@method_decorator(login_required, name='dispatch')
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
        return context


@method_decorator(login_required, name='dispatch')
class UsuarioJogosFormView(View):
    form_class = UsuarioJogosForm()
    template_name = "usuario/form.html"

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {"form": form})
    
    def post(self, request):
        data = request.POST.copy()
        cpf = re.sub(r'\D', '', request.POST.get('cpf'))  # Remove caracteres não numéricos do CPF
        telefone = re.sub(r'\D', '', request.POST.get('telefone'))  # Remove caracteres não numéricos do telefone

        data["cpf"] = cpf
        data["telefone"] = telefone

        form = self.form_class(data)

        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário criado com sucesso')
            return redirect('/')


@login_required
def create_usuario(request):
    if request.method == 'POST':
        data = request.POST.copy()
        cpf = re.sub(r'\D', '', request.POST.get('cpf'))  # Remove caracteres não numéricos do CPF
        telefone = re.sub(r'\D', '', request.POST.get('telefone'))  # Remove caracteres não numéricos do telefone
        data["cpf"] = cpf
        data["telefone"] = telefone
        form = UsuarioJogosForm(data)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('usuario_list')
        else:
            messages.error(request, form.errors)
    else:
        form = UsuarioJogosForm()

    titulo = 'Cadastrar Usuário'
    label_button = 'Cadastrar'
    return render(request, 'create_usuario.html', {'form': form, 'titulo': titulo, 'label_button': label_button})


# Read user details
@login_required
@never_cache
def read_usuario(request, id):
    usuario = get_object_or_404(UsuarioJogos, id=id)
    return render(request, 'read_usuario.html', {'usuario': usuario})


# Update user information
@login_required
@never_cache
def update_usuario(request, id):
    usuario = get_object_or_404(UsuarioJogos, id=id)
    if request.method == 'POST':
        data = request.POST.copy()
        cpf = re.sub(r'\D', '', request.POST.get('cpf'))  # Remove caracteres não numéricos do CPF
        telefone = re.sub(r'\D', '', request.POST.get('telefone'))  # Remove caracteres não numéricos do telefone
        data["cpf"] = cpf
        data["telefone"] = telefone
        form = UsuarioJogosForm(data, instance=usuario)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário atualizado com sucesso!')
            return redirect('usuario_list')
        else:
            messages.error(request, form.errors)
    else:
        form = UsuarioJogosForm(instance=usuario)

    titulo = 'Editar Usuário'
    label_button = 'Atualizar'

    return render(request, 'create_usuario.html', {'form': form, 'titulo': titulo, 'label_button': label_button})


# Delete a user
@login_required
@never_cache
def delete_usuario(request, id):
    usuario = get_object_or_404(UsuarioJogos, id=id)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuário deletado com sucesso!')
        return redirect('usuario_list')  # Redirect to user list after deletion
    return render(request, 'delete_usuario.html', {'usuario': usuario})