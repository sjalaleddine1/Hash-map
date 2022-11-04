# Name: Salim Jalaleddine
# OSU Email: jalaleds@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6
# Due Date: 6/4/2022 (Used 1 free day)
# Description: Implementation of hash map open addressing for collision resolution


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(None)

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
        Uses open addressing (quadratic probing) for collision resolution
        """
        # remember, if the load factor is greater than or equal to 0.5,
        # resize the table before putting the new key/value pair
        if self.table_load() >= 0.5:
            self.resize_table(2*self._capacity)

        bucket = self._hash_function(key) % self._capacity

        if not self._buckets[bucket]:
            self._buckets[bucket] = HashEntry(key, value)
            self._size += 1
            return

        if self._buckets[bucket].key == key and self._buckets[bucket].is_tombstone is True:
            self._buckets[bucket].is_tombstone = False
            self._size += 1
            return

        if self._buckets[bucket].key == key:
            self._buckets[bucket].value = value
            return

        old_bucket = bucket
        j = 1
        while self._buckets[bucket] is not None:
            bucket = (old_bucket + j**2) % self._capacity
            j += 1
            if not self._buckets[bucket]:
                self._buckets[bucket] = HashEntry(key, value)
                self._size += 1
                return
            if self._buckets[bucket].key == key and self._buckets[bucket].is_tombstone is True:
                self._buckets[bucket].is_tombstone = False
                self._size += 1
                return
            elif self._buckets[bucket].key == key:
                self._buckets[bucket].value = value
                return

    def table_load(self) -> float:
        """
        Returns load factor of hash table
        """
        return self.get_size()/self._buckets.length()

    def empty_buckets(self) -> int:
        """
        Returns number of empty buckets in the hash table
        """
        return self._capacity - self._size

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes underlying capacity of the hash table
        """
        # remember to rehash non-deleted entries into new table
        if new_capacity < 1 or new_capacity < self._size:
            return

        hash_holder = DynamicArray()

        for i in range(self._buckets.length()):
            if self._buckets[i] is not None:
                hash_holder.append(self._buckets[i])

        self._capacity = new_capacity
        self._buckets = DynamicArray()

        for _ in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

        for i in range(hash_holder.length()):
            self.put(hash_holder[i].key, hash_holder[i].value)

    def get(self, key: str) -> object:
        """
        Returns value with associated key, if not present, returns None
        """
        bucket = self._hash_function(key) % self._capacity

        if self._buckets.length() == 0:
            return None

        if not self._buckets[bucket] or self._buckets[bucket].is_tombstone is True:
            return None

        if self._buckets[bucket].key == key:
            return self._buckets[bucket].value

        old_bucket = bucket
        j = 1
        while self._buckets[bucket] is not None:
            bucket = (old_bucket + j ** 2) % self._capacity
            j += 1
            if not self._buckets[bucket]:
                return None
            elif self._buckets[bucket].key == key:
                return self._buckets[bucket].value

    def contains_key(self, key: str) -> bool:
        """
        Returns true if key is in map, otherwise returns False
        """
        bucket = self._hash_function(key) % self._capacity

        if self._buckets.length() == 0:
            return False

        if not self._buckets[bucket] or self._buckets[bucket].is_tombstone is True:
            return False

        if self._buckets[bucket].key == key:
            return True

        old_bucket = bucket
        j = 1
        while self._buckets[bucket] is not None:
            bucket = (old_bucket + j**2) % self._capacity
            j += 1
            if not self._buckets[bucket]:
                return False
            elif self._buckets[bucket].key == key:
                return True

    def remove(self, key: str) -> None:
        """
        Removes key/value pair from hashmap
        """
        bucket = self._hash_function(key) % self._capacity

        if not self._buckets[bucket]:
            return

        if self._buckets[bucket].key == key and self._buckets[bucket].is_tombstone is False:
            self._buckets[bucket].is_tombstone = True
            self._size -= 1
            return

        old_bucket = bucket
        j = 1
        while self._buckets[bucket] is not None:
            bucket = (old_bucket + j**2) % self._capacity
            j += 1
            if not self._buckets[bucket]:
                return
            elif self._buckets[bucket].key == key and self._buckets[bucket].is_tombstone is False:
                self._buckets[bucket].is_tombstone = True
                self._size -= 1
                return

    def clear(self) -> None:
        """
        Clears hashmap
        """
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

    def get_keys(self) -> DynamicArray:
        """
        Returns dynamic array containing all keys stored in hashmap
        """
        key_holder = DynamicArray()
        for i in range(self._buckets.length()):
            if self._buckets[i] and self._buckets[i].is_tombstone is False:
                key_holder.append(self._buckets[i].key)

        return key_holder


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

        if m.table_load() >= 0.5:
            print("Check that capacity gets updated during resize(); "
                  "don't wait until the next put()")

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
