from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from .Models.mInformeTrabajo import InformeTrabajo
from .Models.mInformeTrabajo_estado import InformeTrabajo_estado
from .Models.mInformeTrabajo_detalle import InformeTrabajo_detalle
from .Models.mInformeTrabajo_cuadrilla import InformeTrabajo_cuadrilla
from Tratos.Models import Trato, TratoCategoria, UnidadObra, Obra, TratoEspecialidad, TratoCapataz, UnidadMedida, TratoUnidadBloqueada
from decimal import Decimal
from django.core.exceptions import ValidationError
import json
from django.http import JsonResponse
from TratosPY.utils import permission_required_custom
from Tratos.Models.mTratoModelo import TratoModelo
from Tratos.Models.mObraUsuario import ObraUsuario
from Tratos.Models.mObra import Obra
from django.db.models import Q, Sum, Max
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist


@permission_required_custom('Tratos.view_informeTrabajo', redirect_to='home')
def tratos(request):
    user = request.user
    # Obtener las obras asignadas al usuario
    obras_asignadas = ObraUsuario.objects.filter(usuario=user).values_list('obra', flat=True)
    informe_trabajo_list = InformeTrabajo.objects.filter(obra__in=obras_asignadas).order_by('-orden')
    estados_list = InformeTrabajo_estado.objects.all()
    categorias_list = TratoCategoria.objects.all()
    
    
    # Configurar la paginación
    paginator = Paginator(informe_trabajo_list, 30)  # 10 informes por página
    page_number = request.GET.get('page')  # Obtener el número de página de la solicitud GET
    page_obj = paginator.get_page(page_number)  # Obtener la página actual
    
    
    
    return render(request, 'tratos.html',{'title':'Tratos','informesTrabajo':page_obj,'categorias':categorias_list,'estados':estados_list})

@permission_required_custom('Tratos.view_informeTrabajo', redirect_to='home')
def informeTrabajo_buscar(request):

    folio = request.POST['folio']
    categoria = request.POST['categoria']
    fechaInicio = request.POST['fechaInicio']
    fechatermino = request.POST['fechaTermino']
    codTrato = request.POST['codTrato']
    partida = request.POST['partida']
    trabajador = request.POST['trabajador']
    estado = request.POST['estado']
    rPage = request.POST['page']

    filters = Q()
    user = request.user
    obras_asignadas = ObraUsuario.objects.filter(usuario=user).values_list('obra', flat=True)
    filters = Q(obra_id__in=obras_asignadas)
        
    if folio:
        filters &= Q(cod__icontains=folio)
    if categoria:
        filters &= Q(categoria__descripcion__icontains=categoria)
    if fechaInicio:
        filters &= Q(fecha__gte=fechaInicio)
    if fechatermino:
        filters &= Q(fecha__lte=fechatermino)
    if codTrato:
        filters &= Q(informetrabajo_detalle__trato__cod__icontains=codTrato)
    if trabajador:
        filters &= Q(informetrabajo_cuadrilla__nomTrab__icontains=trabajador)
    if partida:
        filters &= Q(informetrabajo_detalle__trato__partida__icontains=partida)
    if estado:
        filters &= Q(idEstado=estado)
    

    
    
    informe_trabajo_list = InformeTrabajo.objects.filter(filters).distinct().order_by('id')

    paginator = Paginator(informe_trabajo_list, 30) 
    page_obj = paginator.get_page(rPage)  # Obtener la página actual   
    
    informes = []
    
    for informe in page_obj:
        
        rebajes = InformeTrabajo_detalle.objects.filter(itrabajo=informe)
        tratos_codigos = [rebaje.trato.cod for rebaje in rebajes]
        tratos_concatenados = ', '.join(tratos_codigos)

        informes.append({
                'folio': informe.folio,
                'obra': informe.obra.descripcion,  
                'fechaInicio': informe.fechaInicio.strftime('%d-%m-%Y'), 
                'total': informe.total,  
                'estado': informe.idEstado.descripcion,  
                'id':informe.id,
                'tratosRebajados':tratos_concatenados
        })
    
    return JsonResponse({
        'informes': informes,
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'num_pages': paginator.num_pages,
        'current_page': page_obj.number,
    })    

