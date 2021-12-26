from quickvote.models.type_votes import Fibonacci


class Object:
    def __init__(self, name, number_of_votes, description):
        self.name = name
        self.description = description
        self.number_of_votes = number_of_votes

    def clear_votes(self):
        self.number_of_votes = 0

    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'number_of_votes': self.number_of_votes
        }


class ObjectPlanning(Object):
    fib = Fibonacci

    def __init__(self, name, number_of_votes, description):
        super().__init__(name, number_of_votes, description)
        self.votes = []

    def clear_votes(self):
        self.number_of_votes = 0
        self.votes = []

    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'number_of_votes': self.number_of_votes,
            'vote': self.votes
        }
