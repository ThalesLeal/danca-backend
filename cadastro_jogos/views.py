from django.shortcuts import render
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Usuario
from django.contrib import messages
from .forms import UsuarioForm
from django.contrib.auth.models import Group as BaseGroup
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.paginator import Paginator
import re
# Create a new user


@login_required
@never_cache
def create_usuario(request):
    # if not request.user.is_authenticated:
    #     messages.error(request, 'Você precisa estar logado para criar um usuário.')
    #     return redirect('usuario_list')

    if request.method == 'POST':
        nome_completo = request.POST.get('nome_completo')
        cpf = request.POST.get('cpf')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        perfil_id = request.POST.get('perfil')

        cpf = re.sub(r'\D', '', cpf)  # Remove caracteres não numéricos do CPF
        # user_instance = request.user._wrapped if hasattr(request.user, '_wrapped') else request.user

        # Cria o usuário
        Usuario.objects.create(
            nome_completo=nome_completo,
            cpf=cpf,
            email=email,
            telefone=telefone,
            perfil=perfil_id
        )
        messages.success(request, 'Usuário criado com sucesso!')
        return redirect('usuario_list')

    form = UsuarioForm()
    titulo = 'Cadastrar Usuário'
    label_button = 'Cadastrar'

    return render(request, 'create_usuario.html', {'form': form, 'titulo': titulo, 'label_button': label_button})

# Read user details
@login_required
@never_cache
def read_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    return render(request, 'read_usuario.html', {'usuario': usuario})

# Update user information
@login_required
@never_cache
def update_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        
        if form.is_valid():
            cpf = re.sub(r'\D', '', request.POST.get('cpf'))  # Remove caracteres não numéricos do CPF
            form.instance.cpf = cpf

            form.save()
            messages.success(request, 'Usuário atualizado com sucesso!')
            return redirect('usuario_list')
        else:
            messages.error(request, form.errors)
    else:
        form = UsuarioForm(instance=usuario)

    titulo = 'Atualizar Usuário'
    label_button = 'Atualizar'

    return render(request, 'create_usuario.html', {'form': form, 'titulo': titulo, 'label_button': label_button})

# Delete a user
@login_required
@never_cache
def delete_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuário deletado com sucesso!')
        return redirect('usuario_list')  # Redirect to user list after deletion
    return render(request, 'delete_usuario.html', {'usuario': usuario})

# List all users
@login_required
@never_cache
def usuario_list(request):
    query = request.GET.get('q')  # Obtém o parâmetro de busca da URL
    if query:
        usuarios = Usuario.objects.filter(nome_completo__icontains=query).order_by('nome_completo')  # Filtra usuários pelo nome
    else:
        usuarios = Usuario.objects.all().order_by('nome_completo')  # Retorna todos os usuários se não houver busca

    # Paginação
    paginator = Paginator(usuarios, 10)  # Mostra 10 usuários por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    total_usuarios = usuarios.count()  # Total de registros

    return render(request, 'index.html', {'page_obj': page_obj, 'total_usuarios': total_usuarios})