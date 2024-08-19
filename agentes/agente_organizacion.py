from llm.gemini import get_response



class AgentOrg:

    def generate_resume(self, informacion):

        # Generar la respuesta utilizando el LLM
        template = """Tu trabajo sera organizar la informacion proporcionada y despues haras un resumen.
        Solo deberas proporcionar el resumen.
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