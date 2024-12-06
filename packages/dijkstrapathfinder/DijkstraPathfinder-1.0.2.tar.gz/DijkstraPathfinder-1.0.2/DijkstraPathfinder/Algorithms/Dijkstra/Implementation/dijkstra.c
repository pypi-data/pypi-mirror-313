#include <stdio.h>
#include <string.h>
#include <limits.h>
#include "dijkstra.h"

// Initializes the shortest path table with vertex names and sets initial distances
void initializeShortestPathTable(shortestPathTable *table, char *vertices){

    memset(table->valid, false, sizeof(table->valid));

    for (int i = 0; i < MAX_NODES && vertices[i] != '\0'; i++){

        int index = hash(vertices[i]);

        table->data[index].name = vertices[i];
        table->data[index].shortestDistance = INT_MAX;
        table->data[index].previousNode = '\0';

        table->valid[index] = true;
    }
}

// Sets a specific vertex's shortest distance and previous node
void setValue(shortestPathTable *table, char name, int shortestDistance, int previousNode){

    int index = hash(name);

    table->data[index].name = name;
    table->data[index].shortestDistance = shortestDistance;
    table->data[index].previousNode = previousNode;

    table->valid[index] = true;
}

// Returns the shortest distance for a specific vertex, or -1 if not found
int getShortestDistance(shortestPathTable table, char name){

    int index = hash(name);

    if (!table.valid[index]) return -1;

    return table.data[index].shortestDistance;
}

// Prints the shortest distance table
void printShortestDistanceTable(shortestPathTable table){

    for (int i = 0; i < MAX_NODES; i++){

        if (!table.valid[i]) continue;

        shortestPathTableNode currentNode = table.data[i];

        printf("Node: %c, Shortest Distance:%d, Previous Node: %c\n", currentNode.name, currentNode.shortestDistance, currentNode.previousNode);
    }
}

// Prints the shortest path to a destination node
void printShortestPath(shortestPathTable table, char destination) {

    if (table.data[hash(destination)].previousNode == '\0') {
        printf("No path found\n");
        return;
    }

    printf("Shortest path: ");

    char current = destination;
    while (current != '\0') {
        printf("%c ", current);
        current = table.data[hash(current)].previousNode;
    }

    printf("\n");
}

// Implements Dijkstra's algorithm to find shortest paths from a source node
shortestPathTable dijkstra(Graph graph, char source){

    bool visited[MAX_NODES] = {false};
    int visitedNumber = 0;
    int totalVertices = 0;

    // Collect vertices from graph
    char vertices[MAX_NODES];
    char *temp = vertices;
    for (int i = 0; i < MAX_NODES; i++){

        if (graph.adjacency_list[i]){

            *temp = graph.adjacency_list[i]->name;
            temp++;

            totalVertices++;
        }
    }
    *temp = '\0';

    shortestPathTable dijkstraTable;
    initializeShortestPathTable(&dijkstraTable, vertices);

    MinHeap heap;
    initMinHeap(&heap);

    // Set initial source node
    setValue(&dijkstraTable, source, 0, '\0');
    Node *vertex = graph.adjacency_list[hash(source)];

    // Traverse edges of the source node
    if (vertex){

        Node *edge = graph.adjacency_list[hash(source)]->next;
        while (edge){

            int currentShortestDistance = getShortestDistance(dijkstraTable, edge->name);

            if (currentShortestDistance != -1){

                setValue(&dijkstraTable, edge->name, edge->weight, vertex->name);
                insert(&heap, edge->name, edge->weight);
            }

            edge = edge->next;
        }

        visited[hash(vertex->name)] = true;
        visitedNumber++;
    }

    // Main loop of Dijkstra's algorithm
    while (visitedNumber <= totalVertices){

        HeapNode minNode = extractMin(&heap);
        if (minNode.key == -1) break;

        Node *edge = graph.adjacency_list[hash(minNode.key)]->next;

        while (edge){

            int currentShortestDistance = dijkstraTable.data[hash(edge->name)].shortestDistance;
            int newDistance = minNode.value + edge->weight;

            // Update shortest distances
            if (currentShortestDistance == INT_MAX){

                setValue(&dijkstraTable, edge->name, newDistance, minNode.key);
                insert(&heap, edge->name, newDistance);
            }


            else if (currentShortestDistance > newDistance && !visited[hash(edge->name)]){

                setValue(&dijkstraTable, edge->name, newDistance, minNode.key);
                updateKey(&heap, heapContains(heap, edge->name), newDistance);
            }

            edge = edge->next;
        }

        visited[hash(minNode.key)] = true;
        visitedNumber++;
    }

    return dijkstraTable;
}
