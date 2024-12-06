#include <stdio.h>
#include "..\Implementation\dijkstra.h"

int main(int argc, char *argv[]){

    // Check if correct number of command line arguments is provided
    if (argc != 3) {

        printf("Invalid Command Line Args");
        return 1;
    }

    FILE *inputFile = fopen(argv[1], "r");
    if (!inputFile){

        printf("Error Opening the input file");
        return 1;
    }

    Graph graph;
    char node, start, source, destination;
    int noOfNodes, weight, directed;

    initializeGraph(&graph);

    // Read the number of nodes and starting node
    fscanf(inputFile, "%d %c", &noOfNodes, &start);

    // Add nodes to the graph
    for (int i = 0; i < noOfNodes; i++){

        fscanf(inputFile, " %c", &node);
        add_node(&graph, node);
    }

    // Add edges to the graph
    while (fscanf(inputFile, "\n%c %c %d %d", &source, &destination, &weight, &directed) != EOF)
        add_edge(&graph, source, destination, weight, directed == 1);

    fclose(inputFile);

    // Run Dijkstra's algorithm
    shortestPathTable table = dijkstra(graph, start);

    FILE *outputFile = fopen(argv[2], "w");
    if (!outputFile){

        printf("Error Opening the output file");
        return 1;
    }

    // Write shortest path results to the output file
    for (int i = 0; i < MAX_NODES; i++){

        if (!table.valid[i]) continue;

        shortestPathTableNode currentNode = table.data[i];

        if (!currentNode.previousNode)
            fprintf(outputFile, "%c %d -\n", currentNode.name, currentNode.shortestDistance);
        else
            fprintf(outputFile, "%c %d %c\n", currentNode.name, currentNode.shortestDistance, currentNode.previousNode);
    }

    fclose(outputFile);
    return 0;
}
