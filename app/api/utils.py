from app.db import get_db


def get_quiz(raw_quiz):
    db = get_db()
    questions = raw_quiz['question_list']
    quiz = {
        '_id': str(raw_quiz['_id']),
        'date': raw_quiz['date'].time,
        'question_list': [],
        'total_num': len(questions),
        'correct_num': len([q['score'] for q in questions if q['score'] == 1]),
        'time_used': raw_quiz['time_used'],
        'scored': len([q['score'] for q in questions if q['score'] == -1]) == 0
    }
    from bson.objectid import ObjectId
    for q in questions:
        tmp_qes = {
            'qid': q['qid'],
            'description': db.question.find_one({'_id': ObjectId(q['qid'])}).get('description'),
            'answer': q['answer']
        }
        if q['score'] == 1:
            tmp_qes['is_correct'] = True
        elif q['score'] == 0:
            tmp_qes['is_correct'] = False
        quiz['question_list'].append(tmp_qes)
    return quiz

