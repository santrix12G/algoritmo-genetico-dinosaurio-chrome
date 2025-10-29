"""
Clases Gen y Genome para el algoritmo genético.
"""
import random
from utils.linear_algebra import random_vector


class Gen:
    """Representa una conexión neuronal con su peso."""
    
    def __init__(self):
        self.source_hidden_layer = random.random() < 0.5
        self.id_source_neuron = random.randint(0, 6)
        
        if self.source_hidden_layer:
            self.id_target_neuron = random.randint(0, 6)
        else:
            self.id_target_neuron = random.randint(0, 1)
        
        self.weight = random.uniform(-1, 1)


class Genome:
    """
    Representa el genoma completo de un dinosaurio.
    Contiene todos los genes (pesos de las conexiones neuronales) y los bias.
    """
    
    def __init__(self):
        self.length = 16
        self.genes = [Gen() for _ in range(self.length)]
        self.hidden_layer_bias = random_vector(7)
        self.output_layer_bias = random_vector(2)
    
    def copy(self):
        """Crea una copia profunda del genoma."""
        copied_genome = Genome()
        
        # Copiar genes
        for i in range(self.length):
            copied_genome.genes[i] = self.genes[i]
        
        # Copiar bias
        for i in range(7):
            copied_genome.hidden_layer_bias[i] = self.hidden_layer_bias[i]
        
        for i in range(2):
            copied_genome.output_layer_bias[i] = self.output_layer_bias[i]
        
        return copied_genome
    
    def mutate(self):
        """
        Crea un genoma mutado basado en este genoma.
        Cambia entre 1 y 4 genes aleatorios.
        """
        mutated_genome = self.copy()
        amount_of_mutations = random.randint(1, 4)
        
        for _ in range(amount_of_mutations):
            index = random.randint(0, self.length - 1)
            mutated_genome.genes[index] = Gen()
        
        return mutated_genome
    
    def crossover(self, another_genome):
        """
        Crea un genoma hijo combinando este genoma con otro.
        Toma entre 1 y 4 genes del otro genoma.
        """
        crossed_genome = self.copy()
        amount_of_crossovers = random.randint(1, 4)
        
        for _ in range(amount_of_crossovers):
            index = random.randint(0, self.length - 1)
            crossed_genome.genes[index] = another_genome.genes[index]
        
        return crossed_genome