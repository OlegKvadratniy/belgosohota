import json
import random

class QuestionLoader:
    def __init__(self, json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            self.questions = json.load(f)
        self.current_mode = None  # Will be set by the app: ('topic', topic_id) or ('exam', None)
    
    def get_topic_questions(self, topic_id, count=10):
        """Return `count` random questions from the given topic. If count is None, return all."""
        topic_questions = [q for q in self.questions if q['topic'] == topic_id]
        if count is None or len(topic_questions) <= count:
            selected = topic_questions
        else:
            selected = random.sample(topic_questions, count)
        return [self._shuffle_question(q) for q in selected]
    
    def get_exam_questions(self):
        """Return exam questions: 2 from topic1, 3 from topic2, 3 from topic3, 2 from topic4."""
        exam_questions = []
        exam_questions.extend(self.get_topic_questions(1, 2))
        exam_questions.extend(self.get_topic_questions(2, 3))
        exam_questions.extend(self.get_topic_questions(3, 3))
        exam_questions.extend(self.get_topic_questions(4, 2))
        # Shuffle the combined list
        random.shuffle(exam_questions)
        return exam_questions
    
    def get_questions_for_mode(self):
        """Return questions based on current_mode."""
        if self.current_mode is None:
            return []
        if self.current_mode[0] == 'topic':
            return self.get_topic_questions(self.current_mode[1])
        elif self.current_mode[0] == 'topic_all':
            return self.get_topic_questions(self.current_mode[1], count=None)
        elif self.current_mode[0] == 'exam':
            return self.get_exam_questions()
        elif self.current_mode[0] == 'all':
            return self.get_all_questions()
        elif self.current_mode[0] == 'test':
            return self.get_test_questions()
        else:
            return []
    
    def get_all_questions(self):
        """Return all questions shuffled with options shuffled per-question."""
        all_qs = [self._shuffle_question(q) for q in self.questions]
        random.shuffle(all_qs)
        return all_qs

    def get_test_questions(self):
        """Return 2 easy questions for quick visual test."""
        easy = [q for q in self.questions if q['topic'] == 1 and len(q['options']) <= 4]
        if len(easy) < 2:
            easy = [q for q in self.questions if q['topic'] == 1]
        selected = random.sample(easy, 2)
        return [self._shuffle_question(q) for q in selected]
    
    def _shuffle_question(self, question):
        """Shuffle the options of a question and adjust correct_answers accordingly."""
        # Make a copy to avoid modifying the original
        shuffled = question.copy()
        options = shuffled['options']
        correct_indices = shuffled['correct_answers']
        
        # Create a list of indices and shuffle them
        indices = list(range(len(options)))
        random.shuffle(indices)
        
        # Reorder options according to shuffled indices
        shuffled['options'] = [options[i] for i in indices]
        
        # Update correct_answers: for each original correct index, find its new position
        new_correct = []
        for orig_idx in correct_indices:
            # Find where the original index went in the shuffled list
            new_pos = indices.index(orig_idx)
            new_correct.append(new_pos)
        shuffled['correct_answers'] = sorted(new_correct)  # sort for consistency
        
        return shuffled