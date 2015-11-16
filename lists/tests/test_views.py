from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from lists.models import Item, List
from lists.views import home_page #1
from django.template.loader import render_to_string

class HomePageTest(TestCase):

#   def test_root_url_resolves_to_home_page_view(self):
#        found = resolve('/')  #2
#        self.assertEqual(found.func, home_page)  #3
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()  #1
        response = home_page(request)  #2
#       self.assertIn('A new list item', response.content.decode())
        expected_html = render_to_string('home.html',
        {'new_item_text':  'A new list item'})
        #self.assertEqual(response.content.decode(), expected_html)
        #self.assertTrue(response.content.startswith(b'<html>'))  #3
        #self.assertIn(b'<title>To-Do lists</title>', response.content)  #4
        #self.assertTrue(response.content.strip().endswith(b'</html>'))  #5
    '''
    def test_home_page_show_auto_comment_empty(self):
       request = HttpRequest()
       response = home_page(request)
    
       self.assertIn('yey, waktunya berlibur', response.content.decode())
       #self.assertEqual(Item.objects.count(), 0, 'yes waktunya berlibur')
    
    def test_home_page_show_auto_comment_less_than_five(self):
       Item.objects.create(text='1: added entry 1')

       request = HttpRequest()
       response = home_page(request)

       self.assertIn('sibuk tapi santai', response.content.decode())
       #self.assertLess(Item.objects.count(), 5, 'sibuk tapi santai')
    
    def test_home_page_show_auto_comment_more_than_four(self):
       Item.objects.create(text='1: added entry 1')
       Item.objects.create(text='2: added entry 2')
       Item.objects.create(text='3: added entry 3')
       Item.objects.create(text='4: added entry 4')
       Item.objects.create(text='5: added entry 5')

       request = HttpRequest()
       response = home_page(request)

       self.assertIn('oh tidak', response.content.decode())
       #self.assertGreaterEqual(Item.objects.count(), 5, 'oh tidak ')
    '''
    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)

    #def test_home_page_displays_all_list_items(self):
        #Item.objects.create(text='itemey 1')
        #Item.objects.create(text='itemey 2')

        #request = HttpRequest()
        #response = home_page(request)

        #self.assertIn('itemey 1', response.content.decode())
        #self.assertIn('itemey 2', response.content.decode())
        
class NewListTest(TestCase):
    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')


    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))
        #self.assertEqual(response.status_code, 302)
        #self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
    '''
    def test_saving_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
    '''

class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)
    '''
    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
   '''

class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/%d/add_item' % (correct_list.id,),
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)


    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/%d/add_item' % (correct_list.id,),
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))