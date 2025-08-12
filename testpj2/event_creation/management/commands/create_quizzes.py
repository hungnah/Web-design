from django.core.management.base import BaseCommand
from event_creation.models import Lesson, QuizQuestion

class Command(BaseCommand):
    help = 'Create quiz questions for Vietnamese language lessons'

    def handle(self, *args, **options):
        self.stdout.write('Creating quiz questions for lessons...')
        
        quiz_data = {
            'greetings': [
                {
                    'question': 'Câu "Xin chào" có nghĩa gì?',
                    'option_a': 'Goodbye',
                    'option_b': 'Hello',
                    'option_c': 'Thank you',
                    'option_d': 'Sorry',
                    'correct_answer': 'B',
                    'explanation': '"Xin chào" có nghĩa là "Hello" trong tiếng Anh'
                },
                {
                    'question': 'Khi nào bạn nói "Chào buổi sáng"?',
                    'option_a': 'Buổi tối',
                    'option_b': 'Buổi trưa',
                    'option_c': 'Buổi sáng',
                    'option_d': 'Cả ngày',
                    'correct_answer': 'C',
                    'explanation': '"Chào buổi sáng" dùng để chào hỏi vào buổi sáng'
                },
                {
                    'question': 'Câu "Bạn khỏe không?" dùng để làm gì?',
                    'option_a': 'Chào hỏi',
                    'option_b': 'Hỏi thăm sức khỏe',
                    'option_c': 'Tạm biệt',
                    'option_d': 'Xin lỗi',
                    'correct_answer': 'B',
                    'explanation': 'Câu này dùng để hỏi thăm sức khỏe của người khác'
                }
            ],
            'self_introduction': [
                {
                    'question': 'Cách giới thiệu tên trong tiếng Việt là gì?',
                    'option_a': 'Tôi là...',
                    'option_b': 'Tôi tên là...',
                    'option_c': 'Tôi đến từ...',
                    'option_d': 'Tôi sống ở...',
                    'correct_answer': 'B',
                    'explanation': '"Tôi tên là..." là cách giới thiệu tên chuẩn trong tiếng Việt'
                },
                {
                    'question': 'Câu "Tôi ... tuổi" dùng để làm gì?',
                    'option_a': 'Giới thiệu tên',
                    'option_b': 'Giới thiệu tuổi',
                    'option_c': 'Giới thiệu quê quán',
                    'option_d': 'Giới thiệu nghề nghiệp',
                    'correct_answer': 'B',
                    'explanation': 'Câu này dùng để giới thiệu tuổi của mình'
                }
            ],
            'asking_directions': [
                {
                    'question': 'Cách hỏi đường lịch sự trong tiếng Việt là gì?',
                    'option_a': 'Chỉ đường cho tôi!',
                    'option_b': 'Xin lỗi, bạn có thể chỉ đường không?',
                    'option_c': 'Đường này đi đâu?',
                    'option_d': 'Tôi muốn đi...',
                    'correct_answer': 'B',
                    'explanation': 'Cách hỏi đường lịch sự nhất là "Xin lỗi, bạn có thể chỉ đường không?"'
                },
                {
                    'question': 'Khi muốn đi thẳng, bạn nói gì?',
                    'option_a': 'Rẽ phải',
                    'option_b': 'Rẽ trái',
                    'option_c': 'Đi thẳng',
                    'option_d': 'Dừng lại',
                    'correct_answer': 'C',
                    'explanation': '"Đi thẳng" có nghĩa là "Go straight"'
                }
            ],
            'shopping': [
                {
                    'question': 'Câu "Cái này giá bao nhiêu?" dùng để làm gì?',
                    'option_a': 'Hỏi giá sản phẩm',
                    'option_b': 'Mặc cả giá',
                    'option_c': 'Yêu cầu giảm giá',
                    'option_d': 'Thanh toán',
                    'correct_answer': 'A',
                    'explanation': 'Câu này dùng để hỏi giá của sản phẩm'
                },
                {
                    'question': 'Khi muốn mua sản phẩm, bạn nói gì?',
                    'option_a': 'Tôi không thích cái này',
                    'option_b': 'Tôi muốn mua cái này',
                    'option_c': 'Cái này đắt quá',
                    'option_d': 'Cho tôi xem cái khác',
                    'correct_answer': 'B',
                    'explanation': '"Tôi muốn mua cái này" có nghĩa là "I want to buy this"'
                }
            ],
            'restaurant': [
                {
                    'question': 'Khi muốn xem menu, bạn nói gì?',
                    'option_a': 'Cho tôi xem thực đơn',
                    'option_b': 'Tôi muốn gọi món',
                    'option_c': 'Món này ngon quá',
                    'option_d': 'Xin hóa đơn',
                    'correct_answer': 'A',
                    'explanation': '"Cho tôi xem thực đơn" có nghĩa là "Please show me the menu"'
                },
                {
                    'question': 'Khi muốn thanh toán, bạn nói gì?',
                    'option_a': 'Cho tôi thêm nước',
                    'option_b': 'Món này cay quá',
                    'option_c': 'Xin hóa đơn',
                    'option_d': 'Tôi muốn gọi món khác',
                    'correct_answer': 'C',
                    'explanation': '"Xin hóa đơn" có nghĩa là "The bill, please"'
                }
            ],
            'transportation': [
                {
                    'question': 'Khi muốn hỏi điểm dừng xe buýt, bạn nói gì?',
                    'option_a': 'Xe buýt dừng ở đâu?',
                    'option_b': 'Tôi muốn đi xe buýt',
                    'option_c': 'Xe buýt có đắt không?',
                    'option_d': 'Xe buýt đi đâu?',
                    'correct_answer': 'A',
                    'explanation': '"Xe buýt dừng ở đâu?" có nghĩa là "Where does the bus stop?"'
                },
                {
                    'question': 'Khi muốn mua vé, bạn nói gì?',
                    'option_a': 'Tôi muốn đi bộ',
                    'option_b': 'Tôi muốn mua vé đến...',
                    'option_c': 'Vé có đắt không?',
                    'option_d': 'Tôi muốn đi taxi',
                    'correct_answer': 'B',
                    'explanation': '"Tôi muốn mua vé đến..." có nghĩa là "I want to buy a ticket to..."'
                }
            ],
            'weather': [
                {
                    'question': 'Khi trời nắng, bạn nói gì?',
                    'option_a': 'Trời mưa',
                    'option_b': 'Trời lạnh',
                    'option_c': 'Hôm nay trời nắng',
                    'option_d': 'Trời âm u',
                    'correct_answer': 'C',
                    'explanation': '"Hôm nay trời nắng" có nghĩa là "It is sunny today"'
                },
                {
                    'question': 'Khi trời mưa, bạn nói gì?',
                    'option_a': 'Trời nắng',
                    'option_b': 'Trời mưa',
                    'option_c': 'Trời lạnh',
                    'option_d': 'Trời nóng',
                    'correct_answer': 'B',
                    'explanation': '"Trời mưa" có nghĩa là "It is raining"'
                }
            ],
            'family': [
                {
                    'question': 'Khi giới thiệu gia đình, bạn nói gì?',
                    'option_a': 'Đây là bạn tôi',
                    'option_b': 'Đây là gia đình tôi',
                    'option_c': 'Đây là nhà tôi',
                    'option_d': 'Đây là phòng tôi',
                    'correct_answer': 'B',
                    'explanation': '"Đây là gia đình tôi" có nghĩa là "This is my family"'
                },
                {
                    'question': 'Khi gọi bố, bạn nói gì?',
                    'option_a': 'Mẹ tôi',
                    'option_b': 'Bố tôi',
                    'option_c': 'Anh trai tôi',
                    'option_d': 'Chị gái tôi',
                    'correct_answer': 'B',
                    'explanation': '"Bố tôi" có nghĩa là "My father"'
                }
            ],
            'health_emergency': [
                {
                    'question': 'Khi bị ốm, bạn nói gì?',
                    'option_a': 'Tôi khỏe',
                    'option_b': 'Tôi bị ốm',
                    'option_c': 'Tôi vui',
                    'option_d': 'Tôi buồn',
                    'correct_answer': 'B',
                    'explanation': '"Tôi bị ốm" có nghĩa là "I am sick"'
                },
                {
                    'question': 'Khi cần cấp cứu, bạn nói gì?',
                    'option_a': 'Gọi cảnh sát',
                    'option_b': 'Gọi cấp cứu',
                    'option_c': 'Gọi taxi',
                    'option_d': 'Gọi xe buýt',
                    'correct_answer': 'B',
                    'explanation': '"Gọi cấp cứu" có nghĩa là "Call an ambulance"'
                }
            ],
            'time_schedule': [
                {
                    'question': 'Khi muốn hỏi giờ, bạn nói gì?',
                    'option_a': 'Bây giờ là mấy giờ?',
                    'option_b': 'Hôm nay là thứ mấy?',
                    'option_c': 'Tháng này là tháng mấy?',
                    'option_d': 'Năm nay là năm mấy?',
                    'correct_answer': 'A',
                    'explanation': '"Bây giờ là mấy giờ?" có nghĩa là "What time is it now?"'
                },
                {
                    'question': 'Khi muốn hỏi lịch rảnh, bạn nói gì?',
                    'option_a': 'Bạn có bận không?',
                    'option_b': 'Bạn có rảnh vào... không?',
                    'option_c': 'Bạn có thời gian không?',
                    'option_d': 'Bạn có thể gặp tôi không?',
                    'correct_answer': 'B',
                    'explanation': '"Bạn có rảnh vào... không?" có nghĩa là "Are you free on...?"'
                }
            ]
        }
        
        created_quizzes = 0
        
        for category, questions in quiz_data.items():
            lesson = Lesson.objects.filter(category=category).first()
            if lesson:
                for i, quiz_info in enumerate(questions):
                    quiz, created = QuizQuestion.objects.get_or_create(
                        lesson=lesson,
                        question=quiz_info['question'],
                        defaults={
                            'option_a': quiz_info['option_a'],
                            'option_b': quiz_info['option_b'],
                            'option_c': quiz_info['option_c'],
                            'option_d': quiz_info['option_d'],
                            'correct_answer': quiz_info['correct_answer'],
                            'explanation': quiz_info['explanation'],
                            'order': i + 1
                        }
                    )
                    
                    if created:
                        created_quizzes += 1
                        self.stdout.write(f'Created quiz for {category}: {quiz.question[:30]}...')
            else:
                self.stdout.write(f'Warning: No lesson found for category {category}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_quizzes} quiz questions!')
        )
