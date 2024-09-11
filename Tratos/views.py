from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.db import IntegrityError
from .Models.mTrato import Trato
from .Models.mObra import Obra
from .Models.mUnidadObra import UnidadObra
from .Models.mUnidadTipo import TipoUnidad
from .Models.mUnidadModelo import UnidadModelo
from .Models.mTratoCategoria import TratoCategoria
from .Models.mTratoEspecialidad import TratoEspecialidad
from .Models.mTratoCapataz import TratoCapataz
from .Models.mTratoModelo import TratoModelo
from .Models.mUnidadMedida import UnidadMedida
from .Models.mObraUsuario import ObraUsuario
from .Models.mObraCategoria import ObraCategoria
from .Models.mTratoUnidadBloqueada import TratoUnidadBloqueada
from Rebajes.Models import InformeTrabajo, InformeTrabajo_detalle
from django.core import serializers 
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
import json
from decimal import Decimal
from django.db.models import Q, Sum
import math

@login_required
def home(request):
    totalObras = Obra.objects.all().count()
    cantTratos = Trato.objects.all().count()
    totalTratos = Trato.objects.aggregate(Sum("valorTrato")) 
    
    
    cantRebajes = InformeTrabajo.objects.all().count()
    totalRebajes = InformeTrabajo.objects.aggregate(Sum("total"))
    
    sumRebajes = "0"
    if totalRebajes["total__sum"] is not None:
        sumRebajes = '{:,}'.format(totalRebajes["total__sum"])
    
    sumTratos = "0"
    if totalTratos["valorTrato__sum"] is not None:
        sumTratos = '{:,}'.format(totalTratos["valorTrato__sum"])
        
    return render(request,'home.html',{'title':'Home','totalObra':totalObras,'totalTratos': sumTratos,
                                       'totalRebajes': sumRebajes,
                                       'cantTratos':cantTratos, 'cantRebajes':cantRebajes})

def signup(request):
    if request.method == "GET":
        return render(request,'signup.html',{
            'form':UserCreationForm
            })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],
                                    password=request.POST['password2'])
                user.save()
                login(request,user)
                return redirect('tratos')
            
            except IntegrityError:
                 return render(request,'signup.html',{
                'form':UserCreationForm,
                'error':'Usuario ya existe'
                })
                
        return render(request,'signup.html',{
        'form':UserCreationForm,
        'error':'Contraseñas no coinciden'
        })

@permission_required('Tratos.create_trato',raise_exception=True)
def tratos_crear(request):
    
    if request.method == "GET":

        obras = Obra.objects.all()  
        return render(request, 'trato_crear.html',{'title':'Trato > crear','obras':obras})
    
    elif request.method == "POST":


        rIdObra = request.POST['idObra']
        user = request.user 
        vUsuariObra = ObraUsuario.objects.filter(usuario=user, obra=rIdObra)
        
        if vUsuariObra.exists():    
            icodFam = request.POST['codFam']
            idCategoria = request.POST['idCategoria']
            idEspecialidad = request.POST['idEspecialidad']
            idUnidadMedida = request.POST['idUnidadMedida']
            idCapataz = request.POST['idCapataz']
            ipartida = request.POST['partida']        
                    
            oCategoria = TratoCategoria.objects.get(id=idCategoria)
            oEspecialidad = TratoEspecialidad.objects.get(id=idEspecialidad)
            oCapataz = TratoCapataz.objects.get(id=idCapataz)
            oObra = Obra.objects.get(id=rIdObra)
            oUnidadMedida = UnidadMedida.objects.get(id=idUnidadMedida)

            try:
                ultimoTrato = Trato.objects.filter(categoria_id=oCategoria,obra=oObra,estado=1).latest("orden")
            except ObjectDoesNotExist:
                ultimoTrato = None
            
            if ultimoTrato is not None:
                icod = oCategoria.cod + "-" + str(int(ultimoTrato.cod.split("-")[1])+1)
            else:
                icod = oCategoria.cod + "-1" 
            
            
            
            vTrato = Trato.objects.filter(cod=icod,obra=oObra,estado=1).exists()
            if vTrato:
                unidad = {'id':'0','desc':'rep','rsp':'NOK'}
            else:
                obj = Trato.objects.create(
                    cod = icod.upper(),
                    codFamilia = icodFam,
                    categoria = oCategoria,
                    especialidad = oEspecialidad,
                    capataz = oCapataz,
                    partida = ipartida.upper(),
                    idUsuario = request.user,
                    obra = oObra,
                    unidadMedida = oUnidadMedida,
                    cantidad = 0
                )
            unidad = {'id':obj.id,'desc':obj.partida,'cod':obj.cod,'rsp':'OK'}

            return JsonResponse(unidad)  
        else:
            unidad = {'id':'0','desc':'rep','rsp':'NOK'}
 
