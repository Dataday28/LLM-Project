from llm.gemini import get_response
import json
import re
import os


class AgentOrg:

    current_dir = os.path.dirname(__file__)
    rec_file_path = os.path.join(current_dir, '../documentos/informacion_recuperada.json')
    estruc_file_path = os.path.join(current_dir, '../documentos/informacion_estructurada.json')
    org_file_path = os.path.join(current_dir, '../documentos/informacion_organizada.json')

    # function para generar un json
    def gen_json_file(self, archivo, name):
        with open(name, 'w') as file:
            json.dump(archivo, file, ensure_ascii=False, indent=4)

    # Cargar la información desde el archivo JSON
    def read_json_file(self, archivo):
        with open(archivo, 'r') as file:
            informcion  = json.load(file)
        return informcion
    

    # Funcion para estructurar la informacion
    def structure(self, informacion):

        organized_data = {
            "fechas_importantes": [],
            "eventos": [],
            "tareas": []
        }

        for item in informacion:
            if item.startswith("Fecha importante"):
                organized_data["fechas_importantes"].append(item)
            elif item.startswith("Evento"):
                organized_data["eventos"].append(item)
            elif item.startswith("Tarea"):
                organized_data["tareas"].append(item)

        def extract_details(patron, texto):
            return re.search(patron, texto).group(1) if re.search(patron, texto) else None

        # Extraer detalles de fechas importantes
        detalles_fechas_importantes = [{"descripcion": extract_details(r": (.*?) el", item), "fecha": extract_details(r"el (\d{4}-\d{2}-\d{2})", item)} for item in organized_data["fechas_importantes"]]

        # Extraer detalles de eventos
        detalles_eventos = []
        for item in organized_data["eventos"]:
            detalles_eventos.append({
                "descripcion": extract_details(r": (.*?) en", item),
                "ubicacion": extract_details(r"en (.*?) el", item),
                "fecha": extract_details(r"el (\d{4}-\d{2}-\d{2})", item),
                "hora": extract_details(r"a las (\d{2}:\d{2})", item),
                "descripcion_detallada": extract_details(r"Descripción: (.*)", item)
            })

        # Extraer detalles de tareas
        detalles_tareas = []
        for item in organized_data["tareas"]:
            detalles_tareas.append({
                "descripcion": extract_details(r": (.*?) con", item),
                "fecha_limite": extract_details(r"fecha límite (\d{4}-\d{2}-\d{2})", item),
                "prioridad": extract_details(r"Prioridad: (\w+)", item),
                "estado": extract_details(r"Estado: (\w+)", item)
            })

        # Guardar los detalles en un archivo JSON
        informacion_estructurada = {
            "fechas_importantes": detalles_fechas_importantes,
            "eventos": detalles_eventos,
            "tareas": detalles_tareas
        }

        return informacion_estructurada
    

    # function para organizar la informacion
    def organice_information(self, informacion):
        informacion_organizada = {
            "Fechas Importantes": informacion.get("fechas_importantes", []),
            "Eventos": informacion.get("eventos", []),
            "Tareas": informacion.get("tareas", [])
        }
        return informacion_organizada
    

    # funcion para generar un resumen mediante un prompt
    def generate_resume(self, informacion):

        # Generar la respuesta utilizando el LLM
        template = """Tu trabajo sera generar un resumen de la informacion proporcionada.
        La informacion esta delimitado por las comillas invertidas.
        Contesta como si la respuesta la estuviera dando un Asistente Personal.

        ```
        {informacion}
        ```

        Proporciona solo la respuesta, sin explicaciónes adicionales.
        """

        final_prompt = template.format(informacion=informacion)

        response = get_response(final_prompt)

        return response
    
    # funcion para procesar toda la informacion
    def agent_org(self, info):
        self.gen_json_file(info, self.rec_file_path)

        informacion_recuperada = self.read_json_file(self.rec_file_path)

        estructurada = self.structure(informacion_recuperada)

        self.gen_json_file(estructurada, self.estruc_file_path)

        informacion_estructurada = self.read_json_file(self.estruc_file_path)

        informacion_organizada = self.organice_information(informacion_estructurada)

        self.gen_json_file(informacion_organizada, self.org_file_path)

        informacion_organizada = self.read_json_file(self.org_file_path)

        resumen = self.generate_resume(informacion_organizada)

        return resumen