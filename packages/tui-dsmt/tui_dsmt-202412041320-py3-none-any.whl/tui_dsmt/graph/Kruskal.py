from typing import Dict, List

import networkx as nx

from .html import graph_to_html
from ..jpanim import JupyterAnimation


class Kruskal(JupyterAnimation):
    def __init__(self, graph: nx.Graph, pos: Dict[str, List[float]]):
        # mirror vertically
        my_pos = {
            key: [value[0], -value[1]]
            for key, value in pos.items()
        }

        # graph to html
        html, css = graph_to_html(graph, my_pos, weights='weight', node_width='7.5rem', node_height='1.4rem')

        html += '<div class="weight-sum">Summe der Gewichte: {{ frame.sum }}</div>'

        css += '''
            .node-container .node {
                font-size: 0.8rem;
            }
            
            .node-container text {
                opacity: 0.8;
            }
        '''

        # initialization
        sum = 0

        frames = {
            'Kantenloser Graph': {
                **{
                    f'name_{node}': node
                    for node in graph.nodes
                },
                **{
                    f'node_{node}': {
                        'backgroundColor': '#aaaaaa'
                    }
                    for node in graph.nodes
                },
                **{
                    f'edge_{u}_{v}': {
                        'backgroundColor': '#dddddd',
                        'color': '#cacaca',
                        'size': 1
                    }
                    for u in graph.nodes
                    for v in graph.nodes
                },
                'sum': sum
            }
        }

        # algorithm
        edges = [(u, v, graph.get_edge_data(u, v)['weight']) for u, v in graph.edges]
        sorted_edges = sorted(edges, key=lambda x: x[2])

        MST = nx.Graph()
        MST.add_nodes_from(graph.nodes)

        for source, target, weight in sorted_edges:
            frames[f'Kante zwischen {source} und {target} betrachten'] = {
                f'edge_{source}_{target}': {
                    'backgroundColor': 'red',
                    'color': 'gray',
                    'size': 4
                }
            }
            MST.add_edge(source, target, weight=weight)

            if len(list(nx.all_simple_paths(MST, source, target))) >= 2:
                frames[f'Kante zwischen {source} und {target} nicht aufnehmen'] = {
                    f'edge_{source}_{target}': {
                        'backgroundColor': '#aaaaaa',
                        'color': '#cacaca',
                        'size': 2
                    }
                }
                MST.remove_edge(source, target)
            else:
                sum += weight
                frames[f'Kante zwischen {source} und {target} aufnehmen'] = {
                    f'edge_{source}_{target}': {
                        'backgroundColor': 'hsl(189, 90%, 50%)',
                        'color': 'gray',
                        'size': 3
                    },
                    'sum': sum
                }

        # finalization
        frames[f'Keine Kanten verbleibend'] = {}

        # initialize parent
        super().__init__(html, frames, css)
