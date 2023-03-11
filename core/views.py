import os

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics

from .models import books, categoria, vigencia, DetalleVigencia, penalidad, DetallePenalidad,Veterinario
from django.db.models import Avg,Sum,Max,Min,Count
from rest_framework.views import APIView
import json

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
#para el combobox
from selenium.webdriver.support.ui import Select

import csv
from django.conf import settings

from PIL import Image
class ApiCategorias(APIView):
    def get(self,request,format=None):
        category=categoria.objects.all()
        listacategorias=[]
        for categorya in category:
            newcategoria={
                'id':categorya.id,
                'name': categorya.name,
            }
            listacategorias.append(newcategoria)
        dump=listacategorias
        rpta=json.dumps(dump)
        return HttpResponse(rpta,content_type='Application/json')

# repaso de ORM de Django
def Api_Ore(request):
    template_name='filter.html'
    #muesta todos los libros
    books2=books.objects.all()
    book2=books.objects.get(pk=8)
    # filtra los libros que su titulo sea igual a python o a cualquier campo del modelo
    #resfilter=books.object.filter(title='python')
    resfilter2 = books.objects.filter(title__contains='a')
    # agrega las condiciones del where como si fueran parametros
    resfilter3 = books.objects.filter(title__contains='a',state=True)
    # gt > mas grande que
    # gte >= mayor igual que
    # lt < menor que
    # lte <= menor igual que
    resfilter4 = books.objects.filter(price__gt=70)
    resfilter5 = books.objects.filter(price__gte=70)
    resfilter6 = books.objects.filter(price__lt=70)
    resfilter7 = books.objects.filter(price__lte=70)

    resfilter7 = books.objects.filter(title__startswith='r')
    #para usar Avg,Sum,Max,Min,Count en una consulta de all()
    resfilter8=books.objects.all().aggregate(Sum('price'))
    resfilter9 = books.objects.all().aggregate(Max('price'))
    context={
        'books':books2,
        'book': book2,
        'resfilter2': resfilter2,
        'resfilter3': resfilter3,
        'resfilter4': resfilter4,
        'resfilter5': resfilter5,
        'resfilter6': resfilter6,
        'resfilter7': resfilter7,
        'resfilter8': resfilter8,
        'resfilter9':resfilter9,
    }

    return render(request,template_name,context)

class ApiProductos(APIView):
    def get(self,request,format=None):
        booksall=books.objects.all()
        listalibros = []
        for book in booksall:
            newbook = {
                'id': book.id,
                'name': book.title,
                'Author': book.author,
                'Price': str(book.price)
            }
            listalibros.append(newbook)
        dump = listalibros
        rpta = json.dumps(dump)
        return HttpResponse(rpta, content_type='Application/json')

class ApiProductosDetalle(APIView):
    def get(self,request,format=None):
        product=request.data['product']
        print('pido el libro')

        listalibros = []
        if books.objects.filter(id=product).exists():
            book = books.objects.get(id=product)
            print('entro')
            newbook = {
                'id': book.id,
                'name': book.title,
                'Author': book.author,
                'Price': str(book.price)
            }
            listalibros.append(newbook)
            dump = listalibros
            rpta = json.dumps(dump)
        else:
            print('else')
            dump={'detail':'No existe data que mostrar'}
            rpta = json.dumps(dump)
        return HttpResponse(rpta, content_type='Application/json')

class ApiCategoriaProducto(APIView):
    def get(self,request,format=None):
        categoria=request.data['categoria']
        booksall = books.objects.filter(category_id=categoria)
        listalibros = []
        for book in booksall:
            newbook = {
                'id': book.id,
                'name': book.title,
                'Author': book.author,
                'Price': str(book.price)
            }
            listalibros.append(newbook)
        dump = listalibros
        rpta = json.dumps(dump)
        return HttpResponse(rpta, content_type='Application/json')

class registerProducto(generics.CreateAPIView):
    def post(self,request,format=None):
        title = request.data['title']
        price = request.data['price']
        author = request.data['author']
        img = request.data['img']
        category=request.data['category']
        newbook=books.objects.create(title=title,price=price,author=author,picture=img,state=True,category_id=category)
        data={'detail':'libro guardado con exito '}
        rpta=json.dumps(data)
        return HttpResponse(rpta,content_type='application/json')

