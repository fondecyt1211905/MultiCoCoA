import sys, os
import json as js
import config
import helpers
import spacy
conf = config.CONFIG

globalcont=0
nlp = spacy.load("es_core_news_lg")
nlp.add_pipe("sentencizer")

class matriz:
    def __init__(self):
        self.matriz_similitud=list()
        self.matriz_cont=list()
        self.matriz_estado=list()
        self.usuarios=list()

    def print_matriz(self):
        print("-"*10)
        for i in self.matriz_similitud:
            print(i)

    def get_usuarios(self):
        aux=[]
        for i in self.usuarios:
            aux.append(i[0])
        return aux

    def get_matriz(self):
        aux=[]
        for i in self.matriz_similitud:
            aux2=[]
            for j in i:
                aux2.append(int(j*100))
            aux.append(aux2)
        return aux

    def print_contador(self):
        for i in self.matriz_cont:
            print(i)

    def print_estado(self):
        for i in self.matriz_estado:
            print(i)

    def agregar_usuario(self,nombre):
        for i in self.usuarios:
            if(i[0]==nombre):
                #print("el usuario ya existe")
                return 0
        self.usuarios.append([nombre,list()])
        if(len(self.matriz_similitud)<len(self.usuarios)):
            if(len(self.matriz_similitud)!=0):
                for i in range(len(self.matriz_similitud)):
                    self.matriz_similitud[i].append(0)
                    self.matriz_cont[i].append(0)
                    self.matriz_estado[i].append(0)
            x=list()
            for i in range(len(self.usuarios)-1):
                x.append(0)
            x.append(0)
            self.matriz_similitud.append(x.copy())
            self.matriz_cont.append(x.copy())
            self.matriz_estado.append(x.copy())

        return 0

    def agregar_palabra(self,nombre,palabra):
        indice=-1
        control=False
        for i in self.usuarios:
            indice=indice+1
            if(i[0]==nombre):
                control=True
                self.usuarios[indice][1].append(palabra)
                break
        if(control):
            for i in range(len(self.usuarios)):
                if(len(self.usuarios[i][1])==0 or self.usuarios[i][0]==nombre):
                    continue
                else:
                    if(self.matriz_similitud[i][indice]==0):
                        similitud=nlp(self.usuarios[i][1][len(self.usuarios[i][1])-1]).similarity(nlp(palabra))
                        self.matriz_similitud[i][indice]=similitud
                        self.matriz_estado[i][indice]=2
                        self.matriz_cont[i][indice]+=1
                    else:
                        similitud=((self.matriz_cont[i][indice]*self.matriz_similitud[i][indice])+nlp(self.usuarios[i][1][len(self.usuarios[i][1])-1]).similarity(nlp(palabra)))/(self.matriz_cont[i][indice]+1)
                        if(self.matriz_similitud[i][indice]>similitud):
                            self.matriz_estado[i][indice]=0
                        elif(self.matriz_similitud[i][indice]==similitud):
                            self.matriz_estado[i][indice]=1
                        elif(self.matriz_similitud[i][indice]<similitud):
                            self.matriz_estado[i][indice]=2
                        self.matriz_similitud[i][indice]=similitud
                        self.matriz_cont[i][indice]+=1

class usuario:
    
    def __init__(self, nombre):
        self.nombre=nombre
        self.frases=list()
        self.metricas_frase=list()
        self.cantidad_palabras=[list(),list()]
        self.palabras_root=list()

    def getNombre(self):
        return self.nombre

    def getRoot(self):
        return self.palabras_root

    def agregarFrase(self,frase,metricas):
        self.frases.append(frase)
        self.metricas_frase.append(metricas)
        for i in metricas:
            if(i["metrics"]["dependencia"]=="ROOT"):
                global globalcont
                self.palabras_root.append(i["palabra"]+"_"+str(globalcont))
        for i in frase.split(" "):
            self.agregarPalabra(i)

    def getCantidadPalabras(self):
        return self.cantidad_palabras

    def getMetricas(self):
        return self.metricas_frase

    def agregarPalabra(self,palabra):
        if(palabra in self.cantidad_palabras[0]):
            indice=self.cantidad_palabras[0].index(palabra)
            self.cantidad_palabras[1][indice]+=1
        else:
            self.cantidad_palabras[0].append(palabra)
            self.cantidad_palabras[1].append(1)

    def getPalabras(self):
        return self.cantidad_palabras[0]

    def getFrases(self):
        return self.frases

    def getCantidad(self):
        return self.cantidad_palabras[1]

