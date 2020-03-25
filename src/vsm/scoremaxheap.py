import heapq

from .score import Score

class ScoreMaxHeap:
    """
    max heap for score objects.
    """

    def __init__(self, scores=[]):
        """
        heap -> compact array heap for scores.
        """
        self.heap = [score for score in scores]
        heapq.heapify(self.heap)

    @classmethod
    def negateScore(cls, scoreObj):
        """
        negates a score into a negative value, to simulate max heap
        from heapq.
        """
        doc, score = scoreObj.doc, scoreObj.score
        return Score(doc, -score)

    @classmethod
    def heapify(cls, scores):
        """
        heapify scores into a max heap (does not mutate list in argument).
        """
        negateScore = ScoreMaxHeap.negateScore
        return ScoreMaxHeap([negateScore(score) for score in scores])
    
    def push(self, score):
        """
        adds a score to the max heap.
        """
        negateScore = ScoreMaxHeap.negateScore
        heapq.heappush(self.heap, negateScore(score))

    def pop(self):
        """
        removes the largest score in the max heap.
        """
        negateScore = ScoreMaxHeap.negateScore
        return negateScore(heapq.heappop(self.heap))

    def __len__(self):
        return len(self.heap)
