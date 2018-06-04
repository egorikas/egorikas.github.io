---
title:  "Max and Min heap implementation with C#"
description: "The easiest implementation of Max and Min heap."
modified: 2018-04-22T23:24:00-03:00
tags:
  - computer science
  - hackerrank
  - .net core
  - .net
---

Hi everyone! Today I want to talk about implementation of Max and Min heap with C#.

## The reason why you can be needed them
Three or four month ago I understood that resolving tasks at <a href="https://www.hackerrank.com/">hackerrank</a> can make you better programmer and give basic understanding of efficient algorithms.
There a lot of task there, which should be implemented with `heap`. But we don't have `heap` in `.net` core library.

## Why did I need them?
Once, I wrote a  about <a href="http://egorikas.com/download-open-street-tiles-for-offline-using/">blog-post</a> dowloading open street maps tiles.
After release, client decided to switch application from usual tiles to vector ones. And that was the strange journey, but I want to share this expirience with you.

* <a href="https://www.hackerrank.com/challenges/ctci-find-the-running-median/problem">first</a>
* <a href="https://www.hackerrank.com/challenges/qheap1/problem">second</a>
* <a href="https://www.hackerrank.com/challenges/jesse-and-cookies/problem">third</a>

## Implementation

There are two common ways for implementing heaps. The first one is using list of nodes, where every node contains two child nodes.
Using array is the second one (I preferred this one).

Gayle Laakmann McDowell gives a good <a href="https://www.youtube.com/watch?v=t0Cq6tVNRBA">explanation</a> about implementation of the data structure.

## Min heap
```csharp
        public class MinHeap
        {
            private readonly int[] _elements;
            private int _size;

            public MinHeap(int size)
            {
                _elements = new int[size];
            }

            private int GetLeftChildIndex(int elementIndex) => 2 * elementIndex + 1;
            private int GetRightChildIndex(int elementIndex) => 2 * elementIndex + 2;
            private int GetParentIndex(int elementIndex) => (elementIndex - 1) / 2;

            private bool HasLeftChild(int elementIndex) => GetLeftChildIndex(elementIndex) < _size;
            private bool HasRightChild(int elementIndex) => GetRightChildIndex(elementIndex) < _size;
            private bool IsRoot(int elementIndex) => elementIndex == 0;

            private int GetLeftChild(int elementIndex) => _elements[GetLeftChildIndex(elementIndex)];
            private int GetRightChild(int elementIndex) => _elements[GetRightChildIndex(elementIndex)];
            private int GetParent(int elementIndex) => _elements[GetParentIndex(elementIndex)];

            private void Swap(int firstIndex, int secondIndex)
            {
                var temp = _elements[firstIndex];
                _elements[firstIndex] = _elements[secondIndex];
                _elements[secondIndex] = temp;
            }

            public bool IsEmpty()
            {
                return _size == 0;
            }

            public int Peek()
            {
                if (_size == 0)
                    throw new IndexOutOfRangeException();

                return _elements[0];
            }

            public int Pop()
            {
                if (_size == 0)
                    throw new IndexOutOfRangeException();

                var result = _elements[0];
                _elements[0] = _elements[_size - 1];
                _size--;

                ReCalculateDown();

                return result;
            }

            public void Add(int element)
            {
                if (_size == _elements.Length)
                    throw new IndexOutOfRangeException();

                _elements[_size] = element;
                _size++;

                ReCalculateUp();
            }

            private void ReCalculateDown()
            {
                int index = 0;
                while (HasLeftChild(index))
                {
                    var smallerIndex = GetLeftChildIndex(index);
                    if (HasRightChild(index) && GetRightChild(index) < GetLeftChild(index))
                    {
                        smallerIndex = GetRightChildIndex(index);
                    }

                    if (_elements[smallerIndex] >= _elements[index])
                    {
                        break;
                    }

                    Swap(smallerIndex, index);
                    index = smallerIndex;
                }
            }

            private void ReCalculateUp()
            {
                var index = _size - 1;
                while (!IsRoot(index) && _elements[index] < GetParent(index))
                {
                    var parentIndex = GetParentIndex(index);
                    Swap(parentIndex, index);
                    index = parentIndex;
                }
            }
        }
```

We are using array as a storage for members of the heap. And doing a few calculation after every add/remove from the top. (The implementation is the same as in the <a href="https://www.youtube.com/watch?v=t0Cq6tVNRBA">video</a>).

## Max heap
If you want to create `Max heap`, you need to change those methods:

```csharp
            private void ReCalculateDown()
            {
                int index = 0;
                while (HasLeftChild(index))
                {
                    var biggerIndex = GetLeftChildIndex(index);
                    if (HasRightChild(index) && GetRightChild(index) > GetLeftChild(index))
                    {
                        biggerIndex = GetRightChildIndex(index);
                    }

                    if (_elements[biggerIndex] < _elements[index])
                    {
                        break;
                    }

                    Swap(biggerIndex, index);
                    index = biggerIndex;
                }
            }

            private void ReCalculateUp()
            {
                var index = _size - 1;
                while (!IsRoot(index) && _elements[index] > GetParent(index))
                {
                    var parentIndex = GetParentIndex(index);
                    Swap(parentIndex, index);
                    index = parentIndex;
                }
            }
```

## P.S.
Solving tasks on <a href="https://www.hackerrank.com/">hackerrank</a> is fun. And I recommend you to try it.

## Conclusion

That’s all, thank you for you attention!
