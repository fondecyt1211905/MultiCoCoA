import sys, os
import json
import config
import helpers
import spacy
conf = config.CONFIG

#Configurations for the pipeline
exchange_in = conf["nlp_in_ex"]
type_exchange_in = conf["nlp_in_ex_type"]
queue_in = conf["nlp_in_q"]
exchange_out = conf["nlp_out_ex"]
queue_out = conf["nlp_out_q"]

nlp = spacy.load("es_core_news_lg")
nlp.add_pipe("sentencizer")

def token_morph(token):
    lista=list()
    for i in token.morph:
        lista.append(i)
    return lista

def tag_to_takataka(tag,info):
    tag=str(tag).upper()
    if(tag=="ADJ"):
        if(info):
            return ["ADJ","Adjetivo","Clase de palabra que acompaña al sustantivo para expresar una cualidad de la cosa designada por él o para determinar o limitar la extensión del mismo."]
        else:
            return ["ADJ","Adjetivo"]
    elif(tag=="ADV"):
        if(info):
            return ["ADV","Adverbio","Palabra invariable que modifica a un verbo, a un adjetivo, a otro adverbio o a todo un período; pueden indicar lugar, tiempo, modo, cantidad, afirmación, negación, duda y otros matices."]
        else:
            return ["ADV","Adverbio"]
    elif(tag=="INTJ"):
        if(info):
            return ["INTJ","Interjeccion","Palabra o expresión que, pronunciada en tono exclamativo, expresa por sí sola un estado de ánimo o capta la atención del oyente; se escriben entre signos de admiración."]
        else:
            return ["INTJ","Interjeccion"]
    elif(tag=="NOUN"):
        if(info):
            return ["NOUN","Sustantivo","Los sustantivos son palabras cuyos referentes son clases de entidades fijas"]
        else:
            return ["NOUN","Sustantivo"]
    elif(tag=="PROPN"):
        if(info):
            return ["PROPN","Sustantivo_Propio","Un nombre propio es el nombre de una entidad específica"]
        else:
            return ["PROPN","Sustantivo_Propio"]
    elif(tag=="VERB"):
        if(info):
            return ["VERB","Verbo","El verbo es la parte de la oración que expresa una acción"]
        else:
            return ["VERB","Verbo"]
    elif(tag=="ADP"):
        if(info):
            return ["ADP","Adposicion","es una clase de palabras que abarca aquellas partículas que permiten expresar los roles semánticos de las frases o palabras a las que están asociadas, en especial relaciones espaciales o temporales."]
        else:
            return ["ADP","Adposicion"]
    elif(tag=="AUX"):
        if(info):
            return ["AUX","Auxiliar","Un auxiliar es una palabra funcional que acompaña al verbo léxico de una frase verbal y expresa distinciones gramaticales que no lleva el verbo léxico, como persona, número, tiempo, modo, aspecto, voz o evidencialidad."]
        else:
            return ["AUX","Auxiliar"]
    elif(tag=="CCONJ"):
        if(info):
            return ["CCONJ","Conjuncion_De_Coordinacion","“Las conjunciones coordinantes enlazan palabras, grupos sintácticos u oraciones, sin establecer ninguna relación de dependencia: sintácticamente, los elementos enlazados son del mismo nivel, o sea, son elementos equifuncionales"]
        else:
            return ["CCONJ","Conjuncion_De_Coordinacion"]
    elif(tag=="DET"):
        if(info):
            return ["DET","Determinante","Los determinantes son palabras que modifican sustantivos o frases nominales y expresan la referencia de la frase nominal en contexto. Es decir, un determinante puede indicar si el sustantivo se refiere a un elemento definido o indefinido de una clase, a un elemento más cercano o más lejano, a un elemento perteneciente a una persona o cosa específica, a un número o cantidad particular, etc."]
        else:
            return ["DET","Determinante"]
    elif(tag=="NUM"):
        if(info):
            return ["NUM","Numeral","Un numeral es una palabra, que normalmente funciona como determinante, adjetivo o pronombre, que expresa un número y una relación con el número, como cantidad, secuencia, frecuencia o fracción."]
        else:
            return ["NUM","Numeral"]
    elif(tag=="PART"):
        if(info):
            return ["PART","Particula","Las partículas son palabras funcionales que deben asociarse con otra palabra o frase para impartir significado y que no satisfacen las definiciones de otras partes universales del discurso"]
        else:
            return ["PART","Particula"]
    elif(tag=="PRON"):
        if(info):
            return ["PRON","Pronombre","Los pronombres son palabras que sustituyen a sustantivos o frases nominales, cuyo significado es recuperable del contexto lingüístico o extralingüístico."]
        else:
            return ["PRON","Pronombre"]
    elif(tag=="SCONJ"):
        if(info):
            return ["SCONJ","Conjuncion Subordinada","Una conjunción Subordinada es una conjunción que une construcciones haciendo que una de ellas sea constituyente de la otra. La conjunción subordinada típicamente marca el constituyente incorporado que tiene el estatus de una cláusula"]
        else:
            return ["SCONJ","Conjuncion Subordinada"]
    elif(tag=="PUNCT"):
        if(info):
            return ["PUNCT","Puntuacion","Los signos de puntuación son caracteres no alfabéticos y grupos de caracteres que se utilizan en muchos idiomas para delimitar unidades lingüísticas en el texto impreso."]
        else:
            return ["PUNCT","Puntuacion"]
    elif(tag=="SYM"):
        if(info):
            return ["SYM","Simbolo","Un símbolo es una entidad parecida a una palabra que se diferencia de las palabras ordinarias por su forma, función o ambas."]
        else:
            return ["SYM","Simbolo"]
    elif(tag=="X"):
        if(info):
            return ["X","NA(spacy)","La etiqueta X se utiliza para palabras a las que, por alguna razón, no se les puede asignar una categoría de parte del discurso real. Debe usarse de forma muy restrictiva."]
        else:
            return ["X","NA(spacy)"]
    else:
        if(info):
            return [tag,"NA","No se encontro nada para identificar esta etiqueta"]
        else:
            return [tag,"NA"]

def main():
    # Connection
    con, channel = helpers.connect(conf["rabbitmq_user"], conf["rabbitmq_password"], conf["rabbitmq_host"], conf["rabbitmq_port"],conf["rabbitmq_timeout"])
    # Declare
    channel = helpers.declare(channel, exchange_in, type_exchange_in, queue_in)

    def callback(ch, method, properties, body):
        if helpers.is_reset(body):
            channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=body)
            return
        if helpers.is_save(body):
            channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=body)
            return
        datos = json.loads(body)
        text = datos["data"]
        doc = nlp(text)
        metrics = list()
        for i in doc:
             metrics.append({
                'palabra':str(i.text),
                'metrics':  {
                    "Part_of_speech":   tag_to_takataka(i.pos_,False),
                    "Forma_base":       i.lemma_,
                    "morph":            token_morph(i),
                    "dependencia":      i.dep_
                }
            }) 
        data = {  
            'frase': text,
            'data': metrics
        }
        jeyson = {
            'name':datos["name"],
            'id_device': datos["id_device"],
            'active_voice':  datos["active_voice"],
            'start_time':datos["start_time"],
            'end_time':datos["end_time"],
            'data': data
        }
        channel.basic_publish(exchange=exchange_out, routing_key=queue_out, body=json.dumps(jeyson))

    channel.basic_consume(queue=queue_in, on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C', flush=True)
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)