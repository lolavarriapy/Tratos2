from django.shortcuts import redirect
from django.urls import reverse

class AdminGroupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Obtener la URL de la página de inicio de sesión
        login_url = reverse('signin')
        
        # Evitar el bucle de redirección para la URL de inicio de sesión
        if request.path != login_url and request.path != "/signin/" and request.path != "/":
            # Verificar si el usuario está autenticado
            if request.user.is_authenticated:
                request.session['is_admin'] = request.user.groups.filter(name='Administrador').exists()
            else:
                request.session['is_admin'] = False

        else:
            if request.user.is_authenticated:
                return redirect('home')
        # Pasar la solicitud al siguiente middleware o vista
        response = self.get_response(request)
        return response