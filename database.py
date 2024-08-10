import os
import ydb

YDB_ENDPOINT = os.getenv("YDB_ENDPOINT")
YDB_DATABASE = os.getenv("YDB_DATABASE")


def get_ydb_pool(ydb_endpoint, ydb_database, timeout=30):
    ydb_driver_config = ydb.DriverConfig(
        ydb_endpoint,
        ydb_database,
        credentials=ydb.credentials_from_env_variables(),
        root_certificates=ydb.load_ydb_root_certificate(),
    )

    ydb_driver = ydb.Driver(ydb_driver_config)
    ydb_driver.wait(fail_fast=True, timeout=timeout)
    return ydb.SessionPool(ydb_driver)


def _format_kwargs(kwargs):
    return {"${}".format(key): value for key, value in kwargs.items()}



def execute_update_query(pool, query, **kwargs):
    def callee(session):
        prepared_query = session.prepare(query)
        session.transaction(ydb.SerializableReadWrite()).execute(
            prepared_query, _format_kwargs(kwargs), commit_tx=True
        )
    return pool.retry_operation_sync(callee)


def execute_select_query(pool, query, **kwargs):
    def callee(session):
        prepared_query = session.prepare(query)
        result_sets = session.transaction(ydb.SerializableReadWrite()).execute(
            prepared_query, _format_kwargs(kwargs), commit_tx=True
        )
        return result_sets[0].rows

    return pool.retry_operation_sync(callee)    


pool = get_ydb_pool(YDB_ENDPOINT, YDB_DATABASE)


#Структура квиза............................
quiz_data = [
    {
        'question': 'Что такое Python?',
        'options': ['Язык программирования', 'Тип данных', 'Музыкальный инструмент', 'Змея на английском'],
        'correct_option': 0
    },
    {
        'question': 'Какой тип данных используется для хранения целых чисел?',
        'options': ['int', 'float', 'str', 'natural'],
        'correct_option': 0
    },
    {
        'question': 'Рассказывают, что один известный человек увидел женщину, баюкавшую младенца, умилился и тоже захотел хоть на время почувствовать себя ребенком. Придя домой, он создал свое изобретение. Уже в нашем веке это изобретение снабдили аккумулятором, позволяющим владельцу самостоятельно запасти энергию для электрической лампы. Назовите это изобретение.',
        'options': ['кресло-качалка', 'массажное кресло', 'люлька', 'детский мобиль'],
        'correct_option': 0
    },
    {
        'question': 'Во внутренних покоях Амберской цитадели в Индии есть так называемый чертог тысячи ИХ, который можно осветить одной свечой. Назовите ИХ.',
        'options': ['зеркала', 'портреты', 'отражения', 'комнаты'],
        'correct_option': 0
    },
    {
        'question': 'В произведении Дэвида Айвза "Слова, слова, слова" действуют герои Мильтон, Свифт и Кафка, являющиеся ИМИ. При этом каждый из НИХ имеет дело с одним и тем же устройством. Назовите это устройство двумя словами.',
        'options': ['печатная машинка', 'компьютер', 'печатный станок', 'Интернет'],
        'correct_option': 0
    },{
        'question': 'Впервые ЭТО СДЕЛАЛ Тадеуш Ватовский в 1924 году. Когда у Николая Фоменко на вступительных экзаменах в театральный вуз спросили, почему он до сих пор не избавился от дефекта речи, актер ответил, что всю жизнь мечтал СДЕЛАТЬ ЭТО. Что такое "СДЕЛАТЬ ЭТО"?',
        'options': ['Сыграть Ленина', 'сыграть Георга 6', 'сыграть Льюиса Кэррола', 'сыграть Уинстона Черчилля'],
        'correct_option': 0
    },
    {
        'question': 'Героиня шуточного рисунка и ее бабушка сидят за столом. Бабушка говорит: "Упс, у меня получился шарф". Ответьте точно, чему ее так и не смогла научить героиня.',
        'options': ['вязать', 'есть лапшу палочками', 'готовить', 'завязывать косички'],
        'correct_option': 1
    },
    {
        'question': 'На футболисте Кака в одном из матчей под разминочной футболкой была куртка с капюшоном. С каким персонажем французской литературы сравнил его в связи с этим комментатор?',
        'options': ['Квазимодо', 'Робин Гуд', 'Красная шапочка', 'Питер Пен'],
        'correct_option': 0
    },
    {
        'question': 'Рекламный слоган одного банка звучал так: "СДЕЛАЙ ЭТО и возьми ипотеку". Герой поучительной истории с печальным концом появился благодаря тому, что сначала СДЕЛАЛИ ЭТО. Назовите упомянутого героя.',
        'options': ['Колобок', 'Ворона', 'Лисица', 'Буратино'],
        'correct_option': 0
    },
    {
        'question': 'Раздаточный материал: После смерти деньги превращаются в чеки. Если изъять любовь, Что останется В чеке? Перед вами фрагмент стихотворения Ивана Полторацкого. Какие четыре английских буквы в этом фрагменте мы пропустили?',
        'options': ['love', 'hate', 'soul', 'like'],
        'correct_option': 0
    },
    # Добавьте другие вопросы
]
