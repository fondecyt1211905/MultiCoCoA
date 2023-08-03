from flask import request, jsonify, send_file
from mongoengine import ValidationError
from database.models import Analysis
from bson.objectid import ObjectId
from controllers.drawtodf import get_df, concat_df_apm, process_data_head
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import io
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout

listcolor = sns.color_palette("Set3")
listcolor2 = sns.color_palette("Set1")

def validate_id_analysis(id_analysis):
    # validar id_analysis existe
    try:
        analysis = Analysis.objects(id=ObjectId(id_analysis)).first()
    except ValidationError:
        return None
    return analysis

def get_chart_segmentation(id_analysis):
    if request.method == "GET":
        indicator_name = "Audio-Segmentation"
        analysis = validate_id_analysis(id_analysis)

        if analysis is None:
            return jsonify({'message': 'Bad request, code 2'}), 400
        
        if indicator_name in analysis.indicators:
            df = get_df(indicator_name, id_analysis)
            
            fig, ax = plt.subplots(figsize=(12,3))
            labelUser = df['active_voice'].dropna().unique()
            maxvalue = labelUser.max()
            for i, user in enumerate(labelUser):
                print(i, user)
                t_df = df.loc[df["active_voice"] == i + 1]
                ax.broken_barh([(x,y) for x,y in zip(t_df['start'],t_df['speaking_time'])], (i+0.5, 1), facecolors=listcolor[i])
            ax.set_title('Segments of spoken interventions')
            ax.set_ylabel('Speaker')
            ax.set_ylim([0.5,maxvalue+0.5])
            #definir numero de tick
            ax.set_yticks(np.arange(1, maxvalue+1, 1))

            ax.set_xlabel('Time (s)')

            img_bytes = io.BytesIO()
            fig.savefig(img_bytes, bbox_inches='tight')
            img_bytes.seek(0)
            fig.clf()
            return send_file(img_bytes, mimetype='image/png')
        else:
            return jsonify({'message': 'Indicator not found'}), 404
    else:
        return jsonify({'message': 'Bad request, code 3'}), 400

def get_chart_vocal_activity(id_analysis):
    if request.method == "GET":
        indicator_name = "VAD-DOA-Features"
        analysis = validate_id_analysis(id_analysis)
        if analysis is None:
            return jsonify({'message': 'Bad request, code 2'}), 400
        if indicator_name in analysis.indicators:
            df = get_df(indicator_name, id_analysis)

            fig, ax = plt.subplots(figsize=(12,3))
            df = df.loc[df['speech_count'] > 5]
            ax.scatter(df["start"], df["direction"], 0.5, color=listcolor2[1])
            ax.set_title('Direction of arrival of the sound source')
            ax.set_ylabel('Direction (degree)')
            ax.set_ylim([0,360])
            ax.set_xlabel('Time (s)')

            img_bytes = io.BytesIO()
            fig.savefig(img_bytes, bbox_inches='tight')
            img_bytes.seek(0)
            fig.clf()
            return send_file(img_bytes, mimetype='image/png')
        else:
            return jsonify({'message': 'Indicator not found'}), 404
    else:
        return jsonify({'message': 'Bad request, code 3'}), 400

def get_chart_apm(id_analysis):
    if request.method == "GET":
        indicator_name = "Acoustic-Prosodic-Features"
        indicator_name2 = "Audio-Segmentation"
        analysis = validate_id_analysis(id_analysis)
        if analysis is None:
            return jsonify({'message': 'Bad request, code 2'}), 400
        if indicator_name in analysis.indicators:
            df = get_df(indicator_name, id_analysis)
            df2 = get_df(indicator_name2, id_analysis)
            df = concat_df_apm(df2,df)


            F0final_sma_amean = np.unique(df['F0final_sma_amean'].values)
            fig, ax = plt.subplots(figsize=(12,3))
            labelUser = df2['active_voice'].dropna().unique()
            for j in labelUser:
                for i in F0final_sma_amean:
                    t_df = df.loc[(df["F0final_sma_amean"] ==  i) & (df["active_voice"] == int(j)+1)]
                    ax.broken_barh([(x,y) for x,y in zip(t_df['start'],t_df['speaking_time'])], (i, 3), facecolors=listcolor[int(j)])
            ax.set_title('Segments of spoken interventions in contrast to Fundamental frequency mean')
            ax.set_ylabel('Fundamental frequency')
            # ax.set_ylabel('Speaker')
            # ax.set_ylim([0.5,6.5])
            for i in labelUser:
                ax.plot([], [], color=listcolor[int(i)], label=f'User {int(i)+1}')
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

            # ax.plot([], [], color=listcolor2[0], label='mean')
            # ax.legend()

            img_bytes = io.BytesIO()
            fig.savefig(img_bytes, bbox_inches='tight')
            img_bytes.seek(0)
            fig.clf()
            return send_file(img_bytes, mimetype='image/png')
        else:
            return jsonify({'message': 'Indicator not found'}), 404
    else:
        return jsonify({'message': 'Bad request, code 3'}), 400

