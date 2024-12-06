#ifndef HEAP_H
#define HEAP_H

#include <stdbool.h>
#define MAX_SIZE 26

// Represents a single node in the heap with a key-value pair
typedef struct {

    int key;
    int value;
} HeapNode;

// Represents a MinHeap data structure
typedef struct {

    HeapNode data[MAX_SIZE];
    int size;
} MinHeap;

// Function declarations
void initMinHeap(MinHeap *minHeap);
bool insert(MinHeap *minHeap, int key, int value);
HeapNode getMin(MinHeap *minHeap);
void heapifyUp(MinHeap *minHeap, int index);
void heapifyDown(MinHeap *minHeap, int index);
HeapNode extractMin(MinHeap *minHeap);
void printHeap(MinHeap minHeap);
void swapHeapNode(HeapNode *node1, HeapNode *node2);
int heapContains(MinHeap MinHeap, int key);
void updateKey(MinHeap *minHeap, int index, int value);

#endif
