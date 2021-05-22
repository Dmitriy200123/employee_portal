from django.contrib.auth.models import User
from django.test import TestCase, Client
from employee_information_site.models import Employee, CompanyDepartment, EmployeePosition


# Create your tests here.

class MainTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@mail.ru', password='password')

        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()
        self.client.login(username='jacob', password='password')

        dep = CompanyDepartment(name='aaaa')
        dep.save()
        dep2 = CompanyDepartment(name='bbbb')
        dep2.save()
        pos0 = EmployeePosition(name='position1', department=dep2)
        pos1 = EmployeePosition(name='position1', department=dep)
        pos2 = EmployeePosition(name='position2', department=dep)
        pos0.save()
        pos1.save()
        pos2.save()

        employee = User.objects.create_user(username='test', email='test@mail.ru', password='test', id=101)
        e = Employee(first_name='First', is_new_employee=False, user_id=employee.id, department=dep2, position=pos0)
        e.save()

        employee = User.objects.create_user(username='test2', email='test2@mail.ru', password='test', id=102)
        e = Employee(first_name='Second', is_new_employee=False, user_id=employee.id, department=dep, position=pos1)
        e.save()

        employee = User.objects.create_user(username='test3', email='test3@mail.ru', password='test', id=103)
        e = Employee(first_name='Third', is_new_employee=False, user_id=employee.id, department=dep, position=pos2)
        e.save()


class FilterTesting(MainTest):

    def test_find_all(self):
        response = self.client.get('/employees_information/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'First')
        self.assertContains(response, 'Second')
        self.assertContains(response, 'Third')

    def test_find_by_name(self):
        response = self.client.get('/employees_information/', {'full_name': 'First'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'First')
        self.assertNotContains(response, 'Second')
        self.assertNotContains(response, 'Third')

    def test_find_by_departament(self):
        response = self.client.get('/employees_information/', {'department': '2'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'First')
        self.assertNotContains(response, 'Second')
        self.assertNotContains(response, 'Third')

    def test_find_by_position(self):
        response = self.client.get('/employees_information/', {'position': '2'})

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'First')
        self.assertContains(response, 'Second')
        self.assertNotContains(response, 'Third')

    def test_find_by_departament_and_position(self):
        response = self.client.get('/employees_information/', {'department': '1', 'position': '3'})

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'First')
        self.assertNotContains(response, 'Second')
        self.assertContains(response, 'Third')

    def test_cant_find(self):
        response = self.client.get('/employees_information/', {'department': '2', 'position': '3'})

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'First')
        self.assertNotContains(response, 'Second')
        self.assertNotContains(response, 'Third')

    def test_can_view_detailed(self):
        response = self.client.get('/employees_information/employee/?user=102')
        self.assertEqual(response.status_code, 200)

    def test_cant_view_details_of_dont_exists_user(self):
        response = self.client.get('/employees_information/employee/?user=999')
        self.assertEqual(response.status_code, 404)
