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
    subsession.group_randomly()


class Group(BaseGroup):
    offer = models.FloatField()


class Player(BasePlayer):
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


class Respond(Page):
    """回应页面"""
    form_model = 'player'
    form_fields = ['respond']

    @staticmethod
    def vars_for_template(player: Player):
        pass

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.RESP_ROLE


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


class Intro(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.round_number == 1


class OfferWaitPage(WaitPage):

    @staticmethod
    def after_all_players_arrive(group: Group):
        group.offer = group.get_player_by_role(C.PROP_ROLE).offer


page_sequence = [Intro, Offer, OfferWaitPage, Respond, ResultsWaitPage, Results]
