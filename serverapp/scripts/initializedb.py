import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )

from ..models import (
    User,
    UserType,
    Question,
    QuestionType,
    Category,
    CategoryType,
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    chapter = CategoryType(name='chapter')
    multichoice = QuestionType(name='multiplechoice')
    adminuser = UserType(name='admin')
    regularuser = UserType(name='regular')
    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        print 'User Type Table: ', str(UserType.__table__)
        print 'Question Type Table', str(QuestionType.__table__)
        print 'Category Type Table', str(CategoryType.__table__)
        dbsession.add(chapter)
        dbsession.add(multichoice)
        dbsession.add(adminuser)
        dbsession.add(regularuser)
        dbsession.flush()
        print 'Chapter is CategoryType id: ', chapter.id
        print 'multichoice is QuestionType id: ', multichoice.id
        print 'admin is UserType id: ', adminuser.id
        print 'regular is UserType id: ', regularuser.id