@permission_required('Tratos.edit_trato',raise_exception=True)   
def tratos_actualizar(request):
    if request.method == "POST":
        idt = request.POST['idT']
        icodFam = request.POST['codFam']
        idCategoria = request.POST['idCategoria']
        idEspecialidad = request.POST['idEspecialidad']
        idUnidadMedida = request.POST['idUnidadMedida']
        idCapataz = request.POST['idCapataz']
        ipartida = request.POST['partida']
            
        oCategoria = TratoCategoria.objects.get(id=idCategoria)
        oEspecialidad = TratoEspecialidad.objects.get(id=idEspecialidad)
        oCapataz = TratoCapataz.objects.get(id=idCapataz)
        oUnidadMedida = UnidadMedida.objects.get(id=idUnidadMedida)

      
        vTrato = Trato.objects.get(id=idt)
        if vTrato:
            
            vTrato.codFamilia = icodFam
            vTrato.categoria = oCategoria
            vTrato.especialidad = oEspecialidad
            vTrato.capataz = oCapataz
            vTrato.unidadMedida = oUnidadMedida
            vTrato.partida = ipartida
                
            vTrato.save()
            trato = {'id':vTrato.id,'desc':vTrato.partida,'cod':vTrato.cod,'rsp':'OK'}
            
        else:
            trato = {'id':'0','desc':'rep','cod':'0','rsp':'NOK'}
            
        
        
        return JsonResponse(trato)  
    
@permission_required('Tratos.edit_trato',raise_exception=True)   
def trato_estado_actualizar(request):
    
    if request.method == "POST":
        
        idt = request.POST['idT']
        estado = request.POST['estado']
        rIdObra = request.POST['obra']
        
        user = request.user 
        vUsuariObra = ObraUsuario.objects.filter(usuario=user, obra=rIdObra)      
      
        if vUsuariObra.exists():
            vTrato = Trato.objects.get(id=idt)
            if vTrato:
                
                vTrato.estado = estado
                vTrato.save()
                trato = {'id':vTrato.id,'desc':vTrato.partida,'cod':vTrato.cod,'rsp':'OK'}
                
            else:
                trato = {'id':'0','desc':'rep','cod':'0','rsp':'NOK'}
                
        
        
        return JsonResponse(trato)      
    
@permission_required('Tratos.view_trato',raise_exception=True)
def tratos_buscar(request):

    rIdObra = request.POST['idObra']
    user = request.user 
    vUsuariObra = ObraUsuario.objects.filter(usuario=user, obra=rIdObra)
    
    if vUsuariObra.exists():    
        icodFam = request.POST['codFam']
        idCategoria = request.POST['idCategoria']
        idEspecialidad = request.POST['idEspecialidad']
        idUnidadMedida = request.POST['idUnidadMedida']
        idCapataz = request.POST['idCapataz']
        ipartida = request.POST['partida']
        
        rPage = request.POST['page']
        
        query_conditions = Q()
        
        #if icod:
        #   query_conditions &= Q(cod__icontains=icod)
            
        if icodFam:
            query_conditions &= Q(codFamilia__icontains=icodFam)
            
        if idCategoria != "null" and idCategoria != "":
            query_conditions &= Q(categoria_id=idCategoria)
            
        if idEspecialidad != "null" and idEspecialidad != "":
            query_conditions &= Q(especialidad__id=idEspecialidad)
            
        if idUnidadMedida != "null" and idUnidadMedida != "":
            query_conditions &= Q(unidadMedida__id=idUnidadMedida)
            
        if idCapataz != "null" and idCapataz != "":
            query_conditions &= Q(capataz__id=idCapataz)
            
        if ipartida != "":
            query_conditions &= Q(partida__icontains=ipartida)
        
        oObra = Obra.objects.get(id=rIdObra)    
        
        query_conditions &=Q(obra=oObra)
        tratos = Trato.objects.filter(query_conditions).order_by('categoria','orden')
        
        rData = ""
    
        paginator = Paginator(tratos, 30) 
        page_obj = paginator.get_page(rPage)  # Obtener la página actual
        tratos = []
        for trato in page_obj:

            modelos_descripciones = [f"{tm.modelo.cod}-{tm.rendimiento}-{tm.valorTratoModelo}|" for tm in trato.tratomodelo_set.all() if tm.estado == True]
            modelos_concatenados = ''.join(modelos_descripciones)

            tratos.append(
                {
                    'id': trato.id,
                    'cod': trato.cod,  
                    'partida': trato.partida, 
                    'unidadMedida': trato.unidadMedida.descripcion, 
                    'nroMaestros':trato.nroMaestros,
                    'nroJornales':trato.nroJornales,
                    'nroAyudantes':trato.nroAyudantes,
                    'sueldoMaestro':trato.sueldoMaestro,
                    'sueldoJornal':trato.sueldoJornal,
                    'sueldoAyudante':trato.sueldoAyudante,
                    'cantidad':trato.cantidad,
                    'valorTrato':trato.valorTrato,
                    'codFamilia':trato.codFamilia,
                    'idEspecialidad':trato.especialidad.id,
                    'idCategoria':trato.categoria.id,
                    'idCapataz':trato.capataz.id,
                    'idUnidadMedida':trato.unidadMedida.id,
                    'modelos_concatenados':modelos_concatenados,
                    'valorCuadrilla':trato.valorCuadrilla,               
                })

        return JsonResponse({
            'tratos': tratos,
            'has_previous': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
            'num_pages': paginator.num_pages,
            'current_page': page_obj.number,
            'rsp':'OK' 
        }) 
 
    else:

        return JsonResponse({
            'tratos': [{}],
            'has_previous': 0,
            'has_next': 0,
            'num_pages': 0,
            'current_page': 0,
            'rsp':'NOK' 
        })   
    
