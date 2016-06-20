import unittest
from v2.generator.views import *
from v2.generator.serializers import *
from .urls import *
# Create your tests here.
# import os
# os.environ['DJANGO_SETTINGS_MODULE'] = "traffic.settings"
#
# import django
# django.setup()



# class TestStreamViewSet(unittest.TestCase):
#     def setUp(self):
#         self.svs = StreamViewSet()
#     def tearDown(self):
#         pass
#
#
#     def test_dir(self):
#         print(dir(self.svs))

# class TestGeneratorViewSet(unittest.TestCase):
#     def setUp(self):
#         self.svs = GeneratorViewSet()
#     def tearDown(self):
#         pass
#
#
#     def test_dir(self):
#         print(dir(self.svs))

class TestGeneratorSerializer(unittest.TestCase):
    def setUp(self):
        self.svs = GeneratorSerializer()
    def tearDown(self):
        pass


    def test_dir(self):
        print(repr(self.svs))
        def print_urls(urls):
            if isinstance(urls, list):
                for url in urls:
                    print_urls(url)
            elif hasattr(urls, 'url_patterns'):
                for url in urls.url_patterns:
                    print_urls(url)
            else:
                print(urls)
        print_urls(urlpatterns)

if __name__ == '__main__':
    unittest.main()