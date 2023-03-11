from django.db import models

# Create your models here.
class store (models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name
class categoria (models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class books(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=9,decimal_places=2)
    picture = models.ImageField(upload_to='books/',null=True,blank=True)
    state=models.BooleanField(default=True)
    category=models.ForeignKey(categoria,on_delete=models.PROTECT)
    store=models.ManyToManyField(store,related_name="store_book")

    def __str__(self):
        return self.title

class customer(models.Model):
    last_name=models.CharField(max_length=50)
    firs_name=models.CharField(max_length=50)
    addres=models.CharField(max_length=50)
    def __str__(self):
        return self.last_name + self.firs_name

class order(models.Model):
    document=models.CharField(max_length=50)
    customer=models.ForeignKey(customer,on_delete=models.PROTECT)
    date=models.DateTimeField()
    def __str__(self):
        return self.document

class ordenDetalle(models.Model):
    books=models.ForeignKey(books,on_delete=models.PROTECT)
    amount=models.IntegerField()
    order=models.ForeignKey(order,on_delete=models.PROTECT)

class vigencia(models.Model):
    anio = models.CharField(max_length=50)
    calificacion = models.CharField(max_length=50)
    has = models.CharField(max_length=50)
    deuda = models.CharField(max_length=50)
    deposito = models.CharField(max_length=50)
    saldo = models.CharField(max_length=50)
    devolucion = models.CharField(max_length=50)
    dm = models.CharField(max_length=50)
    def __str__(self):
        return self.dm

class penalidad(models.Model):
    anio = models.CharField(max_length=50)
    calificacion = models.CharField(max_length=50)
    has = models.CharField(max_length=50)
    deuda = models.CharField(max_length=50)
    deposito = models.CharField(max_length=50)
    saldo = models.CharField(max_length=50)
    devolucion = models.CharField(max_length=50)
    dm = models.CharField(max_length=50)
    def __str__(self):
        return self.dm

class DetalleVigencia(models.Model):
    anio = models.CharField(max_length=50)
    banco = models.CharField(max_length=50)
    boleta = models.CharField(max_length=50)
    fecha = models.CharField(max_length=50)
    moneda = models.CharField(max_length=50)
    deposito = models.CharField(max_length=50)
    dm = models.CharField(max_length=50)
    def __str__(self):
        return self.dm

class DetallePenalidad(models.Model):
    anio = models.CharField(max_length=50)
    banco = models.CharField(max_length=50)
    boleta = models.CharField(max_length=50)
    fecha = models.CharField(max_length=50)
    moneda = models.CharField(max_length=50)
    deposito = models.CharField(max_length=50)
    dm = models.CharField(max_length=50)

    def __str__(self):
        return self.dm

class Veterinario(models.Model):
    id_old=models.CharField(max_length=500)
    tbl_usuario_id=models.CharField(max_length=500)
    tbl_colegio_departamental_id=models.CharField(max_length=500)
    tbl_pais_id=models.CharField(max_length=500)
    tbl_distrito_id=models.CharField(max_length=500)
    cmpv=models.CharField(max_length=500)
    apellidos=models.CharField(max_length=500)
    nombres=models.CharField(max_length=500)
    correo=models.CharField(max_length=500)
    foto=models.CharField(max_length=500)
    fecha_inscripcion=models.CharField(max_length=500)
    fecha_colegiatura=models.CharField(max_length=500)
    fecha_nacimiento=models.CharField(max_length=500)
    estado_civil=models.CharField(max_length=500)
    sexo=models.CharField(max_length=500)
    direccion=models.CharField(max_length=500)
    codigo_postal=models.CharField(max_length=500)
    documento_fac=models.CharField(max_length=500)
    nombre_fac=models.CharField(max_length=500)
    direccion_fac=models.CharField(max_length=500)
    nota=models.CharField(max_length=5000)
    ultima_cuota_old=models.CharField(max_length=500)
    fecha_habilidad_temporal=models.CharField(max_length=500)
    estado_colegio=models.CharField(max_length=500)
    perfil=models.CharField(max_length=500)
    multaelectoral=models.CharField(max_length=500)
    estado=models.CharField(max_length=500)
    creado_por=models.CharField(max_length=500)
    fecha_creado=models.CharField(max_length=500)
    modificado_por=models.CharField(max_length=500)
    fecha_modificado=models.CharField(max_length=500)
    usuario=models.CharField(max_length=500)
    nacionalidad=models.CharField(max_length=500)
    colegioDepartamental=models.CharField(max_length=500)
    name=models.CharField(max_length=500)
    distrito=models.CharField(max_length=500)
    provincia=models.CharField(max_length=500)
    region=models.CharField(max_length=500)
    def __str__(self):
        return self.name
