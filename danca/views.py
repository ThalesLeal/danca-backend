from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, TemplateView, DeleteView

from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.db.models.functions import Lower
from .models import Lote, Categoria, TipoEvento, Evento, Camisa,Planejamento,Artista, Inscricao, InscricaoEvento
from .form import LoteForm,CategoriaForm,TipoEventoForm,EventoForm,CamisaForm,PlanejamentoForm,ArtistaForm, InscricaoForm, InscricaoEventoForm
from django.shortcuts import redirect
from django.db.models import Q


def index(request):
    return render(request, 'index.html')


#@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name="dispatch")
class LoteListView(ListView):
    model = Lote
    paginate_by = 10
    template_name = "lote/list.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Lote.objects.filter(descricao__icontains=query).order_by(Lower('descricao'))
        return Lote.objects.all().order_by(Lower('descricao'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['create_url'] = reverse('create_lote')
        return context

#@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name="dispatch")
class LoteDetailView(TemplateView):
    template_name = "lote/lote.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lote = get_object_or_404(Lote, id=self.kwargs['lote_id'])
        context['lote'] = lote
        return context

#@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name="dispatch")
class LoteFormView(View):
    form_class = LoteForm
    template_name = "lote/form.html"

    def get(self, request, lote_id=None):
        form = self.form_class()
        if lote_id:
            lote = get_object_or_404(Lote, id=lote_id)
            form = self.form_class(instance=lote)
        return render(request, self.template_name, {"form": form})

    def post(self, request, lote_id=None):
        form = self.form_class(request.POST)
        msg = 'Lote criado com sucesso'

        if lote_id:
            lote = get_object_or_404(Lote, id=lote_id)
            form = self.form_class(request.POST, instance=lote)
            msg = 'Lote modificado com sucesso'
    
        if form.is_valid():
            form.save()
            messages.success(request, msg)
            return redirect('list_lotes')

#@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name="dispatch")
class LoteDeleteView(DeleteView):  
    model = Lote
    pk_url_kwarg = "lote_id"    

    def get_success_url(self):
        messages.success(self.request, "Lote removido com sucesso")
        return reverse_lazy('list_lotes')

# CRUD de Categoria

@method_decorator(never_cache, name="dispatch")
class CategoriaListView(ListView):
    model = Categoria
    paginate_by = 10
    template_name = "categoria/list.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Categoria.objects.filter(descricao__icontains=query).order_by(Lower('descricao'))
        return Categoria.objects.all().order_by(Lower('descricao'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['create_url'] = reverse('create_categoria')  
        return context


@method_decorator(never_cache, name="dispatch")
class CategoriaDetailView(TemplateView):
    template_name = "categoria/categoria.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categoria = get_object_or_404(Categoria, id=self.kwargs['categoria_id'])
        context['categoria'] = categoria
        return context

@method_decorator(never_cache, name="dispatch")
class CategoriaFormView(View):
    form_class = CategoriaForm
    template_name = "categoria/form.html"

    def get(self, request, categoria_id=None):
        form = self.form_class()
        if categoria_id:
            categoria = get_object_or_404(Categoria, id=categoria_id)
            form = self.form_class(instance=categoria)
        return render(request, self.template_name, {"form": form})

    def post(self, request, categoria_id=None):
        form = self.form_class(request.POST)
        msg = 'Categoria criada com sucesso'

        if categoria_id:
            categoria = get_object_or_404(Categoria, id=categoria_id)
            form = self.form_class(request.POST, instance=categoria)
            msg = 'Categoria modificado com sucesso'
    
        if form.is_valid():
            form.save()
            messages.success(request, msg)
            return redirect('list_categorias')

#@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name="dispatch")
class CategoriaDeleteView(DeleteView):  
    model = Categoria
    pk_url_kwarg = "categoria_id"    

    def get_success_url(self):
        messages.success(self.request, "Categoria removida com sucesso")
        return reverse_lazy('list_categorias')


@method_decorator(never_cache, name="dispatch")
class TipoEventoListView(ListView):
    model = TipoEvento
    paginate_by = 10
    template_name = "tipo_evento/list.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return TipoEvento.objects.filter(descricao__icontains=query).order_by(Lower('descricao'))
        return TipoEvento.objects.all().order_by(Lower('descricao'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['create_url'] = reverse('create_tipo_evento')  
        return context


@method_decorator(never_cache, name="dispatch")
class TipoEventoDetailView(TemplateView):
    template_name = "tipo_evento/tipo_evento.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tipo_evento = get_object_or_404(TipoEvento, id=self.kwargs['tipo_evento_id'])
        context['tipo_evento'] = tipo_evento
        return context


@method_decorator(never_cache, name="dispatch")
class TipoEventoFormView(View):
    form_class = TipoEventoForm
    template_name = "tipo_evento/form.html"

    def get(self, request, tipo_evento_id=None):
        form = self.form_class()
        if tipo_evento_id:
            tipo_evento = get_object_or_404(TipoEvento, id=tipo_evento_id)
            form = self.form_class(instance=tipo_evento)
        return render(request, self.template_name, {"form": form})

    def post(self, request, tipo_evento_id=None):
        form = self.form_class(request.POST)
        msg = 'Tipo de Evento criado com sucesso'

        if tipo_evento_id:
            tipo_evento = get_object_or_404(TipoEvento, id=tipo_evento_id)
            form = self.form_class(request.POST, instance=tipo_evento)
            msg = 'Tipo de Evento modificado com sucesso'
    
        if form.is_valid():
            form.save()
            messages.success(request, msg)
            return redirect('list_tipo_eventos')


@method_decorator(never_cache, name="dispatch")
class TipoEventoDeleteView(DeleteView):  
    model = TipoEvento
    pk_url_kwarg = "tipo_evento_id"    

    def get_success_url(self):
        messages.success(self.request, "Tipo de Evento removido com sucesso")
        return reverse_lazy('list_tipo_eventos')


# CRUD de Evento

@method_decorator(never_cache, name="dispatch")
class EventoListView(ListView):
    model = Evento
    paginate_by = 10
    template_name = "evento/list.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Evento.objects.filter(descricao__icontains=query).order_by(Lower('descricao'))
        return Evento.objects.all().order_by(Lower('descricao'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['create_url'] = reverse('create_evento')  
        return context


@method_decorator(never_cache, name="dispatch")
class EventoDetailView(TemplateView):
    template_name = "evento/evento.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        evento = get_object_or_404(Evento, id=self.kwargs['evento_id'])
        context['evento'] = evento
        return context


@method_decorator(never_cache, name="dispatch")
class EventoFormView(View):
    form_class = EventoForm
    template_name = "evento/form.html"

    def get(self, request, evento_id=None):
        form = self.form_class()
        if evento_id:
            evento = get_object_or_404(Evento, id=evento_id)
            form = self.form_class(instance=evento)
        return render(request, self.template_name, {"form": form})

    def post(self, request, evento_id=None):
        form = self.form_class(request.POST)
        msg = 'Evento criado com sucesso'

        if evento_id:
            evento = get_object_or_404(Evento, id=evento_id)
            form = self.form_class(request.POST, instance=evento)
            msg = 'Evento modificado com sucesso'
    
        if form.is_valid():
            form.save()
            messages.success(request, msg)
            return redirect('list_eventos')


@method_decorator(never_cache, name="dispatch")
class EventoDeleteView(DeleteView):  
    model = Evento
    pk_url_kwarg = "evento_id"    

    def get_success_url(self):
        messages.success(self.request, "Evento removido com sucesso")
        return reverse_lazy('list_eventos')


# CRUD de Camisa

@method_decorator(never_cache, name="dispatch")
class CamisaListView(ListView):
    model = Camisa
    paginate_by = 10
    template_name = "camisa/list.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Camisa.objects.filter(descricao__icontains=query).order_by('tipo')
        return Camisa.objects.all().order_by('tipo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['create_url'] = reverse('create_camisa')
        return context


@method_decorator(never_cache, name="dispatch")
class CamisaDetailView(TemplateView):
    template_name = "camisa/camisa.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        camisa = get_object_or_404(Camisa, id=self.kwargs['camisa_id'])
        context['camisa'] = camisa
        return context


@method_decorator(never_cache, name="dispatch")
class CamisaFormView(View):
    form_class = CamisaForm
    template_name = "camisa/form.html"

    def get(self, request, camisa_id=None):
        form = self.form_class()
        if camisa_id:
            camisa = get_object_or_404(Camisa, id=camisa_id)
            form = self.form_class(instance=camisa)
        return render(request, self.template_name, {"form": form})

    def post(self, request, camisa_id=None):
        form = self.form_class(request.POST)
        msg = 'Camisa criada com sucesso'

        if camisa_id:
            camisa = get_object_or_404(Camisa, id=camisa_id)
            form = self.form_class(request.POST, instance=camisa)
            msg = 'Camisa modificada com sucesso'
    
        if form.is_valid():
            form.save()
            messages.success(request, msg)
            return redirect('list_camisas')


@method_decorator(never_cache, name="dispatch")
class CamisaDeleteView(DeleteView):  
    model = Camisa
    pk_url_kwarg = "camisa_id"    

    def get_success_url(self):
        messages.success(self.request, "Camisa removida com sucesso")
        return reverse_lazy('list_camisas')


@method_decorator(never_cache, name="dispatch")
class PlanejamentoListView(ListView):
    model = Planejamento
    paginate_by = 10
    template_name = "planejamento/list.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Planejamento.objects.filter(descricao__icontains=query).order_by(Lower('descricao'))
        return Planejamento.objects.all().order_by(Lower('descricao'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['create_url'] = reverse('create_planejamento')
        return context


@method_decorator(never_cache, name="dispatch")
class PlanejamentoDetailView(TemplateView):
    template_name = "planejamento/planejamento.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        planejamento = get_object_or_404(Planejamento, id=self.kwargs['planejamento_id'])
        context['planejamento'] = planejamento
        return context


@method_decorator(never_cache, name="dispatch")
class PlanejamentoFormView(View):
    form_class = PlanejamentoForm
    template_name = "planejamento/form.html"

    def get(self, request, planejamento_id=None):
        form = self.form_class()
        if planejamento_id:
            planejamento = get_object_or_404(Planejamento, id=planejamento_id)
            form = self.form_class(instance=planejamento)
        return render(request, self.template_name, {"form": form})

    def post(self, request, planejamento_id=None):
        form = self.form_class(request.POST)
        msg = 'Planejamento criado com sucesso'

        if planejamento_id:
            planejamento = get_object_or_404(Planejamento, id=planejamento_id)
            form = self.form_class(request.POST, instance=planejamento)
            msg = 'Planejamento modificado com sucesso'
    
        if form.is_valid():
            form.save()
            messages.success(request, msg)
            return redirect('list_planejamentos')


@method_decorator(never_cache, name="dispatch")
class PlanejamentoDeleteView(DeleteView):
    model = Planejamento
    pk_url_kwarg = "planejamento_id"

    def get_success_url(self):
        messages.success(self.request, "Planejamento removido com sucesso")
        return reverse_lazy('list_planejamentos')


@method_decorator(never_cache, name="dispatch")
class ArtistaListView(ListView):
    model = Artista
    template_name = 'artista/list.html'
    context_object_name = 'artistas'

    def get_queryset(self):
        return Artista.objects.all().order_by('nome')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['eventos'] = Evento.objects.all()
        context['create_url'] = reverse('create_artista')
        return context


@method_decorator(never_cache, name="dispatch")
class ArtistaDetailView(TemplateView):
    template_name = "artista/artista.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        artista = get_object_or_404(Artista, id=self.kwargs['artista_id'])
        context['artista'] = artista
        return context


@method_decorator(never_cache, name="dispatch")
class ArtistaFormView(View):
    form_class = ArtistaForm
    template_name = "artista/form.html"

    def get(self, request, artista_id=None):
        form = self.form_class()
        if artista_id:
            artista = get_object_or_404(Artista, id=artista_id)
            form = self.form_class(instance=artista)
        return render(request, self.template_name, {"form": form})

    def post(self, request, artista_id=None):
        form = self.form_class(request.POST)
        msg = 'Artista cadastrado com sucesso'

        if artista_id:
            artista = get_object_or_404(Artista, id=artista_id)
            form = self.form_class(request.POST, instance=artista)
            msg = 'Artista atualizado com sucesso'
        
        if form.is_valid():
            artista = form.save(commit=False)
            artista.save()
            eventos = request.POST.getlist('eventos')
            if eventos:
                eventos = Evento.objects.filter(id__in=eventos)
                artista.eventos.set(eventos)
            messages.success(request, msg)
            return redirect('list_artistas')
        
        return render(request, self.template_name, {"form": form})


@method_decorator(never_cache, name="dispatch")
class ArtistaDeleteView(DeleteView):
    model = Artista
    pk_url_kwarg = "artista_id"

    def get_success_url(self):
        messages.success(self.request, "Artista removido com sucesso")
        return reverse_lazy('list_artistas')


@method_decorator(never_cache, name="dispatch")
class InscricaoListView(ListView):
    model = Inscricao
    paginate_by = 10
    template_name = "inscricao/list.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Inscricao.objects.filter(nome__icontains=query).order_by(Lower('nome'))
        return Inscricao.objects.all().order_by(Lower('nome'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['create_url'] = reverse('create_inscricao')
        return context

@method_decorator(never_cache, name="dispatch")
class InscricaoDetailView(TemplateView):
    template_name = "inscricao/incricao.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inscricao = get_object_or_404(Inscricao, id=self.kwargs['inscricao_id'])
        context['inscricao'] = inscricao
        return context

@method_decorator(never_cache, name="dispatch")
class InscricaoFormView(View):
    form_class = InscricaoForm
    template_name = "inscricao/form.html"

    def get(self, request, inscricao_id=None):
        form = self.form_class()
        eventos = Evento.objects.all()
        if inscricao_id:
            inscricao = get_object_or_404(Inscricao, id=inscricao_id)
            form = self.form_class(instance=inscricao)
        
        # Ensure the lote queryset is populated
        form.fields['lote'].queryset = Lote.objects.all()
        
        return render(request, self.template_name, {"form": form, "eventos": eventos})

    def post(self, request, inscricao_id=None):
        inscricao = None
        if inscricao_id:
            inscricao = get_object_or_404(Inscricao, id=inscricao_id)
            form = self.form_class(request.POST, instance=inscricao)
        else:
            form = self.form_class(request.POST)
    
        form.fields['lote'].queryset = Lote.objects.all()
        
        if form.is_valid():
            inscricao = form.save(commit=False)
            inscricao.save()
    
            # Limpa os eventos existentes antes de adicionar os novos
            inscricao.eventos.clear()
            
            eventos_ids = request.POST.getlist('eventos')
            if eventos_ids:
                eventos = Evento.objects.filter(id__in=eventos_ids)
                inscricao.eventos.set(eventos)
    
            inscricao.valor_total = inscricao.calcular_valor_total()
            inscricao.save()
    
            # Atualiza o contador de inscrições para todos os eventos associados
            for evento in inscricao.eventos.all():
                evento.atualizar_contador_inscricoes()
    
            return redirect('list_inscricoes')
    
        return render(request, self.template_name, {
            'form': form,
            'eventos': Evento.objects.all()
        })

@method_decorator(never_cache, name="dispatch")
class InscricaoDeleteView(DeleteView):
    model = Inscricao
    pk_url_kwarg = "inscricao_id"

    def get_success_url(self):
        messages.success(self.request, "Inscrição removida com sucesso")
        return reverse_lazy('list_inscricoes')

@method_decorator(never_cache, name="dispatch")
class InscricaoEventoFormView(View):
    form_class = InscricaoEventoForm
    template_name = "inscricao/form_evento.html"

    def get(self, request, inscricao_id):
        form = self.form_class()
        inscricao = get_object_or_404(Inscricao, id=inscricao_id)
        return render(request, self.template_name, {
            "form": form,
            "inscricao": inscricao
        })

    def post(self, request, inscricao_id):
        form = self.form_class(request.POST)
        inscricao = get_object_or_404(Inscricao, id=inscricao_id)
        msg = 'Evento adicionado à inscrição com sucesso'

        if form.is_valid():
            inscricao = form.save(commit=False)
            
            # Ainda não salva no banco
            eventos_ids = request.POST.getlist('eventos')
            eventos = Evento.objects.filter(id__in=eventos_ids)
            
            inscricao.valor_total = sum(evento.valor_unitario for evento in eventos) - inscricao.desconto + inscricao.lote.valor_unitario
            inscricao.valor_parcela = inscricao.calcular_valor_parcela()

            inscricao.save()  # Agora sim, já com valores certos
            inscricao.eventos.set(eventos)

            # Atualiza o contador de inscrições
            for evento in eventos:
                evento.atualizar_contador_inscricoes()

            return redirect('list_inscricoes')

@method_decorator(never_cache, name="dispatch")
class InscricaoEventoDeleteView(DeleteView):
    model = InscricaoEvento
    pk_url_kwarg = "inscricao_evento_id"

    def get_success_url(self):
        inscricao_id = self.kwargs['inscricao_id']
        inscricao = get_object_or_404(Inscricao, id=inscricao_id)
        
        # Recalcular valor total da inscrição após remover o evento
        inscricao.valor_total = inscricao.calcular_valor_total()
        inscricao.save()
        
        # Atualiza o contador de inscrições para o evento associado
        inscricao_evento = self.object
        inscricao_evento.evento.atualizar_contador_inscricoes()
        
        messages.success(self.request, "Evento removido da inscrição com sucesso")
        return reverse('detail_inscricao', kwargs={'inscricao_id': inscricao_id})