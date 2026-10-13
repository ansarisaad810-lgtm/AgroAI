# DSA ALGORITHMS: Binary Search, Merge Sort, Heapify / Priority Queue
# USED FOR: Fast crop searching, budget-filtered tool ordering, price sorting.

def binary_search_crop(sorted_crop_list, target_name):
    """
    DSA: Binary Search - O(log N)
    Requires sorted list of dictionaries with 'name' key.
    """
    low = 0
    high = len(sorted_crop_list) - 1
    target = target_name.lower()

    while low <= high:
        mid = (low + high) // 2
        mid_val = sorted_crop_list[mid]['name'].lower()

        if mid_val == target:
            return sorted_crop_list[mid]
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1

    return None


def merge_sort_by_price(items, key='cost'):
    """
    DSA: Merge Sort - O(N log N)
    Used to sort tools or market prices predictably.
    """
    if len(items) <= 1:
        return items

    mid = len(items) // 2
    left = merge_sort_by_price(items[:mid], key)
    right = merge_sort_by_price(items[mid:], key)

    return _merge(left, right, key)


def _merge(left, right, key):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i][key] <= right[j][key]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def heapify(arr, n, i, key='cost'):
    """DSA: Min-Heapify helper for Priority Queue / Budget filtering."""
    smallest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left][key] < arr[smallest][key]:
        smallest = left

    if right < n and arr[right][key] < arr[smallest][key]:
        smallest = right

    if smallest != i:
        arr[i], arr[smallest] = arr[smallest], arr[i]
        heapify(arr, n, smallest, key)


def heap_sort_tools(arr, key='cost'):
    """
    DSA: Heap Sort - O(N log N)
    Sorts farming tools or expenses by budget constraints.
    """
    n = len(arr)
    # Build min heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, key)

    sorted_arr = []
    # Extract elements
    for i in range(n - 1, -1, -1):
        arr[0], arr[i] = arr[i], arr[0]
        sorted_arr.append(arr.pop())
        heapify(arr, i, 0, key)

    return sorted_arr
