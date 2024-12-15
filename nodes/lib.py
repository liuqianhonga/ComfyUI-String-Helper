class AnyType(str):
    """
    A class representing any type in ComfyUI nodes.
    Used for parameters that can accept any type of input.
    """
    def __ne__(self, __value: object) -> bool:
        return False

    @classmethod
    def INPUT_TYPE(cls):
        return (ANY, {})

ANY = AnyType("*")
