from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Usuario
from django.contrib import messages
from .forms import UsuarioForm
from django.contrib.auth.models import Group as BaseGroup
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
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
        perfil = request.POST.get('perfil')

        user_instance = request.user._wrapped if hasattr(request.user, '_wrapped') else request.user

        # Cria o usuário
        usuario = Usuario.objects.create(
            nome_completo=nome_completo,  
            cpf=cpf,
            email=email,
            telefone=telefone,
            perfil=perfil
        )
        messages.success(request, 'Usuário criado com sucesso!')
        return redirect('usuario_list')
    
    form = UsuarioForm()
    return render(request, 'create_usuario.html', {'form': form})

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
            form.save()
            messages.success(request, 'Usuário atualizado com sucesso!')
            return redirect('usuario_list')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'update_usuario.html', {'form': form})

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
    usuarios = Usuario.objects.all()
    print(usuarios)
    return render(request, 'index.html', {'usuarios': usuarios})