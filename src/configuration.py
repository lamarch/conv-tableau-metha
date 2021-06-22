# CONFIG FORMAT :

"""json

{
    "matières":[
        ["m_1", "m_1 variant"],
        ["m_2"]
    ],
    "decalages":{
        "haut":7,
        "gauche":9,
        "entre_clients":1
    }
}

"""


CONFIG_DEFAUT = """
{
    "matières":
    [
        ["Fumier bovins","Fumier bovins C2"],
        ["Fumier bovins mou","Fumier bovins mou C2"],
        ["Lisiers","Lisiers C2"],
        ["Fumier ovins","Fumier ovins C2"],
        ["Maïs ensilage"],
        ["Seigle ensilage"],
        ["Paille"],
        ["DIGESTAT","DIGESTAT C2"],
    ],
    "decalages":{
        "haut":7,
        "gauche":9,
        "entre_clients":1
    }
}
"""


class ChargeurConfiguration:
    def __init__(self, path: str) -> None:
        self.path = path

    def charger(self):
        from json import load
        return load(self.path)

    def defaut(self):
        from json import loads
        return loads(CONFIG_DEFAUT)
