import pickle


class Memento:

    def __init__(self):
        self._states = {}

    def save_state(self, key, state):
        self._states[key] = state

    def get_state(self, key):
        return self._states[key]

    def save_to_disk(self, path):
        with open(path, "wb") as f:
            pickle.dump(self._states, f)

    def restore_from_disk(self, path):
        with open(path, "rb") as f:
            self._states = pickle.load(f)


if __name__ == "__main__":
    m = Memento()
    m.save_state("1", [1, 2, 3, 4])
    m.save_state("2", [3, 4, [5, 6], [7, 8]])
    m.save_to_disk("test.bin")
    m1 = Memento()
    m1.restore_from_disk("test.bin")
    print(m1.get_state("1"))
    print(m1.get_state("2"))
