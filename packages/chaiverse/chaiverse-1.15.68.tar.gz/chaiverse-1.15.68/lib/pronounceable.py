import random


def generate_word(length=5):
    word = [_generate_letter(index) for index in range(length)]
    word = ''.join(word)
    return word


def _generate_letter(index):
    consonants = 'bcdfghjklmnpqrstvwxyz'
    vowels = 'aeiou'
    letter = random.choice(vowels) if index % 2 else random.choice(consonants)
    return letter
