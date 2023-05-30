import random

from otree.api import *

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'ia'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 2

    PROP_ROLE = '提议者'
    RESP_ROLE = '回应者'


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    """保持treatment不变，treatment内随机组合，并且2轮扮演不同角色。
    """


    for p in subsession.get_players():
        p.treatment = p.participant.vars['treatment']

    treatments = list(set([p.treatment for p in subsession.get_players()]))

    # 2个treatment组
    t1p = [p.id_in_subsession for p in subsession.get_players() if p.treatment == treatments[0]]
    t2p = [p.id_in_subsession for p in subsession.get_players() if p.treatment == treatments[1]]

    print(f'{subsession.round_number=}')

    def regroup(x, odd_first=True):
        """ 返回一个奇数在前，或者偶数在前的乱序zip
        1. 乱序
        2. 提取奇数组和偶数组
        3. 奇数和偶数组进行zip
        4. 返回一个奇数在前，或者偶数在前的乱序zip
        :param x: 要处理的list
        :param odd_first: 是否奇数在前
        :return: 乱序后的zip
        """
        tp = x.copy()
        random.shuffle(tp)
        # print(f"乱序:{tp}")

        # 奇数
        tp_o = [p for p in tp if p % 2 == 1]
        tp_e = [p for p in tp if p % 2 == 0]

        if odd_first:
            return list(zip(tp_o, tp_e))
        else:
            return list(zip(tp_e, tp_o))

    rn = subsession.round_number
    gm = regroup(t1p, rn % 2 == 1) + regroup(t2p, rn % 2 == 1)

    print(f'{gm=}')

    subsession.set_group_matrix(gm)



class Group(BaseGroup):
    offer = models.FloatField()
    respond = models.BooleanField()


class Player(BasePlayer):
    treatment = models.StringField()

    respond = models.BooleanField(
        choices=[[True, '接受'],
                 [False, '拒绝']],
        widget=widgets.RadioSelectHorizontal,
        label='请你决定是否接受该分配方案？'
    )

    profit = models.FloatField()
    partner_profit = models.FloatField()

    offer = models.FloatField(
        min=0, max=20,
        label='你将分给配对者多少代币？'
    )


# PAGES
class Offer(Page):
    form_model = 'player'
    form_fields = ['offer']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.PROP_ROLE

    @staticmethod
    def vars_for_template(player: Player):
        info = [(p.participant.id, p.role) for p in player.subsession.get_players()]
        gm = player.subsession.get_group_matrix()

        return dict(info=info, gm=gm)


class Respond(Page):
    """回应页面"""
    form_model = 'player'
    form_fields = ['respond']

    @staticmethod
    def vars_for_template(player: Player):
        info = [(p.participant.id, p.role) for p in player.subsession.get_players()]
        gm = player.subsession.get_group_matrix()

        return dict(info=info, gm=gm)

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.RESP_ROLE


class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        group.respond = group.get_player_by_role(C.RESP_ROLE).respond
        if not group.respond:
            for p in group.get_players():
                p.profit = 0
        else:
            group.get_player_by_role(C.PROP_ROLE).profit = group.offer
            group.get_player_by_role(C.RESP_ROLE).profit = 20 - group.offer


class Results(Page):
    pass


class Intro(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        info = [(p.id_in_subsession, p.role) for p in player.subsession.get_players()]
        gm = player.subsession.get_group_matrix()

        return dict(info=info, gm=gm)


class OfferWaitPage(WaitPage):

    @staticmethod
    def after_all_players_arrive(group: Group):
        group.offer = group.get_player_by_role(C.PROP_ROLE).offer


page_sequence = [Intro, Offer, OfferWaitPage, Respond, ResultsWaitPage, Results]
