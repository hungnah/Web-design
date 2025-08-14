from django.core.management.base import BaseCommand
from event_creation.models import CulturalLocation, CulturalLesson

class Command(BaseCommand):
    help = 'Create cultural lessons for each cultural location'

    def handle(self, *args, **options):
        lessons_data = [
            # Văn Miếu - Quốc Tử Giám
            {
                'location_name': 'Văn Miếu - Quốc Tử Giám',
                'title': 'Văn hóa học tập truyền thống Việt Nam',
                'description': 'Bài học về văn hóa học tập và giáo dục truyền thống của Việt Nam',
                'vocabulary_list': 'Văn Miếu, Quốc Tử Giám, tiến sĩ, bia đá, Khổng Tử, Nho giáo, học tập, truyền thống',
                'essential_phrases': 'Đây là nơi gì? - ここはどこですか？\nTôi muốn tìm hiểu về lịch sử - 歴史について知りたいです\nCó thể chụp ảnh không? - 写真を撮ってもいいですか？',
                'cultural_context': 'Văn Miếu được xây dựng năm 1070, là trường đại học đầu tiên của Việt Nam. Nơi đây thờ Khổng Tử và các bậc hiền triết Nho giáo. Các bia đá ghi danh 82 khoa thi tiến sĩ từ năm 1442-1779.',
                'difficulty': 'intermediate',
                'estimated_duration': 45,
                'order': 1,
            },
            
            # Bảo tàng Dân tộc học
            {
                'location_name': 'Bảo tàng Dân tộc học Việt Nam',
                'title': 'Văn hóa 54 dân tộc Việt Nam',
                'description': 'Tìm hiểu về văn hóa đa dạng của các dân tộc Việt Nam',
                'vocabulary_list': 'dân tộc, văn hóa, bảo tàng, hiện vật, trang phục, công cụ, truyền thống, đa dạng',
                'essential_phrases': 'Dân tộc này có bao nhiêu người? - この民族は何人いますか？\nTrang phục này đẹp quá! - この衣装はとても美しいですね！\nCó thể giải thích thêm không? - もっと詳しく説明してもらえますか？',
                'cultural_context': 'Việt Nam có 54 dân tộc anh em, mỗi dân tộc có văn hóa, trang phục, phong tục tập quán riêng. Bảo tàng trưng bày các hiện vật văn hóa độc đáo của từng dân tộc.',
                'difficulty': 'beginner',
                'estimated_duration': 40,
                'order': 1,
            },
            
            # Chợ Đồng Xuân
            {
                'location_name': 'Chợ Đồng Xuân',
                'title': 'Văn hóa chợ truyền thống Việt Nam',
                'description': 'Học cách mua sắm và giao tiếp tại chợ truyền thống',
                'vocabulary_list': 'chợ, mua sắm, mặc cả, giá cả, hàng hóa, người bán, khách hàng, truyền thống',
                'essential_phrases': 'Cái này bao nhiêu tiền? - これはいくらですか？\nCó thể giảm giá không? - 値段を下げてもらえますか？\nTôi muốn mua cái này - これを買いたいです',
                'cultural_context': 'Chợ Đồng Xuân là chợ truyền thống lớn nhất Hà Nội, có lịch sử hơn 100 năm. Nơi đây bán đủ loại hàng hóa từ thực phẩm đến quần áo, đồ gia dụng. Văn hóa mặc cả giá là nét đặc trưng của chợ Việt Nam.',
                'difficulty': 'beginner',
                'estimated_duration': 35,
                'order': 1,
            },
            
            # Bảo tàng Chứng tích Chiến tranh
            {
                'location_name': 'Bảo tàng Chứng tích Chiến tranh',
                'title': 'Lịch sử và hòa bình',
                'description': 'Tìm hiểu về lịch sử chiến tranh và giá trị của hòa bình',
                'vocabulary_list': 'lịch sử, chiến tranh, hòa bình, bảo tàng, hiện vật, chứng tích, tưởng nhớ, giáo dục',
                'essential_phrases': 'Tôi muốn tìm hiểu về lịch sử - 歴史について知りたいです\nĐây là thời kỳ nào? - これはどの時代ですか？\nCảm ơn vì đã giải thích - 説明してくれてありがとう',
                'cultural_context': 'Bảo tàng trưng bày các chứng tích về chiến tranh Việt Nam, giúp thế hệ trẻ hiểu về quá khứ và trân trọng hòa bình. Nơi đây cũng là bài học về sự tàn khốc của chiến tranh.',
                'difficulty': 'advanced',
                'estimated_duration': 50,
                'order': 1,
            },
            
            # Chợ Bến Thành
            {
                'location_name': 'Chợ Bến Thành',
                'title': 'Văn hóa mua sắm miền Nam',
                'description': 'Trải nghiệm văn hóa mua sắm đặc trưng miền Nam Việt Nam',
                'vocabulary_list': 'chợ, mua sắm, miền Nam, ẩm thực, hàng hóa, giao dịch, văn hóa, truyền thống',
                'essential_phrases': 'Có bán cái này không? - これは売っていますか？\nGiá bao nhiêu? - 値段はいくらですか？\nTôi muốn thử - 試してみたいです',
                'cultural_context': 'Chợ Bến Thành là biểu tượng của TP.HCM, nơi mua sắm và trải nghiệm văn hóa miền Nam. Chợ có kiến trúc độc đáo với tháp đồng hồ, bán đủ loại hàng hóa đặc trưng miền Nam.',
                'difficulty': 'beginner',
                'estimated_duration': 35,
                'order': 1,
            },
            
            # Địa đạo Củ Chi
                {
                'location_name': 'Địa đạo Củ Chi',
                'title': 'Lịch sử kháng chiến và tinh thần Việt Nam',
                'description': 'Tìm hiểu về hệ thống địa đạo và tinh thần kiên cường của người Việt',
                'vocabulary_list': 'địa đạo, kháng chiến, lịch sử, tinh thần, kiên cường, chiến tranh, ẩn nấp, chiến đấu',
                'essential_phrases': 'Địa đạo này sâu bao nhiêu? - この地下道はどのくらい深いですか？\nLàm sao để xây dựng? - どのように建設しましたか？\nThật là tuyệt vời! - 本当に素晴らしいですね！',
                'cultural_context': 'Địa đạo Củ Chi là hệ thống địa đạo phức tạp dài 250km, được sử dụng trong chiến tranh. Nó thể hiện tinh thần kiên cường, sáng tạo và ý chí quyết tâm của người Việt Nam.',
                'difficulty': 'intermediate',
                'estimated_duration': 45,
                'order': 1,
            },
            
            # Đại Nội Huế
            {
                'location_name': 'Đại Nội - Kinh thành Huế',
                'title': 'Văn hóa cung đình triều Nguyễn',
                'description': 'Khám phá văn hóa cung đình và kiến trúc hoàng gia Việt Nam',
                'vocabulary_list': 'cung đình, hoàng gia, triều Nguyễn, kiến trúc, lịch sử, văn hóa, truyền thống, di tích',
                'essential_phrases': 'Cung điện này đẹp quá! - この宮殿はとても美しいですね！\nCó thể chụp ảnh không? - 写真を撮ってもいいですか？\nLịch sử như thế nào? - 歴史はどのようなものですか？',
                'cultural_context': 'Đại Nội là quần thể di tích cố đô Huế, nơi lưu giữ kiến trúc và văn hóa triều Nguyễn. Bao gồm Hoàng thành, Tử cấm thành với các cung điện, đền đài nguy nga tráng lệ.',
                'difficulty': 'intermediate',
                'estimated_duration': 50,
                'order': 1,
            },
            
            # Chùa Thiên Mụ
            {
                'location_name': 'Chùa Thiên Mụ',
                'title': 'Văn hóa tâm linh và Phật giáo Việt Nam',
                'description': 'Tìm hiểu về văn hóa tâm linh và Phật giáo truyền thống',
                'vocabulary_list': 'chùa, Phật giáo, tâm linh, tôn giáo, kiến trúc, truyền thống, văn hóa, tín ngưỡng',
                'essential_phrases': 'Chùa này có từ khi nào? - この寺はいつからありますか？\nCó thể thắp hương không? - お香を焚いてもいいですか？\nThật là thanh tịnh - 本当に清らかですね',
                'cultural_context': 'Chùa Thiên Mụ là ngôi chùa cổ nhất Huế, biểu tượng văn hóa tâm linh của xứ Huế. Chùa có kiến trúc độc đáo với tháp Phước Duyên 7 tầng, nằm bên dòng sông Hương thơ mộng.',
                'difficulty': 'beginner',
                'estimated_duration': 40,
                'order': 1,
            },
            
            # Phố cổ Hội An
            {
                'location_name': 'Phố cổ Hội An',
                'title': 'Văn hóa giao thương quốc tế',
                'description': 'Khám phá văn hóa giao thương và kiến trúc đa văn hóa',
                'vocabulary_list': 'phố cổ, giao thương, quốc tế, kiến trúc, văn hóa, đa dạng, truyền thống, lịch sử',
                'essential_phrases': 'Phố cổ này đẹp quá! - この古い街はとても美しいですね！\nCó thể đi bộ không? - 歩いてもいいですか？\nĐèn lồng đẹp quá! - ランタンがとても美しいですね！',
                'cultural_context': 'Phố cổ Hội An là di sản văn hóa thế giới, nơi lưu giữ kiến trúc và văn hóa giao thương quốc tế. Phố cổ với kiến trúc Nhật Bản, Trung Quốc và Việt Nam, nổi tiếng với đèn lồng và ẩm thực.',
                'difficulty': 'beginner',
                'estimated_duration': 45,
                'order': 1,
            },
            
            # Bản Cát Cát
            {
                'location_name': 'Bản Cát Cát',
                'title': 'Văn hóa dân tộc miền núi',
                'description': 'Trải nghiệm văn hóa dân tộc H\'Mông và cuộc sống miền núi',
                'vocabulary_list': 'bản làng, dân tộc, miền núi, văn hóa, truyền thống, nhà sàn, ruộng bậc thang, thổ cẩm',
                'essential_phrases': 'Bản làng này có bao nhiêu người? - この村には何人いますか？\nNhà sàn đẹp quá! - 高床式の家はとても美しいですね！\nCó thể thử mặc trang phục không? - 衣装を着てみてもいいですか？',
                'cultural_context': 'Bản Cát Cát là bản làng của người H\'Mông, nơi trải nghiệm văn hóa dân tộc miền núi. Bản làng truyền thống với nhà sàn, ruộng bậc thang, nghề dệt thổ cẩm và chăn nuôi.',
                'difficulty': 'intermediate',
                'estimated_duration': 50,
                'order': 1,
            },
            
            # Tháp Bà Ponagar
            {
                'location_name': 'Tháp Bà Ponagar',
                'title': 'Văn hóa Chăm Pa cổ đại',
                'description': 'Khám phá văn hóa và kiến trúc Chăm Pa cổ đại',
                'vocabulary_list': 'tháp, Chăm Pa, cổ đại, văn hóa, kiến trúc, lịch sử, tôn giáo, di tích',
                'essential_phrases': 'Tháp này đẹp quá! - この塔はとても美しいですね！\nCó thể leo lên không? - 登ってもいいですか？\nLịch sử như thế nào? - 歴史はどのようなものですか？',
                'cultural_context': 'Tháp Bà Ponagar là quần thể đền tháp Chăm Pa cổ, nơi thờ nữ thần Po Nagar. Kiến trúc Chăm Pa độc đáo với 4 tháp chính, nằm trên đồi cao nhìn ra vịnh Nha Trang.',
                'difficulty': 'intermediate',
                'estimated_duration': 45,
                'order': 1,
            },
            
            # Bảo tàng Dân tộc Lâm Đồng
            {
                'location_name': 'Bảo tàng Dân tộc Lâm Đồng',
                'title': 'Văn hóa Tây Nguyên',
                'description': 'Tìm hiểu về văn hóa các dân tộc Tây Nguyên',
                'vocabulary_list': 'Tây Nguyên, dân tộc, văn hóa, bảo tàng, hiện vật, trang phục, nhạc cụ, truyền thống',
                'essential_phrases': 'Văn hóa Tây Nguyên như thế nào? - タイ・グエンの文化はどのようなものですか？\nCồng chiêng là gì? - ゴング・チエンとは何ですか？\nCó thể thử chơi nhạc cụ không? - 楽器を演奏してみてもいいですか？',
                'cultural_context': 'Bảo tàng trưng bày văn hóa các dân tộc Tây Nguyên. Nơi lưu giữ các hiện vật văn hóa, trang phục, nhạc cụ của các dân tộc Tây Nguyên. Đặc biệt nổi tiếng với văn hóa cồng chiêng.',
                'difficulty': 'beginner',
                'estimated_duration': 40,
                'order': 1,
            },
        ]
        
        for lesson_data in lessons_data:
            try:
                location = CulturalLocation.objects.get(name=lesson_data['location_name'])
                
                lesson, created = CulturalLesson.objects.get_or_create(
                    location=location,
                    title=lesson_data['title'],
                    defaults={
                        'description': lesson_data['description'],
                        'vocabulary_list': lesson_data['vocabulary_list'],
                        'essential_phrases': lesson_data['essential_phrases'],
                        'cultural_context': lesson_data['cultural_context'],
                        'difficulty': lesson_data['difficulty'],
                        'estimated_duration': lesson_data['estimated_duration'],
                        'order': lesson_data['order'],
                    }
                )
                
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'Successfully created cultural lesson: {lesson.title} for {location.name}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Cultural lesson already exists: {lesson.title} for {location.name}')
                    )
                    
            except CulturalLocation.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Location not found: {lesson_data["location_name"]}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully processed {len(lessons_data)} cultural lessons')
        )
