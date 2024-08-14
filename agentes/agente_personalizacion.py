from llm.gemini import get_response

class AgentPers:

    def greeting(self):

        template_rag = """
        Eres un asistente personal.
        Seras un asistente con una actitud seria y formal.

        Tu trabajo sera generar un saludo.

        """

        final_prompt = template_rag.format()

        response = get_response(final_prompt)

        return response

    def farewell(self):

        template_rag = """
        Eres un asistente personal.
        Seras un asistente con una actitud seria y formal.

        Tu trabajo sera generar una despedida aleatoria.
        """

        final_prompt = template_rag.format()

        response = get_response(final_prompt)

        return response

    def personality(self, question):

        template_rag = """
        Eres un asistente personal.
        Apartir de ahora responderas todas las preguntas de manera seria y formal.
        Darás respuestas cortas y fáciles de entender.

        Pregunta: {question}
        """

        final_prompt = template_rag.format(question=question)

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