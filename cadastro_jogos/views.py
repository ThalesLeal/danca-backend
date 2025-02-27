from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import UsuarioJogos
from django.contrib import messages
from .forms import UsuarioJogosForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


@login_required
@never_cache
def create_usuario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        perfil = request.POST.get('perfil')

        # Cria o usuário
        usuario = UsuarioJogos.objects.create(
            nome=nome,  
            cpf=cpf,
            email=email,
            telefone=telefone,
            perfil=perfil
        )

        usuario.save()
        messages.success(request, 'Usuário criado com sucesso!')
        return redirect('usuario_list')
    
    form = UsuarioJogosForm()
    return render(request, 'create_usuario.html', {'form': form})


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
        form = UsuarioJogosForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário atualizado com sucesso!')
            return redirect('usuario_list')
    else:
        form = UsuarioJogosForm(instance=usuario)
    return render(request, 'update_usuario.html', {'form': form})


# Delete a user
@login_required
@never_cache
def delete_usuario(request, id):
    usuario = get_object_or_404(UsuarioJogosForm, id=id)
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
        usuarios = UsuarioJogos.objects.filter(nome__icontains=query)  # Filtra usuários pelo nome
    else:
        usuarios = UsuarioJogos.objects.all()  # Retorna todos os usuários se não houver busca

    return render(request, 'index.html', {'usuarios': usuarios})