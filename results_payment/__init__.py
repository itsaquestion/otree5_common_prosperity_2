import os
import random

from otree.api import *

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'results_payment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    final_payment = models.FloatField()


class Results(Page):

    @staticmethod
    def vars_for_template(player: Player):
        pick = random.choice([1, 3, 4])
        picks = sorted([2, pick])
        p1 = player.participant.vars['holt_risk']['profit']
        p2 = sum(player.participant.vars['ug']['profit'])
        p3 = player.participant.vars['holt_risk_2']['profit']
        p4 = player.participant.vars['ia']['profit']

        profits = [p1, p2, p3, p4]

        player.final_payment = sum([profits[pi - 1] for pi in picks]) / 10 + 10

        return dict(
            picks=picks,
            p1=p1,
            p2=p2,
            p3=p3,
            p4=p4,
            profits=profits,
            final_payment=player.final_payment

        )


page_sequence = [Results]
