# Asistente Personal

Este proyecto es un asistente personal en cual puedes gestionar una agenda.
El objetivo de este proyecto es crear un asistente con un LLM que te pueda ayudar a gestionar una eventos o tareas de una agenda por medio de lenguaje natural.

# Instrucciones

Para ejecutar es necesario modificar el archivo Gemini que esta en el folder de llm y agregar una api key de Gemini.
Tambien pudes modificarlo al LLM que desees solo modifoca el archivo o crea uno nuevo.
Ya teniendo una api key de cualquier modelo, solo es necesario ejecutar el main en una consola.

# Ejemplo de Uso

Con este asistente puedes hacer preguntas que acualquier chatbot le puedes hacer.

Por Ejemplo: 
"¿Que es un LLM?"
"¿Cuanto es 2 + 2?"

La diferencia es que hay un archivo JSON que almacena datos de tareas, eventos y fechas importantes.
El asistente hacer consultas en ese archivo JSON, genera un resumen y despues te hace algunas suguerencias.
Para que te diga informacion del archivo JSON solo haz preguntas hacerca de la agenda.

Por Ejemplo: 
"¿Que tareas hay?"
"¿Que eventos tengo?"

Por medio del asistente puedes modificar o agregar mas tareas, eventos o  fechas importantes.

Por Ejemplo: 
"La tarea de actualizar el sitio web cambialo a prioridad alta"
"Agrega una nueva fecha importante con el nombre de vacaciones con la fecha de 1 de diciembre del 2024"

# Tecnologias utilizadas
- Python
- Gemini
  
