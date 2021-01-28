from rest_framework.serializers import ModelSerializer

from course.models import CourseCategory, Teacher, Course, CourseChapter, CourseLesson


class CourseCategoryModelSerializer(ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id', 'name']


class TeacherModelSerializer(ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name', 'title', 'signature', 'image', 'brief']


class CourseModelSerializer(ModelSerializer):
    teacher = TeacherModelSerializer()

    class Meta:
        model = Course
        fields = ["id", "name", "course_img", "students", "lessons", "pub_lessons", "price", "teacher", 'lesson_list']


class CourseDetailModelSerializer(ModelSerializer):
    '''课程信息详情'''
    teacher = TeacherModelSerializer()

    class Meta:
        model = Course

        fields = ["id", "name", "course_img", "students", "lessons", "pub_lessons", "price", "teacher", 'lesson_list',
                  'level']


class CapterLessonModelSerializer(ModelSerializer):
    class Meta:
        model = CourseLesson
        fields = ['id', 'name', 'duration', 'free_trail']


class CourseCapterModelSerializer(ModelSerializer):
    coursesections = CapterLessonModelSerializer(many=True)

    class Meta:
        model = CourseChapter
        fields = ['id', 'name', 'chapter','coursesections']