@permission_required('Tratos.edit_trato',raise_exception=True)   
@login_required
def tratos_cuadrilla_actualizar(request):
    
    
    idTrato = request.POST['idTrato']
    nroMaestros = request.POST['nroMaestros']
    sueldoMaestros = request.POST['sueldoMaestros']
    nroJornales = request.POST['nroJornales']
    sueldoJornales = request.POST['sueldoJornales']
    nroAyudantes = request.POST['nroAyudantes']
    sueldoAyudantes = request.POST['sueldoAyudantes']

    nroMaestros = int(nroMaestros) if nroMaestros else 0
    sueldoMaestros = int(sueldoMaestros) if sueldoMaestros else 0
    nroJornales = int(nroJornales) if nroJornales else 0
    sueldoJornales = int(sueldoJornales) if sueldoJornales else 0 
    nroAyudantes = int(nroAyudantes) if nroAyudantes else 0 
    sueldoAyudantes = int(sueldoAyudantes) if sueldoAyudantes else 0 


    obj = Trato.objects.get(id=idTrato)      
    obj.nroMaestros = nroMaestros
    obj.sueldoMaestro = sueldoMaestros
    obj.nroJornales = nroJornales
    obj.sueldoJornal = sueldoJornales
    obj.nroAyudantes = nroAyudantes
    obj.sueldoAyudante = sueldoAyudantes
    
    sumCuadrilla =(nroMaestros*sueldoMaestros)+(nroAyudantes*sueldoAyudantes)+(nroJornales*sueldoJornales)
    diaCuadrilla = round(sumCuadrilla/21,0) 
    valorRedondeado = math.ceil(diaCuadrilla / 100) * 100
    obj.valorCuadrilla = valorRedondeado

    obj.save()

    data = {'id':obj.id,'vCuadrilla':valorRedondeado,'rsp':"OK"}

    return JsonResponse(data)

@permission_required('Tratos.edit_trato',raise_exception=True)   
def tratos_modelos_actualizar(request):
    idTrato = request.POST['idTrato']
    modelos = request.POST['modelos']
    rsp = "OK"
    if modelos:
        json_object = json.loads(modelos)
    
    oTrato = Trato.objects.get(id=idTrato)
    rCod = ""
    canTotal = 0
    valorTotal = 0
    for vModelo in json_object:

        vUnidadModelo = UnidadModelo.objects.get(id=vModelo['idm'])        
        error = 0

        if vUnidadModelo.tipo.medicion == "CAN":
            if vModelo["cant"] == "":
                cantidad = 0
            else:
                cantidad = int(vModelo["cant"])
        else:
            cantidad = UnidadObra.objects.filter(idModelo=vUnidadModelo,estado=1).count()

        
        if vModelo["rend"] == "":
            rendimiento = 0
        else:
            rendimiento = Decimal(vModelo["rend"])
        
        if rendimiento > 0:
            valorTrato = round(oTrato.valorCuadrilla/rendimiento,0)
        else:
            valorTrato=0
            
        if vModelo["checked"] == "1" and (cantidad < 0 or rendimiento < 0):
            error = 1
            rsp = "NOK"
            
        valorTratoModelo = math.ceil(valorTrato / 100) * 100
        if error == 0:
            
            
            try:
                vTratoModelo = TratoModelo.objects.get(trato=oTrato, modelo = vUnidadModelo)
                vTratoModelo.cantidad = cantidad
                vTratoModelo.rendimiento = rendimiento
                vTratoModelo.estado = vModelo["checked"]
                vTratoModelo.valorTratoModelo = valorTratoModelo
                vTratoModelo.save()
                vModelo["cod"] = vTratoModelo.modelo.cod
                
            except ObjectDoesNotExist:
                TratoModelo.objects.create(trato=oTrato, 
                                                modelo=vUnidadModelo,
                                                cantidad=cantidad,
                                                rendimiento=rendimiento,
                                                idUsuario=request.user,

                                                valorTratoModelo = valorTratoModelo,
                                                estado=vModelo["checked"])  

            if vModelo["checked"]== "1":
                rCod += '{"cod":"'+vModelo["cod"]+'","rend":"'+str(rendimiento)+'","valorTrato":"'+str(valorTratoModelo)+'"},' 
        else:
           rCod += '{"cod":"0"},'  
           rsp = "NOK"
           break
        
        
        if vModelo["checked"]  == "1":
            canTotal += cantidad
            valorTotal += (valorTratoModelo*cantidad)
    
    
    oTrato.valorTrato = valorTotal
    oTrato.cantidad = canTotal
    oTrato.save()
    
    rCod = '['+rCod[:-1]+']' 
    data = '{"idTrato":"'+idTrato+'","models":'+rCod+',"valorTotal":"'+str(valorTotal)+'","canTotal":"'+str(canTotal)+'","rsp":"'+rsp+'"}'    

    return JsonResponse(data, safe=False)

