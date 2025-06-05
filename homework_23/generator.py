from faker import Faker
import random

fake = Faker()

def unique_word_generator(count: int):
    """
    Yield `count` unique readable words using Faker.
    Max count = 10_000.
    """
    if not isinstance(count, int) or not (1 <= count <= 10_000):
        raise ValueError("Count must be an integer between 1 and 10_000.")

    words = set()
    attempts = 0
    max_attempts = count * 10

    while len(words) < count and attempts < max_attempts:
        word = fake.word()
        words.add(word)
        attempts += 1

    if len(words) < count:
        raise RuntimeError("Could not generate enough unique words.")

    for word in words:
        yield word
