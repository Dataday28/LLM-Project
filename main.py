from agentes.agente_personalizacion import AgentPers
from agentes.agente_recuperacion import Agent_Rec
from agentes.agente_organizacion import Agent_Org
from agentes.agente_generacion import AgenteGen
from agentes.agente_dialogo import AgentDialg

def main():
    agent_org = Agent_Org()
    agent_rec = Agent_Rec()
    agent_pers = AgentPers()
    agent_gen = AgenteGen()
    agent_dialg = AgentDialg()

    agent_dialg.interact_with_agent()


if __name__ == '__main__':
    main()