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

ROOT_FOLDER = os.path.join(os.getcwd(), 'serverapp')
DATA_FOLDER = os.path.join(ROOT_FOLDER, 'scripts')
EXCEL_FILE_NAME = 'PMP Questions Bank.xlsx'

def get_filepath(filename):
    return os.path.join(DATA_FOLDER, filename)

def read_from(filename, sheet):
    wb = load_workbook(filename = get_filepath(filename), read_only=True)
    return wb[sheet]


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

    chaptercategorytype = CategoryType(name='chapter')
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
        
        user = User(name='sudha', full_name='Sudha Sankaran', type_id=teacheruser.id)
        user.set_password('abc123')
        dbsession.add(user)
        dbsession.flush()
        
        chaptercategory = Category(name='TM', type_id=chaptercategorytype.id, creator_id=user.id)
        dbsession.add(chaptercategory)
        dbsession.flush()
        
        print 'Chapter category type is CategoryType id: ', chaptercategorytype.id
        print 'TM Chapter category is Category id: ', chaptercategory.id
        print 'multichoice is QuestionType id: ', multichoice.id
        print 'Teacher is UserType id: ', teacheruser.id
        print 'Student is UserType id: ', studentuser.id

        # Get Questions and Options from Excel File
        table = 'Sheet1'
        header = 'Sl. No.'
        ws = read_from(EXCEL_FILE_NAME, table)
        for row in ws.rows:
            if row[0].value != header and row[2].value != None:
                category = row[1].value
                question = Question(question=row[2].value, type_id=multichoice.id)
                dbsession.add(question)
                dbsession.flush()
                if category == 'TM':
                    dbsession.add(CategoryQuestion(category_id=chaptercategory.id, question_id=question.id))
                correct_option = row[7].value
                # print 'Correct option for question ', question.question, 'is ', correct_option
                q_options = []
                q_options.append(Option(option=row[3].value, question_id=question.id, isCorrectAnswer=False))
                q_options.append(Option(option=row[4].value, question_id=question.id, isCorrectAnswer=False))
                q_options.append(Option(option=row[5].value, question_id=question.id, isCorrectAnswer=False))
                q_options.append(Option(option=row[6].value, question_id=question.id, isCorrectAnswer=False))
                q_options[ord(correct_option)-65].isCorrectAnswer = True
                dbsession.add_all(q_options)

        dbsession.flush()