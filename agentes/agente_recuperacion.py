from sentence_transformers import SentenceTransformer, util
from llm.gemini import get_response
from datetime import datetime
import json
import torch
import os


class AgentRec:

    current_dir = os.path.dirname(__file__)

    json_file_path = os.path.join(current_dir, '../agenda/agenda.json')

    # Función para leer el contenido de un archivo JSON
    def read_json_file(self,file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
        
    # Funcion para generar un JSON
    def gen_json_file(self, archivo, name):
        with open(name, 'w') as file:
            json.dump(archivo, file, ensure_ascii=False, indent=4)

    def obtener_fecha_hora_actual(self):
        ahora = datetime.now()
        fecha_hora_formateada = ahora.strftime("%Y-%m-%d %H:%M:%S")
        return fecha_hora_formateada

    # Función para cargar documentos desde un archivo JSON
    def load_documents_from_json(self, file_path):
        agenda_data = self.read_json_file(file_path)
        documents = []
        
        for event in agenda_data.get('events', []):
            documents.append({"content": f"Evento: {event['title']} en {event['location']} el {event['date']} a las {event['time']}. Descripción: {event['description']}"})
        
        for task in agenda_data.get('tasks', []):
            documents.append({"content": f"Tarea: {task['title']} con fecha límite {task['due_date']}. Prioridad: {task['priority']}. Estado: {task['status']}"})
        
        for important_date in agenda_data.get('important_dates', []):
            documents.append({"content": f"Fecha importante: {important_date['title']} el {important_date['date']}"})
        
        return documents
    
    # Función para crear un prompt para agregar o modificar un item en la agenda
    def prompt_add_or_mod_item(self, context, input):

        date = self.obtener_fecha_hora_actual()

        template_rag = """
        Eres un asistente que modifica archivos JSON según las instrucciones del usuario.
        El archivo JSON contiene una agenda en formato JSON.
        Tu trabajo sera agregar un nuevo item a la agenda o modificarlo, dependiendo del input.
        Las fechas no siempre se mencionan completamente, sino que a veces aparecen mencionadas como “ayer”, “mañana”, etc.
        Para saber la fecha actual utilizaras: fecha

        Debe abstenerse de utilizar comillas invertidas junto con palabras como "json", solo imprime el puro JSON.

        archivo JSON:{context}

        input:{input}

        fcha:{date}

        """

        final_prompt = template_rag.format(context=context, input=input, date=date)

        response = get_response(final_prompt)

        return response
    
    
    # Función para realizar el cambio en la agenda
    def add_or_mod_item(self, question):
        try:

            agenda_data2 = self.read_json_file(self.json_file_path)
            answer = self.prompt_add_or_mod_item(agenda_data2, question)

            json_data = json.loads(answer)
            self.gen_json_file(json_data, self.json_file_path)

            result = "El cambio ha sido realizado con éxito."

            return result
            
        except Exception as ex:
            return ex


    # Función para realizar la consulta y generar la respuesta (igual que antes)
    def rag_query_with_embeddings(self, question):

        embedder = SentenceTransformer('all-MiniLM-L6-v2')

        documents = self.load_documents_from_json(self.json_file_path)

        # Obtener el embedding de la pregunta
        question_embedding = embedder.encode(question, convert_to_tensor=True)

        # Obtener los embeddings de los documentos
        document_embeddings = embedder.encode([doc['content'] for doc in documents], convert_to_tensor=True)

        # Calcular la similitud entre la pregunta y los documentos
        scores = util.pytorch_cos_sim(question_embedding, document_embeddings)
        top_k = torch.topk(scores, k=5).indices.tolist()[0]  # Convertir a una lista de índices

        # Recuperar los documentos más relevantes
        context = [documents[idx]['content'] for idx in top_k]

        return context