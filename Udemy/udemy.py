import re
import os
import datetime
import requests
import json
from udemy_driver import Driver

UDEMY_EMAIL = ''
UDEMY_PASSWORD = ''

#For more into about HEADER visit: https://www.udemy.com/developers/
HEADER = {
    "Authorization": ''}

today = datetime.datetime.now()

CATEGORIES = {
    'Business': ['All Business', 'Finance', 'Entrepreneurship', 'Communications', 'Management', 'Sales', 'Strategy',
                 'Operations', 'Project Management', 'Business Law', 'Data & Analytics', 'Home Business',
                 'Human Resources', 'Industry', 'Media', 'Real Estate', 'Other'],
    'Health & Fitness': ['All Health & Fitness', 'Fitness', 'General Health', 'Sports', 'Nutrition', 'Yoga',
                         'Mental Health', 'Dieting', 'Self Defense', 'Safety & First Aid', 'Dance', 'Meditation',
                         'Other'],
    'Personal Development': ['All Personal Development', 'Personal Transformation', 'Productivity', 'Leadership',
                             'Personal Finance', 'Career Development', 'Parenting & Relationships', 'Happiness',
                             'Religion & Spirituality', 'Personal Brand Building', 'Creativity', 'Influence',
                             'Self Esteem', 'Stress Management', 'Memory & Study Skills', 'Motivation', 'Other'],
    'Lifestyle': ['All Lifestyle', 'Arts & Crafts', 'Food & Beverage', 'Beauty & Makeup', 'Travel', 'Gaming',
                  'Home Improvement', 'Pet Care & Training', 'Other'],
    'Office Productivity': ['All Office Productivity', 'Microsoft', 'Apple', 'Google', 'SAP', 'Intuit', 'Salesforce',
                            'Oracle', 'Other'],
    'Photography': ['All Photography', 'Digital Photography', 'Photography Fundamentals', 'Portraits', 'Landscape',
                    'Black & White', 'Photography Tools', 'Mobile Photography', 'Travel Photography',
                    'Commercial Photography', 'Wedding Photography', 'Wildlife Photography', 'Video Design', 'Other'],
    'IT & Software': ['All IT & Software', 'IT Certification', 'Network & Security', 'Hardware', 'Operating Systems',
                      'Other'],
    'Marketing': ['All Marketing', 'Digital Marketing', 'Search Engine Optimization', 'Social Media Marketing',
                  'Branding', 'Marketing Fundamentals', 'Analytics & Automation', 'Public Relations', 'Advertising',
                  'Video & Mobile Marketing', 'Content Marketing', 'Non-Digital Marketing', 'Growth Hacking',
                  'Affiliate Marketing', 'Product Marketing', 'Other'],
    'Development': ['All Development', 'Web Development', 'Mobile Apps', 'Programming Languages', 'Game Development',
                    'Databases', 'Software Testing', 'Software Engineering', 'Development Tools', 'E-Commerce'],
    'Language': ['All Language', 'English', 'Spanish', 'German', 'French', 'Japanese', 'Portuguese', 'Chinese',
                 'Russian', 'Latin', 'Arabic', 'Hebrew', 'Italian', 'Other'],
    'Test Prep': ['All Test Prep', 'Grad Entry Exam', 'International High School', 'College Entry Exam',
                  'Test Taking Skills', 'Other'],
    'Academics': ['All Academics', 'Social Science', 'Math & Science', 'Humanities'],
    'Design': ['All Design', 'Web Design', 'Graphic Design', 'Design Tools', 'User Experience', 'Game Design',
               'Design Thinking', '3D & Animation', 'Fashion', 'Architectural Design', 'Interior Design', 'Other'],
    'Music': ['All Music', 'Instruments', 'Production', 'Music Fundamentals', 'Vocal', 'Music Techniques',
              'Music Software', 'Other'],
    'Teacher Training': ['All Teacher Training', 'Instructional Design', 'Educational Development', 'Teaching Tools',
                         'Other']}

file_dir = os.path.dirname(__file__)


def check_free_courses(subcategory, page_number='1', page_size='100', price='price-free', ordering='most-reviewed'):
    params = {
        'page': page_number,
        'page_size': page_size,
        'price': price,
        'ordering': ordering,
        'language': 'en',
        'subcategory': subcategory
    }
    req = requests.get('https://www.udemy.com/api-2.0/courses', headers=HEADER, params=params)
    return json.loads(req.content)


def round_up(number_of_courses):
    q, r = divmod(number_of_courses, 100)
    return q + int(bool(r))


def save_dict_as_file(dict_of_courses):
    with open(os.path.join(file_dir, '{} free courses.txt'.format(today.strftime('%d %b %Y'))), 'wt') as f:
        json.dump(dict_of_courses, f, indent=4, sort_keys=True)


def get_today_free_courses():
    free_courses = {}
    for category in CATEGORIES:
        print '\n*** {} ***\n'.format(category)
        for subcategory in CATEGORIES[category]:
            if 'All' not in subcategory:
                print 'Getting free courses for {}'.format(subcategory)
                json_req = check_free_courses(subcategory)
                courses_list = json_req['results']

                number_of_pages = round_up(json_req['count'])
                if number_of_pages > 1:
                    for page_number in range(2, number_of_pages + 1):
                        print '    Making request for page 1 from {} \n    Making request for page {} from {}'.format(number_of_pages,
                                                                                                        page_number,
                                                                                                        number_of_pages)
                        req = check_free_courses(subcategory=subcategory, page_number=page_number)
                        courses_list += req['results']

                for course in range(len(courses_list)):
                    title = courses_list[course]['title'].encode('utf-8').replace(",", "")
                    url = 'https://www.udemy.com{}'.format(courses_list[course]['url'].encode('utf-8'))

                    free_courses.setdefault(category, {}).setdefault(subcategory, {})[title] = url

                save_dict_as_file(free_courses)
    return free_courses


def get_already_added_list():
    pattern = re.compile('name: (?P<course_name>.*)\surl: (?P<url>.*)')
    already_added_list = []

    with open(os.path.join(file_dir, 'already_added.txt'), 'r') as read:
        for line in read.readlines():
            match = re.match(pattern, line)
            if match:
                already_added_list.append(match.group('course_name'))
    return already_added_list


def add_to_aleady_added(name, url):
    with open(os.path.join(file_dir, 'already_added.txt'), 'a') as already_added:
        already_added.write('\nname: {} url: {}'.format(name, url))


def add_to_statistics(new_added):
    with open(os.path.join(file_dir, 'statistics.txt'), 'a') as statistics:
        statistics.write('date: {} new_added: {}'.format(today.strftime('%d %b %Y'), new_added))


def run():
    all_free_courses = get_today_free_courses()
    already_added_list = get_already_added_list()

    new_added = 0
    with Driver() as driver:
        driver.udemy_login(UDEMY_EMAIL, UDEMY_PASSWORD)

        for category in all_free_courses.values():
            for subcategory in category.values():
                for name, url in subcategory.viewitems():
                    if name in already_added_list:
                        print '+++ {} course already exist on your account +++'.format(name)
                    else:
                        print '\n*** Adding {} course ***'.format(name)
                        driver.add_course(url, name)

                        new_added += 1
                        add_to_aleady_added(name, url)
        print '\n          *** Added {} new courses ***'.format(new_added)
    add_to_statistics(new_added)

if __name__ == '__main__':
    run()
