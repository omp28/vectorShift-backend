from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

class Node(BaseModel):
    id: str
    type: str
    position: dict
    data: dict

class Edge(BaseModel):
    id: str
    source: str
    target: str
    sourceHandle: str
    targetHandle: str

class Pipeline(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

@app.get('/')
def read_root():
    return {'Ping': 'Pong'}

@app.post('/pipelines/parse')
def parse_pipeline(pipeline: Pipeline):
    m1 = {}
    mp2 = {}
    is_dag = True  

    for edge in pipeline.edges:
        start, end = edge.source, edge.target
        if start not in m1:
            m1[start] = [end]
        else:
            m1[start].append(end)

    for key, values in m1.items():
        for value in values:
            if value not in mp2:
                mp2[value] = 1
            else:
                if key in mp2:
                    is_dag = False
                    break
        if not is_dag:
            break

    num_nodes = len(pipeline.nodes)
    num_edges = len(pipeline.edges)

    return {
        'num_nodes': num_nodes,
        'num_edges': num_edges,
        'is_dag': is_dag
    }