@permission_required_custom('Tratos.create_informeTrabajo', redirect_to='home')
def informeTrabajo_cabecera_guardar(request):
    
    vObra = request.POST['idObra']
    user = request.user 
    vUsuariObra = ObraUsuario.objects.filter(usuario=user, obra=vObra)
        
    if vUsuariObra.exists():
        
        vFolio = request.POST['vFolio']
        vFechaInicio = request.POST['vFechaInicio']
        vFechaTermino = request.POST['vFechatermino']
        vIdInforme = request.POST['vIdInforme']
        
        #max_order = InformeTrabajo.objects.aggregate(Max('orden'))['orden__max'] or 0   
           

        oObra = get_object_or_404(Obra,id=vObra)
        estado = get_object_or_404(InformeTrabajo_estado, id=1)
        if vIdInforme == '':
            
            try:
                ultimoInforme = InformeTrabajo.objects.filter(obra=oObra).latest('fechaCreacion')
                if ultimoInforme.folio is not None and ultimoInforme.folio.strip() != "":
                    maxId = int(ultimoInforme.folio.split("-")[1])
                else:
                    maxId=0
            except ObjectDoesNotExist:
                maxId = 0

            fecha_actual = datetime.now()
            # Formatear la fecha en "MMYY"
            vFolio = fecha_actual.strftime("%m%y")+"-"+str(maxId+1)
            
            try:

                vInformeTrabajo = InformeTrabajo.objects.filter(obra=oObra,idEstado=estado,folio=vFolio)
                
                if not vInformeTrabajo.exists():
                    obj = InformeTrabajo.objects.create(obra=oObra,
                                                folio=vFolio,
                                                fechaInicio=vFechaInicio,
                                                fechaTermino=vFechaTermino,
                                                idUsuario=request.user,
                                                idEstado = estado,
                                                total = 0
                                                )
                    cabecera = {'id':obj.id,'folio':obj.folio,'fechaIngreso':obj.fechaCreacion.strftime('%d-%m-%Y'),'msj':'OK'}
                else:
                    cabecera = {'id':'0','folio':'rep','msj':'NOK'}
            except ValidationError as e:
                print("Error de validación al crear el objeto:", e)
                
        else:
            vInformeTrabajo = InformeTrabajo.objects.filter(obra=oObra,idEstado=estado,folio=vFolio).exclude(id=vIdInforme)
            if not vInformeTrabajo.exists():
                obj = InformeTrabajo.objects.get(id=vIdInforme)
                obj.folio=vFolio
                obj.fechaInicio=vFechaInicio
                obj.fechaTermino=vFechaTermino
                obj.save()
                
                cabecera = {'id':obj.id,'folio':obj.folio,'fechaIngreso':obj.fechaCreacion.strftime('%d-%m-%Y'),'msj':'OK'}
            else:
                cabecera = {'id':'0','folio':'rep','msj':'NOK'}
                
        return JsonResponse(cabecera)
    else:
        cabecera = {'id':'0','folio':'rep'}
        return JsonResponse(cabecera)
        