@permission_required('Tratos.view_trato',raise_exception=True)
def trato_modelos_obtener(request):
    
    idObra = request.POST['idObra']
    idTrato = request.POST['idTrato']
    
    modelosTrato = UnidadModelo.objects.prefetch_related('tratomodelo_set').filter(idObra=idObra,estado=1)
    
    result = ""
    for modelo in modelosTrato:
        
        cantidad = UnidadObra.objects.filter(idModelo_id=modelo.id,estado=1).count()
        med = ""
        result += '{"cod":"'+modelo.cod+'","desc":"'+modelo.descripcion+'"'
        if len(modelo.tratomodelo_set.filter(trato__id=idTrato)):
            for modeloTrato in modelo.tratomodelo_set.filter(trato__id=idTrato):
                if modeloTrato.estado:
                    check = "1"
                else:
                    check = "0"
                med = modeloTrato.modelo.tipo.medicion
                if med == "CAN":
                    cantidad = modeloTrato.cantidad
                elif med == "UNI":
                    cantidad = cantidad
                    
                result += ',"rendimiento":"'+str(modeloTrato.rendimiento)+'","check":"'+check+'","cantidad":"'+str(cantidad)+'","id":"'+str(modelo.id)+'","valor":"'+str(modeloTrato.valorTratoModelo)+'","med":"'+med+'"'
        else:
            result += ',"rendimiento":"0","check":"0","cantidad":"'+str(cantidad)+'","id":"'+str(modelo.id)+'","valor":"0","med":"'+str(modelo.tipo.medicion)+'"'
        result += '},'
    
    result = "["+result[:-1]+"]"

    return JsonResponse(result, safe=False)

@permission_required('Tratos.view_trato',raise_exception=True)
def trato_partida_obtener(request):
    
    vIdObra = request.POST['idObra']
    vCodTrato = request.POST['codTrato']
    vObra = Obra.objects.get(id = vIdObra)

    try:
        trato = Trato.objects.get(cod=vCodTrato, obra = vObra,estado=1)
        partida = {'partida':trato.partida,'v':'1','max':trato.cantidad}
    except:
        partida = {'partida':'No se encontro partida. Verifique el código de trato.','v':'0','max':0}

    return JsonResponse(partida)   
    
