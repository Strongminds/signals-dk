from django.contrib.auth.models import Permission
from rest_framework import status

from signals.apps.signals.factories import CategoryFactory, DepartmentFactory, ParentCategoryFactory
from signals.apps.signals.models import Department
from tests.test import SIAReadWriteUserMixin, SignalsBaseApiTestCase


class TestPrivateDepartmentEndpoint(SIAReadWriteUserMixin, SignalsBaseApiTestCase):
    list_endpoint = '/signals/v1/private/departments/'
    detail_endpoint = '/signals/v1/private/departments/{pk}'

    def setUp(self):
        self.department_read = Permission.objects.get(
            codename='sia_department_read'
        )
        self.department_write = Permission.objects.get(
            codename='sia_department_write'
        )
        self.sia_read_write_user.user_permissions.add(self.department_read)
        self.sia_read_write_user.user_permissions.add(self.department_write)

        self.department = DepartmentFactory.create()

        self.maincategory = ParentCategoryFactory.create()
        self.subcategory = CategoryFactory.create(parent=self.maincategory)

    def test_get_list(self):
        self.client.force_authenticate(user=self.sia_read_write_user)

        response = self.client.get(self.list_endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data['count'], 20)
        self.assertEqual(len(data['results']), 20)

    def test_get_detail(self):
        self.client.force_authenticate(user=self.sia_read_write_user)

        response = self.client.get(self.detail_endpoint.format(pk=self.department.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data['name'], self.department.name)
        self.assertEqual(data['code'], self.department.code)
        self.assertEqual(data['is_intern'], self.department.is_intern)
        self.assertEqual(data['can_direct'], self.department.can_direct)

        self.assertEqual(len(data['categories']), 0)

    def test_post(self):
        self.client.force_authenticate(user=self.sia_read_write_user)

        data = {
            'name': 'The department',
            'code': 'TDP',
            'is_intern': True,
            'can_direct': True,
            'categories': [
                {
                    'category_id': self.subcategory.pk,
                    'is_responsible': True
                }
            ]
        }

        response = self.client.post(
            self.list_endpoint, data=data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()
        self.assertEqual(data['name'], 'The department')
        self.assertEqual(data['code'], 'TDP')
        self.assertEqual(data['is_intern'], True)
        self.assertEqual(data['can_direct'], True)
        self.assertEqual(len(data['categories']), 1)

        self.assertTrue(data['categories'][0]['is_responsible'])
        self.assertTrue(data['categories'][0]['can_view'])
        self.assertEqual(data['categories'][0]['category']['departments'][0]['code'], 'TDP')

    def test_post_no_categories(self):
        self.client.force_authenticate(user=self.sia_read_write_user)

        data = {
            'name': 'The department',
            'code': 'TDP',
            'is_intern': True,
            'can_direct': False
        }

        response = self.client.post(
            self.list_endpoint, data=data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()
        self.assertEqual(data['name'], 'The department')
        self.assertEqual(data['code'], 'TDP')
        self.assertEqual(data['is_intern'], True)
        self.assertEqual(len(data['categories']), 0)

    def test_post_invalid_data(self):
        self.client.force_authenticate(user=self.sia_read_write_user)

        data = {
            'name': 'The department',
            'code': 'TDP-too-long-code',
        }

        response = self.client.post(
            self.list_endpoint, data=data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = response.json()
        self.assertEqual(data['code'][0],
                         'Zorg ervoor dat dit veld niet meer dan 3 karakters bevat.')

    def test_patch(self):
        self.client.force_authenticate(user=self.sia_read_write_user)
        can_direct = not self.department.can_direct

        data = {
            'name': 'A way better name than generated by the factory',
            'categories': [
                {
                    'category_id': self.subcategory.pk,
                    'is_responsible': True
                }
            ],
            'can_direct': can_direct,
        }

        response = self.client.patch(
            self.detail_endpoint.format(pk=self.department.pk), data=data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data['name'], 'A way better name than generated by the factory')
        self.assertEqual(data['code'], self.department.code)
        self.assertEqual(data['is_intern'], self.department.is_intern)
        self.assertEqual(data['can_direct'], can_direct)
        self.assertTrue(data['categories'][0]['is_responsible'])
        self.assertTrue(data['categories'][0]['can_view'])
        self.assertEqual(data['categories'][0]['category']['departments'][0]['code'],
                         self.department.code)

    def test_patch_invalid_data(self):
        self.client.force_authenticate(user=self.sia_read_write_user)

        data = {
            'code': 'way too long to get accepted'  # can only be 3 characters long
        }

        response = self.client.patch(
            self.detail_endpoint.format(pk=self.department.pk), data=data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = response.json()
        self.assertEqual(data['code'][0],
                         'Zorg ervoor dat dit veld niet meer dan 3 karakters bevat.')

    def test_delete_method_not_allowed(self):
        self.client.force_authenticate(user=self.sia_read_write_user)

        response = self.client.delete(self.detail_endpoint.format(pk=1))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_SIG_2287(self):
        # Connect a parent category to the Department so that we can check the URL generated for this category
        self.maincategory.departments.add(self.department, through_defaults={'is_responsible': True, 'can_view': True})

        # Connect a child category to the Department so that we can check the URL generated for this category
        self.subcategory.departments.add(self.department, through_defaults={'is_responsible': True, 'can_view': True})

        # This should be the link of the parent category
        expected_parent_url = 'http://testserver/signals/v1/public/terms/categories/{}'.format(self.maincategory.slug)

        # This should be the link of the child category
        expected_child_url = 'http://testserver/signals/v1/public/terms/categories/{}/sub_categories/{}'.format(
            self.subcategory.parent.slug, self.subcategory.slug
        )

        self.client.force_authenticate(user=self.sia_read_write_user)
        response = self.client.get(self.detail_endpoint.format(pk=self.department.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data['categories']), 2)

        # Check the link
        category_assignment = data['categories'][0]
        category = category_assignment['category']
        category_url = category['_links']['self']['href']

        if 'sub_categories' in category_url:
            self.assertEqual(expected_child_url, category_url)
        else:
            self.assertEqual(expected_parent_url, category_url)

        # Check the link
        category_assignment = data['categories'][1]
        category = category_assignment['category']
        category_url = category['_links']['self']['href']

        if 'sub_categories' in category_url:
            self.assertEqual(expected_child_url, category_url)
        else:
            self.assertEqual(expected_parent_url, category_url)

    def test_department_filter_set(self):
        DepartmentFactory.create(can_direct=False)
        DepartmentFactory.create_batch(2, can_direct=True)
        n_can_direct = Department.objects.filter(can_direct=True).count()
        n_cannot_direct = Department.objects.filter(can_direct=False).count()

        self.client.force_authenticate(user=self.sia_read_write_user, )

        # no filter
        response = self.client.get(self.list_endpoint)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], Department.objects.count())

        # filter can_direct=True
        response = self.client.get(self.list_endpoint, {'can_direct': True})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], n_can_direct)

        # filter can_direct=False
        response = self.client.get(self.list_endpoint, {'can_direct': False})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], n_cannot_direct)
