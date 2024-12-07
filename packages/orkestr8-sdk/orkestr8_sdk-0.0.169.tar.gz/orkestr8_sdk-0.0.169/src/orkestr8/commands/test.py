from .base import Command


class TestArg:
    pass


class TestCommand(Command[TestArg]):
    @staticmethod
    def parse(args):
        pass

    def run(self):
        with open("main.py", "w") as server_script:
            with open("../../test_script.py") as f:
                data = f.read()
            server_script.write(data)
