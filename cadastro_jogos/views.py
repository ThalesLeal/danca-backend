from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from .models import Instituicao, UsuarioJogos, Regional, UsuarioRegional
from django.contrib import messages
from .forms import InstituicaoForm, UsuarioJogosForm, RegionalForm, UsuarioRegionalForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import DeleteView
from django.utils.decorators import method_decorator
import re
from django.db.models.functions import Lower


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name="dispatch")
class UsuarioJogosListView(ListView):
    model = UsuarioJogos
    paginate_by = 10
    template_name = "usuario/list.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return UsuarioJogos.objects.filter(nome__icontains=query).order_by(Lower('nome'))
        return UsuarioJogos.objects.all().order_by(Lower('nome'))

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
        usuario = get_object_or_404(UsuarioJogos, id=self.kwargs['usuario_id'])
        context['usuario'] = usuario
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name="dispatch")
class UsuarioJogosFormView(View):
    form_class = UsuarioJogosForm
    template_name = "usuario/form.html"

    def get(self, request, usuario_id=None):
        form = self.form_class()
        titulo = 'Cadastrar Usuário'

        if usuario_id:
            usuario = get_object_or_404(UsuarioJogos, id=usuario_id)
            form = self.form_class(instance=usuario)
            titulo = 'Editar Usuário'
        return render(request, self.template_name, {"form": form, "titulo": titulo})

    def post(self, request, usuario_id=None):
        data = request.POST.copy()
        cpf = re.sub(r'\D', '', request.POST.get('cpf'))
        telefone = re.sub(r'\D', '', request.POST.get('telefone'))

        data["cpf"] = cpf
        data["telefone"] = telefone

        form = self.form_class(data)
        msg = 'Usuário criado com sucesso'

        if usuario_id:
            usuario = get_object_or_404(UsuarioJogos, id=usuario_id)
            form = self.form_class(data, instance=usuario)
            msg = 'Usuário modificado com sucesso'

        if form.is_valid():
            form.save()
            messages.success(request, msg)
            return redirect('/')
        return render(request, self.template_name, {"form": form})


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name="dispatch")
class UsuarioJogosDeleteView(DeleteView):
    model = UsuarioJogos
    pk_url_kwarg = "usuario_id"

    def get_success_url(self):
        messages.success(self.request, "Usuário removido com sucesso")
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
            return Regional.objects.filter(nome__icontains=query).order_by(Lower('nome'))
        return Regional.objects.all().order_by(Lower('nome'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['create_url'] = reverse('create_regional')
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name="dispatch")
class RegionalDetailView(TemplateView):
    template_name = "regional/regional.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        regional = get_object_or_404(Regional, id=self.kwargs['regional_id'])
        context['regional'] = regional
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name="dispatch")
class RegionalFormView(View):
    form_class = RegionalForm
    template_name = "regional/form.html"

    def get(self, request, regional_id=None):
        form = self.form_class()
        if regional_id:
            regional = get_object_or_404(Regional, id=regional_id)
            form = self.form_class(instance=regional)
        return render(request, self.template_name, {"form": form})

    def post(self, request, regional_id=None):
        form = self.form_class(request.POST)
        msg = 'Regional criada com sucesso'

        if regional_id:
            regional = get_object_or_404(Regional, id=regional_id)
            form = self.form_class(request.POST, instance=regional)
            msg = 'Regional modificada com sucesso'
    
        if form.is_valid():
            form.save()
            messages.success(request, msg)
            return redirect('list_regionais')
        return render(request, self.template_name, {"form": form})


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name="dispatch")
class RegionalDeleteView(DeleteView):
    model = Regional
    pk_url_kwarg = "regional_id"

    def get_success_url(self):
        messages.success(self.request, "Regional removida com sucesso")
        return reverse_lazy('list_regionais')


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name="dispatch")
class UsuarioRegionalListView(ListView):
    model = UsuarioRegional
    paginate_by = 10
    template_name = "usuario_regional/list.html"

    def get_queryset(self):
        regional_id = self.kwargs.get('regional_id')
        query = self.request.GET.get('q')

        queryset = UsuarioRegional.objects.filter(regional_id=regional_id)

        if query:
            queryset = queryset.filter(usuario__nome__icontains=query)
        return queryset.order_by(Lower('usuario__nome'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        regional = get_object_or_404(Regional, id=self.kwargs['regional_id'])
        
        context['q'] = self.request.GET.get('q', '')
        context['regional'] = get_object_or_404(Regional, id=self.kwargs['regional_id'])
        context['regional_nome'] = regional.nome
        context['regional_numero'] = regional.numero
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name="dispatch")
class UsuarioRegionalDetailView(TemplateView):
    template_name = "usuario_regional/usuario_regional.html"

    def get_object(self):
        regional_id = self.kwargs.get('regional_id')
        usuario_regional_id = self.kwargs.get('usuario_regional_id')
        return get_object_or_404(UsuarioRegional, id=usuario_regional_id, regional_id=regional_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario_regional'] = self.get_object()
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name="dispatch")
class UsuarioRegionalFormView(View):
    form_class = UsuarioRegionalForm
    template_name = "usuario_regional/form.html"

    def get(self, request, regional_id, usuario_regional_id=None):
        regional = get_object_or_404(Regional, id=regional_id)
        form = self.form_class(regional=regional)

        if usuario_regional_id:
            usuario_regional = get_object_or_404(
                UsuarioRegional, id=usuario_regional_id, regional=regional
            )
            form = self.form_class(instance=usuario_regional)
        return render(request, self.template_name, {"form": form, "regional": regional})

    def post(self, request, regional_id, usuario_regional_id=None):
        regional = get_object_or_404(Regional, id=regional_id)
        form = self.form_class(request.POST)
        msg = 'Usuário Regional criado com sucesso'

        if usuario_regional_id:
            usuario_regional = get_object_or_404(
                UsuarioRegional, id=usuario_regional_id, regional=regional
            )
            form = self.form_class(request.POST, instance=usuario_regional)
            msg = "Usuário Regional modificado com sucesso"

        if form.is_valid():
            form.save()
            messages.success(request, msg)
            return redirect('list_usuario_regional', regional_id=regional.id)
        return render(request, self.template_name, {"form": form, "regional": regional})


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name="dispatch")
class UsuarioRegionalDeleteView(DeleteView):
    model = UsuarioRegional
    pk_url_kwarg = "usuario_regional_id"

    def get_success_url(self):
        messages.success(self.request, "Usuario Regional removido com sucesso")
        regional_id = self.object.regional.id
        return reverse('list_usuario_regional', args=[regional_id])
    

