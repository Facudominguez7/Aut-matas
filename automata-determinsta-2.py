import graphviz
from PIL import Image, ImageDraw, ImageFont
import os

class Automata:
    def __init__(self, estados, alfabeto, transiciones, estado_inicial, estados_aceptacion):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transiciones = transiciones
        self.estado_inicial = estado_inicial
        self.estados_aceptacion = estados_aceptacion

    def graficar(self, aceptado):
        dot = graphviz.Digraph()

        # Agregar estados
        for estado in self.estados:
            if estado in self.estados_aceptacion:
                dot.node(estado, shape='doublecircle')
            else:
                dot.node(estado)

        # Agregar transiciones
        for estado, transicion in self.transiciones.items():
            for simbolo, destino in transicion.items():
                dot.edge(estado, destino, label=simbolo)

        # Guardar el gráfico temporalmente
        dot.render('afd', format='png', cleanup=False)
        
        # Abrir la imagen del autómata
        img = Image.open('afd.png')
        
        # Cargar la imagen de la palomita de aprobación o la X roja
        if aceptado:
            simbolo_img = Image.open("acepta.png")
        else:
            simbolo_img = Image.open("rechaza.png")
            
        # Convertir la imagen a modo RGBA para admitir transparencia
        simbolo_img = simbolo_img.convert("RGBA")
        
        # Ajustar la transparencia de la imagen
        alpha = 128  # 0 (transparente) a 255 (opaco)
        simbolo_img.putalpha(alpha)

        # Escalar el símbolo para que quepa en la imagen del autómata
        width, height = img.size
        simbolo_img.thumbnail((width // 4, height // 4))

        # Posicionar el símbolo en la esquina superior derecha
        img.paste(simbolo_img, (width - simbolo_img.width - 10, 10), simbolo_img)
        
        # Mostrar la imagen
        img.show()

        # Eliminar el archivo del autómata después de mostrar la imagen
        os.remove('afd.png')

    def acepta_cadena(self, cadena):
        estado_actual = self.estado_inicial
        for simbolo in cadena:
            if simbolo not in self.alfabeto:
                return False, "La cadena contiene símbolos fuera del alfabeto."

            if estado_actual not in self.transiciones or simbolo not in self.transiciones[estado_actual]:
                return False, "El autómata no tiene una transición definida para el estado {} con el símbolo {}.".format(estado_actual, simbolo)

            estado_actual = self.transiciones[estado_actual][simbolo]

        return estado_actual in self.estados_aceptacion


# Ejemplo de uso
estados = {'q0', 'q1', 'q2'}
alfabeto = {'0', '1'}
transiciones = {'q0': {'0': 'q1', '1': 'q2'},
                'q1': {'0': 'q1', '1': 'q2'},
                'q2': {'0': 'q2', '1': 'q2'}}
estado_inicial = 'q0'
estados_aceptacion = {'q2'}

afd = Automata(estados, alfabeto, transiciones, estado_inicial, estados_aceptacion)

cadena = input("Ingrese una cadena para verificar si el autómata la acepta o no: ")

# Verifica si la cadena contiene solo símbolos del alfabeto
if all(simbolo in alfabeto for simbolo in cadena):
    aceptado = afd.acepta_cadena(cadena)
    afd.graficar(aceptado)
    if aceptado:
        print("El autómata acepta la cadena.")
    else:
        print("El autómata rechaza la cadena.")
else:
    print("La cadena contiene símbolos fuera del alfabeto.")