@permission_required_custom('Tratos.create_informeTrabajo', redirect_to='home')
def informeTrabajo_detalle_guardar(request):
        
    vIdObra = request.POST['idObra']    
    user = request.user 
    vUsuariObra = ObraUsuario.objects.filter(usuario=user, obra=vIdObra)
        
    if vUsuariObra.exists():    
        vItrabajo = request.POST['idInforme']
        vData = request.POST['data']

        oObra = Obra.objects.get(id=vIdObra)
        vError = ""
        idr = 0
        jdata = json.loads(vData) 
        for row in jdata: 
            oUnidad = UnidadObra.objects.get(cod=row["codUnidad"],idObra = oObra,estado=1)        
            medicion = oUnidad.idModelo.tipo.medicion
            oInforme = InformeTrabajo.objects.get(id=vItrabajo)
            oTrato = Trato.objects.get(cod=row["codTrato"], obra=oObra)
            
            #OBTIENE REBAJES EN OTROS INFORMES DE TRABAJO PARA EL MISMO TRATO/UNIDAD
            if row["id"] == "P":
                rebajes = InformeTrabajo_detalle.objects.filter(unidad=oUnidad,itrabajo__obra=oObra,trato=oTrato).exclude(trato=oTrato,unidad=oUnidad,itrabajo=oInforme)
            else:             
                rebajes = InformeTrabajo_detalle.objects.filter(unidad=oUnidad,itrabajo__obra=oObra,trato=oTrato).exclude(id=row["id"])
            
            #VALIDA MEDICION // PUEDE SER POR UNIDAD O CANTIDAD, SI ES UNIDAD VALIDA EL % DE AVANCE
            if medicion =="UNI":
                if Decimal(row["cantidad"]) > 1:
                    vError += '{"unidad":"'+row["codUnidad"]+'","trato":"'+row["codTrato"]+'", "folio":"0","medicion":"uni","err":"Cantidad no puede ser mayor a 1"},'
                    #break
                
                avanzado = 0
                if rebajes.exists():
                    avanzado = rebajes.aggregate(Sum('avance'))
                    vPorcentaje = avanzado['avance__sum'] + Decimal(row["porcentaje"])
                    
                    if vPorcentaje > 100:
                        avanDisp = 100-avanzado['avance__sum']
                        folios_concatenated = '<br /> '.join([str(detalle.itrabajo.folio) for detalle in rebajes])
                        vError += '{"unidad":"'+row["codUnidad"]+'","trato":"'+row["codTrato"]+'", "folio":"'+folios_concatenated+'","medicion":"uni","disp":"'+str(int(avanDisp))+'","err":"% de avance no puede ser mayor a 100"},'
                        #break
                else:
                    vPorcentaje = Decimal(row["porcentaje"])
                    if vPorcentaje > 100:
                        #avanDisp = 100-avanzado['avance__sum']
                        avanDisp = vPorcentaje
                        vError += '{"unidad":"'+row["codUnidad"]+'","trato":"'+row["codTrato"]+'","medicion":"uni","disp":"'+str(int(avanDisp))+'","err":"% No puede ser Mayor a 100"},'
                        #break
                        
            elif medicion == "CAN":
                
                cantidad = 0
                if rebajes.exists():
                    cantidad = rebajes.aggregate(Sum('cantidad'))
                    vCantidad = cantidad['cantidad__sum'] + Decimal(row["cantidad"])
                    
                    if vCantidad > rebajes[0].trato.cantidad:
                        cantDisp = rebajes[0].trato.cantidad-cantidad['cantidad__sum']
                        folios_concatenated = '<br /> '.join([str(detalle.itrabajo.folio) for detalle in rebajes])
                        vError += '{"unidad":"'+row["codUnidad"]+'","trato":"'+row["codTrato"]+'", "folio":"'+rebajes[0].itrabajo.folio+'","medicion":"can","max":"'+str(int(rebajes[0].trato.cantidad))+'","disp":"'+str(cantDisp)+'","err":"Cantidad no puede ser mayor al máximo disponible"},'
                else:
                    trato = Trato.objects.get(cod=row["codTrato"])
                    cantidad = Decimal(row["cantidad"])
                    if cantidad > trato.cantidad:
                        cantDisp = trato.cantidad-cantidad['cantidad__sum']
                        vError += '{"unidad":"'+row["codUnidad"]+'","trato":"'+row["codTrato"]+'","medicion":"can","max":"'+str(trato.cantidad)+'","disp":"'+str(int(cantDisp))+'","err":"Cantidad no puede ser mayor al máximo disponible"},'
        sumtotal = 0
        if vError == "":
            for row in jdata: 
                oInforme = InformeTrabajo.objects.get(id=vItrabajo)
                oTrato = Trato.objects.get(cod=row["codTrato"],obra=oObra)
                oUnidad = UnidadObra.objects.get(cod=row["codUnidad"],idObra = oObra,estado=1)
                oTratoModelo = TratoModelo.objects.get(trato=oTrato,modelo=oUnidad.idModelo)
                idReg = row["id"]
                med = row["med"]
                

                valorTotal = 0
                if med == "UNI":
                    valorTotal = (oTratoModelo.valorTratoModelo / 100) * float(row["porcentaje"])
                    valorTotal = round(valorTotal / 10) * 10  # Redondear a la decima más cercana
                if med == "CAN":
                    #valorTotal = (oTratoModelo.valorTratoModelo / oTratoModelo.cantidad) * float(row["cantidad"])
                    valorTotal = (oTratoModelo.valorTratoModelo) * float(row["cantidad"])
                    valorTotal = round(valorTotal / 10) * 10  # Redondear a la decima más cercana            
            
            
                if idReg == "0":
                    obj = InformeTrabajo_detalle.objects.create(itrabajo=oInforme,
                                            trato=oTrato,
                                            unidad=oUnidad,
                                            cantidad=row["cantidad"],
                                            avance=row["porcentaje"],
                                            idUsuario=request.user,
                                            total = valorTotal
                                            )
                else:
                    if idReg == "P":
                        obj = InformeTrabajo_detalle.objects.get(trato=oTrato,unidad=oUnidad,itrabajo=oInforme)
                    else:
                        obj = InformeTrabajo_detalle.objects.get(id=idReg)
                        
                    obj.cantidad = row["cantidad"]
                    obj.avance = row["porcentaje"]
                    obj.unidad = oUnidad
                    obj.total = valorTotal
                    obj.save()  
                
                sumtotal += obj.total
                idr = obj.id
            
            it = InformeTrabajo.objects.get(id=vItrabajo)   
            it.total = sumtotal
            it.save()
            
        else:
            vError = vError[:-1]

        detalle = {'id':idr,'idIt':vItrabajo,'msj':'['+vError+']','sumTotal':sumtotal}
        return JsonResponse(detalle)
    else:
        detalle = {'id':0,'idIt':0,'msj':'[]','sumTotal':0}
        return JsonResponse(detalle)

