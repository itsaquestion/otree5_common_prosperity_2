from os import environ

SESSION_CONFIGS = [
    dict(
        name='ug_inequity',
        app_sequence=['ug', 'inequity_aversion'],
        num_demo_participants=2,
    ),

    dict(
        name='ug_inequity_p8',
        app_sequence=['ug', 'inequity_aversion'],
        num_demo_participants=8,
    ),

    dict(
        name='preface',
        app_sequence=['preface'],
        num_demo_participants=1,
    ),

    dict(
        name='holt_risk_x2_results_payment',
        app_sequence=['holt_risk', 'holt_risk_2', 'results_payment'],
        num_demo_participants=1,
    ),

    dict(
        name='demographics',
        app_sequence=['demographics'],
        num_demo_participants=1,
    ),

    dict(
        name='inequity_aversion_unfinished',
        app_sequence=['inequity_aversion'],
        num_demo_participants=2,
    ),
]

ROOMS = [
    {
        'name': 'pc_99',
        'display_name': 'Room 418',
        'participant_label_file': '_rooms/pc_99.txt'}
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.1, participation_fee=10.00, doc=""
)

PARTICIPANT_FIELDS = [
    'endowment'
    'tag'
]
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'zh-hans'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'CNY'
USE_POINTS = True
POINTS_CUSTOM_NAME = ' '

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '6559744369738'

BROWSER_COMMAND = r"C:\Program Files\Mozilla Firefox\firefox.exe"
