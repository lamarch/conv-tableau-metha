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


class Configuration:
    def __init__(self, path: str) -> None:
        self.path = path

    def load(self):
        from json import load
        return load(self.path)
