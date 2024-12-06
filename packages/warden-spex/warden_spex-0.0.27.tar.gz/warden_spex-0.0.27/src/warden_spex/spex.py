import base64
from hashlib import sha256
from importlib.metadata import version

import numpy as np
from rbloom import Bloom

from warden_spex import models


def pkg_version():
    return version("warden_spex")


def hash_array(array: np.ndarray, decimals: int = 4) -> int:
    """
    Given a NumPy array as input and a number of significant decimals
    to consider, return an hash of it, representing the item to be
    inserted in the Bloom fikter.
    """

    assert isinstance(array, np.ndarray)

    # We encode floats to ints, retaining a fixed number of decimals.
    # Differences caused by different digits at a higher decimal position are ignored.
    # https://dassencio.org/98
    # https://stackoverflow.com/questions/14943817/does-stdhash-guarantee-equal-hashes-for-equal-floating-point-numbers
    array = array * (10**decimals)

    # Ensure the array is formatted in memory consistently with fixed type.
    array = np.ascontiguousarray(array.astype(np.uint64))

    # determine hash as bytes.
    hash_bytes = sha256(array.tobytes()).digest()

    # Return hash as int in the range expected by rbloom.
    # https://github.com/KenanHanke/rbloom?tab=readme-ov-file#documentation
    return int.from_bytes(hash_bytes[:16], "big") - 2**127


class Blossom:
    """
    Bloom filter with additional capabilities used by SPEX.
    """

    def __init__(
        self,
        expected_items: int = 1000,
        false_positive_rate: float = 0.01,
        create: bool = True,
    ):
        """
        Create a Bloom filter with a certain number of expected items inserted, and
        an acceptable false positive rate.
        """

        self.inserted_items = 0
        self.expected_items = expected_items

        if create:
            self.bloom = Bloom(
                expected_items=expected_items,
                false_positive_rate=false_positive_rate,
                hash_func=hash_array,
            )
        else:
            self.bloom = None

    def dump(self) -> bytes:
        """
        Serialize Bloom filter to a Base64 sequence of bytes.
        """
        return base64.b64encode(self.bloom.save_bytes())

    def is_hit(self, array: np.ndarray) -> bool:
        """
        Return True if the input `array` is a hit in the Bloom filter.
        """
        return array in self.bloom

    def add(self, array: np.ndarray):
        """
        Add `array` to the Bloom filter.
        """
        if self.inserted_items + 1 > self.expected_items:
            raise Exception("Bloom filter is full, increase `expected_items`")
        self.inserted_items += 1
        self.bloom.add(array)

    @classmethod
    def load(cls, binary: bytes):
        """
        Load `binary` as a serialized Bloom filter.
        """
        blossom = cls(create=False)
        blossom.bloom = Bloom.load_bytes(base64.b64decode(binary), hash_func=hash_array)
        return blossom

    def estimate_false_positive_rate(self):
        """
        Estimate the false positive rate of the current Bloom filter.
        """
        hits = 0
        n = 100000

        for _ in range(n):
            hits += np.random.rand(1) in self.bloom

        estimated = hits / n
        return estimated

    def verify_false_positive_rate(self, expected_rate=0.01, tolerance=0.01):
        """
        Decide if the estimated false positive rate is consistent with the expected value.
        """
        # TODO: tolerance might need to go up if the number of predictions is very low
        # to match the deteriorating estimate quality.
        estimated = self.estimate_false_positive_rate()
        print(
            f"[debug] estimated={estimated} expected={expected_rate} tolerance={tolerance}"
        )
        return expected_rate + tolerance >= estimated


class Solver:
    """
    Class to implement for solver tasks, to implement solvers and verifiers.
    """

    @staticmethod
    def solve(request: models.SolverRequest) -> models.SolverResponse: ...

    @staticmethod
    def verify(request: models.VerifierRequest) -> models.VerifierResponse: ...
