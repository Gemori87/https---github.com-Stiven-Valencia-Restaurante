from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistroUsuarioForm, ContactForm
from .models import Pedido, DetallePedido, Platillos, Cliente
from .forms import PedidoForm, DetallePedidoForm
from django.utils import timezone
def logout_view(request):
    logout(request)
    return redirect('login')  
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils.crypto import get_random_string


def inicio(request):
    return render(request, 'paginas/inicio.html')

def nosotros(request):
    form = ContactForm(request.POST)  
    if request.method == 'POST' and form.is_valid():
        
        nombre = form.cleaned_data['nombre']
        email = form.cleaned_data['email']
        mensaje = form.cleaned_data['mensaje']
        
        send_mail(
            f'Mensaje de {nombre}',
            mensaje,
            email,
            ['brayan12.es@gmail.com'],
            fail_silently=False,
        )
        messages.success(request, "¡Tu mensaje ha sido enviado con éxito!")  
        return render(request, 'paginas/nosotros.html', {'form': form})  
    return render(request, 'paginas/nosotros.html', {'form': form})  

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

def menu(request):
    platillos = Platillos.objects.all()
    return render(request, "menu.html", {"platillos": platillos})

def listar_platillos(request):
    platillos = Platillos.objects.all()  
    return render(request, 'platillos/index.html', {'platillos': platillos})

def agregar_platillo(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        imagen = request.FILES.get('imagen')
        descripcion = request.POST.get('descripcion')

        if not nombre:
            messages.error(request, "El nombre del platillo es obligatorio.")
            return redirect('agregar_platillo')
        if not descripcion:
            messages.error(request, "La descripción del platillo es obligatoria.")
            return redirect('agregar_platillo')
        if not precio:
            messages.error(request, "El precio del platillo es obligatorio.")  # Validar el precio
            return redirect('agregar_platillo')
        if not imagen:
            messages.warning(request, "No se ha proporcionado una imagen para el platillo.")

        nuevo_platillo = Platillos(nombre=nombre, precio=precio, imagen=imagen, descripcion=descripcion)
        nuevo_platillo.save()

        messages.success(request, 'Platillo agregado exitosamente.')
        return redirect('platillos')  

    return render(request, 'platillos/crear.html')

def editar_platillo(request, id):
    platillo = get_object_or_404(Platillos, id=id)
    print(platillo.nombre, platillo.precio, platillo.descripcion)  # Para depuración
    if request.method == 'POST':
        platillo.nombre = request.POST.get('nombre')
        platillo.descripcion = request.POST.get('descripcion')

        
        precio = request.POST.get('precio')
        if precio:
            platillo.precio = float(precio)

        if request.FILES.get('imagen'):
            platillo.imagen = request.FILES.get('imagen')  
        
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
    platillo.activo = False  
    platillo.save()

    messages.success(request, 'Platillo ocultado correctamente.')
    return redirect('platillos')

def mostrar_platillo(request, id):
    platillo = get_object_or_404(Platillos, id=id)
    platillo.activo = True  
    platillo.save()

    return redirect('platillos')

def crear_pedido(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        platillos_ids = request.POST.getlist('platillos')  
        cantidades = request.POST.getlist('cantidades')  

        cliente = Cliente.objects.get(id=cliente_id)  
        codigo_pedido = get_random_string(10)  
        total = 0  

        
        pedido = Pedido.objects.create(
            codigo=codigo_pedido,
            cliente=cliente,
            fecha_hora=timezone.now(),
            total=total
        )

       
        for platillo_id, cantidad in zip(platillos_ids, cantidades):
            platillo = Platillos.objects.get(id=platillo_id)
            cantidad = int(cantidad)
            subtotal = platillo.precio * cantidad
            total += subtotal

            DetallePedido.objects.create(
                pedido=pedido,
                platillo=platillo,
                cantidad=cantidad,
                valor_unitario=platillo.precio,
                subtotal=subtotal
            )

        
        pedido.total = total
        pedido.save()

        messages.success(request, 'Pedido creado correctamente.')
        return redirect('listar_pedidos')  

    platillos = Platillos.objects.all()  
    clientes = Cliente.objects.all()  
    return render(request, 'crear_pedido.html', {'platillos': platillos, 'clientes': clientes})

def listar_pedidos(request):
    pedidos = Pedido.objects.all()  
    return render(request, 'listar_pedidos.html', {'pedidos': pedidos})

def ver_detalles_pedido(request, id):
    pedido = Pedido.objects.get(id=id)
    detalles = pedido.detalles.all()  
    return render(request, 'ver_detalles_pedido.html', {'pedido': pedido, 'detalles': detalles})

@login_required
def agregar_al_carrito(request):
    if "carrito" not in request.session:
        request.session["carrito"] = []  

    if request.method == "POST":
        platillo_id = request.POST.get("platillo_id")
        cantidad = int(request.POST.get("cantidad", 1))

        platillo = get_object_or_404(Platillos, id=platillo_id)

        carrito = request.session["carrito"]

        
        for item in carrito:
            if item["platillo_id"] == platillo_id:
                item["cantidad"] += cantidad
                break
        else:
           
            carrito.append({
                "platillo_id": platillo_id,
                "nombre": platillo.nombre,
                "precio": float(platillo.precio),
                "cantidad": cantidad
            })

        request.session["carrito"] = carrito  
        messages.success(request, "Platillo agregado al carrito.")
        return redirect("ver_carrito")

    platillos = Platillos.objects.all()
    return render(request, "menu.html", {"platillos": platillos})

@login_required
def ver_carrito(request):
    carrito = request.session.get("carrito", [])
    total = sum(item["precio"] * item["cantidad"] for item in carrito)
    
    return render(request, "carrito.html", {"carrito": carrito, "total": total})

def login_view(request):
    if request.method == 'POST':
        if 'admin_login' in request.POST:
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                if user.is_staff:  
                    login(request, user)
                    return redirect('admin_dashboard')  
        else:
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('perfil')  

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

#@login_required 
def crear_pedido(request):
    if request.method == 'POST':
        pedido_form = PedidoForm(request.POST)
        if pedido_form.is_valid():
            pedido = pedido_form.save(commit=False)
            
            
            cliente = get_object_or_404(Cliente, user=request.user)
            pedido.cliente = cliente  
            
            pedido.save()
            return redirect('menu')  
    else:
        pedido_form = PedidoForm()

    return render(request, 'crear_pedido.html', {'pedido_form': pedido_form})

@login_required
def agregar_detalle(request, pedido_id):
    pedido = Pedido.objects.get(pk=pedido_id)
    
    if request.method == 'POST':
        detalle_form = DetallePedidoForm(request.POST)
        if detalle_form.is_valid():
            detalle = detalle_form.save(commit=False)
            detalle.pedido = pedido
            detalle.save()
            return redirect('menu')

    else:
        detalle_form = DetallePedidoForm()

    return render(request, 'agregar_detalle.html', {'detalle_form': detalle_form, 'pedido': pedido})