from llm.gemini import get_response
from agentes.agente_personalizacion import AgentPers
from agentes.agente_recuperacion import AgentRec
from agentes.agente_organizacion import AgentOrg
from agentes.agente_generacion import AgenteGen
import time

class AgentDialg:

    # Imprime el texto lentamente
    def print_slowly(self, text, delay=0.03):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    # Por medio del LLM analisa la clase de pregunta 
    def answer(self, question):
        template = """
        Eres un asistente personal.
        Tu trabajo sera analisar la pregunta del usuario basado en una agenda y responder dependiendo a las instrucciones de abajo.

        1. Analizaras si la pregunta es una consulta a la agenda o es una instrucion de modificar, agregar o eliminar datos de la agenda.
        2. Si la pregunta tiene que ver con una consulta imprimiras la palabra entre comillas: "consulta"
        3. Si la pregunta tiene que ver con una instrucion imprimiras la palabra entre comillas: "instrucion"
        4. Si la pregunta no tiene que ver con una consulta ni con una instrucion imprimiras la palabra entre comillas: "nada"

        Pregunta: {question}
        """

        final_prompt = template.format(question=question)

        response = get_response(final_prompt)

        return response

    # Funciones para dialogar normalmente 
    def dialogue_normal(self, question):

        agent_pers = AgentPers().personality(question)

        return agent_pers

    # funcion para agregar o modificar la informacion
    def dialogue_add(self, question):

        agent_rag = AgentRec().add_or_mod_item(question)
        agent_pers = AgentPers().add_and_mod(agent_rag)

        return agent_pers


    # funcion para hacer una consulta con RAG
    def query_and_organize(self, question):

        agent_rag = AgentRec().rag_query_with_embeddings(question)
        agent_orga = AgentOrg().generate_resume(agent_rag)
        gen_ideas = AgenteGen().generate_ideas(agent_orga)
        persona = AgentPers().consultation(gen_ideas)

        return persona



    # Función para interactuar con el agente
    def interact_with_agent(self):

        query = AgentPers().greeting()
        self.print_slowly(f"\n {str(query)}")
        
        while True:
            user_input = input("Tú: ")

            if "salir" in user_input.lower() or "adios" in user_input.lower():
                query = AgentPers().farewell()
                self.print_slowly(f"\n {str(query)}")
                break

            dialogue_org = self.answer(user_input)

            if "consulta" in dialogue_org:
                query = self.query_and_organize(user_input)
                response = str(query)
            elif "instrucion" in dialogue_org:
                query = self.dialogue_add(user_input)
                response = str(query)
            elif "nada" in dialogue_org:
                query = self.dialogue_normal(user_input)
                response = str(query)
            else:
                response = "Lo siento, no entiendo tu pregunta."

            self.print_slowly(f"\n Agente: {response}")
