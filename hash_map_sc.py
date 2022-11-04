# Name: Salim Jalaleddine
# OSU Email: jalaleds@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6
# Due Date: 6/4/2022 (Used 1 free day)
# Description: Implementation of hash map chaining for collision resolution


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(LinkedList())

        self._capacity = capacity
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates key/value pair in hashmap. If present, replaces value, if not, adds key/value pair.
        Uses single linked-list chaining for collision resolution
        """
        bucket = self._hash_function(key) % self._capacity
        linked_list = self._buckets[bucket]
        linked_list_node = linked_list.contains(key)
        if linked_list_node:
            linked_list_node.value = value
        else:
            linked_list.insert(key, value)
            self._size += 1
        return

    def empty_buckets(self) -> int:
        """
        Returns number of empty buckets in the hash table
        """
        count = 0
        for bucket in range(self._buckets.length()):
            if self._buckets[bucket].length() == 0:
                count += 1

        return count

    def table_load(self) -> float:
        """
        Returns load factor of hash table
        """
        count_buckets = self._buckets.length()
        count_elements = self.get_size()

        return count_elements/count_buckets

    def clear(self) -> None:
        """
        Clears hashmap
        """
        for i in range(self._buckets.length()):
            if self._buckets[i].length() != 0:
                self._buckets[i] = LinkedList()
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes underlying capacity of the hash table
        """
        if new_capacity < 1:
            return

        node_holder = DynamicArray()
        for i in range(self._buckets.length()):
            if self._buckets[i].length() != 0:
                linked_list_iter = iter(self._buckets[i])
                while True:
                    try:
                        node_holder.append(next(linked_list_iter))
                    except StopIteration:
                        break

        self._capacity = new_capacity
        self._buckets = DynamicArray()
        for i in range(self._capacity):
            self._buckets.append(LinkedList())
        self._size = 0

        for i in range(node_holder.length()):
            self.put(node_holder[i].key, node_holder[i].value)

    def get(self, key: str) -> object:
        """
        Returns value with associated key, if not present, returns None
        """
        bucket = self._hash_function(key) % self._capacity
        linked_list = self._buckets[bucket]
        linked_list_node = linked_list.contains(key)
        if linked_list_node:
            return linked_list_node.value
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns true if key is in map, otherwise returns False
        """
        bucket = self._hash_function(key) % self._capacity
        linked_list = self._buckets[bucket]
        linked_list_node = linked_list.contains(key)
        if linked_list_node:
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes key/value pair from hashmap
        """
        bucket = self._hash_function(key) % self._capacity
        linked_list = self._buckets[bucket]
        linked_list_node = linked_list.contains(key)
        if linked_list_node:
            linked_list.remove(key)
            self._size -= 1

    def get_keys(self) -> DynamicArray:
        """
        Returns dynamic array containing all keys stored in hashmap
        """
        key_holder = DynamicArray()
        for i in range(self._buckets.length()):
            if self._buckets[i].length() != 0:
                linked_list_iter = iter(self._buckets[i])
                while True:
                    try:
                        key_holder.append(next(linked_list_iter).key)
                    except StopIteration:
                        break
        return key_holder


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Returns tuple of, Dynamic Array of most frequently repeating values of given array, and highest frequency
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap(da.length() // 3, hash_function_1)
    for i in range(da.length()):
        cur_val = map.get(da[i])
        if not cur_val:
            map.put(da[i], 1)
        else:
            map.put(da[i], cur_val + 1)

    max_value = 0
    for i in range(da.length()):
        cur_val = map.get(da[i])
        if max_value < cur_val:
            max_value = cur_val

    list_of_keys = map.get_keys()
    max_keys = DynamicArray()

    for i in range(list_of_keys.length()):
        cur_val = map.get(list_of_keys[i])
        if cur_val == max_value:
            max_keys.append(list_of_keys[i])

    return max_keys, max_value


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    map = HashMap(da.length() // 3, hash_function_1)
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        map = HashMap(da.length() // 3, hash_function_2)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}\n")