@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name="dispatch")
class InstituicaoListView(ListView):
    model = Instituicao
    paginate_by = 10
    template_name = "instituicao/list.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Instituicao.objects.filter(nome__icontains=query).order_by(Lower('nome'))
        return Instituicao.objects.all().order_by(Lower('nome'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['create_url'] = reverse('create_instituicao')
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name="dispatch")
class InstituicaoDetailView(TemplateView):
    template_name = "instituicao/instituicao.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instituicao = get_object_or_404(Instituicao, id=self.kwargs['instituicao_id'])
        context['instituicao'] = instituicao
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name="dispatch")
class InstituicaoFormView(View):
    form_class = InstituicaoForm
    template_name = "instituicao/form.html"

    def get(self, request, instituicao_id=None):
        form = self.form_class()
        if instituicao_id:
            instituicao = get_object_or_404(Instituicao, id=instituicao_id)
            form = self.form_class(instance=instituicao)
        return render(request, self.template_name, {"form": form})

    def post(self, request, instituicao_id=None):
        form = self.form_class(request.POST)
        msg = 'Instituição criada com sucesso'

        if instituicao_id:
            regional = get_object_or_404(Instituicao, id=instituicao_id)
            form = self.form_class(request.POST, instance=regional)
            msg = 'Instituição modificada com sucesso'
    
        if form.is_valid():
            form.save()
            messages.success(request, msg)
            return redirect('list_instituicoes')
        return render(request, self.template_name, {"form": form})
    

@login_required
@never_cache
def get_regionais(request):
    tipo_regional = request.GET.get('tipo_regional')
    regionais = Regional.objects.filter(tipo_regional=tipo_regional).values('id', 'nome')
    return JsonResponse(list(regionais), safe=False)


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name="dispatch")
class InstituicaoDeleteView(DeleteView):
    model = Instituicao
    pk_url_kwarg = "instituicao_id"

    def get_success_url(self):
        messages.success(self.request, "Instituição removida com sucesso")
        return reverse('list_instituicoes')


