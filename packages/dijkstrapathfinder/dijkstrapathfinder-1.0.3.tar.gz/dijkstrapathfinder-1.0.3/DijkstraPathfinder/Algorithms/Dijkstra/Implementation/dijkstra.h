#ifndef DIJKSTRA_H
#define DIJKSTRA_H

#include "..\..\..\DataStructures\Graph\graph.h"
#include "..\..\..\DataStructures\Heap\heap.h"

// Structure to store information about each node in the shortest path table
typedef struct {

    char name;
    int shortestDistance;
    char previousNode;

} shortestPathTableNode;

// Structure for the entire shortest path table
typedef struct {

    shortestPathTableNode data[MAX_NODES];
    bool valid[MAX_NODES];

} shortestPathTable;

// Function prototypes for Dijkstra's algorithm
void initializeShortestPathTable(shortestPathTable *table, char *vertices);
void setValue(shortestPathTable *table, char name, int shortestDistance, int previousNode);
int getShortestDistance(shortestPathTable table, char name);
void printShortestDistanceTable(shortestPathTable table);
void printShortestPath(shortestPathTable table, char destination);
shortestPathTable dijkstra(Graph graph, char source);

#endif