@login_required
def obras(request):
    if request.method == "GET":
        current_url = request.path
        if "crear" in current_url:
             return render(request, 'obras_crear.html',{'title':'Obras > Crear'})
        else:
            user = request.user            
            # Obtener las obras asignadas al usuario
            obras_asignadas = ObraUsuario.objects.filter(usuario=user).values_list('obra__id', flat=True)
            obras_list = Obra.objects.filter(id__in=obras_asignadas).order_by('id')
            # Configurar la paginación
            paginator = Paginator(obras_list, 30)  # 10 informes por página
            page_number = request.GET.get('page')  # Obtener el número de página de la solicitud GET
            page_obj = paginator.get_page(page_number)  # Obtener la página actual
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                obras = [
                    {
                        'codigo': obra.cod,
                        'descripcion': obra.descripcion,  
                        'direccionCalle': obra.direccionCalle, 
                        'direccionNumero': obra.direccionNumero, 
                        'id':obra.id
                    }
                    for obra in page_obj
                ]
                
                # Si la solicitud es AJAX, devolver datos en formato JSON
                #informes = list(page_obj.object_list.values())
                return JsonResponse({
                    'obras': obras,
                    'has_previous': page_obj.has_previous(),
                    'has_next': page_obj.has_next(),
                    'num_pages': paginator.num_pages,
                    'current_page': page_obj.number,
                })    
            
            
            return render(request, 'obras.html',{'title':'Obras','obrasU':page_obj})        
            #return render(request, 'obras.html',{'title':'Obras','obrasU':obras})
        
    if request.method == "POST":
        rMethod = request.POST['mt']
        
        if rMethod == "INS":
            try:
                cod = request.POST['cod']
                descObra = request.POST['descripcion']
                direccionCalle = request.POST['direccionCalle']
                direccionNumero = request.POST['direccionNumero']
                tipoObra = request.POST['tipoObra']

                Obra.objects.create(cod=cod,descripcion=descObra,idUsuario=request.user,direccionCalle=direccionCalle,direccionNumero=direccionNumero,tipoObra=tipoObra)
                return redirect('obras')
                #return render(request,'obras.html',{'mensaje':'OK'})
            
            except IntegrityError as e:
                print(e)
                return render(request,'obras_crear.html',{
                'error':'error'+str(e)
                })
        if rMethod == "UPD":
            try:
                id = request.POST['id'] 
                
                vObra = Obra.objects.get(id=id)
                if vObra:
            
                    vObra.cod = request.POST['cod']
                    vObra.descripcion = request.POST['desc']
                    vObra.direccionCalle = request.POST['dirCalle']
                    vObra.direccionNumero = request.POST['dirNumero']
                    vObra.tipoObra = request.POST['tipo']
                    
                    vObra.save()

                    updObra = {'id':vObra.id,'descripcion':vObra.descripcion,'direccionCalle':vObra.direccionCalle,'direccionNumero':vObra.direccionNumero,'tipoObra': vObra.tipoObra,'rsp':'OK'}
                    return JsonResponse(updObra) 
                           
            except IntegrityError as e:
                print(e)
                updObra = {'id':'0','descripcion':'','direccionCalle':'','direccionNumero':'','tipoObra': '','rsp':'NOK'}
                return JsonResponse(updObra)   
                
@permission_required('Tratos.view_trato',raise_exception=True)
def obras_configuracion(request, id):   
    
    user = request.user 
    vUsuariObra = ObraUsuario.objects.filter(usuario=user, obra=id)
        
    if vUsuariObra.exists():
        
        unidadesObra = []
        totalUnidades = 0
        try:
            obra = get_object_or_404(Obra,pk=id)
            unidadesObra = UnidadObra.objects.filter(idObra=id,estado=1)      
            totalUnidades = unidadesObra.count()
        except:
            unidadesObra = []
        
        
        tratos = Trato.objects.filter(obra=id).order_by('categoria','orden')
        totalTratos = tratos.count()
        tipoUnidad = TipoUnidad.objects.filter(estado=1)
        modeloUnidad = UnidadModelo.objects.filter(idObra=id, estado=1)

        unidadesMedida = UnidadMedida.objects.all()
        
        categorias_asignadas = ObraCategoria.objects.filter(obra=obra, estado=1).values_list('categoria', flat=True)
        categorias = TratoCategoria.objects.filter(categoria__in=categorias_asignadas)

        especialidad = TratoEspecialidad.objects.all()
        capataces = TratoCapataz.objects.filter(idObra=id)
        
        
        # Configurar la paginación
        paginator = Paginator(tratos, 30) 
        page_number = request.GET.get('page')  # Obtener el número de página de la solicitud GET
        page_obj = paginator.get_page(page_number)  # Obtener la página actual
        
        
        
        return render(request, 'obras_configuracion.html',{'title':'Obras > Configuración','obra': obra,'unidadesObra':unidadesObra,'tipoUnidad':tipoUnidad,'modeloUnidad':modeloUnidad,'tratos':page_obj,'categorias':categorias,'especialidades':especialidad,'capataces':capataces,'unidadesMedida':unidadesMedida,'totalTratos':totalTratos,'totalUnidades':totalUnidades})
    else:
        return redirect('home')

@permission_required('Tratos.view_trato',raise_exception=True)
def obras_categorias_obtener(request):

    idObra = request.POST.get('idObra')
    idTrato = request.POST.get('idTrato')
    
    # Obtener todas las categorías asociadas a la obra específica
    categorias = TratoCategoria.objects.prefetch_related('trato_set').all()
    
    result = ""
    for categoria in categorias:
        result += '{"cod":"'+categoria.cod+'","desc":"'+categoria.descripcion+'"'
        
        # Verificar si la categoría está asociada a la obra y el estado
        obra_categoria = ObraCategoria.objects.filter(
            obra_id=idObra,
            categoria=categoria
        ).first()
        
        if obra_categoria:
            check = "1" if obra_categoria.estado == 1 else "0"
            result += ',"check":"'+check+'","id":"'+str(obra_categoria.categoria.id)+'"'
        else:
            result += ',"check":"0","id":"'+str(categoria.id)+'"'
        
        result += '},'
    
    result = "["+result[:-1]+"]"
    
    return JsonResponse(result, safe=False)

