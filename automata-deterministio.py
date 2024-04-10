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

        for estado in self.estados:
            if estado in self.estados_aceptacion:
                #genera un circulo doble
                dot.node(estado, shape='doublecircle')
            else:
                #circulo simple
                dot.node(estado)

        for estado, transicion in self.transiciones.items():
                # Iterar sobre las transiciones desde el estado actual
            for simbolo, destino in transicion.items():
                # Para cada transición desde el estado actual, donde:
                # - 'simbolo' es el símbolo que activa la transición
                # - 'destino' es el estado al que se transita desde el estado actual
                dot.edge(estado, destino, label=simbolo)
                # Agregar una arista al grafo del autómata que va desde el estado actual
                # hasta el estado destino, etiquetada con el símbolo que activa la transición


        dot.render('afd', format='png', cleanup=False)
        
        img = Image.open('afd.png')
        
        if aceptado:
            simbolo_img = Image.open("acepta.png")
        else:
            simbolo_img = Image.open("rechaza.png")
            
        simbolo_img = simbolo_img.convert("RGBA")
        
        alpha = 128 
        simbolo_img.putalpha(alpha)

        width, height = img.size
        simbolo_img.thumbnail((width // 4, height // 4))

        img.paste(simbolo_img, (width - simbolo_img.width - 10, 10), simbolo_img)
        
        img.show()

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


estados = {'q0', 'q1', 'q2'}
alfabeto = {'0', '1'}
transiciones = {'q0': {'0': 'q0', '1': 'q1'},
                'q1': {'0': 'q2', '1': 'q1'},
                'q2': {'0': 'q2', '1': 'q1'}}
estado_inicial = 'q0'
estados_aceptacion = {'q2'}

afd = Automata(estados, alfabeto, transiciones, estado_inicial, estados_aceptacion)

cadena = input("Ingrese una cadena para verificar si el autómata la acepta o no: ")

if all(simbolo in alfabeto for simbolo in cadena):
    aceptado = afd.acepta_cadena(cadena)
    afd.graficar(aceptado)
    if aceptado:
        print("El autómata acepta la cadena.")
    else:
        print("El autómata rechaza la cadena.")
else:
    print("La cadena contiene símbolos fuera del alfabeto.")