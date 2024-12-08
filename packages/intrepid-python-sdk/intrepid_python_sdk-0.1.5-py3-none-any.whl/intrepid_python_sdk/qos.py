class Qos:
    def __init__(self, reliability=None, durability=None, history=None, deadline=None, lifespan=None):
        self.reliability = reliability  # Reliability QoS
        self.durability = durability    # Durability QoS
        self.history = history          # History QoS
        self.deadline = deadline        # Deadline QoS
        self.lifespan = lifespan        # Lifespan QoS

    def set_reliability(self, reliability):
        self.reliability = reliability

    def set_durability(self, durability):
        self.durability = durability

    def set_history(self, history):
        self.history = history

    def set_deadline(self, deadline):
        self.deadline = deadline

    def set_lifespan(self, lifespan):
        self.lifespan = lifespan

    def __str__(self):
        return f"QoS(reliability={self.reliability}, durability={self.durability}, " \
               f"history={self.history}, deadline={self.deadline}, lifespan={self.lifespan})"
