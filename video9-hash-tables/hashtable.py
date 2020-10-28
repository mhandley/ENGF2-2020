import pprint

class HashTable:
    def __init__(self, element_list):
        # initialize an empty table 
        self.bucket_count = len(element_list) * 2 - 1
        # create a list consisting of bucket_count empty lists
        self.buckets = [[] for i in range(self.bucket_count)]

        # insert the elements
        for key, value in element_list:
            self.insert(key, value)

    def get_index(self, key):
        print(key, hash(key)%16)
        return hash(key) % self.bucket_count

    def insert(self, key, value):
        index = self.get_index(key)
        self.buckets[index].append( (key,value) )

    def lookup(self, search_key):
        index = self.get_index(search_key)
        for key, value in self.buckets[index]:
            if key == search_key:
                return value
        return None

    def __str__(self):
        return pprint.pformat(self.buckets)

if __name__ == "__main__":
    people = [
        ("Mark", "m.handley@cs.ucl.ac.uk"),
        ("Licia", "l.capra@ucl.ac.uk"),
        ("Graham", "graham.roberts@ucl.ac.uk"),
        ("Steve", "s.hailes@ucl.ac.uk")
        ]

    hashtable = HashTable(people)
    print(hashtable)
    print(f"Mark's email address is {hashtable.lookup('Mark')}")
