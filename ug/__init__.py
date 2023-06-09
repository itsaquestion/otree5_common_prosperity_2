import itertools
import random

import pandas as pd

from otree.api import *

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'ug'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 10
    PROP_ROLE = '提议者'
    RESP_ROLE = '回应者'

    PARAMS_DF = pd.read_csv('ug/params.csv').astype(int, errors='ignore')

    PARAMS = dict()


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    """
    创建session时，乱序，并分配endowment
    """
    p1: Player
    p2: Player
    p: Player
    g: Group

    """
    所有人循环分配treatment，因此奇数和偶数分别是一个treatment
    """

    treatments = ['cue', 'cue', 'no_cue', 'no_cue']
    tm = itertools.cycle(treatments)
    for p in subsession.get_players():
        p.treatment = next(tm)
        p.participant.vars['treatment'] = p.treatment

    print([p.treatment for p in subsession.get_players()])

    """
    对同一个treatment的player，进行乱序，重组，再组成完整的group matrix

    """
    n = len(subsession.get_players())
    id_list = (list(range(1, n + 1)))

    p = subsession.get_players()[0]

    cue_list = [p.participant.id_in_session for p in subsession.get_players() if p.treatment == 'cue']
    no_cue_list = [p.participant.id_in_session for p in subsession.get_players() if p.treatment == 'no_cue']

    def group_elements(original_list):
        """
        对一个List乱序，然后22组合；
        """
        random.shuffle(original_list)

        new_list = []

        for i in range(0, len(original_list), 2):
            new_list.append(original_list[i:i + 2])

        return new_list

    group_matrix = group_elements(cue_list) + group_elements(no_cue_list)
    print(group_matrix)

    subsession.set_group_matrix(group_matrix)

    """
    读取本轮参数，然后写入每个组以及参与人中
    """
    # 生成一个大列表，按轮次,抽取某一行作为参数
    params = get_params(subsession.round_number)
    print(f"{params=}")


def get_params(round_number):
    # 生成一个大列表，按轮次,抽取某一行作为参数
    params = C.PARAMS_DF.query(f"round == {round_number}").iloc[0].to_dict()
    return params


class Group(BaseGroup):
    choice = models.StringField()
    respond = models.BooleanField()
    real_plan = models.StringField()
    offer = models.FloatField()


class Player(BasePlayer):
    treatment = models.StringField()

    choice = models.StringField(
        choices=['A', 'B'],
        widget=widgets.RadioSelect,
        label='你的选择是？'
    )

    respond = models.BooleanField(
        choices=[[True, '接受'],
                 [False, '拒绝']],
        widget=widgets.RadioSelectHorizontal,
        label='请你决定是否接受提议者的分配方案？'
    )

    profit = models.FloatField()
    partner_profit = models.FloatField()

    offer = models.FloatField(
        min=0,
        label='你愿意转移多少代币给配对者？'
    )

    keep = models.FloatField()

    hope = models.FloatField(
        min=0,
        label='1. 你希望配对者转移多少代币给你？'
    )

    guess = models.FloatField(
        min=0,
        label='2.你猜测配对者实际将转移多少代币给你？'
    )


def offer_max(player):
    return player.profit


class Intro(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group_matrix = player.subsession.get_group_matrix()
        return dict(gm=group_matrix)

    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.round_number == 1


class Propose(Page):
    """提议页面"""

    form_model = 'player'
    form_fields = ['choice']

    @staticmethod
    def vars_for_template(player: Player):
        group_matrix = player.subsession.get_group_matrix()
        params_dict = get_params(player.round_number)
        return dict(gm=group_matrix, params=params_dict)

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.PROP_ROLE


class Respond(Page):
    """回应页面"""
    form_model = 'player'
    form_fields = ['respond']

    @staticmethod
    def vars_for_template(player: Player):
        group_matrix = player.subsession.get_group_matrix()
        params_dict = get_params(player.round_number)
        return dict(gm=group_matrix, params=params_dict)

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.RESP_ROLE


class PropWaitPage(WaitPage):

    @staticmethod
    def after_all_players_arrive(group: Group):
        group.choice = group.get_player_by_role(C.PROP_ROLE).choice


class RespWaitPage(WaitPage):

    @staticmethod
    def after_all_players_arrive(group: Group):
        params = get_params(group.round_number)

        p1 = group.get_player_by_role(C.PROP_ROLE)
        p2 = group.get_player_by_role(C.RESP_ROLE)

        group.choice = p1.choice
        group.real_plan = p1.choice

        group.respond = p2.respond

        if not p2.respond:
            group.real_plan = 'A' if p1.choice == 'B' else 'B'

        print(f'{p2.respond=}')
        print(f'{p1.choice=}')
        print(f'{group.real_plan=}')

        p1.profit = params[group.real_plan.lower() + '_prop']
        p2.profit = params[group.real_plan.lower() + '_resp']

        p2.partner_profit = p1.profit
        p1.partner_profit = p2.profit


class PropResults(Page):
    pass


class ResultsWaitPage(Page):
    pass


class RespResults(Page):
    pass


class Results(Page):
    pass


class Offer(Page):
    form_model = 'player'
    form_fields = ['offer']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.PROP_ROLE


class Guess(Page):
    form_model = 'player'
    form_fields = ['guess', 'hope']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.RESP_ROLE


class OfferWaitPage(WaitPage):

    @staticmethod
    def after_all_players_arrive(group: Group):
        p1 = group.get_player_by_role(C.PROP_ROLE)
        p2 = group.get_player_by_role(C.RESP_ROLE)

        group.offer = p1.offer

        p1.profit -= p1.offer
        p2.profit += p1.offer

        if group.round_number == C.NUM_ROUNDS:
            for p in group.get_players():
                rounds = list(range(1, C.NUM_ROUNDS + 1))
                pick = random.sample(rounds, 2)

                profit = [p.in_round(x).profit for x in pick]

                p.participant.vars['ug'] = dict(
                    pick=pick,
                    profit=profit
                )


class OfferResults(Page):
    pass


page_sequence = [Intro,
                 Propose, PropWaitPage, Respond, RespWaitPage, RespResults,
                 Offer, Guess, OfferWaitPage, OfferResults
                 ]
