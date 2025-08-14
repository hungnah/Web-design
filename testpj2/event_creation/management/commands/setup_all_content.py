from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Setup all content: phrases and cultural content'

    def handle(self, *args, **options):
        self.stdout.write('Setting up all content for Vietnam-Japan Connect...')
        
        # Create phrases
        self.stdout.write('\n1. Creating Vietnamese phrases...')
        try:
            call_command('create_phrases')
            self.stdout.write(self.style.SUCCESS('✓ Phrases created successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error creating phrases: {e}'))
        
        # Create cultural locations
        self.stdout.write('\n2. Creating cultural locations...')
        try:
            call_command('create_cultural_locations')
            self.stdout.write(self.style.SUCCESS('✓ Cultural locations created successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error creating cultural locations: {e}'))
        
        # Create cultural lessons
        self.stdout.write('\n3. Creating cultural lessons...')
        try:
            call_command('create_cultural_lessons')
            self.stdout.write(self.style.SUCCESS('✓ Cultural lessons created successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error creating cultural lessons: {e}'))
        
        # Create cultural challenges
        self.stdout.write('\n4. Creating cultural challenges...')
        try:
            call_command('create_cultural_challenges')
            self.stdout.write(self.style.SUCCESS('✓ Cultural challenges created successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error creating cultural challenges: {e}'))
        
        # Seed basic content
        self.stdout.write('\n5. Seeding basic content...')
        try:
            call_command('seed_content')
            self.stdout.write(self.style.SUCCESS('✓ Basic content seeded successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error seeding basic content: {e}'))
        
        self.stdout.write(
            self.style.SUCCESS('\n🎉 All content setup completed! Users can now create posts with rich content.')
        )
        
        self.stdout.write('\n📚 Available content:')
        self.stdout.write('   • Vietnamese phrases with translations')
        self.stdout.write('   • Cultural lessons for both countries')
        self.stdout.write('   • Cultural challenges and activities')
        self.stdout.write('   • Cafe locations for language exchange meetings')
        
        self.stdout.write('\n💡 Users can now:')
        self.stdout.write('   • Learn about Vietnamese and Japanese culture')
        self.stdout.write('   • Create language exchange posts using phrases')
        self.stdout.write('   • Find partners for language practice')
        self.stdout.write('   • Arrange meetings at suggested cafe locations')