@permission_required_custom('Tratos.delete_informeTrabajo', redirect_to='home')
def informeTrabajo_detalle_eliminar(request):
    try:
        vIdetalle = int(request.POST['idInforme'])

        iDetalle = InformeTrabajo_detalle.objects.get(id=vIdetalle)
        detalle = {'id':iDetalle.id,'idIt':vIdetalle,'totalDetalle':iDetalle.total}
        iDetalle.delete()
        
    except:
        detalle = {'id':0,'idIt':0,'totalDetalle':0}

    return JsonResponse(detalle)

@permission_required_custom('Tratos.create_informeTrabajo', redirect_to='home')
def informeTrabajo_cuadrilla_guardar(request):
    
    vItrabajo = request.POST['idInforme']
    vIdObra = request.POST['idObra']
    
    user = request.user 
    vUsuariObra = ObraUsuario.objects.filter(usuario=user, obra=vIdObra)
    if vUsuariObra.exists():   
        vData = request.POST['data']

        oObra = Obra.objects.get(id=vIdObra)

        jdata = json.loads(vData) 
        totalCuadrilla = 0
        for row in jdata: 
            oInforme = InformeTrabajo.objects.get(id=vItrabajo)
            idReg = int(row["id"])
            
            if idReg == 0:
                obj = InformeTrabajo_cuadrilla.objects.create(itrabajo=oInforme,
                                        codTalana=row["codTalana"],
                                        nomTrab=row["nomtrab"],
                                        lunTrab=row["luntrab"],
                                        marTrab=row["martrab"],
                                        mieTrab=row["mietrab"],
                                        jueTrab=row["juetrab"],
                                        vieTrab=row["vietrab"],
                                        totalDias=row["totalDias"],
                                        valorDia=row["valorDia"],
                                        total=row["total"],
                                        idUsuario=request.user,
                                        )
                
            elif idReg > 0:
                obj = InformeTrabajo_cuadrilla.objects.get(id=idReg)
                obj.nomTrab=row["nomtrab"]
                obj.lunTrab=row["luntrab"]
                obj.marTrab=row["martrab"]
                obj.mieTrab=row["mietrab"]
                obj.jueTrab=row["juetrab"]
                obj.vieTrab=row["vietrab"]
                obj.totalDias=row["totalDias"]
                obj.valorDia=row["valorDia"]
                obj.total=row["total"]
                obj.idUsuario=request.user
                obj.save()
                
            totalCuadrilla+=Decimal(row["total"])
            
        detalle = {'id':obj.id,'idIt':vItrabajo,'totalCuadrilla':totalCuadrilla}

        return JsonResponse(detalle)
    else:
        detalle = {'id':0,'idIt':0}
        return JsonResponse(detalle)

