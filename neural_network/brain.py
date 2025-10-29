"""
Red neuronal (cerebro) para controlar el comportamiento del dinosaurio.
"""
import pygame
import numpy as np
from utils.linear_algebra import matrix_vector_multiplication, zeroes_matrix


class Brain:
    """
    Red neuronal simple con:
    - 7 neuronas de entrada
    - 7 neuronas ocultas
    - 2 neuronas de salida (saltar, agacharse)
    """
    
    def __init__(self, genome):
        self.inputs = np.zeros(7)
        self.outputs = np.array([1, 0])
        
        # Inicializar pesos desde el genoma
        self.hidden_layer_weights = zeroes_matrix(7, 7)
        self.output_layer_weights = zeroes_matrix(2, 7)
        
        for gen in genome.genes:
            if gen.source_hidden_layer:
                self.hidden_layer_weights[gen.id_target_neuron][gen.id_source_neuron] = gen.weight
            else:
                self.output_layer_weights[gen.id_target_neuron][gen.id_source_neuron] = gen.weight
        
        self.hidden_layer_bias = genome.hidden_layer_bias
        self.output_layer_bias = genome.output_layer_bias
        self.hidden_outputs = np.zeros(7)
    
    def relu(self, x):
        """Función de activación ReLU."""
        return max(0, x)
    
    
    def feed_forward(self, input_layer_values):
        """
        Propaga los valores de entrada a través de la red.
        
        Args:
            input_layer_values: array de 7 valores normalizados
        """
        self.inputs = np.array(input_layer_values)
        
        # Capa oculta
        self.hidden_outputs = matrix_vector_multiplication(self.hidden_layer_weights, input_layer_values)
        for i in range(len(self.hidden_outputs)):
            self.hidden_outputs[i] += self.hidden_layer_bias[i]
            self.hidden_outputs[i] = self.relu(self.hidden_outputs[i])
        
        # Capa de salida
        self.outputs = matrix_vector_multiplication(self.output_layer_weights, self.hidden_outputs)
        for i in range(len(self.outputs)):
            self.outputs[i] += self.output_layer_bias[i]
            self.outputs[i] = self.relu(self.outputs[i])
    
    def set_neural_connection_stroke(self, weight):
        """
        Determina el color y grosor de las líneas según el peso.
        
        Returns:
            tuple: (color, width)
        """
        if weight > 0:
            color = (0, 255, 0)  # Verde para pesos positivos
        elif weight < 0:
            color = (255, 0, 0)  # Rojo para pesos negativos
        else:
            color = (200, 200, 200)  # Gris para peso cero
        
        # Mapear el grosor basado en el valor absoluto del peso
        abs_weight = abs(weight)
        width = max(0.5, min(5, abs_weight * 5))
        
        return color, width
    
    def draw(self, screen, font):
        """
        Dibuja la visualización de la red neuronal.
        
        Args:
            screen: superficie de pygame
            font: fuente para el texto
        """
        # Etiquetas
        labels = [
            (550, 67, "(obstacle) distance"),
            (598, 107, "(obstacle) x"),
            (598, 147, "(obstacle) y"),
            (568, 187, "(obstacle) width"),
            (563, 227, "(obstacle) height"),
            (625, 267, "(dino) y"),
            (586, 307, "(game) speed"),
            (927, 168, "jump"),
            (925, 208, "crouch")
        ]
        
        for x, y, text in labels:
            text_surface = font.render(text, True, (0, 0, 0))
            screen.blit(text_surface, (x, y))
        
        # Dibujar conexiones y nodos
        for i in range(7):
            # Conexiones de entrada a capa oculta
            for j in range(7):
                weight = self.hidden_layer_weights[i][j]
                color, width = self.set_neural_connection_stroke(weight)
                pygame.draw.line(screen, color, (700 + 16, 64 + i * 40), (800 - 16, 64 + j * 40), int(width))
            
            # Conexiones de capa oculta a salida
            for j in range(2):
                weight = self.output_layer_weights[j][i]
                color, width = self.set_neural_connection_stroke(weight)
                pygame.draw.line(screen, color, (800 + 16, 64 + i * 40), (900 - 16, 165 + j * 40), int(width))
            
            # Círculos de capa de entrada
            pygame.draw.circle(screen, (255, 255, 255), (700, 64 + i * 40), 16)
            pygame.draw.circle(screen, (83, 83, 83), (700, 64 + i * 40), 16, 1)
            
            # Círculos de capa oculta
            if self.hidden_outputs[i] == 0:
                fill_color = (255, 255, 255)
            else:
                fill_color = (170, 170, 170)
            pygame.draw.circle(screen, fill_color, (800, 64 + i * 40), 16)
            pygame.draw.circle(screen, (0, 0, 0), (800, 64 + i * 40), 16, 1)
            
            # Texto de valores de entrada
            small_font = pygame.font.Font(None, 20)
            input_text = f"{self.inputs[i]:.3f}"
            text_surface = small_font.render(input_text, True, (0, 0, 0))
            screen.blit(text_surface, (688, 58 + i * 40))
        
        # Círculos de salida
        for j in range(2):
            if self.outputs[j] == 0:
                fill_color = (255, 255, 255)
            else:
                fill_color = (170, 170, 170)
            pygame.draw.circle(screen, fill_color, (900, 165 + j * 40), 16)
            pygame.draw.circle(screen, (0, 0, 0), (900, 165 + j * 40), 16, 1)
    def get_weights(self):
        return {
            "input_hidden": self.inputs,
            "hidden_output": self.hidden_layer_weights
        }