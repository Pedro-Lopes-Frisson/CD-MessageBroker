O nosso protocolo é composto por um conjunto de mensagens. Cada uma com um certo método a invocar, à medida que o programa necessita.
	
	Há 3 tipos de serializações possíveis: JSON, XML e Pickle. Definimos um Enum para cada um, para ao longo do programa poder existir diferentes tipos de mensagens e associar cada uma à sua descodificação/codificação correta.
	
	Posteriormente são enviadas em TCP na porta 1401.
	



|          Objetivo      | 				Mensagem                                  |                             Explicação |
|-----------------------:|--|--
| Get a topic Response   | { "method" : "ACK_GET", "topic" : "topic_name", "topic" : "value" }    | Retorna um valor do tópico associado   |
| Put a topic            | { "method" : "PUT_TOPIC", "topic" : "topic_name", "value": "Value" }   | Insere um novo tópico (caso ele não exista) juntamente com o seu valor |
| List of all topics     | { "method" : "LIST_TOPICS" }                                           | Pede a lista de todos os tópicos |
| List of all topics REP | { "method" : "ACK_LIST", "topics" : "allTopicsAndSubtopics"  }         | Retorna todos os tópicos e subtópicos |
| Subscribe              | { "method" : "SUBSCRIBE", "topic" : "topic_name"} 		          | Subscreve a um certo tópico 				|
| Unsubscribe            | { "method" : "UNSUBSCRIBE", "topic" : "topic_name"}                    | Deixa de subscrever a um certo tópico (não recebe as mensagens) |