@permission_required('Tratos.view_trato',raise_exception=True)
def obras_categorias_actualizar(request):
    
    idObra = request.POST['idObra'] 
    user = request.user 
    vUsuariObra = ObraUsuario.objects.filter(usuario=user, obra=idObra)
        
    if vUsuariObra.exists():    
        
        categorias = request.POST['categorias']
        user = request.user 
        if categorias:
            json_object = json.loads(categorias)
        
        oObra = Obra.objects.get(id=idObra)
        rCod = ""
        for vCategoria in json_object:

            categoriaTrato = TratoCategoria.objects.get(id=vCategoria['id'])        

            try:
                vTratoModelo = ObraCategoria.objects.get(obra=oObra, categoria = categoriaTrato)
                vTratoModelo.estado = vCategoria["checked"]

                vTratoModelo.save()

            except ObjectDoesNotExist:
                ObraCategoria.objects.create(obra=oObra, 
                                            categoria=categoriaTrato,
                                            estado=vCategoria["checked"],
                                            usuario = user)  

            if vCategoria["checked"]== "1":
                rCod += '{"id":"'+vCategoria["id"]+'","desc":"'+categoriaTrato.descripcion+'"},'

        if rCod != "":    
            rCod = '['+rCod[:-1]+']' 
        else:
            rCod = "[]"
        data = '{"idObra":"'+idObra+'","categorias":'+rCod+'}'    

        return JsonResponse(data, safe=False)
    else:
        return redirect('home')

@permission_required('Tratos.view_trato',raise_exception=True)
def tiposUnidad(request):
    
    if request.method == "GET":
        tiposUnidad = TipoUnidad.objects.all()
        return render(request, 'tiposUnidad.html',{'title':'Tipos unidad','tiposUnidad':tiposUnidad})

    if request.method == "POST":
        rMethod = request.POST['mt']
        if rMethod == "INS":
            rCod = request.POST['cod'].upper()
            rDescripcion = request.POST['desc'].upper()
            rMed = request.POST['med']
            rIdObra = request.POST['idObra']
            
            user = request.user 
            vUsuariObra = ObraUsuario.objects.filter(usuario=user)
        
            if vUsuariObra.exists():
                oObra = Obra.objects.get(id=rIdObra)
                
                vUnidad = TipoUnidad.objects.filter(cod=rCod,obra=oObra,estado=1)
                if vUnidad.exists():
                    unidad = {'id':'0','desc':'rep'}
                else: 
                    obj = TipoUnidad.objects.create(
                        cod = rCod,
                        descripcion = rDescripcion,
                        medicion = rMed,
                        obra = oObra,
                        idUsuario = request.user
                    )
                    unidad = {'id':obj.id,'desc':obj.descripcion}
                    
                    
                return JsonResponse(unidad)
            else:
                unidad = {'id':'0','desc':'rep'}
        if rMethod == "DEL":
            id =  request.POST['id']
            try:
            
                vTipo = get_object_or_404(TipoUnidad, id=id,estado=1)
                vModelos = UnidadModelo.objects.filter(tipo = vTipo, estado = 1)

                if vModelos.exists():
                    tipoUnidad = {'id':'0','descripcion':''}
                else:
                    vTipo.estado = 0
                    vTipo.save()
                    tipoUnidad = {'id':vTipo.id,'descripcion':vTipo.descripcion}

            except:
                tipoUnidad = {'id':'0','descripcion':''}
            
            
                
            return JsonResponse(tipoUnidad)
              
