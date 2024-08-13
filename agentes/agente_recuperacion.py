from sentence_transformers import SentenceTransformer, util
import json
import torch
from llm.gemini import get_response
import os


class Agent_Rec:

    current_dir = os.path.dirname(__file__)

    json_file_path = os.path.join(current_dir, '../agenda/agenda.json')
    # Función para leer el contenido de un archivo JSON
    def read_json_file(self,file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    def gen_pdf(self, archivo, name):
        with open(name, 'w') as file:
            json.dump(archivo, file, ensure_ascii=False, indent=4)

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
    
    def add_item(self, context, input):

        template_rag = """
        Eres un asistente que modifica archivos JSON según las instrucciones del usuario.
        El archivo JSON contiene una agenda en formato JSON.
        Tu trabajo sera agregar un nuevo item a la agenda o midificarlo, dependiendo del input.

        Debe abstenerse de utilizar comillas invertidas junto con palabras como "json", solo imprime el puro JSON.

        archivo JSON:{context}

        input:{input}

        """

        final_prompt = template_rag.format(context=context, input=input)

        response = get_response(final_prompt)

        return response
    
    
    def add_or_mod_item(self, question):
        try:

            agenda_data2 = self.read_json_file(self.json_file_path)
            answer = self.add_item(agenda_data2, question)

            json_data = json.loads(answer)
            self.gen_pdf(json_data, self.json_file_path)

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