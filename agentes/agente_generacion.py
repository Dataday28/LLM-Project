from llm.gemini import get_response_creative

class AgenteGen:

    def generar_ideas(self, informacion):

        template_rag = """
        Eres un asistente personal.
        Tu trabajo sera generar ideas, sugerencias o soluciones creativas basandote en la informacion proporcionada.

        Primero mostraras la informacion proporcionada.
        despues usa 2 0 3 horaciones para generar ideas, sugerencias o soluciones creativas de la informacion proporcionada.

        Utiliza frases o oraciones como: "Le suguiero", "Le aconsejo", "Puedes intentar", etc.
        Entre cada ideas, sugerencias o soluciones creativa utiliza contectores.
        Evita mostrar etiquetas como: "## Información:", "## Ideas:", "## Sugerencias:", "## Soluciones Creativas:"

        Si no tienes ideas, sugerencias o soluciones creativas, no respondas, solo muestra la informacion proporcionada.

        Informacion:{informacion}


        """

        final_prompt = template_rag.format(informacion=informacion)

        response = get_response_creative(final_prompt)

        return response