# Distributed Computation
## Proffessor:
Diogo Gomes & Nuno Lau

## Tests:

run `pytest`


## Diagram:

```https://www.websequencediagrams.com```
title Message Broker

note left of Consumer: Connection estabilished
Consumer->Broker: Announce Serialization Mechanism

note left of Consumer: Can subscribe to topics any time

Consumer->Broker: Subscribe to topic X
Broker->Consumer: Send Last saved message in X

note right of Broker: List just the topic names

Consumer->Broker: Request list of all topics
Broker->Consumer: Response list of all topics

note left of Producer: Connection estabilished

Producer -> Broker: Announce Serialization Mechanism
Producer -> Broker: Publish message to topic X

Broker ->Consumer: Send message to consumer
Consumer -> Broker: Cancel topic X subscriptionCancel changes

Producer -> Broker: Publish message to topic X
note left of Consumer: Doesn't receive last message


## About
### Team
Mariana Rosa
Pedro Lopes

### Clarifications

	O nosso protocolo é composto por um conjunto de mensagens. Cada uma com um certo método a invocar, à medida que o programa necessita.

	Há 3 tipos de serializações possíveis: JSON, XML e Pickle. Definimos um Enum para cada um, para ao longo do programa poder existir diferentes tipos de mensagens e associar cada uma à sua descodificação/codificação correta.

	Posteriormente são enviadas em TCP na porta 1401.




|               Objetivo | Mensagem                                                             | Explicação                                                             |
|-----------------------:|----------------------------------------------------------------------|------------------------------------------------------------------------|
|   Get a topic Response | { "method" : "ACK_GET", "topic" : "topic_name", "topic" : "value" }  | Retorna um valor do tópico associado                                   |
|            Put a topic | { "method" : "PUT_TOPIC", "topic" : "topic_name", "value": "Value" } | Insere um novo tópico (caso ele não exista) juntamente com o seu valor |
|     List of all topics | { "method" : "LIST_TOPICS" }                                         | Pede a lista de todos os tópicos                                       |
| List of all topics REP | { "method" : "ACK_LIST", "topics" : "allTopicsAndSubtopics"  }       | Retorna todos os tópicos e subtópicos                                  |
|              Subscribe | { "method" : "SUBSCRIBE", "topic" : "topic_name"}                    | Subscreve a um certo tópico                                            |
|            Unsubscribe | { "method" : "UNSUBSCRIBE", "topic" : "topic_name"}                  | Deixa de subscrever a um certo tópico (não recebe as mensagens)        |
