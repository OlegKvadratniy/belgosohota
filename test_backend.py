import json
from utils.question_loader import QuestionLoader

def test_question_loader():
    # Initialize with our test questions (we'll use the same file)
    loader = QuestionLoader("questions.json")
    
    # Test getting topic questions
    print("Testing topic 1 questions (should get 10, but we have less, so all):")
    topic1_qs = loader.get_topic_questions(1)
    print(f"Got {len(topic1_qs)} questions from topic 1")
    for i, q in enumerate(topic1_qs[:2]):  # Show first 2
        print(f"  Q{i+1}: {q['question']}")
        print(f"    Options: {q['options']}")
        print(f"    Correct indices: {q['correct_answers']}")
        print(f"    Is multiple: {q['is_multiple']}")
    
    # Test exam questions
    print("\nTesting exam questions:")
    exam_qs = loader.get_exam_questions()
    print(f"Got {len(exam_qs)} questions for exam")
    # Count by topic
    topic_count = {1:0, 2:0, 3:0, 4:0}
    for q in exam_qs:
        topic_count[q['topic']] += 1
    print(f"Topic distribution: {topic_count}")
    
    # Test shuffling: ensure correct_answers are updated correctly
    print("\nTesting shuffling consistency:")
    # Take a question and shuffle it multiple times, check that the correct answers are still correct
    original_q = loader.questions[0]  # First question
    print(f"Original question: {original_q['question']}")
    print(f"Original options: {original_q['options']}")
    print(f"Original correct: {original_q['correct_answers']}")
    
    # Shuffle it 5 times
    for i in range(5):
        shuffled = loader._shuffle_question(original_q)
        print(f"\nShuffle {i+1}:")
        print(f"  Options: {shuffled['options']}")
        print(f"  Correct indices: {shuffled['correct_answers']}")
        # Verify that the options at the correct indices are indeed the correct ones
        for idx in shuffled['correct_answers']:
            # The option at this index should be one of the originally correct options
            option_text = shuffled['options'][idx]
            # Find this option in the original options
            if option_text in original_q['options']:
                orig_idx = original_q['options'].index(option_text)
                if orig_idx in original_q['correct_answers']:
                    print(f"    Option '{option_text}' is correct (was originally at index {orig_idx})")
                else:
                    print(f"    ERROR: Option '{option_text}' is marked correct but was not originally correct")
            else:
                print(f"    ERROR: Option '{option_text}' not found in original options")

if __name__ == "__main__":
    test_question_loader()