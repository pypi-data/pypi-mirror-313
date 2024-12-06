#include <stdio.h>
#include <stdlib.h>
#include "graph.h"

// Initialize the graph by setting all adjacency lists to NULL
// Time Complexity: O(N), where N = MAX_NODES
void initializeGraph(Graph *graph){

    for (int i = 0; i < MAX_NODES; i++)
        graph->adjacency_list[i] = NULL;
}

// Hash function to map a letter (A-Z) to an index (0-25)
// Time Complexity: O(1)
int hash(char letter){

    if (letter >= 'A' && letter <= 'Z')
        return letter - 'A';

    return -1; // Return -1 for invalid input
}

// Add a node to the graph if it does not already exist
// Time Complexity: O(1)
bool add_node(Graph* graph, char name){

    int index = hash(name);

    // Invalid node or node already exists
    if (index == -1 || graph->adjacency_list[index])
        return false;

    Node *node = (Node *) malloc(sizeof(Node));
    if (!node) return false;

    node->name = name;
    node->next = NULL;
    node->weight = -1;  // Vertex should have invalid weight

    graph->adjacency_list[index] = node;

    return true;
}

// Add an edge between two nodes (directed or undirected)
// Time Complexity: O(N) where N is the number of nodes in the adjacency list
bool add_edge(Graph *graph, char source, char destination, int weight, bool directed){

    int sourceIndex = hash(source);
    int destinationIndex = hash(destination);

    // Validate source and destination nodes
    if (sourceIndex == -1 || destinationIndex == -1)
        return false;

    if (!graph->adjacency_list[sourceIndex] || !graph->adjacency_list[destinationIndex])
        return false;

    Node *node = (Node *) malloc(sizeof(Node));
    if (!node) return false;

    node->name = destination;
    node->weight = weight;
    node->next = NULL;

    Node *sourceHead = graph->adjacency_list[sourceIndex];

    // Traverse to the end and add
    while (sourceHead->next)
        sourceHead = sourceHead->next;

    sourceHead->next = node;

    if (!directed){

        Node *newNode = (Node *) malloc(sizeof(Node));
        if (!newNode) return false;

        newNode->name = source;
        newNode->weight = weight;
        newNode->next = NULL;

        Node *destinationHead = graph->adjacency_list[destinationIndex];

        // Traverse to the end and add
        while (destinationHead->next)
            destinationHead = destinationHead->next;

        destinationHead->next = newNode;
    }

    return true;
}

// Print the entire graph in adjacency list format
// Time Complexity: O(N + E), where N = number of nodes and E = number of edges
void print_graph(Graph graph){

    for (int i = 0; i < MAX_NODES; i++){

        Node *vertex = graph.adjacency_list[i];
        Node *temp = NULL;

        if (vertex){

            printf("%c", vertex->name);
            temp = vertex->next;
        }

        while (temp){

            printf(" -> %c(%d)", temp->name, temp->weight);
            temp = temp->next;
        }

        if (vertex) printf("\n");
    }
}

// Free the memory allocated for the graph
// Time Complexity: O(N + E), where N = number of nodes and E = number of edges
void free_graph(Graph *graph){

    for (int i = 0; i < MAX_NODES; i++){

        Node *node = graph->adjacency_list[i];

        while (node){

            Node *temp = node;
            node = node->next;
            free(temp);
        }
    }
}