class buscaData(generics.CreateAPIView):
    def post(self,request,format=None):
        title = request.data['title']
        try:
            padron = cargaDatos()
            for row in padron:
                codigominero = row
                datosvigencia(row)
                global GGvigenciaDP
                GGvigenciaDP = [[]]
                global GGvigenciaDV
                GGvigenciaDV = [[]]
                global GGvigencia
                GGvigencia = [[]]
                global GGPenalidad
                GGPenalidad = [[]]
                codigominero = ""
            #guardar()

            # nuevo = input("sadsadsadsada")
        except ValueError as err:
            #guardar()
            print(err)
        data={'detail':'libro guardado con exito '}
        rpta=json.dumps(data)
        return HttpResponse(rpta,content_type='application/json')

def cargaDatos():
    base_dir = settings.MEDIA_ROOT
    my_file = os.path.join(base_dir, str('padronminero.csv'))
    with open('padronminero.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        datos = []
        for row in reader:
            datos.append(row['codigo'])
    print("carga de datos lista")
    return datos

def datosvigencia(codigoMD):
    print("carga datos dddd" + codigoMD)
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get('https://portal.ingemmet.gob.pe/web/guest/depositos-de-vigencia-y/o-penalidad')

    codigo_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "//input[@name='_igmdepositovigencia_WAR_igmsidemcatportlet_codigo']")))

    # codigoMD = "01004279X01"
    codigo_input.send_keys(codigoMD)

    buscar_button = WebDriverWait(driver, 80).until(EC.presence_of_element_located(
        (By.XPATH, "//input[@name='_igmdepositovigencia_WAR_igmsidemcatportlet_buscar_penalidad']")))
    buscar_button.click()
    time.sleep(5)
    nombre_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "//input[@name='_igmdepositovigencia_WAR_igmsidemcatportlet_nombre']")))
    print('hola')
    print(nombre_input.text)

    vigencia_dates = WebDriverWait(driver, 55).until(
        EC.presence_of_element_located((By.XPATH, "//table[@id='grid_vigencia']"))
    )
    # Accedemos a cada fila (que es una lista)
    event_td = vigencia_dates.find_elements(By.XPATH, "//td[@role='gridcell']/tbody/tr/td")
    # tabla de vigencia
    rows = driver.find_elements(By.XPATH, "//table[@id='grid_vigencia']/tbody/tr")
    cells = driver.find_elements(By.XPATH, "//table[@id='grid_vigencia']/tbody/tr/td")
    print(len(cells))
    print(len(rows))
    codigos = [element.text for element in cells]
    # print(codigos)
    matriz_vigencia = []
    data_vigencia = []
    contador = 0
    for p in cells:
        data_vigencia.append(p.text)
        contador = contador + 1
        if (contador % 7 == 0):
            matriz_vigencia.append(data_vigencia)
            data_vigencia = []

    DDvigencia = [["año", "Calificación", "Hectareas", "Deuda", "Deposito", "Saldo", "Devolución", "MD"]]
    for i in range(len(matriz_vigencia)):
        print(matriz_vigencia[i])
        aux = matriz_vigencia[i]
        if(aux[0]):
            vigenciadata = vigencia.objects.create(anio=aux[0], calificacion=aux[1], has=aux[2], deuda=aux[3], deposito=aux[4],saldo=aux[5] ,devolucion=aux[6],dm=codigoMD)
        aux.append(codigoMD)
        print(type(aux))
        DDvigencia.append(aux)
    print(type(DDvigencia))
    # tabla de Detalle pagos de vigencia
    rowsDV = driver.find_elements(By.XPATH, "//table[@id='grid_vigencia_det']/tbody/tr")
    cellsDV = driver.find_elements(By.XPATH, "//table[@id='grid_vigencia_det']/tbody/tr/td")
    print(len(cellsDV))
    print(len(rowsDV))
    codigosDV = [element.text for element in cellsDV]
    # print(codigos)
    matriz_vigenciaDV = []
    data_vigenciaDV = []
    contadorDV = 0
    for p in cellsDV:
        data_vigenciaDV.append(p.text)
        contadorDV = contadorDV + 1
        if (contadorDV % 6 == 0):
            matriz_vigenciaDV.append(data_vigenciaDV)
            data_vigenciaDV = []

    DDvigenciaDV = [["año", "Banco", "Boleta", "Fecha de deposito", "Moneda", "Deposito", "MD"]]
    for i in range(len(matriz_vigenciaDV)):
        print(matriz_vigenciaDV[i])
        auxDV = matriz_vigenciaDV[i]
        if (auxDV[0]):
            detallevigencia = DetalleVigencia.objects.create(anio=auxDV[0], banco=auxDV[1], boleta=auxDV[2], fecha=auxDV[3],
                                               moneda=auxDV[4], deposito=auxDV[5], dm=codigoMD)
        auxDV.append(codigoMD)
        print(type(auxDV))
        DDvigenciaDV.append(auxDV)
    print(type(DDvigenciaDV))

    # tabla de Penalidad
    rowsP = driver.find_elements(By.XPATH, "//table[@id='grid_penalidad']/tbody/tr")
    cellsP = driver.find_elements(By.XPATH, "//table[@id='grid_penalidad']/tbody/tr/td")
    print(len(cellsP))
    print(len(rowsP))
    codigos = [element.text for element in cellsP]
    # print(codigos)
    matriz_vigenciaP = []
    data_vigenciaP = []
    contadorP = 0
    for p in cellsP:
        data_vigenciaP.append(p.text)
        contadorP = contadorP + 1
        if (contadorP % 7 == 0):
            matriz_vigenciaP.append(data_vigenciaP)
            data_vigenciaP = []

    DDvigenciaP = [["año", "Calificación", "Hectareas", "Deuda", "Deposito", "Saldo", "Devolución", "MD"]]
    for i in range(len(matriz_vigenciaP)):
        print(matriz_vigenciaP[i])
        auxP = matriz_vigenciaP[i]
        if (auxP[0]):
            Penalidad = penalidad.objects.create(anio=auxP[0], calificacion=auxP[1], has=auxP[2], deuda=auxP[3],
                                               deposito=auxP[4], saldo=auxP[5], devolucion=auxP[6], dm=codigoMD)
        auxP.append(codigoMD)
        print(type(auxP))
        DDvigenciaP.append(auxP)
    print(type(DDvigenciaP))

    # tabla de Detalle pagos de Penalidad
    rowsDP = driver.find_elements(By.XPATH, "//table[@id='grid_penalidad_det']/tbody/tr")
    cellsDP = driver.find_elements(By.XPATH, "//table[@id='grid_penalidad_det']/tbody/tr/td")
    print(len(cellsDP))
    print(len(rowsDP))
    codigosDV = [element.text for element in cellsDP]
    # print(codigos)
    matriz_vigenciaDP = []
    data_vigenciaDP = []
    contadorDP = 0
    for p in cellsDP:
        data_vigenciaDP.append(p.text)
        contadorDP = contadorDP + 1
        if (contadorDP % 6 == 0):
            matriz_vigenciaDP.append(data_vigenciaDP)
            data_vigenciaDP = []

    DDvigenciaDP = [["año", "Banco", "Boleta", "Fecha de deposito", "Moneda", "Deposito", "MD"]]
    for i in range(len(matriz_vigenciaDP)):
        print(matriz_vigenciaDP[i])
        auxDP = matriz_vigenciaDP[i]
        if (auxDP[0]):
            detallepenalidad = DetallePenalidad.objects.create(anio=auxDP[0], banco=auxDP[1], boleta=auxDP[2], fecha=auxDP[3],
                                               moneda=auxDP[4], deposito=auxDP[5], dm=codigoMD)
        auxDP.append(codigoMD)
        print(type(auxDP))
        DDvigenciaDP.append(auxDP)
    print(type(DDvigenciaDP))

    driver.quit()

    global GGvigencia
    GGvigencia = GGvigencia + DDvigencia
    global GGvigenciaDV
    GGvigenciaDV = GGvigenciaDV + DDvigenciaDV
    global GGvigenciaDP
    GGvigenciaDP = GGvigenciaDP + DDvigenciaDP
    global GGPenalidad
    GGPenalidad = GGPenalidad + DDvigenciaP

