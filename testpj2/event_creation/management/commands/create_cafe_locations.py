from django.core.management.base import BaseCommand
from event_creation.models import CafeLocation

class Command(BaseCommand):
    help = 'Create additional cafe locations for language exchange meetings'

    def handle(self, *args, **options):
        cafes = [
            # Hà Nội
            {
                'name': 'Cafe Tranquil',
                'address': '123 Nguyễn Huệ, Hoàn Kiếm, Hà Nội',
                'city': 'hanoi',
                'cafe_type': 'cafe',
                'price_range': 'moderate',
                'description': 'Quán cafe yên tĩnh, phù hợp cho việc học tập và trò chuyện',
                'opening_hours': '7:00 AM - 10:00 PM',
                'has_wifi': True,
                'has_parking': False,
                'is_quiet': True,
            },
            {
                'name': 'The Coffee House - Tràng Tiền',
                'address': '45 Tràng Tiền, Hoàn Kiếm, Hà Nội',
                'city': 'hanoi',
                'cafe_type': 'cafe',
                'price_range': 'moderate',
                'description': 'Chuỗi cafe nổi tiếng với không gian rộng rãi',
                'opening_hours': '7:00 AM - 11:00 PM',
                'has_wifi': True,
                'has_parking': True,
                'is_quiet': False,
            },
            {
                'name': 'Cafe Giảng',
                'address': '39 Nguyễn Hữu Huân, Hoàn Kiếm, Hà Nội',
                'city': 'hanoi',
                'cafe_type': 'cafe',
                'price_range': 'budget',
                'description': 'Cafe truyền thống với trứng gà nướng nổi tiếng',
                'opening_hours': '6:00 AM - 9:00 PM',
                'has_wifi': False,
                'has_parking': False,
                'is_quiet': True,
            },
            
            # Hồ Chí Minh
            {
                'name': 'The Workshop',
                'address': '27 Ngô Đức Kế, Quận 1, TP.HCM',
                'city': 'hochiminh',
                'cafe_type': 'cafe',
                'price_range': 'premium',
                'description': 'Cafe chuyên về cà phê đặc biệt, không gian hiện đại',
                'opening_hours': '7:30 AM - 10:30 PM',
                'has_wifi': True,
                'has_parking': False,
                'is_quiet': True,
            },
            {
                'name': 'L\'Usine Le Loi',
                'address': '151 Đồng Khởi, Quận 1, TP.HCM',
                'city': 'hochiminh',
                'cafe_type': 'cafe',
                'price_range': 'premium',
                'description': 'Cafe kết hợp với concept store, không gian đẹp',
                'opening_hours': '8:00 AM - 11:00 PM',
                'has_wifi': True,
                'has_parking': False,
                'is_quiet': False,
            },
            {
                'name': 'Cafe 1985',
                'address': '14 Tôn Thất Đạm, Quận 1, TP.HCM',
                'city': 'hochiminh',
                'cafe_type': 'cafe',
                'price_range': 'moderate',
                'description': 'Cafe với thiết kế retro, phù hợp cho việc học tập',
                'opening_hours': '7:00 AM - 10:00 PM',
                'has_wifi': True,
                'has_parking': False,
                'is_quiet': True,
            },
            
            # Hải Phòng
            {
                'name': 'Mun Coffee',
                'address': '123 Trần Phú, Hồng Bàng, Hải Phòng',
                'city': 'haiphong',
                'cafe_type': 'cafe',
                'price_range': 'moderate',
                'description': 'Cafe với view biển đẹp, không gian thoáng đãng',
                'opening_hours': '7:00 AM - 10:00 PM',
                'has_wifi': True,
                'has_parking': True,
                'is_quiet': True,
            },
            {
                'name': 'Cafe Ocean',
                'address': '45 Lạch Tray, Ngô Quyền, Hải Phòng',
                'city': 'haiphong',
                'cafe_type': 'cafe',
                'price_range': 'budget',
                'description': 'Cafe bình dân với view cảng biển',
                'opening_hours': '6:00 AM - 9:00 PM',
                'has_wifi': False,
                'has_parking': False,
                'is_quiet': False,
            },
            
            # Đà Nẵng
            {
                'name': '43 Factory',
                'address': '43 Lê Văn Hiến, Ngũ Hành Sơn, Đà Nẵng',
                'city': 'danang',
                'cafe_type': 'cafe',
                'price_range': 'premium',
                'description': 'Cafe chuyên về cà phê rang xay, không gian công nghiệp',
                'opening_hours': '7:00 AM - 10:00 PM',
                'has_wifi': True,
                'has_parking': True,
                'is_quiet': True,
            },
            {
                'name': 'Cafe Biển',
                'address': '123 Võ Nguyên Giáp, Sơn Trà, Đà Nẵng',
                'city': 'danang',
                'cafe_type': 'cafe',
                'price_range': 'moderate',
                'description': 'Cafe view biển Mỹ Khê, không gian lãng mạn',
                'opening_hours': '6:00 AM - 11:00 PM',
                'has_wifi': True,
                'has_parking': True,
                'is_quiet': False,
            },
            
            # Cần Thơ
            {
                'name': 'Cafe 1985',
                'address': '45 Nguyễn Việt Dũng, Ninh Kiều, Cần Thơ',
                'city': 'cantho',
                'cafe_type': 'cafe',
                'price_range': 'moderate',
                'description': 'Cafe với thiết kế hiện đại, phù hợp cho việc học tập',
                'opening_hours': '7:00 AM - 10:00 PM',
                'has_wifi': True,
                'has_parking': False,
                'is_quiet': True,
            },
            {
                'name': 'Cafe Sông Hậu',
                'address': '78 Đường 30/4, Ninh Kiều, Cần Thơ',
                'city': 'cantho',
                'cafe_type': 'cafe',
                'price_range': 'budget',
                'description': 'Cafe view sông Hậu, không gian thoáng mát',
                'opening_hours': '6:00 AM - 9:00 PM',
                'has_wifi': False,
                'has_parking': False,
                'is_quiet': True,
            },
            
            # Nha Trang
            {
                'name': 'Cafe Biển Nha Trang',
                'address': '123 Trần Phú, Lộc Thọ, Nha Trang',
                'city': 'nhatrang',
                'cafe_type': 'cafe',
                'price_range': 'moderate',
                'description': 'Cafe view biển Nha Trang, không gian đẹp',
                'opening_hours': '7:00 AM - 10:00 PM',
                'has_wifi': True,
                'has_parking': True,
                'is_quiet': False,
            },
            
            # Đà Lạt
            {
                'name': 'Cafe Đà Lạt',
                'address': '45 Nguyễn Chí Thanh, Đà Lạt',
                'city': 'dalat',
                'cafe_type': 'cafe',
                'price_range': 'moderate',
                'description': 'Cafe với view núi rừng Đà Lạt, không gian yên tĩnh',
                'opening_hours': '7:00 AM - 9:00 PM',
                'has_wifi': True,
                'has_parking': False,
                'is_quiet': True,
            },
            
            # Huế
            {
                'name': 'Cafe Cung Đình',
                'address': '78 Lê Lợi, Thành phố Huế',
                'city': 'hue',
                'cafe_type': 'cafe',
                'price_range': 'moderate',
                'description': 'Cafe với kiến trúc Huế truyền thống',
                'opening_hours': '7:00 AM - 10:00 PM',
                'has_wifi': True,
                'has_parking': False,
                'is_quiet': True,
            },
        ]
        
        created_count = 0
        for cafe_data in cafes:
            cafe, created = CafeLocation.objects.get_or_create(
                name=cafe_data['name'],
                city=cafe_data['city'],
                defaults=cafe_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created cafe: {cafe.name} in {cafe.get_city_display()}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Cafe already exists: {cafe.name} in {cafe.get_city_display()}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new cafe locations')
        )
