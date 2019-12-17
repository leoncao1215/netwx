from app.db import get_db

def get_quiz(raw_quiz):
    db = get_db()
    questions = raw_quiz['question_list']
    quiz = {
        'id': raw_quiz['id'],
        'date': raw_quiz['date'].time,
        'question_list': [],
        'total_num': len(questions),
        'correct_num': len([q['score'] for q in questions if q['score'] == 1]),
        'timing': sum([q['timing'] for q in questions]),
        'scored': len([q['score'] for q in questions if q['score'] == -1]) == 0
    }
    for q in questions:
        tmp_qes = {
            'qid': q['qid'],
            'description': db.question.find_one({'id': q['qid']}).get('question'),
            'answer': q['answer'],
            'scored': q['score'] != -1,
            'timing': q['timing']
        }
        if q['score'] == 1:
            tmp_qes['is_correct'] = True
        elif q['score'] == 0:
            tmp_qes['is_correct'] = False
        quiz['question_list'].append(tmp_qes)
    return quiz

