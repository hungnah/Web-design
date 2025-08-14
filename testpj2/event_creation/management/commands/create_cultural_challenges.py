from django.core.management.base import BaseCommand
from event_creation.models import CulturalLocation, CulturalChallenge

class Command(BaseCommand):
    help = 'Create cultural challenges for each cultural location'

    def handle(self, *args, **options):
        challenges_data = [
            # Văn Miếu - Quốc Tử Giám
            {
                'location_name': 'Văn Miếu - Quốc Tử Giám',
                'title': 'Thử thách tìm hiểu lịch sử',
                'description': 'Giao tiếp với hướng dẫn viên để tìm hiểu về lịch sử Văn Miếu',
                'challenge_type': 'conversation',
                'difficulty': 'medium',
                'objective': 'Hỏi và tìm hiểu về lịch sử Văn Miếu, các bia đá tiến sĩ, và văn hóa học tập truyền thống',
                'success_criteria': 'Có thể hỏi được ít nhất 3 câu hỏi về lịch sử và hiểu được câu trả lời',
                'time_limit': 15,
                'helpful_phrases': 'Văn Miếu được xây dựng khi nào? - 文廟はいつ建てられましたか？\nBia đá có ý nghĩa gì? - 石碑にはどんな意味がありますか？\nCó thể giải thích thêm không? - もっと詳しく説明してもらえますか？',
                'cultural_tips': 'Tôn trọng không khí trang nghiêm, nói chuyện nhỏ nhẹ, lắng nghe cẩn thận',
                'is_final_challenge': True,
                'order': 1,
            },
            
            # Bảo tàng Dân tộc học
            {
                'location_name': 'Bảo tàng Dân tộc học Việt Nam',
                'title': 'Thử thách khám phá văn hóa dân tộc',
                'description': 'Tương tác với nhân viên bảo tàng để tìm hiểu về văn hóa các dân tộc',
                'challenge_type': 'question_asking',
                'difficulty': 'easy',
                'objective': 'Hỏi về văn hóa của ít nhất 2 dân tộc khác nhau và hiểu được sự khác biệt',
                'success_criteria': 'Có thể hỏi và hiểu được thông tin về 2 dân tộc khác nhau',
                'time_limit': 20,
                'helpful_phrases': 'Dân tộc này có đặc điểm gì? - この民族にはどんな特徴がありますか？\nTrang phục này có ý nghĩa gì? - この衣装にはどんな意味がありますか？\nCó thể kể thêm về văn hóa không? - 文化についてもっと教えてもらえますか？',
                'cultural_tips': 'Tò mò và quan tâm đến văn hóa, hỏi câu hỏi cụ thể, ghi chú nếu cần',
                'is_final_challenge': True,
                'order': 1,
            },
            
            # Chợ Đồng Xuân
            {
                'location_name': 'Chợ Đồng Xuân',
                'title': 'Thử thách mua sắm tại chợ',
                'description': 'Mua một món hàng bằng cách giao tiếp với người bán hàng',
                'challenge_type': 'local_interaction',
                'difficulty': 'medium',
                'objective': 'Mua được một món hàng bằng cách giao tiếp hoàn toàn bằng tiếng Việt',
                'success_criteria': 'Có thể hỏi giá, mặc cả và mua được món hàng mong muốn',
                'time_limit': 25,
                'helpful_phrases': 'Cái này bao nhiêu tiền? - これはいくらですか？\nCó thể giảm giá không? - 値段を下げてもらえますか？\nTôi muốn mua cái này - これを買いたいです\nCảm ơn bạn - ありがとうございます',
                'cultural_tips': 'Mặc cả giá một cách thân thiện, tôn trọng người bán, không quá cứng rắn',
                'is_final_challenge': True,
                'order': 1,
            },
            
            # Bảo tàng Chứng tích Chiến tranh
            {
                'location_name': 'Bảo tàng Chứng tích Chiến tranh',
                'title': 'Thử thách tìm hiểu lịch sử',
                'description': 'Giao tiếp với hướng dẫn viên để hiểu sâu hơn về lịch sử',
                'challenge_type': 'cultural_exchange',
                'difficulty': 'hard',
                'objective': 'Thảo luận về ý nghĩa của hòa bình và tác động của chiến tranh',
                'success_criteria': 'Có thể tham gia thảo luận về hòa bình và hiểu được quan điểm của người Việt',
                'time_limit': 30,
                'helpful_phrases': 'Tôi muốn hiểu thêm về lịch sử - 歴史についてもっと理解したいです\nHòa bình có ý nghĩa gì với bạn? - 平和はあなたにとってどんな意味がありますか？\nCảm ơn vì đã chia sẻ - 共有してくれてありがとう',
                'cultural_tips': 'Tôn trọng không khí trang nghiêm, lắng nghe với sự đồng cảm, hỏi câu hỏi có ý nghĩa',
                'is_final_challenge': True,
                'order': 1,
            },
            
            # Chợ Bến Thành
            {
                'location_name': 'Chợ Bến Thành',
                'title': 'Thử thách mua sắm miền Nam',
                'description': 'Mua sắm và giao tiếp với người bán hàng tại chợ Bến Thành',
                'challenge_type': 'local_interaction',
                'difficulty': 'medium',
                'objective': 'Mua được món hàng đặc trưng miền Nam và giao tiếp với người bán',
                'success_criteria': 'Có thể hỏi về món hàng, mặc cả giá và mua được sản phẩm',
                'time_limit': 20,
                'helpful_phrases': 'Đây là món gì? - これは何ですか？\nCó đặc biệt không? - 特別ですか？\nGiá bao nhiêu? - 値段はいくらですか？\nTôi muốn thử - 試してみたいです',
                'cultural_tips': 'Thân thiện và vui vẻ, hỏi về đặc điểm của món hàng, tôn trọng văn hóa mặc cả',
                'is_final_challenge': True,
                'order': 1,
            },
            
            # Địa đạo Củ Chi
            {
                'location_name': 'Địa đạo Củ Chi',
                'title': 'Thử thách khám phá địa đạo',
                'description': 'Giao tiếp với hướng dẫn viên để hiểu về lịch sử địa đạo',
                'challenge_type': 'conversation',
                'difficulty': 'medium',
                'objective': 'Tìm hiểu về cách xây dựng địa đạo và cuộc sống của người dân trong chiến tranh',
                'success_criteria': 'Có thể hỏi và hiểu được ít nhất 2 thông tin về địa đạo',
                'time_limit': 25,
                'helpful_phrases': 'Địa đạo này sâu bao nhiêu? - この地下道はどのくらい深いですか？\nLàm sao để xây dựng? - どのように建設しましたか？\nCuộc sống như thế nào? - 生活はどのようなものでしたか？',
                'cultural_tips': 'Tôn trọng lịch sử, hỏi câu hỏi có ý nghĩa, lắng nghe với sự tôn trọng',
                'is_final_challenge': True,
                'order': 1,
            },
            
            # Đại Nội Huế
            {
                'location_name': 'Đại Nội - Kinh thành Huế',
                'title': 'Thử thách khám phá cung đình',
                'description': 'Giao tiếp với hướng dẫn viên để hiểu về văn hóa cung đình',
                'challenge_type': 'cultural_exchange',
                'difficulty': 'medium',
                'objective': 'Tìm hiểu về kiến trúc, lịch sử và văn hóa cung đình triều Nguyễn',
                'success_criteria': 'Có thể hỏi và hiểu được thông tin về kiến trúc và lịch sử',
                'time_limit': 30,
                'helpful_phrases': 'Cung điện này có ý nghĩa gì? - この宮殿にはどんな意味がありますか？\nKiến trúc như thế nào? - 建築はどのようなものですか？\nLịch sử ra sao? - 歴史はどのようなものですか？',
                'cultural_tips': 'Tôn trọng không khí trang nghiêm, hỏi câu hỏi có ý nghĩa, lắng nghe cẩn thận',
                'is_final_challenge': True,
                'order': 1,
            },
            
            # Chùa Thiên Mụ
            {
                'location_name': 'Chùa Thiên Mụ',
                'title': 'Thử thách tìm hiểu văn hóa tâm linh',
                'description': 'Giao tiếp với nhà sư hoặc người quản lý chùa',
                'challenge_type': 'cultural_exchange',
                'difficulty': 'easy',
                'objective': 'Tìm hiểu về lịch sử chùa và văn hóa Phật giáo Việt Nam',
                'success_criteria': 'Có thể hỏi và hiểu được thông tin về chùa và văn hóa Phật giáo',
                'time_limit': 20,
                'helpful_phrases': 'Chùa này có từ khi nào? - この寺はいつからありますか？\nCó ý nghĩa gì? - どんな意味がありますか？\nVăn hóa Phật giáo như thế nào? - 仏教文化はどのようなものですか？',
                'cultural_tips': 'Tôn trọng không gian tâm linh, nói chuyện nhỏ nhẹ, tỏ thái độ tôn kính',
                'is_final_challenge': True,
                'order': 1,
            },
            
            # Phố cổ Hội An
            {
                'location_name': 'Phố cổ Hội An',
                'title': 'Thử thách khám phá phố cổ',
                'description': 'Giao tiếp với người dân địa phương để tìm hiểu về văn hóa',
                'challenge_type': 'local_interaction',
                'difficulty': 'easy',
                'objective': 'Tìm hiểu về văn hóa, ẩm thực và cuộc sống của người dân Hội An',
                'success_criteria': 'Có thể hỏi và hiểu được thông tin về văn hóa địa phương',
                'time_limit': 25,
                'helpful_phrases': 'Phố cổ này có gì đặc biệt? - この古い街には何か特別なものがありますか？\nẨm thực như thế nào? - 料理はどのようなものですか？\nCuộc sống ở đây ra sao? - ここの生活はどのようなものですか？',
                'cultural_tips': 'Thân thiện và tò mò, hỏi về văn hóa địa phương, tôn trọng truyền thống',
                'is_final_challenge': True,
                'order': 1,
            },
            
            # Bản Cát Cát
            {
                'location_name': 'Bản Cát Cát',
                'title': 'Thử thách trải nghiệm văn hóa dân tộc',
                'description': 'Giao tiếp với người dân địa phương để hiểu về văn hóa dân tộc',
                'challenge_type': 'cultural_exchange',
                'difficulty': 'medium',
                'objective': 'Tìm hiểu về cuộc sống, văn hóa và truyền thống của người H\'Mông',
                'success_criteria': 'Có thể hỏi và hiểu được thông tin về văn hóa dân tộc',
                'time_limit': 30,
                'helpful_phrases': 'Cuộc sống ở đây như thế nào? - ここの生活はどのようなものですか？\nVăn hóa truyền thống ra sao? - 伝統文化はどのようなものですか？\nCó thể học thêm gì không? - 他に何か学べることはありますか？',
                'cultural_tips': 'Tôn trọng văn hóa địa phương, hỏi câu hỏi có ý nghĩa, lắng nghe với sự tôn trọng',
                'is_final_challenge': True,
                'order': 1,
            },
            
            # Tháp Bà Ponagar
            {
                'location_name': 'Tháp Bà Ponagar',
                'title': 'Thử thách khám phá văn hóa Chăm Pa',
                'description': 'Giao tiếp với hướng dẫn viên để hiểu về văn hóa Chăm Pa',
                'challenge_type': 'conversation',
                'difficulty': 'medium',
                'objective': 'Tìm hiểu về lịch sử, kiến trúc và văn hóa Chăm Pa cổ đại',
                'success_criteria': 'Có thể hỏi và hiểu được thông tin về văn hóa Chăm Pa',
                'time_limit': 25,
                'helpful_phrases': 'Tháp này có ý nghĩa gì? - この塔にはどんな意味がありますか？\nVăn hóa Chăm Pa như thế nào? - チャンパ文化はどのようなものですか？\nLịch sử ra sao? - 歴史はどのようなものですか？',
                'cultural_tips': 'Tôn trọng di tích lịch sử, hỏi câu hỏi có ý nghĩa, lắng nghe cẩn thận',
                'is_final_challenge': True,
                'order': 1,
            },
            
            # Bảo tàng Dân tộc Lâm Đồng
            {
                'location_name': 'Bảo tàng Dân tộc Lâm Đồng',
                'title': 'Thử thách tìm hiểu văn hóa Tây Nguyên',
                'description': 'Giao tiếp với nhân viên bảo tàng để hiểu về văn hóa Tây Nguyên',
                'challenge_type': 'cultural_exchange',
                'difficulty': 'easy',
                'objective': 'Tìm hiểu về văn hóa, âm nhạc và truyền thống các dân tộc Tây Nguyên',
                'success_criteria': 'Có thể hỏi và hiểu được thông tin về văn hóa Tây Nguyên',
                'time_limit': 20,
                'helpful_phrases': 'Văn hóa Tây Nguyên như thế nào? - タイ・グエンの文化はどのようなものですか？\nCồng chiêng có ý nghĩa gì? - ゴング・チエンにはどんな意味がありますか？\nTruyền thống ra sao? - 伝統はどのようなものですか？',
                'cultural_tips': 'Tò mò về văn hóa, hỏi câu hỏi cụ thể, lắng nghe với sự quan tâm',
                'is_final_challenge': True,
                'order': 1,
            },
        ]
        
        for challenge_data in challenges_data:
            try:
                location = CulturalLocation.objects.get(name=challenge_data['location_name'])
                
                challenge, created = CulturalChallenge.objects.get_or_create(
                    location=location,
                    title=challenge_data['title'],
                    defaults={
                        'description': challenge_data['description'],
                        'challenge_type': challenge_data['challenge_type'],
                        'difficulty': challenge_data['difficulty'],
                        'objective': challenge_data['objective'],
                        'success_criteria': challenge_data['success_criteria'],
                        'time_limit': challenge_data['time_limit'],
                        'helpful_phrases': challenge_data['helpful_phrases'],
                        'cultural_tips': challenge_data['cultural_tips'],
                        'is_final_challenge': challenge_data['is_final_challenge'],
                        'order': challenge_data['order'],
                    }
                )
                
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'Successfully created cultural challenge: {challenge.title} for {location.name}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Cultural challenge already exists: {challenge.title} for {location.name}')
                    )
                    
            except CulturalLocation.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Location not found: {challenge_data["location_name"]}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully processed {len(challenges_data)} cultural challenges')
        )