def guardar():
    global codigominero
    myFile = open('vigencia' + codigominero + '.csv', 'w')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(GGvigencia)
    myFile = open('Detallevigencia' + codigominero + '.csv', 'w')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(GGvigenciaDV)
    myFile = open('Penalidad' + codigominero + '.csv', 'w')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(GGPenalidad)
    myFile = open('DetallePenalidad' + codigominero + '.csv', 'w')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(GGvigenciaDP)

GGvigenciaDP = [[]]
GGvigenciaDV = [[]]
GGvigencia = [[]]
GGPenalidad = [[]]
codigominero = ""

class AgregarVeterinario(generics.CreateAPIView):
    def post(self,request,format=None):
        title = request.data['title']
        lst=[{}]
        keys= lst[1].keys()
        for diccionario in lst:
            id_old = diccionario.get('id')
            tbl_usuario_id = diccionario.get('tbl_usuario_id')
            tbl_colegio_departamental_id = diccionario.get('tbl_colegio_departamental_id')
            tbl_pais_id = diccionario.get('tbl_pais_id')
            tbl_distrito_id = diccionario.get('tbl_distrito_id')
            cmpv = diccionario.get('cmpv')
            apellidos = diccionario.get('apellidos')
            nombres = diccionario.get('nombres')
            correo = diccionario.get('correo')
            foto = diccionario.get('foto')
            fecha_inscripcion = diccionario.get('fecha_inscripcion')
            fecha_colegiatura = diccionario.get('fecha_colegiatura')
            fecha_nacimiento = diccionario.get('fecha_nacimiento')
            estado_civil = diccionario.get('estado_civil')
            sexo = diccionario.get('sexo')
            direccion = diccionario.get('direccion')
            codigo_postal = diccionario.get('codigo_postal')
            documento_fac = diccionario.get('documento_fac')
            nombre_fac = diccionario.get('nombre_fac')
            direccion_fac = diccionario.get('direccion_fac')
            nota = diccionario.get('nota')
            ultima_cuota_old = diccionario.get('ultima_cuota_old')
            fecha_habilidad_temporal = diccionario.get('fecha_habilidad_temporal')
            estado_colegio = diccionario.get('estado_colegio')
            perfil = diccionario.get('perfil')
            multaelectoral = diccionario.get('multaelectoral')
            estado = diccionario.get('estado')
            creado_por = diccionario.get('creado_por')
            fecha_creado = diccionario.get('fecha_creado')
            modificado_por = diccionario.get('modificado_por')
            fecha_modificado = diccionario.get('fecha_modificado')
            usuario = diccionario.get('usuario')
            nacionalidad = diccionario.get('nacionalidad')
            colegioDepartamental = diccionario.get('colegioDepartamental')
            name = diccionario.get('name')
            distrito = diccionario.get('distrito')
            provincia = diccionario.get('provincia')
            region = diccionario.get('region')
            id = diccionario.get('id')
            tbl_usuario_id = diccionario.get('tbl_usuario_id')
            tbl_colegio_departamental_id = diccionario.get('tbl_colegio_departamental_id')
            tbl_pais_id = diccionario.get('tbl_pais_id')
            tbl_distrito_id = diccionario.get('tbl_distrito_id')
            cmpv = diccionario.get('cmpv')
            apellidos = diccionario.get('apellidos')
            nombres = diccionario.get('nombres')
            correo = diccionario.get('correo')
            foto = diccionario.get('foto')
            fecha_inscripcion = diccionario.get('fecha_inscripcion')
            fecha_colegiatura = diccionario.get('fecha_colegiatura')
            fecha_nacimiento = diccionario.get('fecha_nacimiento')
            estado_civil = diccionario.get('estado_civil')
            sexo = diccionario.get('sexo')
            direccion = diccionario.get('direccion')
            codigo_postal = diccionario.get('codigo_postal')
            documento_fac = diccionario.get('documento_fac')
            nombre_fac = diccionario.get('nombre_fac')
            direccion_fac = diccionario.get('direccion_fac')
            nota = diccionario.get('nota')
            ultima_cuota_old = diccionario.get('ultima_cuota_old')
            fecha_habilidad_temporal = diccionario.get('fecha_habilidad_temporal')
            estado_colegio = diccionario.get('estado_colegio')
            perfil = diccionario.get('perfil')
            multaelectoral = diccionario.get('multaelectoral')

            #veterinario = Veterinario.objects.create(anio=aux[0], calificacion=aux[1], has=aux[2], deuda=aux[3],
             #                            deposito=aux[4], saldo=aux[5], devolucion=aux[6], dm=codigoMD)
            veterinario = Veterinario.objects.create(id_old=id_old, tbl_usuario_id=tbl_usuario_id,
                                                     tbl_colegio_departamental_id=tbl_colegio_departamental_id,
                                                     tbl_pais_id=tbl_pais_id, tbl_distrito_id=tbl_distrito_id,
                                                     cmpv=cmpv, apellidos=apellidos, nombres=nombres, correo=correo,
                                                     foto=foto, fecha_inscripcion=fecha_inscripcion,
                                                     fecha_colegiatura=fecha_colegiatura,
                                                     fecha_nacimiento=fecha_nacimiento, estado_civil=estado_civil,
                                                     sexo=sexo, direccion=direccion, codigo_postal=codigo_postal,
                                                     documento_fac=documento_fac, nombre_fac=nombre_fac,
                                                     direccion_fac=direccion_fac, nota=nota,
                                                     ultima_cuota_old=ultima_cuota_old,
                                                     fecha_habilidad_temporal=fecha_habilidad_temporal,
                                                     estado_colegio=estado_colegio, perfil=perfil,
                                                     multaelectoral=multaelectoral, estado=estado,
                                                     creado_por=creado_por, fecha_creado=fecha_creado,
                                                     modificado_por=modificado_por, fecha_modificado=fecha_modificado,
                                                     usuario=usuario, nacionalidad=nacionalidad,
                                                     colegioDepartamental=colegioDepartamental, name=name,
                                                     distrito=distrito, provincia=provincia, region=region)
        print(keys)
        data={'detail':'veterinario guardado con exito '}
        rpta=json.dumps(data)
        return HttpResponse(rpta,content_type='application/json')

