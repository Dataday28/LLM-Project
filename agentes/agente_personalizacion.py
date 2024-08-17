from llm.gemini import get_response
from datetime import datetime

class AgentPers:
    
    def obtener_fecha_hora_actual(self):
        ahora = datetime.now()
        fecha_hora_formateada = ahora.strftime("%Y-%m-%d %H:%M:%S")
        return fecha_hora_formateada

    def greeting(self):

        template = """
        Eres un asistente personal.
        Seras un asistente con una actitud seria y formal.

        Tu trabajo sera generar un saludo.

        """

        final_prompt = template.format()

        response = get_response(final_prompt)

        return response

    def farewell(self):

        template = """
        Eres un asistente personal.
        Seras un asistente con una actitud seria y formal.

        Tu trabajo sera generar una despedida aleatoria.
        """

        final_prompt = template.format()

        response = get_response(final_prompt)

        return response

    def personality(self, question):

        date = self.obtener_fecha_hora_actual()

        template = """
        Eres un asistente personal.
        Apartir de ahora responderas todas las preguntas de manera seria y formal.
        Utilizaras fecha_hora para responder preguntas o temas acerca de la fecha y hora. 
        Darás respuestas cortas y fáciles de entender.

        Pregunta: {question}
        fecha_hora: {date}
        """

        final_prompt = template.format(question=question, date=date)

        response = get_response(final_prompt)

        return response

    def add_and_mod(self, informacion):

        template_rag = """
        Eres un asistente personal.
        Seras un asistente con una actitud seria y formal.

        Recibiras informacion, donde se trate de un mensaje de exito o un error.
        Tu trabajo sera generar un mensaje dependiendo de la informacion.

        Si es un mensaje de exito, genera un mensaje como: "Lo cambios se han realizado con exito".
        Si es un mensaje de error, genera un mensaje como: "Ha ocuurido un error, lo siento, vuelva a intentar".

        informacion:{informacion}
        """

        final_prompt = template_rag.format(informacion=informacion)

        response = get_response(final_prompt)

        return response

    def consultation(self, informacion):

        template_rag = """
        Eres un asistente personal.
        Seras un asistente con una actitud seria y formal.

        Recibiras informacion.
        La informacion contiene un resumen y algunas sugerencias de una agenda.

        Redacta la informacion en un tono amigable y formal.

        Evita mostrar etiquetas como: "## Información y Sugerencias", **Información:**:

        Informacion:{informacion}


        """

        final_prompt = template_rag.format(informacion=informacion)

        response = get_response(final_prompt)

        return response
    