#include <stdio.h>
#include "heap.h"

// Initializes the MinHeap by setting its size to 0
void initMinHeap(MinHeap *minHeap){

    minHeap->size = 0;
}

// Swaps the data of two HeapNodes
void swapHeapNode(HeapNode *node1, HeapNode *node2){

    HeapNode temp = *node1;
    *node1 = *node2;
    *node2 = temp;
}

// Inserts a new node with the specified key and value into the heap
bool insert(MinHeap *minHeap, int key, int value){

    if (minHeap->size >= MAX_SIZE) return false;

    minHeap->data[minHeap->size].key = key;
    minHeap->data[minHeap->size].value = value;

    heapifyUp(minHeap, minHeap->size);

    minHeap->size++;
    return true;
}

// Restores the heap property by moving the element at 'index' up the heap
void heapifyUp(MinHeap *minHeap, int index){

    int parent;

    while (index > 0){

        parent = (index - 1) / 2;

        if (minHeap->data[index].value < minHeap->data[parent].value){

            swapHeapNode(&minHeap->data[index], &minHeap->data[parent]);
            index = parent;
        }

        else break;
    }
}

// Restores the heap property by moving the element at 'index' down the heap
void heapifyDown(MinHeap *minHeap, int index){

    int smallest = index;
    int leftChild = 2 * index + 1;
    int rightChild = 2 * index + 2;


    if (leftChild < minHeap->size && minHeap->data[leftChild].value < minHeap->data[smallest].value)
        smallest = leftChild;

    if (rightChild < minHeap->size && minHeap->data[rightChild].value < minHeap->data[smallest].value)
        smallest = rightChild;

    if (smallest != index){

        swapHeapNode(&minHeap->data[smallest], &minHeap->data[index]);
        heapifyDown(minHeap, smallest);
    }
}

// Returns the minimum element from the heap without removing it
HeapNode getMin(MinHeap *minHeap){

    if (minHeap->size <= 0){

        HeapNode emptyNode = {.key = -1, .value = -1};
        return emptyNode;
    }

    return minHeap->data[0];
}

// Extracts and removes the minimum element from the heap
HeapNode extractMin(MinHeap *minHeap){

    if (minHeap->size <= 0){

        HeapNode emptyNode = {.key = -1, .value = -1};
        return emptyNode;
    }

    HeapNode minNode = minHeap->data[0];

    minHeap->data[0] = minHeap->data[minHeap->size - 1];
    minHeap->size--;

    heapifyDown(minHeap, 0);

    return minNode;
}

// Returns the index of the key if exists, otherwise -1
int heapContains(MinHeap minHeap, int key){

    for (int i = 0; i < minHeap.size; i++){

        if (minHeap.data[i].key == key)
            return i;
    }

    return -1;
}

// Updates the value of a key and restores the heap property
void updateKey(MinHeap *minHeap, int index, int value){

    if (index < 0 || index >= minHeap->size){

        printf("Invalid Index");
        return;
    }

    if (minHeap->data[index].value < value){

        minHeap->data[index].value = value;
        heapifyDown(minHeap, index);
    }

    else {

        minHeap->data[index].value = value;
        heapifyUp(minHeap, index);
    }
}

// Prints all elements of the heap
void printHeap(MinHeap minHeap){

    if (minHeap.size <= 0){

        printf("Empty Heap\n");
        return;
    }

    for (int i = 0; i < minHeap.size; i++){

        printf("{%d, %d} ", minHeap.data[i].key, minHeap.data[i].value);
    }

    printf("\n");
}
