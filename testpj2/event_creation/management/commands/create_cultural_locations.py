from django.core.management.base import BaseCommand
from event_creation.models import CulturalLocation

class Command(BaseCommand):
    help = 'Create cultural and tourist locations for language exchange meetings'

    def handle(self, *args, **options):
        locations = [
            # Hà Nội
            {
                'name': 'Văn Miếu - Quốc Tử Giám',
                'location_type': 'historical',
                'address': '58 Quốc Tử Giám, Đống Đa, Hà Nội',
                'city': 'hanoi',
                'cultural_description': 'Trường đại học đầu tiên của Việt Nam, xây dựng năm 1070. Nơi thờ Khổng Tử và các bậc hiền triết Nho giáo.',
                'best_time_to_visit': 'Sáng sớm hoặc chiều muộn để tránh đông khách',
                'entrance_fee': '30,000 VND',
                'opening_hours': '8:00 AM - 5:00 PM',
                'description': 'Di tích lịch sử văn hóa quan trọng, nơi lưu giữ nhiều bia đá ghi danh các tiến sĩ qua các triều đại.',
                'cultural_tips': 'Mặc trang phục lịch sự, giữ yên lặng, không chạm vào các hiện vật cổ.',
                'latitude': 21.0278,
                'longitude': 105.8342,
            },
            {
                'name': 'Bảo tàng Dân tộc học Việt Nam',
                'location_type': 'museum',
                'address': 'Nguyễn Văn Huyên, Nghĩa Đô, Cầu Giấy, Hà Nội',
                'city': 'hanoi',
                'cultural_description': 'Bảo tàng trưng bày văn hóa của 54 dân tộc Việt Nam với kiến trúc độc đáo.',
                'best_time_to_visit': 'Buổi sáng để có thời gian khám phá đầy đủ',
                'entrance_fee': '40,000 VND',
                'opening_hours': '8:30 AM - 5:30 PM (Đóng thứ 2)',
                'description': 'Nơi lưu giữ và trưng bày các hiện vật văn hóa, trang phục, công cụ lao động của các dân tộc.',
                'cultural_tips': 'Chụp ảnh được phép, nhưng cần tôn trọng các hiện vật văn hóa.',
                'latitude': 21.0389,
                'longitude': 105.7828,
            },
            {
                'name': 'Chợ Đồng Xuân',
                'location_type': 'market',
                'address': 'Đồng Xuân, Hoàn Kiếm, Hà Nội',
                'city': 'hanoi',
                'cultural_description': 'Chợ truyền thống lớn nhất Hà Nội, nơi mua sắm và trải nghiệm văn hóa dân gian.',
                'best_time_to_visit': 'Sáng sớm để trải nghiệm không khí chợ sôi động',
                'entrance_fee': 'Miễn phí',
                'opening_hours': '6:00 AM - 6:00 PM',
                'description': 'Chợ có lịch sử hơn 100 năm, bán đủ loại hàng hóa từ thực phẩm đến quần áo, đồ gia dụng.',
                'cultural_tips': 'Mặc cả giá khi mua hàng, chú ý an toàn tài sản cá nhân.',
                'latitude': 21.0353,
                'longitude': 105.8477,
            },
            
            # Hồ Chí Minh
            {
                'name': 'Bảo tàng Chứng tích Chiến tranh',
                'location_type': 'museum',
                'address': '28 Võ Văn Tần, Quận 3, TP.HCM',
                'city': 'hochiminh',
                'cultural_description': 'Bảo tàng trưng bày các chứng tích về chiến tranh Việt Nam, giúp hiểu về lịch sử đất nước.',
                'best_time_to_visit': 'Buổi sáng để có thời gian xem kỹ các hiện vật',
                'entrance_fee': '40,000 VND',
                'opening_hours': '7:30 AM - 6:00 PM',
                'description': 'Nơi lưu giữ các hiện vật, hình ảnh về chiến tranh, giúp thế hệ trẻ hiểu về quá khứ.',
                'cultural_tips': 'Cần tôn trọng không khí trang nghiêm, không chụp ảnh ở một số khu vực.',
                'latitude': 10.7796,
                'longitude': 106.6907,
            },
            {
                'name': 'Chợ Bến Thành',
                'location_type': 'market',
                'address': 'Lê Lợi, Quận 1, TP.HCM',
                'city': 'hochiminh',
                'cultural_description': 'Chợ biểu tượng của TP.HCM, nơi mua sắm và trải nghiệm văn hóa miền Nam.',
                'best_time_to_visit': 'Sáng sớm hoặc chiều muộn để tránh nắng nóng',
                'entrance_fee': 'Miễn phí',
                'opening_hours': '6:00 AM - 6:00 PM',
                'description': 'Chợ có kiến trúc độc đáo với tháp đồng hồ, bán đủ loại hàng hóa đặc trưng miền Nam.',
                'cultural_tips': 'Mặc cả giá khi mua hàng, chú ý chất lượng sản phẩm.',
                'latitude': 10.7720,
                'longitude': 106.6983,
            },
            {
                'name': 'Địa đạo Củ Chi',
                'location_type': 'historical',
                'address': 'Phú Hiệp, Củ Chi, TP.HCM',
                'city': 'hochiminh',
                'cultural_description': 'Hệ thống địa đạo phức tạp được sử dụng trong chiến tranh, thể hiện tinh thần kiên cường của người Việt.',
                'best_time_to_visit': 'Buổi sáng để tránh nắng nóng',
                'entrance_fee': '110,000 VND',
                'opening_hours': '7:00 AM - 5:00 PM',
                'description': 'Địa đạo dài 250km với nhiều tầng, phòng họp, bệnh viện dưới lòng đất.',
                'cultural_tips': 'Mặc trang phục thoải mái, mang giày đế bằng, chuẩn bị tinh thần cho không gian chật hẹp.',
                'latitude': 11.0616,
                'longitude': 106.5178,
            },
            
            # Huế
            {
                'name': 'Đại Nội - Kinh thành Huế',
                'location_type': 'heritage',
                'address': 'Phú Hậu, TP. Huế, Thừa Thiên Huế',
                'city': 'hue',
                'cultural_description': 'Quần thể di tích cố đô Huế, nơi lưu giữ kiến trúc và văn hóa triều Nguyễn.',
                'best_time_to_visit': 'Sáng sớm hoặc chiều muộn để tránh nắng nóng',
                'entrance_fee': '150,000 VND',
                'opening_hours': '7:00 AM - 5:30 PM',
                'description': 'Bao gồm Hoàng thành, Tử cấm thành với các cung điện, đền đài nguy nga tráng lệ.',
                'cultural_tips': 'Mặc trang phục lịch sự, giữ yên lặng, không chạm vào các hiện vật cổ.',
                'latitude': 16.4637,
                'longitude': 107.5909,
            },
            {
                'name': 'Chùa Thiên Mụ',
                'location_type': 'temple',
                'address': 'Kim Long, TP. Huế, Thừa Thiên Huế',
                'city': 'hue',
                'cultural_description': 'Ngôi chùa cổ nhất Huế, biểu tượng văn hóa tâm linh của xứ Huế.',
                'best_time_to_visit': 'Sáng sớm để nghe tiếng chuông chùa',
                'entrance_fee': 'Miễn phí',
                'opening_hours': '6:00 AM - 6:00 PM',
                'description': 'Chùa có kiến trúc độc đáo với tháp Phước Duyên 7 tầng, nằm bên dòng sông Hương thơ mộng.',
                'cultural_tips': 'Mặc trang phục kín đáo, giữ yên lặng, không chụp ảnh ở khu vực thờ cúng.',
                'latitude': 16.4567,
                'longitude': 107.5733,
            },
            
            # Hội An
            {
                'name': 'Phố cổ Hội An',
                'location_type': 'heritage',
                'address': 'Phố cổ Hội An, Quảng Nam',
                'city': 'hoian',
                'cultural_description': 'Di sản văn hóa thế giới, nơi lưu giữ kiến trúc và văn hóa giao thương quốc tế.',
                'best_time_to_visit': 'Chiều tối để ngắm đèn lồng và không khí lãng mạn',
                'entrance_fee': '120,000 VND (vé tham quan)',
                'opening_hours': '24/7 (các điểm tham quan: 8:00 AM - 9:00 PM)',
                'description': 'Phố cổ với kiến trúc Nhật Bản, Trung Quốc và Việt Nam, nổi tiếng với đèn lồng và ẩm thực.',
                'cultural_tips': 'Đi bộ để khám phá, thử các món ăn địa phương, mua đèn lồng làm quà lưu niệm.',
                'latitude': 15.8801,
                'longitude': 108.3383,
            },
            
            # Sa Pa
            {
                'name': 'Bản Cát Cát',
                'location_type': 'cultural_center',
                'address': 'San Sả Hồ, Sa Pa, Lào Cai',
                'city': 'sapa',
                'cultural_description': 'Bản làng của người H\'Mông, nơi trải nghiệm văn hóa dân tộc miền núi.',
                'best_time_to_visit': 'Sáng sớm để tránh đông khách du lịch',
                'entrance_fee': '70,000 VND',
                'opening_hours': '6:00 AM - 6:00 PM',
                'description': 'Bản làng truyền thống với nhà sàn, ruộng bậc thang, nghề dệt thổ cẩm và chăn nuôi.',
                'cultural_tips': 'Tôn trọng văn hóa địa phương, hỏi ý kiến trước khi chụp ảnh, mua hàng thủ công để ủng hộ.',
                'latitude': 22.3366,
                'longitude': 103.8440,
            },
            
            # Nha Trang
            {
                'name': 'Tháp Bà Ponagar',
                'location_type': 'temple',
                'address': '2 Tháng 4, Nha Trang, Khánh Hòa',
                'city': 'nhatrang',
                'cultural_description': 'Quần thể đền tháp Chăm Pa cổ, nơi thờ nữ thần Po Nagar.',
                'best_time_to_visit': 'Sáng sớm hoặc chiều muộn để tránh nắng nóng',
                'entrance_fee': '22,000 VND',
                'opening_hours': '6:00 AM - 6:00 PM',
                'description': 'Kiến trúc Chăm Pa độc đáo với 4 tháp chính, nằm trên đồi cao nhìn ra vịnh Nha Trang.',
                'cultural_tips': 'Mặc trang phục kín đáo, giữ yên lặng, không chạm vào các hiện vật cổ.',
                'latitude': 12.2654,
                'longitude': 109.1940,
            },
            
            # Đà Lạt
            {
                'name': 'Bảo tàng Dân tộc Lâm Đồng',
                'location_type': 'museum',
                'address': '4 Đinh Tiên Hoàng, Đà Lạt, Lâm Đồng',
                'city': 'dalat',
                'cultural_description': 'Bảo tàng trưng bày văn hóa các dân tộc Tây Nguyên.',
                'best_time_to_visit': 'Buổi sáng để có thời gian khám phá',
                'entrance_fee': '20,000 VND',
                'opening_hours': '7:30 AM - 5:00 PM (Đóng thứ 2)',
                'description': 'Nơi lưu giữ các hiện vật văn hóa, trang phục, nhạc cụ của các dân tộc Tây Nguyên.',
                'cultural_tips': 'Chụp ảnh được phép, tìm hiểu về văn hóa cồng chiêng và các lễ hội truyền thống.',
                'latitude': 11.9404,
                'longitude': 108.4580,
            },
        ]
        
        for location_data in locations:
            location, created = CulturalLocation.objects.get_or_create(
                name=location_data['name'],
                defaults=location_data
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created cultural location: {location.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Cultural location already exists: {location.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully processed {len(locations)} cultural locations')
        )
