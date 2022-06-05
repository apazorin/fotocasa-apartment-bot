class Variable:
    def __init__(self, tipo_vivienda, accion, superficie, habitaciones, banyos, precio, distancia_playa, \
        planta, orientacion, antiguedad, estado_inmueble, eficiencia, ascensor, jardin, amueblado, terraza, descripcion, \
        localidad, barrio, calle, telefono, habitaclia, photos_path, comunidad, fianza):
        self.tipo_vivienda = tipo_vivienda
        self.accion = accion                                                    
        self.superficie = superficie
        self.habitaciones = habitaciones
        self.precio = precio
        self.banyos = banyos
        self.distancia_playa = distancia_playa
        self.planta = planta
        self.orientacion = orientacion
        self.antiguedad = antiguedad
        self.estado_inmueble = estado_inmueble
        self.eficiencia = eficiencia
        self.ascensor = ascensor
        self.jardin = jardin
        self.amueblado = amueblado
        self.terraza = terraza
        self.descripcion = descripcion
        self.precio = precio
        self.localidad = localidad
        self.barrio = barrio
        self.calle = calle
        self.telefono = telefono
        self.habitaclia = habitaclia
        self.photos_path = photos_path
        self.comunidad = comunidad
        self.fianza = fianza
    
    def to_string(self):
        return f"Data: {self.tipo_vivienda}, {self.accion}, {self.superficie}"
