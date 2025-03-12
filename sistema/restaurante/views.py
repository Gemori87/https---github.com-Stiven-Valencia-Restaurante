from django.shortcuts import redirect, render
from .models import Pedido, DetallePedido  # Importar los modelos de Pedido y DetallePedido
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .forms import RegistroUsuarioForm, ContactForm

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirige a la página de inicio de sesión después de cerrar sesión
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Platillos, Cliente





def crear_pedido(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        descripcion = request.POST.get('descripcion')
        total = float(request.POST.get('total'))  # Total calculado desde el formulario

        nuevo_pedido = Pedido(cliente_id=cliente_id, descripcion=descripcion, total=total)
        nuevo_pedido.save()

        # Guardar detalles del pedido
        for platillo_id in request.POST.getlist('platillos'):
            cantidad = int(request.POST.get(f'cantidad_{platillo_id}'))
            valor_unitario = float(request.POST.get(f'valor_unitario_{platillo_id}'))
            subtotal = cantidad * valor_unitario

            detalle = DetallePedido(pedido=nuevo_pedido, codigo_platillo_id=platillo_id, cantidad=cantidad, valor_unitario=valor_unitario, subtotal=subtotal)
            detalle.save()

        messages.success(request, 'Pedido creado exitosamente.')
        return redirect('inicio')  # Redirigir a la página de inicio

    platillos = Platillos.objects.all()  # Obtener todos los platillos para el formulario
    clientes = Cliente.objects.all()  # Obtener todos los clientes para el formulario
    return render(request, 'pedidos/crear.html', {'platillos': platillos, 'clientes': clientes})



def listar_pedidos(request):
    pedidos = Pedido.objects.all()  # Obtener todos los pedidos
    return render(request, 'pedidos/listar.html', {'pedidos': pedidos})

def inicio(request):
    return render(request, 'paginas/inicio.html')

def nosotros(request):
    form = ContactForm(request.POST)  # Asegúrate de que el formulario de contacto esté definido
    if request.method == 'POST' and form.is_valid():
        # Aquí puedes manejar el envío del formulario
        nombre = form.cleaned_data['nombre']
        email = form.cleaned_data['email']
        mensaje = form.cleaned_data['mensaje']
        # Lógica para enviar el mensaje o guardarlo
        send_mail(
            f'Mensaje de {nombre}',
            mensaje,
            email,
            ['brayan12.es@gmail.com'],
            fail_silently=False,
        )
        messages.success(request, "¡Tu mensaje ha sido enviado con éxito!")  # Agregar mensaje de éxito
        return render(request, 'paginas/nosotros.html', {'form': form})  # Pasa el formulario al contexto
    return render(request, 'paginas/nosotros.html', {'form': form})  # Pasa el formulario al contexto

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)  
        if form.is_valid():
            user = form.save()  
            print(f"Usuario {user.username} creado.")  
            login(request, user)  
            messages.success(request, f'Cuenta creada para {user.username}! Bienvenido.')
            return redirect('perfil')  
        else:
            print("Formulario no válido")  
    else:
        form = RegistroUsuarioForm()
    
    return render(request, 'registration/registrar.html', {'form': form})

def listar_platillos(request):
    platillos = Platillos.objects.all()  
    return render(request, 'platillos/index.html', {'platillos': platillos})

def agregar_platillo(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        imagen = request.FILES.get('imagen')
        precio = request.POST.get('precio')
        descripcion = request.POST.get('descripcion')

        if not nombre:
            messages.error(request, "El nombre del platillo es obligatorio.")
            return redirect('agregar_platillo')
        if not descripcion:
            messages.error(request, "La descripción del platillo es obligatoria.")
            return redirect('agregar_platillo')
        if not descripcion:
            messages.error(request, "El precio del platillo es obligatorio.")
            return redirect('agregar_platillo')
        if not imagen:
            messages.warning(request, "No se ha proporcionado una imagen para el platillo.")

        nuevo_platillo = Platillos(platillo=nombre, imagen=imagen, precio=precio, descripcion=descripcion)
        nuevo_platillo.save()

        messages.success(request, 'Platillo agregado exitosamente.')
        return redirect('platillos')  # Redirigir a la lista de platillos

    return render(request, 'platillos/crear.html')

def editar_platillo(request, id):
    platillo = get_object_or_404(Platillos, id=id)

    if request.method == 'POST':
        platillo.platillo = request.POST.get('nombre')
        if request.FILES.get('imagen'):
            platillo.imagen = request.FILES.get('imagen')  # Si se subió una nueva imagen
        platillo.descripcion = request.POST.get('descripcion')
        platillo.precio = request.POST.get('precio')
        platillo.save()

        messages.success(request, 'Platillo actualizado correctamente.')
        return redirect('platillos')

    return render(request, 'platillos/editar.html', {'platillo': platillo})

def eliminar_platillo(request, id):
    platillo = get_object_or_404(Platillos, id=id)
    platillo.delete()
    messages.success(request, 'Platillo eliminado exitosamente.')
    return redirect('listar_platillos')

def ocultar_platillo(request, id):
    platillo = get_object_or_404(Platillos, id=id)
    platillo.activo = False  # Cambiar el estado a no visible
    platillo.save()

    messages.success(request, 'Platillo ocultado correctamente.')
    return redirect('platillos')

def mostrar_platillo(request, id):
    platillo = get_object_or_404(Platillos, id=id)
    platillo.activo = True  
    platillo.save()

    return redirect('platillos')

def login_view(request):
    if request.method == 'POST':
        if 'admin_login' in request.POST:
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                if user.is_staff:  # Check if the user is an admin
                    login(request, user)
                    return redirect('admin_dashboard')  # Redirect to admin dashboard
        else:
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('perfil')  # Redirect to user profile

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():  
            return redirect('inicio')  
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def perfil(request):
    if request.method == 'POST':
        if 'add_phone' in request.POST and request.POST.get('phone_number'):
            phone_number = request.POST.get('phone_number')
            request.user.profile.phone_number = phone_number
            request.user.profile.save()
        elif 'remove_phone' in request.POST:
            request.user.profile.phone_number = ''
            request.user.profile.save()
    
    return render(request, 'registration/perfil.html', {'user': request.user})

def recuperar_contrasena(request):
    if request.method == "POST":
        email = request.POST["email"]
        try:
            user = User.objects.get(email=email)
            nueva_contrasena = User.objects.make_random_password()
            user.set_password(nueva_contrasena)
            user.save()

            send_mail(
                "Recuperación de contraseña",
                f"Hola {user.username}, tu nueva contraseña es: {nueva_contrasena}",
                "tuemail@gmail.com",
                [email],
                fail_silently=False,
            )

            messages.success(request, "Se ha enviado un correo con tu nueva contraseña.")
            return redirect("login")
        except User.DoesNotExist:
            messages.error(request, "No se encontró una cuenta con ese correo.")
    
    return render(request, "recuperar_contrasena.html")
