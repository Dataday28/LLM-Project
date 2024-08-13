from llm.gemini import get_response
from agentes.agente_personalizacion import AgentPers
from agentes.agente_recuperacion import Agent_Rec
from agentes.agente_organizacion import Agent_Org
from agentes.agente_generacion import AgenteGen

class AgentDialg:

    def respuesta(self, question):
        template_rag = """
        Eres un asistente personal.
        Tu trabajo sera analisar la pregunta del usuario basado en una agenda y responder dependiendo a las instrucciones de abajo.

        1. Analizaras si la pregunta es una consulta a la agenda o es una instrucion de modificar, agregar o eliminar datos de la agenda.
        2. Si la pregunta tiene que ver con una consulta imprimiras la palabra entre comillas: "consulta"
        3. Si la pregunta tiene que ver con una instrucion imprimiras la palabra entre comillas: "instrucion"
        4. Si la pregunta no tiene que ver con una consulta ni con una instrucion imprimiras la palabra entre comillas: "nada"

        Pregunta: {question}
        """

        final_prompt = template_rag.format(question=question)

        response = get_response(final_prompt)

        return response

    def dialogue_normal(self, question):

        agent_pers = AgentPers().personalidad(question)

        return agent_pers

    def dialogue_add(self, question):

        agent_rag = Agent_Rec().add_or_mod_item(question)
        agent_pers = AgentPers().add_and_mod(agent_rag)

        return agent_pers


    def query_and_organize(self, question):

        agent_rag = Agent_Rec().rag_query_with_embeddings(question)
        agent_orga = Agent_Org().agent_org(agent_rag)
        gen_ideas = AgenteGen().generar_ideas(agent_orga)
        persona = AgentPers().consulta(gen_ideas)

        return persona



    # Función para interactuar con el agente
    def interact_with_agent(self):

        print(AgentPers().saludo())
        
        while True:
            user_input = input("Tú: ")

            if "salir" in user_input.lower() or "adios" in user_input.lower():
                print(AgentPers().despedida())
                break

            dialogue_org = self.respuesta(user_input)

            if "consulta" in dialogue_org:
                response = self.query_and_organize(user_input)
            elif "instrucion" in dialogue_org:
                response = self.dialogue_add(user_input)
            elif "nada" in dialogue_org:
                response = self.dialogue_normal(user_input)
            else:
                response = "Lo siento, no entiendo tu pregunta."

            print(f"Agente: {response}")
