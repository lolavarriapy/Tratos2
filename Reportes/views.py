from django.shortcuts import render
from Tratos.Models import Trato
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from Tratos.Models.mObraUsuario import ObraUsuario
from Tratos.Models.mTratoCapataz import TratoCapataz
from Tratos.Models.mUnidadObra import UnidadObra
from Tratos.Models.mObra import Obra
from django.db.models import Q, Sum
from django.http import JsonResponse
from Rebajes.Models.mInformeTrabajo_detalle import InformeTrabajo_detalle
# Create your views here.
@login_required
def reporteCapataz(request):
    user = request.user
    if request.method == "GET":
        
        obrasList = ObraUsuario.objects.filter(usuario=user).select_related('obra')
        
        if obrasList.exists():
            capatazList = TratoCapataz.objects.filter(idObra=obrasList[0].obra)
            tratosList = Trato.objects.filter(obra=obrasList[0].obra).order_by('categoria','id')
            
            # Configurar la paginación
            paginator = Paginator(tratosList, 30)  # 10 informes por página
            page_number = request.GET.get('page')  # Obtener el número de página de la solicitud GET
            page_obj = paginator.get_page(page_number)  # Obtener la página actual
            
            return render(request, 'rptCapataz.html',{'title':'Reporte Capataz','tratos':page_obj,'obrasList':obrasList,'capatazList':capatazList})    
        else:
            return render(request, 'rptCapataz.html',{'title':'Reporte Capataz','tratos':'','obrasList':'','capatazList':''})    

    if request.method == "POST":
        
        obra = request.POST['idObra']
        capataz = request.POST['idCapataz']
        vObra = Obra.objects.get(id=obra)
        vUsuariObra = ObraUsuario.objects.filter(usuario=user, obra=vObra).exists()
        if vUsuariObra:

            query_conditions = Q()
            query_conditions &= Q(obra_id=obra)
            
            if not capataz == "0":
                query_conditions &= Q(capataz_id=capataz)
                
            tratosList = Trato.objects.filter(query_conditions).order_by('categoria','id')
            
            paginator = Paginator(tratosList, 30)  # 10 informes por página
            page_number = request.GET.get('page')  # Obtener el número de página de la solicitud GET
            page_obj = paginator.get_page(page_number)  # Obtener la página actual
            
            tratos = []
            for trato in page_obj:

                modelos_descripciones = [f"{tm.modelo.cod} $[ {tm.valorTratoModelo_sep()} ] <br />" for tm in trato.tratomodelo_set.all() if tm.estado == True]
                modelos_concatenados = ''.join(modelos_descripciones)

                tratos.append(
                    {
                        'cod': trato.cod,  
                        'codFamilia':trato.codFamilia,
                        'partida': trato.partida, 
                        'valorTrato':trato.valorTrato,
                        'modelos_concatenados':modelos_concatenados,
                        'unidadMedida': trato.unidadMedida.descripcion,
                    })


            return JsonResponse({
                'tratos': tratos,
                'has_previous': page_obj.has_previous(),
                'has_next': page_obj.has_next(),
                'num_pages': paginator.num_pages,
                'current_page': page_obj.number,
            })      

@login_required
def capatazImprimir(request):
    user = request.user
    obra = request.GET.get('obra')
    capataz = request.GET.get('capataz')
    vObra = Obra.objects.get(id=obra)
    vUsuariObra = ObraUsuario.objects.filter(usuario=user, obra=vObra).exists()
    if vUsuariObra:    
        # Obtén los datos que deseas mostrar en el reporte
        query_conditions = Q()
        query_conditions &= Q(obra_id=obra)
        
        if not capataz == "0":
            query_conditions &= Q(capataz_id=capataz)
            
        tratosList = Trato.objects.filter(query_conditions).order_by('categoria','id')

        # Renderiza la plantilla a un string HTML
        html = render_to_string('rptCapatazPrint.html', {'tratos': tratosList})

        # Crea un objeto HttpResponse con el tipo de contenido PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_capataz.pdf"'

        # Convierte el HTML a PDF usando xhtml2pdf
        pisa_status = pisa.CreatePDF(html, dest=response)

        # Verifica si hay errores al generar el PDF
        if pisa_status.err:
            return HttpResponse('Hubo un error al generar el PDF', status=500)
    
    return response


@login_required
def capatazObra(request):
    

    if request.method == "POST":
        
        obra = request.POST['idObra']
        vObra = Obra.objects.get(id=obra)
        
        capatazList = TratoCapataz.objects.filter(idObra = vObra)
        
        result=""
        for capataz in capatazList:
            result += '{"id":"'+str(capataz.id)+'","nombre":"'+capataz.nombre+' '+capataz.apellido+'"},'
        
        if not result == "": 
            result = "["+result[:-1]+"]"
        else:
            result = "[]"
        return JsonResponse(result, safe=False)
    
    
def reporteRebajes(request):
    user = request.user
    if request.method == "GET":
        
        obrasList = ObraUsuario.objects.filter(usuario=user).select_related('obra')       
        return render(request, 'rptRebajes.html', {'title': 'Resumen Rebajes', 'obrasList': obrasList}) 
        
    if request.method == "POST":
        # Filtra los datos según la obra que necesites
        obra_id = request.POST['idObra']
        vObra = Obra.objects.filter(id=obra_id)
        vUsuariObra = ObraUsuario.objects.filter(usuario=user, obra=vObra[0])
        
        if vUsuariObra.exists():
            # Obtener todos los tratos y unidades de la obra específica
            tratos = Trato.objects.filter(obra=obra_id).order_by('categoria', 'id')
            unidades = UnidadObra.objects.filter(idObra=obra_id, estado=1)
            
            # Inicializa un diccionario para almacenar los datos de la tabla pivote
            matriz_pivote = {}
            
            for trato in tratos:
                # Concatenar "partida" con "cod" para la clave
                key = f"{trato.cod} | {trato.partida}"
                matriz_pivote[key] = {}
                
                for unidad in unidades:
                    detalles = InformeTrabajo_detalle.objects.filter(trato=trato, unidad=unidad)
                    if detalles.exists():
                        tipo_unidad = unidad.idModelo.tipo  # Asumiendo que UnidadObra tiene una relación con TipoUnidad
                        if tipo_unidad.medicion == "CAN":
                            total_cantidad = sum(d.cantidad for d in detalles)
                            matriz_pivote[key][unidad.cod] = {
                                'valor': ', '.join(detalle.itrabajo.folio+"|"+str(detalle.itrabajo.id) for detalle in detalles),
                                'color': 'red' if total_cantidad == 0 else 'yellow' if total_cantidad < trato.cantidad else '#7df77d'
                            }
                        elif tipo_unidad.medicion == "UNI":
                            total_avance = sum(d.avance for d in detalles)
                            matriz_pivote[key][unidad.cod] = {
                                'valor': ', '.join(detalle.itrabajo.folio+"|"+str(detalle.itrabajo.id) for detalle in detalles),
                                'color': 'red' if total_avance == 0 else 'yellow' if total_avance < 100 else '#7df77d'
                            }
                    else:
                        matriz_pivote[key][unidad.cod] = {'valor': '', 'color': 'white'}
            
            return JsonResponse(matriz_pivote)