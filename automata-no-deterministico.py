import graphviz
from PIL import Image, ImageDraw, ImageFont
import os

class AutomataND:
    def __init__(self, estados, alfabeto, transiciones, estado_inicial, estados_aceptacion):
        """
        Inicializa un objeto AutomataND con los parámetros dados.

        estados: conjunto de estados del autómata
        alfabeto: conjunto de símbolos del alfabeto del autómata
        transiciones: diccionario que representa las transiciones del autómata
        estado_inicial: estado inicial del autómata
        estados_aceptacion: conjunto de estados de aceptación del autómata
        """
        self.estados = estados
        self.alfabeto = alfabeto
        self.transiciones = transiciones
        self.estado_inicial = estado_inicial
        self.estados_aceptacion = estados_aceptacion

    def graficar(self, aceptado):
        dot = graphviz.Digraph()

        for estado in self.estados:
            if estado in self.estados_aceptacion:
                dot.node(estado, shape='doublecircle')
            else:
                dot.node(estado)

        for estado, transicion in self.transiciones.items():
            for simbolo, destinos in transicion.items():
                for destino in destinos:
                    dot.edge(estado, destino, label=simbolo)

        dot.render('afnd', format='png', cleanup=False)
        
        img = Image.open('afnd.png')
        
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

        os.remove('afnd.png')

    def acepta_cadena(self, cadena):
        def transitar(estado_actual, cadena):
            if not cadena:
                return {estado_actual}
            else:
                siguiente_simbolo = cadena[0]
                restante = cadena[1:]
                siguientes_estados = set()
                if estado_actual in self.transiciones and siguiente_simbolo in self.transiciones[estado_actual]:
                    for estado_destino in self.transiciones[estado_actual][siguiente_simbolo]:
                        siguientes_estados |= transitar(estado_destino, restante)
                return siguientes_estados

        estados_actuales = transitar(self.estado_inicial, cadena)
        return any(estado in self.estados_aceptacion for estado in estados_actuales)


# Ejemplo de uso
estados = {'q0', 'q1', 'q2'}
alfabeto = {'0', '1'}
transiciones = {
    'q0': {'0': {'q0', 'q1'}, '1': {'q1'}},
    'q1': {'1': {'q1', 'q2'}}, 
    'q2': {'1': {'q2'}}
}
estado_inicial = 'q0'
estados_aceptacion = {'q2'}

afnd = AutomataND(estados, alfabeto, transiciones, estado_inicial, estados_aceptacion)

cadena = input("Ingrese una cadena para verificar si el autómata la acepta o no: ")

# Verifica si la cadena contiene solo símbolos del alfabeto
if all(simbolo in alfabeto for simbolo in cadena):
    aceptado = afnd.acepta_cadena(cadena)
    afnd.graficar(aceptado)
    if aceptado:
        print("El autómata acepta la cadena.")
    else:
        print("El autómata rechaza la cadena.")
else:
    print("La cadena contiene símbolos fuera del alfabeto.")