from agentes.agente_personalizacion import AgentPers
from agentes.agente_recuperacion import AgentRec
from agentes.agente_organizacion import AgentOrg
from agentes.agente_generacion import AgenteGen
from agentes.agente_dialogo import AgentDialg

def main():
    agent_org = AgentOrg()
    agent_rec = AgentRec()
    agent_pers = AgentPers()
    agent_gen = AgenteGen()
    agent_dialg = AgentDialg()

    agent_dialg.interact_with_agent()


if __name__ == '__main__':
    main()