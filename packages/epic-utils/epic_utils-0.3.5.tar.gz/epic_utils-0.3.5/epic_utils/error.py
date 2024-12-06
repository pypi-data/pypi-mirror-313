class ErrorHandler:
    def raiseError(typ, message : str):
        raise typ(message)
    def isType(obj, typ) -> bool:
        return isinstance(obj, typ)
    def isTypes(obj, types) -> bool:
        for typ in types:
            if isinstance(obj, typ):
                return True
        return False