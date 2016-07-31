import os
import sys
import transaction

from openpyxl import load_workbook
from openpyxl.workbook import Workbook
from openpyxl.compat import range
from openpyxl.cell import get_column_letter

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
    Option,
    QuestionType,
    Category,
    CategoryType,
    CategoryQuestion,
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

    chaptercategorytype = CategoryType(name='Chapter')
    multichoice = QuestionType(name='multiplechoice')
    teacheruser = UserType(name='Teacher')
    studentuser = UserType(name='Student')
    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        print 'User Type Table: ', str(UserType.__table__)
        print 'Question Type Table', str(QuestionType.__table__)
        print 'Category Type Table', str(CategoryType.__table__)
        dbsession.add(chaptercategorytype)
        dbsession.add(multichoice)
        dbsession.add(teacheruser)
        dbsession.add(studentuser)
        dbsession.flush()
        
        # user = User(name='sudha', full_name='Sudha Sankaran', type_id=teacheruser.id)
        # user.set_password('abc123')
        # dbsession.add(user)
        # dbsession.flush()
        
        # chaptercategory = Category(name='TM', type_id=chaptercategorytype.id, creator_id=user.id)
        # dbsession.add(chaptercategory)
        # dbsession.flush()
        
        # print 'Chapter category type is CategoryType id: ', chaptercategorytype.id
        # print 'TM Chapter category is Category id: ', chaptercategory.id
        # print 'multichoice is QuestionType id: ', multichoice.id
        # print 'Teacher is UserType id: ', teacheruser.id
        # print 'Student is UserType id: ', studentuser.id


        dbsession.flush()