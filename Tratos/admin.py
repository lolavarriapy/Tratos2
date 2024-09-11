from django.contrib import admin
from .Models.mObra import Obra
from .Models.mUnidadModelo import UnidadModelo
from .Models.mTrato import Trato 
from .Models.mUnidadTipo import TipoUnidad
from .Models.mUnidadObra import UnidadObra
from .Models.mTratoCategoria import TratoCategoria
from .Models.mTratoModelo import TratoModelo
from .Models.mTratoEspecialidad import TratoEspecialidad
from .Models.mTratoCapataz import TratoCapataz
from .Models.mUnidadMedida import UnidadMedida
from .Models.mObraUsuario import ObraUsuario
from .Models.mObraCategoria import ObraCategoria
from .Models.mTratoUnidadBloqueada import TratoUnidadBloqueada

# Register your models here.



class ObraAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        # Excluye campos especiales de Django que no se deben mostrar
        return [field for field in self.model().__dict__.keys() if not field.startswith('_')]
    search_fields = ('id', 'descripcion')  # Campos que serán buscables
    
class ModeloUnidadAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        # Excluye campos especiales de Django que no se deben mostrar
        return [field for field in self.model().__dict__.keys() if not field.startswith('_')]
    search_fields = ('id', 'descripcion')  # Campos que serán buscables
    
class TratoAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        # Excluye campos especiales de Django que no se deben mostrar
        return [field for field in self.model().__dict__.keys() if not field.startswith('_')]
    search_fields = ('cod', 'partida')  # Campos que serán buscables

class TipoUnidadAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        # Excluye campos especiales de Django que no se deben mostrar
        return [field for field in self.model().__dict__.keys() if not field.startswith('_')]
    search_fields = ('id', 'descripcion')  # Campos que serán buscables

class UnidadObraAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        # Excluye campos especiales de Django que no se deben mostrar
        return [field for field in self.model().__dict__.keys() if not field.startswith('_')]
    search_fields = ('id', 'descripcion')  # Campos que serán buscables

class TratoCategoriaAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        # Excluye campos especiales de Django que no se deben mostrar
        return [field for field in self.model().__dict__.keys() if not field.startswith('_')]
    search_fields = ('id', 'descripcion')  # Campos que serán buscables
    
class TratoModeloAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        # Excluye campos especiales de Django que no se deben mostrar
        return [field for field in self.model().__dict__.keys() if not field.startswith('_')]
    search_fields = ('id', 'descripcion')  # Campos que serán buscables  
    
class TratoEspecialidadAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        # Excluye campos especiales de Django que no se deben mostrar
        return [field for field in self.model().__dict__.keys() if not field.startswith('_')]
    search_fields = ('id', 'descripcion')  # Campos que serán buscables  
    
class TratoCapatazAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        # Excluye campos especiales de Django que no se deben mostrar
        return [field for field in self.model().__dict__.keys() if not field.startswith('_')]
    search_fields = ('id', 'descripcion')  # Campos que serán buscables   
    
class UnidadMedidaAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        # Excluye campos especiales de Django que no se deben mostrar
        return [field for field in self.model().__dict__.keys() if not field.startswith('_')]
    search_fields = ('id', 'descripcion')  # Campos que serán buscables   
        
class UnidadMedidaAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        # Excluye campos especiales de Django que no se deben mostrar
        return [field for field in self.model().__dict__.keys() if not field.startswith('_')]
    search_fields = ('id', 'descripcion')  # Campos que serán buscables
  
class ObraUsuarioAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        # Excluye campos especiales de Django que no se deben mostrar
        return [field for field in self.model().__dict__.keys() if not field.startswith('_')]
    search_fields = ('id', 'descripcion')  # Campos que serán buscables  

class ObraCategoriaAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        # Excluye campos especiales de Django que no se deben mostrar
        return [field for field in self.model().__dict__.keys() if not field.startswith('_')]
    search_fields = ('id', 'descripcion')  # Campos que serán buscables  

class TratoUnidadBloqueadaAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        # Excluye campos especiales de Django que no se deben mostrar
        return [field for field in self.model().__dict__.keys() if not field.startswith('_')]
    search_fields = ('id', 'descripcion')  # Campos que serán buscables  

admin.site.register(Trato, TratoAdmin)
admin.site.register(Obra, ObraAdmin)
admin.site.register(UnidadModelo, ModeloUnidadAdmin)
admin.site.register(TipoUnidad, TipoUnidadAdmin)
admin.site.register(UnidadObra, UnidadObraAdmin)
admin.site.register(TratoCategoria, TratoCategoriaAdmin)
admin.site.register(TratoModelo, TratoModeloAdmin)
admin.site.register(TratoEspecialidad, TratoEspecialidadAdmin)
admin.site.register(TratoCapataz, TratoCapatazAdmin)
admin.site.register(UnidadMedida, UnidadMedidaAdmin)
admin.site.register(ObraUsuario, ObraUsuarioAdmin)
admin.site.register(ObraCategoria, ObraCategoriaAdmin)
admin.site.register(TratoUnidadBloqueada, TratoUnidadBloqueadaAdmin)


