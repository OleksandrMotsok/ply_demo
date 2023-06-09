from user_space import func


class Runtime:
    def __init__(self):
        self.modules = [func]

    def get_function(self, name: str):
        for m in self.modules:
            function = getattr(m, name, None)
            if function:
                break

        return function
