from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import Libro, Nota, ProgresoLibro
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .forms import UserUpdateForm, CustomUserCreationForm 
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from .forms import LibroForm # Importamos el nuevo formulario


def index(request):
    query = request.GET.get('b', '')
    if query:
        resultados = Libro.objects.filter(Q(titulo__icontains=query) | Q(autor__icontains=query))
    else:
        resultados = Libro.objects.all()
    return render(request, 'index.html', {'datos': resultados})

@login_required
def libro_detalle(request, id):
    libro = get_object_or_404(Libro, id=id)
    progreso, created = ProgresoLibro.objects.get_or_create(usuario=request.user, libro=libro)
    notas = Nota.objects.filter(libro=libro, usuario=request.user).order_by('-creado_en')

    if request.method == "POST":
        if "pagina_actual" in request.POST:
            progreso.pagina_actual = request.POST.get("pagina_actual")
        if "categoria" in request.POST:
            progreso.categoria = request.POST.get("categoria")
        if "rating" in request.POST:
            rating = request.POST.get("rating")
            progreso.rating = rating if rating else None
        
        progreso.save()

        if "comentario" in request.POST and request.POST.get("comentario").strip():
            comentario_texto = request.POST["comentario"]
            color = request.POST.get("color", "green")
            Nota.objects.create(libro=libro, usuario=request.user, comentario=comentario_texto, color=color)
            messages.success(request, "Nota agregada con éxito.")
        
        return redirect('libro_detalle', id=libro.id)

    return render(request, 'libro_detalle.html', {
        'libro': libro,
        'progreso': progreso,
        'notas': notas
    })

@login_required
def eliminar_nota(request, nota_id):
    nota = get_object_or_404(Nota, id=nota_id, usuario=request.user)
    libro_id = nota.libro.id
    if request.method == "POST":
        nota.delete()
        messages.success(request, "Nota eliminada con éxito.")
    return redirect('libro_detalle', id=libro_id)

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class PanelLibroListView(StaffRequiredMixin, ListView):
    model = Libro
    template_name = 'panel/libro_list.html' 
    context_object_name = 'libros'
    paginate_by = 10

class PanelLibroCreateView(StaffRequiredMixin, CreateView):
    model = Libro
    form_class = LibroForm
    template_name = 'panel/libro_form.html'
    success_url = reverse_lazy('panel:libro_list') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Añadir Nuevo Libro'
        return context

class PanelLibroUpdateView(StaffRequiredMixin, UpdateView):
    model = Libro
    form_class = LibroForm
    template_name = 'panel/libro_form.html'
    success_url = reverse_lazy('panel:libro_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Editar Libro'
        return context

class PanelLibroDeleteView(StaffRequiredMixin, DeleteView):
    model = Libro
    template_name = 'panel/libro_confirm_delete.html'
    success_url = reverse_lazy('panel:libro_list')

class LibroUsuarioCreateView(LoginRequiredMixin, CreateView):
    """
    Vista para que cualquier usuario autenticado pueda añadir un libro.
    """
    model = Libro
    form_class = LibroForm
    template_name = 'libro_usuario_form.html' # Usaremos una nueva plantilla para el usuario
    success_url = reverse_lazy('index') # Al terminar, redirige al índice principal

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Añadir un Nuevo Libro a la Biblioteca'
        return context

    def form_valid(self, form):
        messages.success(self.request, '¡Gracias por tu contribución! El libro ha sido añadido.')
        return super().form_valid(form)

class LibroDeleteView(LoginRequiredMixin, DeleteView):
    model = Libro
    # Apunta a la plantilla que mostrará la pregunta de confirmación
    template_name = 'libro_confirm_delete.html'
    # URL a la que se redirigirá al usuario después de eliminar el libro
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        # Añade un mensaje de éxito que se mostrará en la siguiente página
        messages.success(self.request, f"El libro '{self.object.titulo}' ha sido eliminado correctamente.")
        return super().form_valid(form)
class UserListView(StaffRequiredMixin, ListView):
    model = User
    template_name = 'panel/usuario_list.html'
    context_object_name = 'usuarios'
    paginate_by = 10

class UserCreateView(StaffRequiredMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'panel/usuario_form.html'
    success_url = reverse_lazy('panel:usuario_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Crear Nuevo Usuario'
        return context

class UserUpdateView(StaffRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'panel/usuario_form.html'
    success_url = reverse_lazy('panel:usuario_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Editar Usuario'
        return context

class UserDeleteView(StaffRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'panel/usuario_confirm_delete.html'
    success_url = reverse_lazy('panel:usuario_list')

    def test_func(self):
        # Medida de seguridad: un usuario no puede eliminarse a sí mismo.
        return self.get_object() != self.request.user

    def form_valid(self, form):
        messages.success(self.request, f"El usuario '{self.object.username}' ha sido eliminado.")
        return super().form_valid(form)