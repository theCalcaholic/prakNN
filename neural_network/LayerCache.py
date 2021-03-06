
class LayerCache(object):
    """
    caches the inputs, results and losses of an CachingNerualLayer's feedforward process.
    Supports double linking (predecessor, successor)
    """
    def __init__(self):
        """initialize cache"""
        # inputs
        self.input_values = None
        # results
        self.output_values = None
        # loss
        self.loss = None
        # list implementation stuff
        self.predecessor = None
        self.successor = None
        self.is_first_cache = False
        self.is_last_cache = False

    def insert_before(self, cache):
        """insert cache before this one in cache chain"""
        cache.predecessor = self.predecessor
        cache.successor = self
        self.predecessor.successor = cache
        self.predecessor = cache

    def insert_after(self, cache):
        """insert cache after this one in cache chain"""
        cache.successor = self.successor
        cache.predecessor = self
        self.successor = cache

    def remove(self):
        """remove this cache from cache chain"""
        self.predecessor.successor = self.successor
        self.successor.predecessor = self.predecessor