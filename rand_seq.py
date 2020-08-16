# -*- coding: utf-8 -*-
from random import randint, choice

alphabet = ["abcdefghijklmnopqrstuvwxyz-", "ABCDEFGHIJKLMNOPQRSTUVWXYZ-"]

def get_new(length=100):

    new_sequence = ''

    while len(new_sequence) != length:
        next_step = choice(["number", "letter"])

        current_step = {
            "number": randint(0, 9),
            "letter": choice(choice(alphabet)),
        }

        for key, value in current_step.items():
            if next_step == key:
                new_sequence += str(value)

    return new_sequence