@permission_required('Tratos.view_trato',raise_exception=True)
def modelosUnidad(request):
    
    if request.method == "POST":
        
        rMethod = request.POST['mt']
        data = []
        if rMethod == "GXT":
            rTipo = request.POST['tipo']
            rObra = request.POST['obra']
            
            try:
                oObra = Obra.objects.get(id=rObra)
                oTipo = TipoUnidad.objects.get(id=rTipo,estado=1,obra=oObra)
            
                modelosList = UnidadModelo.objects.filter(tipo=oTipo,estado=1)
                
                for modelo in modelosList:
                    data.append({
                    'id': modelo.id,
                    'descripcion': modelo.descripcion,
                })
            except TipoUnidad.DoesNotExist:
                data = []
                            
            return JsonResponse(data,safe=False)
        
        if rMethod == "INS":        
            rCod = request.POST['cod'].upper()
            rDescripcion = request.POST['desc'].upper()
            rTipo = request.POST['tipo']
            rIdObra = request.POST['idObra']

            user = request.user 
            vUsuariObra = ObraUsuario.objects.filter(usuario=user, obra=rIdObra)
        
            if vUsuariObra.exists():
                oTipo = TipoUnidad.objects.get(id=rTipo)
                oObra = Obra.objects.get(id=rIdObra)
                
                vUnidad = UnidadModelo.objects.filter(cod=rCod,idObra=oObra,tipo=oTipo,estado=1)
                if vUnidad.exists():
                    unidad = {'id':'0','desc':'rep'}
                else: 
                    obj = UnidadModelo.objects.create(
                        cod = rCod,
                        descripcion = rDescripcion,
                        idObra = oObra,
                        tipo = oTipo,
                        idUsuario = request.user
                    )
                    unidad = {'id':obj.id,'desc':obj.descripcion}                
            else: 
                unidad = {'id':'0','desc':'rep'}
            return JsonResponse(unidad)
        if rMethod == "DEL":
            id =  request.POST['id']
            try:               
                vModelo = UnidadModelo.objects.filter(id=id,estado=1)[0]
                vTratoModelo = TratoModelo.objects.filter(modelo = vModelo, estado = True)

                vUnidades = UnidadObra.objects.filter(idModelo=vModelo, estado = 1)
                if not vUnidades.exists():
                    if not vTratoModelo.exists():
                        vModelo.estado = 0
                        vModelo.save()
                        modeloUnidad = {'id':vModelo.id,'descripcion':vModelo.descripcion}
                    else:
                        modeloUnidad = {'id':'0','descripcion':''}
                else:
                    modeloUnidad = {'id':'0','descripcion':''}
            except:
                modeloUnidad = {'id':'0','descripcion':''}
            
            return JsonResponse(modeloUnidad)

@permission_required('Tratos.edit_trato',raise_exception=True)   
def unidadObra_actualizar(request):
     if request.method == "POST":
        idu = request.POST['idT']
        estado = request.POST['estado']

      
        vUnidadObra = UnidadObra.objects.get(id=idu)
        if vUnidadObra:
            
            vUnidadObra.estado = estado
            vUnidadObra.save()
            unidadObra = {'id':vUnidadObra.id,'desc':vUnidadObra.descripcion}
        else:
            unidadObra = {'id':'0','desc':'0'}      
        
        return JsonResponse(unidadObra)  

@permission_required('Tratos.view_trato',raise_exception=True)   
def unidadObra_obtener(request):
    rIdObra = request.POST['idObra']
    unidadesObra = []
    try:
        unidadesObra = UnidadObra.objects.filter(idObra=rIdObra,estado=1)      
    except:
        unidadesObra = []
    qs_json = serializers.serialize('json', unidadesObra, use_natural_foreign_keys=True, use_natural_primary_keys=True)
    return JsonResponse(qs_json,safe=False)

@permission_required('Tratos.create_trato',raise_exception=True)   
def unidadObra_crear(request):
    rCod = request.POST['cod'].upper()
    rDescripcion = request.POST['desc'].upper()
    rIdModelo = request.POST['modeloUnidad']
    rIdObra = request.POST['idObra']
    
    oModelo = UnidadModelo.objects.get(id=rIdModelo)
    oObra = Obra.objects.get(id=rIdObra)
    
    vUnidad = UnidadObra.objects.filter(cod=rCod,idObra=oObra,estado=1)
    if vUnidad.exists():
        unidad = {'id':'0','desc':'rep'}
    else: 
        obj = UnidadObra.objects.create(
            cod = rCod,
            descripcion = rDescripcion,
            idModelo = oModelo,
            idUsuario = request.user,
            idObra = oObra
        )
        unidad = {'id':obj.id,'desc':obj.descripcion}
        
        
    return JsonResponse(unidad)

@permission_required('Tratos.delete_trato',raise_exception=True)  
def unidadObra_eliminar(request):
    id =  request.POST['id']
    try:               
        vUnidad = get_object_or_404(UnidadObra, id=id,estado=1)
        vRebaje = InformeTrabajo_detalle.objects.filter(unidad = vUnidad)

        if not vRebaje.exists():
                vUnidad.estado = 0
                vUnidad.save()
                unidad = {'id':vUnidad.id,'descripcion':vUnidad.descripcion}
        else:
            unidad = {'id':'0','descripcion':''}
    except:
        unidad = {'id':'0','descripcion':''}

    return JsonResponse(unidad)

