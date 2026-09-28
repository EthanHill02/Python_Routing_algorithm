#create hash table class
class hashTable:
    def __init__(self, initial_capacity=40 ):
        self.list = []
        for i in range(initial_capacity):
            self.list.append([])

# inserting a new item into hash table
    def insert(self, key, item):
        #find bucket list for where item will be inserted
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]

        #update key if is already present within bucket
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        #insert item in the end of bucket list if not already present
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    #lookup items in hash table
    def lookup(self, key):
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]
        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]
        return None

    #removal from hash method
    def remove(self, key):
        spot = hash(key) % len(self.list)
        destination = self.list[spot]

        #look through bucket to see if matching key is found
        for kv in destination:
            if kv[0] == key:
                #remove key value pair
                destination.remove(kv)
                return True
        return False