class usuarios:
    users=list()
    def agregar(self,usuario):
        self.users.append(usuario)

    def esta(self,usuario):
        for i in self.users:
            if(i.getNombre()==usuario.getNombre()):
                return True
        return False

    def getIndice(self,usuario):
        contador=0
        for i in self.users:
            if(i.getNombre()==usuario.getNombre()):
                return contador
            contador=contador+1
        return None

    def modificar(self, users):
        self.users=users

    def getLista(self):
        return self.users

    def __iter__(self):
        self.cont=0
        return self

    def getUsuarios(self):
        aux=list()
        for i in self.users:
            aux.append(i.getNombre())
        return aux

    def __next__(self):
        if(self.cont<len(self.users)):
            retorno=self.users[self.cont]
            self.cont+=1
            return retorno
        else:
            raise StopIteration

users=usuarios()
m=matriz()

def main():
    # Connection
    channel = helpers.connect(conf["user"], conf["password"], conf["host"], conf["port"],conf["timeout"])
    # Declare
    channel = helpers.declare(channel, conf["exchange_direct"], "direct", conf["queue11"])

    def callback(ch, method, properties, body):
        global globalcont
        global users
        global m
        if helpers.is_reset(body):
            globalcont = 0
            users=usuarios()
            m=matriz()
            channel.basic_publish(exchange=conf["exchange_direct"], routing_key=conf["queue16"], body=body)
            return
        if helpers.is_save(body):
            channel.basic_publish(exchange=conf["exchange_direct"], routing_key=conf["queue16"], body=body)
            return
        message = js.loads(body) #Le puse nombre message ya que son muchos cambios
        user=usuario(str(int(message["id_device"]))+"_"+str(message["active_voice"]))
        user.agregarFrase(message["data"]["frase"],message["data"]["data"])
        if(users.esta(user)):
            indice=users.getIndice(user)
            if(indice!=None):
                lista=users.getLista()
                lista[indice].agregarFrase(message["data"]["frase"],message["data"]["data"])
                users.modificar(lista)
        else:
            users.agregar(user)
        
        for i in message["data"]["data"]:
            if(i["metrics"]["dependencia"]=="ROOT"):
                m.agregar_usuario(str(int(message["id_device"]))+"_"+str(message["active_voice"]))
                m.agregar_palabra(str(int(message["id_device"]))+"_"+str(message["active_voice"]),i["palabra"])
                break
        matriz1=m.get_matriz()
        usuarios1=m.get_usuarios()
        aux2=list()
        for i in range(len(usuarios1)):
            aux=list()
            for j in range(len(usuarios1)):
                if(usuarios1[i]==usuarios1[j]):
                    continue
                jeysonaux={
                        'subject': usuarios1[j],
                        'A': int(matriz1[i][j]),
                        'fullMark': 100,
                }
                aux.append(jeysonaux)
            aux2.append(aux)
        Usuarios_tematica=list()
        contador_tematica=list()
        return_tematica=list()
        colores=["#1f77b4","#fe7f0d","#2b9f2b","#d62728","#9467bd","#8c564b","#e276c1","#7f7f7f","#a90cfd","#1f519e","#85660d","#782ab5","#565656","#1c8356","#15fe32","#f7e1a0"]
        temas=conf["tematica"]
        margen=conf["margen"]
        for j in message["data"]["frase"].split(" "):
            for k in temas:
                if(nlp(j).similarity(nlp(k))>=margen):
                    json={}
                    if(str(int(message["id_device"]))+"_"+str(message["active_voice"]) in Usuarios_tematica):
                        indice=Usuarios_tematica.index(str(int(message["id_device"]))+"_"+str(message["active_voice"]))
                        contador_tematica[indice]+=1
                        json["name"]=str(int(message["id_device"]))+"_"+str(message["active_voice"])
                        json["value"]=contador_tematica[indice]
                        return_tematica[indice]=json
                    else:
                        Usuarios_tematica.append(str(int(message["id_device"]))+"_"+str(message["active_voice"]))
                        contador_tematica.append(1)
                        json["name"]=str(int(message["id_device"]))+"_"+str(message["active_voice"])
                        json["value"]=1
                        return_tematica.append(json)
        
        colors_aux=list()
        for j in range(len(m.get_usuarios())):
            colors_aux.append(colores[j])
        matrizc=m.get_matriz()
        for j in range(len(matrizc)):
            for k in range(len(matrizc[j])):
                if(matrizc[j][k]<0):
                    matrizc[j][k]=0
        radarchart={'data':aux2}
        jeyson1={
                'radar-chart':radarchart,
                'usuarios':m.get_usuarios(),
                'pie-chart': return_tematica,
                'matriz': m.get_matriz(),
                'colores': colors_aux,
                'matriz_chord':matrizc,
            }
        jeyson={
            'name':message["name"],
            'id_device': message["id_device"],
            'start_time':message["start_time"],
            'end_time':message["end_time"],
            'data':jeyson1,
            }
        channel.basic_publish(exchange=conf["exchange_direct"], routing_key=conf["queue16"], body=js.dumps(jeyson))
        globalcont = globalcont + 1
    channel.basic_consume(queue=conf["queue11"], on_message_callback=callback, auto_ack=True)
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