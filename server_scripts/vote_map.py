import random as rand

"""
What still needs to be done (for now):
    Stop players from voting twice
    Allow players to change their vote
    Have the bot make an embedded post
"""

class VoteError(Exception):
    pass

# VoteMap(SqRCON, generate_layer_list, self.last_layer)

class VoteMap:
    def __init__(self, rcon, layer_generator, last_layer):
        """Initializes the votemap class with all components"""
        self.layer_gen = layer_generator
        self.rcon = rcon
        self.last_layer = last_layer
        self.layers = self.layer_gen(self.last_layer)
        self.voted_users = []

    def reinit(self, new_layer):
        """Resets VoteMap for a new layer"""
        self.last_layer = new_layer
        self.layers = self.layer_gen(self.last_layer)
        self.voted_users = []

    async def add_vote(self, choice_index, weight, user_id):
        if user_id not in self.voted_users:
            self.voted_users.append(user_id)
            voted_layer = list(self.layers.keys())[choice_index]
            self.layers[voted_layer]['votes'] += weight
            print('vote added')
            await self.evaluate_votes()
            return voted_layer, self.layers[voted_layer]
        else:
            raise VoteError

    async def evaluate_votes(self):
        """Evaluates the existing votes and sets the next map"""
        max_votes = 0
        next_layer = ''
        for name, values in self.layers.items():
            if values['votes'] > max_votes:
                next_layer = name
                max_votes = values['votes']

        vote_list = [v['votes'] for v in self.layers.values()]

        # Three way tie breaker
        if vote_list.count(max(vote_list)) > 2:
            next_layer = rand.choice(list(self.layers.keys()))
        # Two way tie breaker
        elif vote_list.count(max(vote_list)) > 1:
            layer_index = rand.choice(
                [vote_list.index(max(vote_list)), vote_list[::-1].index(max(vote_list))]
            )
            next_layer = list(self.layers.keys())[layer_index]

        await self.rcon.send_command(f'setnextmap {next_layer}')