@permission_required_custom('Tratos.delete_informeTrabajo', redirect_to='home')
def informeTrabajo_cuadrilla_eliminar(request):
    try:
        viCuadrilla = int(request.POST['idInforme'])

        iCuadrilla = InformeTrabajo_cuadrilla.objects.get(id=viCuadrilla)
        detalle = {'id':iCuadrilla.id,'idIt':viCuadrilla,'total':iCuadrilla.total}
        iCuadrilla.delete()
        
    except:
        detalle = {'id':0,'idIt':0,'total':0}

    return JsonResponse(detalle)

@permission_required_custom('Tratos.edit_informeTrabajo', redirect_to='home')
def informeTrabajo_finalizar(request):
    try:
        
        oEstado = InformeTrabajo_estado.objects.get(cod="FIN")
        vIdInforme = request.POST['idInforme']
        iTrabajo = InformeTrabajo.objects.get(id=vIdInforme)
        
        idDetalle = InformeTrabajo_detalle.objects.filter(itrabajo = iTrabajo)
        totalRebaje = idDetalle.aggregate(Sum('total'))['total__sum']
        
        iCuadrilla = InformeTrabajo_cuadrilla.objects.filter(itrabajo = iTrabajo)
        totalCuadrilla = iCuadrilla.aggregate(Sum('total'))['total__sum']
        
        if totalRebaje == totalCuadrilla:
            iTrabajo.idEstado = oEstado
            iTrabajo.save()
            
            detalle = {'id':iTrabajo.id,'idIt':vIdInforme}   
        else:
            detalle = {'id':'-1','idIt':'-1'}

    except:
        detalle = {'id':0,'idIt':0}

    return JsonResponse(detalle)

@permission_required_custom('Tratos.view_informeTrabajo', redirect_to='home')
def informeTrabajo_ver(request,vid):
    
    if request.method == "GET":
        
        if vid != None:
            user = request.user
            itCabecera = InformeTrabajo.objects.get(id=vid)
            idDetalle = InformeTrabajo_detalle.objects.filter(itrabajo = itCabecera)
            totalRebaje = idDetalle.aggregate(Sum('total'))['total__sum']
            totalRebaje = totalRebaje if totalRebaje is not None else 0
            
            iCuadrilla = InformeTrabajo_cuadrilla.objects.filter(itrabajo = itCabecera)
            totalCuadrilla = iCuadrilla.aggregate(Sum('total'))['total__sum']
            totalCuadrilla = totalCuadrilla if totalCuadrilla is not None else 0
            obras = ObraUsuario.objects.filter(usuario=user).select_related('obra')
            
            obra = obras.exclude(obra__cod=999).first()
            obraSelect = obra.obra.id
            unidadesList = UnidadObra.objects.filter(idObra=obra.obra)
                
        else:
            itCabecera = None 
            idDetalle = None
            iCuadrilla = None
            obras = None
            obraSelect = None
            
        return render(request, './informeTrabajo_crear.html',{'title':'Trato > ver: Folio '+ itCabecera.folio ,'obrasU':obras,'itCabecera':itCabecera,'idDetalle':idDetalle,'iCuadrilla':iCuadrilla,'totalRebaje':totalRebaje,'totalCuadrilla':totalCuadrilla,'obraSelect':obraSelect,'unidadesList':unidadesList})
    
