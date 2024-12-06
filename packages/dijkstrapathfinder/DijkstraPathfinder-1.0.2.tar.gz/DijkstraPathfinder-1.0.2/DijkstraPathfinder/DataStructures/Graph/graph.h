#ifndef GRAPH_H
#define GRAPH_H

#include <stdbool.h>
#define MAX_NODES 26  // Number of Nodes (representing A - Z)

// Represents a node in the adjacency list
typedef struct Node {
    char name;
    int weight;
    struct Node *next;
} Node;

// Graph structure using an adjacency list representation
typedef struct {
    Node *adjacency_list[MAX_NODES];
} Graph;


// Function declarations
void initializeGraph(Graph *graph);
int hash(char letter);
bool add_node(Graph* graph, char name);
bool add_edge(Graph *graph, char source, char destination, int weight, bool directed);
void print_graph(Graph graph);
void free_graph(Graph *graph);

#endif