@permission_required('Tratos.edit_trato',raise_exception=True)  
@login_required
def unidadTrato_bloqueo(request):
    
    if request.method == "GET":
        unidadesBloq = []
        idTrato = request.GET.get('id', None)
        try:
            oTrato = Trato.objects.get(id=idTrato)
            unidadesBloq = TratoUnidadBloqueada.objects.filter(trato=oTrato, estado =1)      
        except:
            unidadesBloq = []
            
        result = ""
        for unidadb in unidadesBloq:
            result += '{"id":"'+str(unidadb.id)+'","motivo":"'+unidadb.motivo+'","codUnidad":"'+unidadb.unidad.cod+'","descUnidad":"'+unidadb.unidad.descripcion+'","idUnidad":"'+str(unidadb.unidad.id)+'"},'
          
        result = "["+result[:-1]+"]"
        return JsonResponse(result, safe=False)
        
    if request.method == "POST":
        
        rMethod = request.POST['mt']
        if rMethod == "INS":
            rIdTrato = request.POST['idTrato']
            rIdUnidad = request.POST['idUnidad']
            rMotivo = request.POST['motivo']
            
            oUnidad = UnidadObra.objects.get(id=rIdUnidad)
            oTrato = Trato.objects.get(id=rIdTrato)
            
            vBloqueo = TratoUnidadBloqueada.objects.filter(unidad=oUnidad,trato=oTrato,estado=1)
            if vBloqueo.exists():
                unidadBoqueada = {'id':'0','motivo':'','codUnidad':'0','descUnidad':''}
            else: 
                obj = TratoUnidadBloqueada.objects.create(
                    trato = oTrato,
                    unidad = oUnidad,
                    motivo = rMotivo,
                    idUsuario = request.user
                )
                unidadBoqueada = {'id':obj.id,'motivo':obj.motivo,'codUnidad':oUnidad.cod,'descUnidad':oUnidad.descripcion}
                
                
            return JsonResponse(unidadBoqueada)
        if rMethod == "DEL":
            rIdBloqueo = request.POST['idbloqueo']
            try:
                vBloqueo = TratoUnidadBloqueada.objects.get(id=rIdBloqueo)
            except:
                vBloqueo = None
            
            if vBloqueo != None:
                
                vBloqueo.estado = 0
                vBloqueo.save()
                
                unidadBoqueada = {'id':vBloqueo.id,'motivo':vBloqueo.motivo,'codUnidad':vBloqueo.unidad.cod,'descUnidad':vBloqueo.unidad.descripcion,'UnID': vBloqueo.unidad.id}
            else:
                unidadBoqueada = {'id':'0','motivo':'','codUnidad':'0','descUnidad':'','unID':0}
                
            return JsonResponse(unidadBoqueada)
    
    
@permission_required('Tratos.create_trato',raise_exception=True)      
def item_crear(request):
    if request.method == "POST":
        
        user = request.user
        item = request.POST['item']
        valor = request.POST['valor'].strip().upper()
        idObra = request.POST['idObra']
        
        vObra = Obra.objects.filter(id=idObra)
        vUsuariObra = ObraUsuario.objects.filter(usuario=user, obra=vObra[0])
        
        if vUsuariObra.exists():
            
            if item == "E":
                vReg = TratoEspecialidad.objects.filter(descripcion=valor).exists()
                if not vReg:
                    obj = TratoEspecialidad.objects.create(
                        cod = "",
                        descripcion=valor,
                        idUsuario=user
                    )
                    item = {'id':obj.id,'desc':obj.descripcion}
                else:
                    item = {'id':'0','desc':''}   
            elif item == "C":
                arValor = valor.split("|")
                vReg = TratoCapataz.objects.filter(nombre=arValor[0].strip(),apellido=arValor[1].strip()).exists()
                if not vReg:
                    nombre = arValor[0]
                    apellido = arValor[1]
                    obj = TratoCapataz.objects.create(
                        nombre = nombre,
                        apellido=apellido,
                        idUsuario=user,
                        idObra=vObra[0]
                    )
                    item = {'id':obj.id,'desc':obj.nombre+' '+obj.apellido}        
                else:
                    item = {'id':'0','desc':''}   
                        
            elif item == "U":
                vReg = UnidadMedida.objects.filter(descripcion=valor).exists()
                if not vReg:
                    obj = UnidadMedida.objects.create(
                        cod = "",
                        descripcion=valor,
                        idUsuario=user
                    )
                    item = {'id':obj.id,'desc':obj.descripcion}
                else:
                    item = {'id':'0','desc':''} 
            else:
                item = {'id':'0','desc':''}  
                
        return JsonResponse(item)

def signout(request):
    logout(request)
    return redirect('signin')


def signin(request):
        
    if request.method == 'GET':
        return render(request,'signin.html',{
            'form':AuthenticationForm
        })
    else:
        user = authenticate(request, 
                     username=request.POST["username"],
                     password=request.POST["password"])
        if user is None:
            return render(request,'signin.html',{
            'form':AuthenticationForm,
            'error':'Usuario o contraseña incorrecto'
            })
        else:
            login(request,user)
            return redirect('home')
        
        
def check_session(request):
    if request.user.is_authenticated:
        return JsonResponse({'session_active': True})
    else:
        return JsonResponse({'session_active': False})