@permission_required_custom('Tratos.create_informeTrabajo', redirect_to='home')
def informeTrabajo_crear(request):
    
    if request.method == "GET":
        
        itCabecera = None 
        user = request.user
        obras = ObraUsuario.objects.filter(usuario=user).select_related('obra')
        obra = obras.exclude(obra__cod=999).first()
        obraSelect = obra.obra.id
        unidadesList = UnidadObra.objects.filter(idObra=obra.obra)
        return render(request, 'informeTrabajo_crear.html',{'title':'Trato > crear','obrasU':obras,'itCabecera':itCabecera,'obraSelect':obraSelect,'unidadesList':unidadesList})
    
    elif request.method == "POST":
        
        rIdObra = request.POST['idObra']
        user = request.user 
        vUsuariObra = ObraUsuario.objects.filter(usuario=user, obra=rIdObra)
            
        if vUsuariObra.exists():              
            icod = request.POST['cod']
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

            vTrato = Trato.objects.filter(cod=icod).exists()
            if vTrato:
                unidad = {'id':'0','desc':'rep'}
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
            unidad = {'id':obj.id,'desc':obj.partida}

            return JsonResponse(unidad)
        else:
            unidad = {'id':0,'desc':0}
            return JsonResponse(unidad)
        
@permission_required_custom('Tratos.view_informeTrabajo', redirect_to='home')
def unidadTrato_obtener(request):
    
    vIdObra = request.POST['idObra']
    user = request.user 
    vUsuariObra = ObraUsuario.objects.filter(usuario=user, obra=vIdObra)
        
    if vUsuariObra.exists():
        
        vCodTrato = request.POST['codTrato'].upper()
        oObra = Obra.objects.get(id=vIdObra)
        oTrato = Trato.objects.get(cod=vCodTrato,estado=1,obra=oObra)

        
        modelosTratoList = TratoModelo.objects.filter(trato=oTrato, estado=True)

        # Obtener los IDs de los modelos presentes en modelosTratoList
        modelos_ids = modelosTratoList.values_list('modelo__id', flat=True)
        unidadesList = UnidadObra.objects.filter(idObra=oObra,idModelo__id__in=modelos_ids)
        # Crear un diccionario para un acceso rápido a los objetos TratoModelo por modelo ID
        modelo_trato_dict = {modelo.modelo.id: str(modelo.valorTratoModelo)+"|"+str(modelo.cantidad) for modelo in modelosTratoList}

        # Crear un listado en formato JSON
        unidades_json = []
        for unidad in unidadesList:
            
            #vUnidad = 0 
            avanzado = 0
            rebajesList = InformeTrabajo_detalle.objects.filter(unidad=unidad,trato=oTrato)
            
            medicion = unidad.idModelo.tipo.medicion
            valor_trato = modelo_trato_dict.get(unidad.idModelo.id, 0)  # Obtiene el valorTrato, 0 si no existe
            cant_trato = valor_trato.split("|")[1]
            
            disp = 0
            if medicion == "UNI":
                avanzado = rebajesList.aggregate(Sum('avance'))['avance__sum'] or 0
                disp = 100 - avanzado
                #vUnidad = 1 if avanzado < 100 else 0
            if medicion == "CAN":
                avanzado = rebajesList.aggregate(Sum('cantidad'))['cantidad__sum'] or 0   
                disp = int(cant_trato) - avanzado
                #vUnidad = 1 if avanzado < int(cant_trato) else 0 

            #if vUnidad == 1: 
                
            unidad_json = {
                'cod': unidad.cod,
                'descripcion': unidad.descripcion,
                #'estado': '1' if unidad.idModelo.id in modelos_ids else '0',
                'estado': '1' if disp > 0 else '0',
                'valorTrato': valor_trato.split("|")[0]+"|"+medicion+"|"+str(disp),
                'disp': str(disp)
            }
            unidades_json.append(unidad_json)

        # Retornar el JSON con los datos
        return JsonResponse({'unidades': unidades_json})
        
        