class AgusIncaRail(generics.CreateAPIView):
    def post(self,request,format=None):
        buscarinfoInca()
        data={'detail':'libro guardado con exito '}
        rpta=json.dumps(data)
        return HttpResponse(rpta,content_type='application/json')

def buscarinfoInca():
    print("carga datos www")
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get('https://operadores.machupicchu.gob.pe/')
    usuario_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "//input[@name='Usuario']")))
    Usuario = "AG0755"
    usuario_input.send_keys(Usuario)
    print('usuario')
    pwd_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "//input[@name='Contraseña']")))
    password = "VJ4U3K"
    pwd_input.send_keys(password)
    print('pasword')
    condiciones_button = WebDriverWait(driver, 80).until(EC.presence_of_element_located(
        (By.XPATH, "//span[@class='checkboxFalse']")))
    condiciones_button.click()
    buscar_button = WebDriverWait(driver, 80).until(EC.presence_of_element_located(
        (By.XPATH, "//td[@class='button']")))
    buscar_button.click()
    print('ingresar')
    #time.sleep(5)
    menu_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "//td[@class='toolStripButton']")))
    menu_input.click()

    #Reservas_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    #    (By.XPATH, "//div[@id='isc_34']")))
    #Reservas_input.click()

    asignar_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "//td[@id='isc_TreeGrid_0_valueCell25']")))
    asignar_input.click()
    time.sleep(2)
    combo_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "//table[@id='isc_4A']")))
    combo_input.click()
    time.sleep(2)
    print("cambiar el combo para Machupicchu")
    machupicchu=driver.find_element_by_xpath("//*[@id='isc_PickListMenu_1_row_1']")
    machupicchu.click()
    time.sleep(5)
    combo_input.click()
    camino=driver.find_element_by_xpath("//*[@id='isc_PickListMenu_1_row_0']")
    camino.click()
    time.sleep(25)
    #selectItemLiteControl


