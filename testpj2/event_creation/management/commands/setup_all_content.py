from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Setup all content: lessons, phrases, and quizzes'

    def handle(self, *args, **options):
        self.stdout.write('Setting up all content for Vietnam-Japan Connect...')
        
        # Create lessons
        self.stdout.write('\n1. Creating lessons...')
        try:
            call_command('create_lessons')
            self.stdout.write(self.style.SUCCESS('✓ Lessons created successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error creating lessons: {e}'))
        
        # Create additional lessons
        self.stdout.write('\n2. Creating additional lessons...')
        try:
            call_command('create_additional_lessons')
            self.stdout.write(self.style.SUCCESS('✓ Additional lessons created successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error creating additional lessons: {e}'))
        
        # Create culture lessons
        self.stdout.write('\n3. Creating culture lessons...')
        try:
            call_command('create_culture_lessons')
            self.stdout.write(self.style.SUCCESS('✓ Culture lessons created successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error creating culture lessons: {e}'))
        
        # Create phrases
        self.stdout.write('\n4. Creating Vietnamese phrases...')
        try:
            call_command('create_phrases')
            self.stdout.write(self.style.SUCCESS('✓ Phrases created successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error creating phrases: {e}'))
        
        # Create quizzes
        self.stdout.write('\n5. Creating quiz questions...')
        try:
            call_command('create_quizzes')
            self.stdout.write(self.style.SUCCESS('✓ Quiz questions created successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error creating quizzes: {e}'))
        
        # Create theory data
        self.stdout.write('\n6. Creating theory sections...')
        try:
            call_command('create_theory_data')
            self.stdout.write(self.style.SUCCESS('✓ Theory sections created successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error creating theory sections: {e}'))
        
        # Seed basic content
        self.stdout.write('\n7. Seeding basic content...')
        try:
            call_command('seed_content')
            self.stdout.write(self.style.SUCCESS('✓ Basic content seeded successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error seeding basic content: {e}'))
        
        self.stdout.write(
            self.style.SUCCESS('\n🎉 All content setup completed! Users can now create posts with rich lesson content.')
        )
        
        self.stdout.write('\n📚 Available content:')
        self.stdout.write('   • 30 comprehensive Vietnamese language lessons')
        self.stdout.write('   • 150+ Vietnamese phrases with translations')
        self.stdout.write('   • 20+ quiz questions for learning')
        self.stdout.write('   • Theory sections with conversation examples')
        self.stdout.write('   • Cultural lessons for both countries')
        self.stdout.write('   • Cafe locations for language exchange meetings')
        
        self.stdout.write('\n💡 Users can now:')
        self.stdout.write('   • Browse lessons by category and difficulty')
        self.stdout.write('   • Learn about Vietnamese and Japanese culture')
        self.stdout.write('   • Create language exchange posts using phrases')
        self.stdout.write('   • Take quizzes to test their knowledge')
        self.stdout.write('   • Find partners for language practice')
        self.stdout.write('   • Arrange meetings at suggested cafe locations')
