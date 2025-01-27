class Map:
    def __init__(self, life_path, balance, expression, lpe_bridge, heart_desire, birthday,
                 personality, hdp_bridge, maturity, karmic_lessons, rational_thought, subconscious_confidence,
                 hidden_passion, challenge, pinnacle, year, month):
        self.life_path = life_path
        self.balance = balance
        self.expression = expression
        self.lpe_bridge = lpe_bridge
        self.heart_desire = heart_desire
        self.birthday = birthday
        self.personality = personality
        self.hdp_bridge = hdp_bridge
        self.maturity = maturity
        self.karmic_lessons = karmic_lessons
        self.rational_thought = rational_thought
        self.subconscious_confidence = subconscious_confidence
        self.hidden_passion = hidden_passion
        self.challenge = challenge
        self.pinnacle = pinnacle
        self.year = year
        self.month = month


# Example of creating a Map instance
map_instance = Map(
    life_path=22,
    balance=3,
    expression=1,
    lpe_bridge=3,
    heart_desire=9,
    birthday=8,
    personality=1,
    hdp_bridge=8,
    maturity=5,
    karmic_lessons=[4, 6],
    rational_thought=3,
    subconscious_confidence=7,
    hidden_passion=[5, 6],
    challenge=[0, 2, 2, 2],
    pinnacle=[7, 5, 3, 5],
    year=[2, 3, 4, 5, 6],
    month=[7, 6, 7]
)
