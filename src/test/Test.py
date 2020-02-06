
from src.NameGenerator import NameGenerator

if __name__ == "__main__":
    ng = NameGenerator()

    for i in range(10):
        print(ng.get_god_name())