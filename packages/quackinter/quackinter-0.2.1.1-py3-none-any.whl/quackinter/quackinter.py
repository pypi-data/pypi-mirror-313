from quackinter.config import Config
from quackinter.interpreter import Interpreter


def interpret(ducky: str, config: Config | None = None):
    interpreter = Interpreter(config=config)
    return interpreter.interpret_text(ducky)

def main():
    print("Await 1 second...")
    config = Config(delay=1000)
    interpret(
        """
WIN r
DELAY 1000
STRINGLN powershell
DELAY 1000
STRINGLN notepad
DELAY 1000
STRINGLN -----------------------
STRINGLN       QUACKINTER
STRINGLN -----------------------
STRINGLN  -> The best DuckyScript 
STRINGLN     interpreter for 
STRINGLN     Windows/Mac/Linux
""",
        config,
    )

if __name__ == "__main__":
    main()
