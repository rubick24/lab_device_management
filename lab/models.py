from django.db import models

class DeviceType(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Device(models.Model):
    STATUS_CHOICES = (
        (0,'正常'),
        (1,'维修中'),
        (2,'已报废')
    )
    name = models.CharField(max_length=256)
    device_type = models.ForeignKey(DeviceType, on_delete=models.PROTECT)
    model = models.CharField(max_length=256)
    status = models.SmallIntegerField(choices=STATUS_CHOICES,default=0)
    manager = models.CharField(max_length=256)
    manufacturer = models.CharField(max_length=256)
    purchase_at = models.DateTimeField()
    scrap_at = models.DateField(null=True,blank=True)
    
    def status_str(self): 
        return Device.STATUS_CHOICES[self.status][1]
    def __str__(self):
        return self.name


class Repair(models.Model):
    STATUS_CHOICES = (
        (0,'修理中'),
        (1,'已完成')
    )

    device = models.ForeignKey(Device,on_delete=models.PROTECT)
    status = models.SmallIntegerField(choices=STATUS_CHOICES,default=0)
    price = models.DecimalField(max_digits=12, decimal_places=1)
    person_in_charge = models.CharField(max_length=256)
    repair_manufacturer = models.CharField(max_length=256)
    start_at = models.DateField()
    finish_at = models.DateField(null=True,blank=True)
    def status_str(self): 
        return Repair.STATUS_CHOICES[self.status][1]
    def __str__(self):
        return str(self.id)+self.device.name+" 维修记录"


class Scrap(models.Model):
    device = models.ForeignKey(Device,on_delete=models.PROTECT)
    scrap_at = models.DateField()
    reason = models.CharField(max_length=512)
    def __str__(self):
        return str(self.id)+' '+self.device.name+" 报废记录"

class ApplyRecord(models.Model):
    STATUS_CHOICES = (
        (0,'已申请'),
        (1,'已审核'),
        (2,'已完成'),
        (3,'被否决')
    )
    applicant = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    status = models.SmallIntegerField(choices=STATUS_CHOICES,default=0)
    device_type = models.ForeignKey(DeviceType,on_delete=models.PROTECT)
    model = models.CharField(max_length=256)
    unit_price = models.DecimalField(max_digits=10, decimal_places=1)
    count = models.PositiveIntegerField()
    reason = models.CharField(max_length=512)
    manufacturer = models.CharField(max_length=256)
    apply_at = models.DateField()
    accept_at = models.DateField(null=True,blank=True)
    finish_at = models.DateField(null=True,blank=True)
    def status_str(self): 
        return ApplyRecord.STATUS_CHOICES[self.status][1]
    def __str__(self):
        return str(self.id)+' '+self.device_type.name+" 申请记录"