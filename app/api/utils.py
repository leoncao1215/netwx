from app.db import get_db


def get_quiz(raw_quiz):
    db = get_db()
    questions = raw_quiz['question_list']
    quiz = {
        '_id': str(raw_quiz['_id']),
        'date': raw_quiz['date'].time * 1000,
        'question_list': [],
        'total_num': len(questions),
        'correct_num': len([q['score'] for q in questions if q['score'] == 1]),
        'time_used': raw_quiz['time_used'],
        'scored': len([q['score'] for q in questions if q['score'] == -1]) == 0,
        'category': str(raw_quiz['category'])
    }
    from bson.objectid import ObjectId
    for q in questions:
        ques = db.question.find_one({'_id': ObjectId(q['qid'])})
        tmp_qes = {
            'qid': q['qid'],
            'description': ques['description'],
            'answer': ques['answer'],
            'myAnswer': q['answer'],
            'date': ques['date'].time * 1000,
            'url': ques['url'] if 'url' in ques else None
        }
        if q['score'] == 1:
            tmp_qes['is_correct'] = True
        elif q['score'] == 0:
            tmp_qes['is_correct'] = False
        quiz['question_list'].append(tmp_qes)
    return quiz


def boolean(v: str):
    if v.lower() == 'true':
        return True
    return False


def get_upload_path():
    import os
    import sys
    return os.path.join(sys.path[0], 'static/uploads')

