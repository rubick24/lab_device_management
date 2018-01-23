import datetime

from django.utils import timezone
from django.test import TestCase,Client

from django.contrib.auth.models import User,Group,Permission
from django.contrib.auth import authenticate
from .models import DeviceType,Device,Repair,Scrap,ApplyRecord


class UserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user('user1', 'u1@example.com', 'password')
        User.objects.create_user('user2', 'u2@example.com', 'password')

    def test_user_can_register(self):
        self.client.post('/register',{'username':'user3','email':'u3@example.com','password':'password'})
        u = User.objects.get(username='user3')
        self.assertEqual(u.email,'u3@example.com')

    def test_user_can_login(self):
        self.assertIs(self.client.login(username='user1', password='password'), True)
        self.assertIs(self.client.login(username='user2', password='wrong password'), False)
        self.assertIs(self.client.login(username='user3', password='password'), False)

class DeviceTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user('user1', 'email@example.com', 'password',is_superuser=True)
       
        self.client.login(username='user1', password='password')
        device_type = DeviceType.objects.create(name='type1')
        Device.objects.create(name='device1',device_type=device_type,model='model1', manager='manager1',manufacturer='manufacturer1',purchase_at=timezone.now())

    def test_add_new_device(self):
        device_type = DeviceType.objects.create(name='type2')
        device = Device(name='device2',device_type=device_type,model='model2', manager='manager2',manufacturer='manufacturer2',purchase_at=timezone.now())
        device.save()
        self.assertEqual(device,Device.objects.get(model='model2'))

    def test_get_device_list(self):
        device_list = Device.objects.all()
        self.assertEqual(device_list.count(),1)

    def test_repair_device(self):
        self.client.post('/device/1/repair',{'price':200,'person_in_charge':'me','repair_manufacturer':'jd'})
        device = Device.objects.get(pk=1)
        repair_record = Repair.objects.get(pk=1)
        self.assertEqual(device.status,1)
        self.assertEqual(repair_record.person_in_charge,'me')
        self.assertEqual(repair_record.status,0)
        self.client.post('/repair/1/finish')
        device = Device.objects.get(pk=1)
        repair_record = Repair.objects.get(pk=1)
        self.assertEqual(device.status,0)
        self.assertEqual(repair_record.status,1)

    def test_scrap_device(self):
        self.client.post('/device/1/scrap',{'reason':'swap new one'})
        device = Device.objects.get(pk=1)
        scrap_record = Scrap.objects.get(pk=1)
        self.assertEqual(device.status,2)
        self.assertEqual(scrap_record.reason,'swap new one')



class ApplyTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user('user1', 'email@example.com', 'password',is_superuser=True)
        self.client.login(username='user1', password='password')
        device_type = DeviceType.objects.create(name='type1')
        ApplyRecord.objects.create(
            applicant='applicant1',
            name='first batch',
            device_type=device_type,
            model='model1', 
            unit_price='0.5',
            count='2',
            reason='some reason',
            manufacturer='manufacturer1',
            apply_at=timezone.now()
            )
        ApplyRecord.objects.create(
            accept_at=timezone.now(),
            status=1,
            applicant='applicant2',
            name='second batch',
            device_type=device_type,
            model='model2',
            unit_price='50000',
            count='20',
            reason='some more reason',
            manufacturer='manufacturer1',
            apply_at=timezone.now()
            )

    def test_add_new_apply(self):
        self.client.post('/apply/add',{
            'applicant':'applicant1',
            'name':'third batch',
            'device_type':'new type',
            'model':'model2',
            'unit_price':'2.5',
            'count':3,
            'reason':'reason1',
            'manufacturer':'manufacturer1',
            })
        apply = ApplyRecord.objects.get(pk=3)
        self.assertEqual(apply.count,3)

    def test_accept_apply(self):
        self.client.post('/apply/1/accept')
        apply = ApplyRecord.objects.get(pk=1)
        self.assertEqual(apply.status,1)
        
    def test_refuse_apply(self):
        self.client.post('/apply/1/refuse')
        apply = ApplyRecord.objects.get(pk=1)
        self.assertEqual(apply.status,3)

    def test_finish_apply(self):
        self.client.post('/apply/2/finish')
        apply = ApplyRecord.objects.get(pk=2)
        self.assertEqual(apply.status,2)
        devices = Device.objects.all()
        self.assertEqual(devices.count(),20)
        self.assertEqual(devices[11].name,apply.name+'-12')