from llm.gemini import get_response
import json
import re
import os


class Agent_Org:

    current_dir = os.path.dirname(__file__)
    rec_file_path = os.path.join(current_dir, '../documentos/informacion_recuperada.json')
    estruc_file_path = os.path.join(current_dir, '../documentos/informacion_estructurada.json')
    org_file_path = os.path.join(current_dir, '../documentos/informacion_organizada.json')

    def gen_pdf(self, archivo, name):
        with open(name, 'w') as file:
            json.dump(archivo, file, ensure_ascii=False, indent=4)

    # Cargar la información desde el archivo JSON
    def read_pdf(self, archivo):
        with open(archivo, 'r') as file:
            informcion  = json.load(file)
        return informcion
    

    def estructura(self, informacion):

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

        def extraer_detalles(patron, texto):
            return re.search(patron, texto).group(1) if re.search(patron, texto) else None

        # Extraer detalles de fechas importantes
        detalles_fechas_importantes = [{"descripcion": extraer_detalles(r": (.*?) el", item), "fecha": extraer_detalles(r"el (\d{4}-\d{2}-\d{2})", item)} for item in organized_data["fechas_importantes"]]

        # Extraer detalles de eventos
        detalles_eventos = []
        for item in organized_data["eventos"]:
            detalles_eventos.append({
                "descripcion": extraer_detalles(r": (.*?) en", item),
                "ubicacion": extraer_detalles(r"en (.*?) el", item),
                "fecha": extraer_detalles(r"el (\d{4}-\d{2}-\d{2})", item),
                "hora": extraer_detalles(r"a las (\d{2}:\d{2})", item),
                "descripcion_detallada": extraer_detalles(r"Descripción: (.*)", item)
            })

        # Extraer detalles de tareas
        detalles_tareas = []
        for item in organized_data["tareas"]:
            detalles_tareas.append({
                "descripcion": extraer_detalles(r": (.*?) con", item),
                "fecha_limite": extraer_detalles(r"fecha límite (\d{4}-\d{2}-\d{2})", item),
                "prioridad": extraer_detalles(r"Prioridad: (\w+)", item),
                "estado": extraer_detalles(r"Estado: (\w+)", item)
            })

        # Guardar los detalles en un archivo JSON
        informacion_estructurada = {
            "fechas_importantes": detalles_fechas_importantes,
            "eventos": detalles_eventos,
            "tareas": detalles_tareas
        }

        return informacion_estructurada
    

    def organizar_informacion(self, informacion):
        informacion_organizada = {
            "Fechas Importantes": informacion.get("fechas_importantes", []),
            "Eventos": informacion.get("eventos", []),
            "Tareas": informacion.get("tareas", [])
        }
        return informacion_organizada
    

    def generar_resumen(self, informacion):

        # Generar la respuesta utilizando el LLM
        template_rag = """Tu trabajo sera generar un resumen de la informacion proporcionada.
        La informacion esta delimitado por las comillas invertidas.
        Contesta como si la respuesta la estuviera dando un Asistente Personal.

        ```
        {informacion}
        ```

        Proporciona solo la respuesta, sin explicaciónes adicionales.
        """

        final_prompt = template_rag.format(informacion=informacion)

        response = get_response(final_prompt)

        return response
    
    def agent_org(self, info):
        self.gen_pdf(info, self.rec_file_path)

        informacion_recuperada = self.read_pdf(self.rec_file_path)

        estructurada = self.estructura(informacion_recuperada)

        self.gen_pdf(estructurada, self.estruc_file_path)

        informacion_estructurada = self.read_pdf(self.estruc_file_path)

        informacion_organizada = self.organizar_informacion(informacion_estructurada)

        self.gen_pdf(informacion_organizada, self.org_file_path)

        informacion_organizada = self.read_pdf(self.org_file_path)

        resumen = self.generar_resumen(informacion_organizada)

        return resumen