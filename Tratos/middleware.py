from django.shortcuts import redirect
from django.urls import reverse

class AdminGroupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Obtener la URL de la página de inicio de sesión
        login_url = reverse('signin')

        if request.path != login_url and request.path != "/signin/" and request.path != "/" and request.path != "/logout/":
            # Verificar si el usuario está autenticado
            if request.user.is_authenticated:
                if not request.user.userextend.primerAcceso:
                   if request.path != reverse('cambiarContrasena') and request.path != reverse('logout'):
                        return redirect('cambiarContrasena')  # Redirige a la página de cambio de contraseña   
                        
                request.session['is_admin'] = request.user.groups.filter(name='Administrador').exists()
            else:
                request.session['is_admin'] = False

        else:
            if request.user.is_authenticated and request.path != "/logout/": 
                return redirect('home')

        response = self.get_response(request)
        return response