def get_chart_head_sight(id_analysis):
    if request.method == "GET":
        indicator_name = "HeadSight-Features"
        analysis = validate_id_analysis(id_analysis)
        if analysis is None:
            return jsonify({'message': 'Bad request, code 2'}), 400
        if indicator_name in analysis.indicators:
            df = get_df(indicator_name, id_analysis)
            df = process_data_head(df)
            num_user = 0
            for i in range(1,7):
                try:
                    a = df[i]
                    num_user += 1
                except KeyError:
                    break
            fig, ax = plt.subplots(figsize=(12,3))
            for i in df.index:
                for j in range(1,num_user+1):
                    if df[j][i] == True:
                        aux = df.loc[df[j] == True, ['start',f'{j}-x',f'{j}-y',f'{j}-w',f'{j}-h',f'{j}-is_confirmed',f'{j}-is_tentative',f'{j}-distanceToObservedUser',f'{j}-ObservedUser']]
                        aux.columns = ['start','x','y','w','h','is_confirmed','is_tentative','distanceToObservedUser','ObservedUser']
                        try:
                            observed = int(aux["ObservedUser"][i])
                        except ValueError:
                            continue
                        ax.broken_barh([(aux["start"][i], 0.2)], (j-0.5, 1), facecolors=listcolor[observed-1])

            #set title
            ax.set_title('Observed User')
            #set x label
            ax.set_xlabel('Time (s)')
            #set y label
            ax.set_ylabel('Observer')
            # set legend
            for i in range(0,num_user):
                ax.plot([], [], color=listcolor[int(i)], label=f'User {int(i+1)}')
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

            img_bytes = io.BytesIO()
            fig.savefig(img_bytes, bbox_inches='tight')
            img_bytes.seek(0)
            fig.clf()
            return send_file(img_bytes, mimetype='image/png')
        else:
            return jsonify({'message': 'Indicator not found'}), 404
    else:
        return jsonify({'message': 'Bad request, code 3'}), 400

def get_chart_graph(id_analysis):
    if request.method == "GET":
        indicator_name = "Audio-Segmentation"
        analysis = validate_id_analysis(id_analysis)
        if analysis is None:
            return jsonify({'message': 'Bad request, code 2'}), 400
        if indicator_name in analysis.indicators:
            df = get_df(indicator_name, id_analysis)
            # agrupar por usuario
            df_node = df.groupby(['active_voice']).agg({'start': 'min', 'end': 'max', 'speaking_time': 'sum', 'active_voice': 'max'})
            df_node["label"] = [f"User {int(i)}" for i in df_node["active_voice"]]

            # crear relaciones entre usuarios
            df_edge = df.dropna(subset=["active_voice"])
            df_edge = df_edge.rename(columns={"active_voice": "source"})
            # create target
            df_edge["target"] = df_edge["source"].shift(-1)
            df_edge = df_edge.groupby(['source', 'target']).agg({'source': 'max', 'target': 'max', 'speaking_time': 'count'})
            # remove if source == target
            df_edge = df_edge[df_edge["source"] != df_edge["target"]]
            # cambiar columna speaking_time por weight
            df_edge = df_edge.rename(columns={"speaking_time": "weight"})
            # Normalizar peso
            df_edge["weight"] = df_edge["weight"].apply(lambda x: (x - df_edge["weight"].min()) / (df_edge["weight"].max() - df_edge["weight"].min()))
            # cambiar columa source y target por int
            df_edge["source"] = df_edge["source"].astype(int)
            df_edge["target"] = df_edge["target"].astype(int)

            # create grafo
            G = nx.DiGraph()
            nodescolor = []
            node_labels = {}
            node_sizes = []

            # add nodes
            for i, node in df_node.iterrows():
                G.add_node(int(i))
                nodescolor.append(listcolor[int(i)-1])
                node_sizes.append(node["speaking_time"]*10)
                node_labels[int(i)] = f"User {int(i)}"
            # add edges
            edges = df_edge.values.tolist()
            G.add_weighted_edges_from(edges)

            # Dibujamos el grafo
            fig, ax = plt.subplots(figsize=(5, 5))
            pos = nx.circular_layout(G, scale=1)  # Calculamos la posición de los nodos
            nx.draw_networkx_nodes(G, pos, ax=ax, node_color=nodescolor, node_size=node_sizes)
            nx.draw_networkx_labels(G, pos, ax=ax, labels=node_labels, )
            
            # draw edge labels
            arc_rad = 0.25
            for (u, v, d) in G.edges(data=True):
                nx.draw_networkx_edges(G, pos, ax=ax, edgelist=[(u, v)], width=((d['weight'] * 2) + 0.1), connectionstyle=f'arc3, rad = {arc_rad}', min_target_margin=30)

            # Ajustamos los límites del gráfico para alejar los nodos del borde
            padding = 0.4 # Valor de espacio adicional alrededor del gráfico
            ax.set_xlim(min(x for x, y in pos.values()) - padding, max(x for x, y in pos.values()) + padding)
            ax.set_ylim(min(y for x, y in pos.values()) - padding, max(y for x, y in pos.values()) + padding)

            #set title
            ax.set_title('Graph of the conversation')

            # Guardamos el grafo como una imagen
            img_bytes = io.BytesIO()
            fig.savefig(img_bytes, bbox_inches='tight')
            img_bytes.seek(0)
            fig.clf()
            return send_file(img_bytes, mimetype='image/png')
        else:
            return jsonify({'message': 'Indicator not found'}), 404
    else:
        return jsonify({'message': 'Bad request, code 3'}), 400