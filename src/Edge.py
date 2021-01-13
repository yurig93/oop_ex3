class Edge(object):
    INVALID_ENTRY = -1

    def __init__(self, src: int = None, dest: int = None, weight: float = None, info: str = None, tag: int = None):
        self.src: int = src if src is not None else self.INVALID_ENTRY
        self.dest: int = dest if dest is not None else self.INVALID_ENTRY
        self.weight: float = weight if weight is not None else 0
        self.info: str = info if info is not None else ""
        self.tag: int = tag if tag is not None else self.INVALID_ENTRY

    @classmethod
    def from_dict(cls, data: dict):
        if 'src' not in data or 'dest' not in data:
            raise ValueError("Malformed JSON.")

        src = data.get('src')
        dest = data.get('dest')
        weight = data.get('weight')
        weight = data.get('w') if weight is None else weight

        if weight is None:
            raise ValueError("Edge is missing weight.")

        info = data.get("info")
        tag = data.get("tag")

        return cls(src=src,
                   dest=dest,
                   weight=weight,
                   info=info,
                   tag=tag)

    def to_dict(self):
        return {'src': self.src,
                'dest': self.dest,
                'weight': self.weight,
                'info': self.info,
                'tag': self.tag}
