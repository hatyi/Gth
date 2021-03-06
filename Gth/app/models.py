from django.db import models
from django.contrib.auth.models import User
from itertools import chain
from django.db.models.query_utils import Q

#------------------------Users
def user_directory_path(instance, filename):
    return 'user_docs/user_{0}/{1}'.format(instance.user.username, filename)


class Profile(models.Model):
    ADMIN = 0
    DRIVER = 1
    COWORKER = 2
    ROLES = (
        (ADMIN, 'Admin'),    
        (DRIVER, 'Driver'),    
        (COWORKER, 'Co-Worker')    
    )
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    role = models.SmallIntegerField(default=DRIVER, choices=ROLES)
    name = models.CharField(max_length=255)
    date_of_birth = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return self.user.username

class FileData(models.Model):
    expire_date = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=255, default='This is a new report', blank=True, null=True)
    document = models.FileField(upload_to=user_directory_path, max_length=255)

    def __str__(self):
        return self.title + '_' + profile.user.username

class BusDriver(Profile):
    role = Profile.DRIVER
    bus_driver_id = models.ForeignKey(FileData, on_delete=models.CASCADE, related_name='dc_1')
    driving_licence_num = models.ForeignKey(FileData, on_delete=models.CASCADE, related_name='dc_2')
    passport_number = models.ForeignKey(FileData, on_delete=models.CASCADE, related_name='dc_3')
    digital_tachograph_card_number = models.ForeignKey(FileData, on_delete=models.CASCADE, related_name='dc_4')
    medical_check = models.ForeignKey(FileData, on_delete=models.CASCADE, related_name='dc_5')
    jobcontract = models.ForeignKey(FileData, on_delete=models.CASCADE, related_name='dc_6')
    paf = models.ForeignKey(FileData, on_delete=models.CASCADE, related_name='dc_7')

#------------------------Users



#------------------------Helpers
class ChoiceGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name


class ChoiceModel(models.Model):
    name = models.CharField(max_length=25, default='Choice 1')
    color = models.CharField(max_length=7, default='#FFFFFF')
    value = models.IntegerField(default=1)
    is_default_answer = models.BooleanField(default=False)
    is_bad_answer = models.BooleanField(default=False)
    must_comment = models.BooleanField(default=False)
    group = models.ForeignKey(ChoiceGroup, on_delete=models.CASCADE, default=None, blank=True, null=True, related_name='choices')

    def __str__(self):
        return self.name
#------------------------Helpers


#------------------------ReportModel
class Report(models.Model):
    title = models.CharField(max_length=50, default='New Report')
    description = models.CharField(max_length=255, default='This is a new report', blank=True, null=True)
    active = models.BooleanField(default=True)
    needs_bus = models.BooleanField(default=True)
    needs_user_data = models.BooleanField(default=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='child')


    def __str__(self):
        return self.title


class Page(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='pages', blank=True, null=True)
    title = models.CharField(max_length=50, default='New Page')
    description = models.CharField(max_length=255, default='This is a new page')
    page = models.SmallIntegerField(default=1)
    

    @property
    def inputs_ordered(self):
        groups = self.groups.all()
        simple_inputs = self.inputs.filter(Q(group=None))
        result = chain(groups, simple_inputs)
        result = {x.page_order:x for x in result}
        result = [result[key] for key in sorted(result)]
        return result

    def __str__(self):
        return '%s - %s' % (self.report.title, self.title)

class ReportInputGroupModel(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='groups', blank=True, null=True)
    title = models.CharField(max_length=50, default='New Group')
    description = models.CharField(max_length=255, blank=True, null=True, default='This is a new input group')
    page_order = models.SmallIntegerField(default=1)

    @property
    def inputs_ordered(self):
        return self.inputs.order_by('page_order')

    def __str__(self):
        return '%s - %s - %s' % (self.page.report.title, self.page.title, self.title)

class ReportInputModel(models.Model):
    TEXT = 0
    DATE = 1
    SLIDER = 2
    CHOICES = 3
    SIGNATURE = 4
    TYPES = (
        (CHOICES, 'Choices'),    
        (DATE, 'Date'),    
        (SLIDER, 'Slider'),    
        (TEXT, 'Text'),    
        (SIGNATURE, 'Signature')    
    )


    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='inputs', blank=True, null=True)
    group = models.ForeignKey(ReportInputGroupModel, on_delete=models.CASCADE, related_name='inputs', default=None, blank=True, null=True)
    
    title = models.CharField(max_length=50, default='New Input')
    placeholder = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True, default='This is a new input field')
    
    input_type = models.SmallIntegerField(choices=TYPES, default=CHOICES)
    page_order = models.SmallIntegerField(default=1)
    group_order = models.SmallIntegerField(default=1)

    can_be_empty = models.BooleanField(default=False)
    can_comment = models.BooleanField(default=True)
    must_comment = models.BooleanField(default=False)
    

    def __str__(self):
        return self.title

    @property
    def type_as_str(self):
        return {x[0]:x[1] for x in self.TYPES}.get(self.input_type)

class TextInputModel(ReportInputModel):
    input_type = ReportInputModel.TEXT
    default_text = models.CharField(max_length=255, blank=True, null=True)

class DateInputModel(ReportInputModel):
    TODAY = 'Today'
    DATEEXPRESSIONS = (
        (TODAY, 'Today'),
        )

    input_type = ReportInputModel.DATE
    default_date = models.DateTimeField(blank=True, null=True)
    default_date_expression = models.CharField(max_length=50, choices=DATEEXPRESSIONS, blank=True, null=True)

class RangeInputModel(ReportInputModel):
    input_type = ReportInputModel.SLIDER
    default_value = models.IntegerField(blank=True, null=True)
    increment = models.IntegerField(blank=True, null=True, default=1)
    min_value = models.IntegerField(blank=True, null=True)
    max_value = models.IntegerField(blank=True, null=True)

class ChoicesInputModel(ReportInputModel):
    input_type = ReportInputModel.CHOICES
    choices = models.ForeignKey(ChoiceGroup, on_delete=models.PROTECT)

class SignatureInputModel(ReportInputModel):
    input_type = ReportInputModel.SIGNATURE
    default_typed_signature = models.CharField(max_length=255, blank=True, null=True)

#------------------------ReportModel



#------------------------ReportResult
class ReportResult(models.Model):
    report = models.ForeignKey(Report, on_delete=models.PROTECT, related_name='report_results')
    profile = models.OneToOneField(Profile, on_delete = models.PROTECT)
    finished_editing_timestamp = models.DateTimeField()
    uploaded_timestamp = models.DateTimeField(auto_now=True)

    

    def __str__(self):
        return '%s - %s' % (self.report.title, self.profile.user.username)

def user_signature_path(instance, filename):
    return 'user_docs/user_{0}/signatures/%Y_%M_%D_{1}'.format(instance.user.username, filename)

class ReportResultInput(models.Model):
    input_model = models.ForeignKey(ReportInputModel, on_delete=models.PROTECT, related_name='input_results')
    
    text_value = models.CharField(max_length=255, blank=True, null=True)
    date_value = models.DateTimeField(blank=True, null=True)
    range_value = models.FloatField(blank=True, null=True)
    choice_value = models.ForeignKey(ChoiceModel, on_delete=models.PROTECT, related_name='dk_3', blank=True, null=True)
    signature_typed_value = models.CharField(max_length=255, blank=True, null=True)
    signature_value = models.FileField(upload_to=user_signature_path, blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.input_model.title, self.text_value or self.date_value or self.range_value or self.choice_value)


class Comment(models.Model):
    text = models.CharField(max_length=1000)
    target_input = models.OneToOneField(ReportResultInput, on_delete = models.CASCADE, blank=True, null=True, related_name='comment')


def user_comment_path(instance, filename):
    return 'user_docs/user_{0}/comments/%Y_%M_%D/{1}'.format(instance.user.username, filename)

class CommentFileUpload(models.Model):
    profile = models.ForeignKey(Profile)
    file = models.FileField(upload_to=user_comment_path)
    timestamp = models.DateTimeField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True, related_name='files')
#------------------------ReportResult


def bus_image_path(instance, filename):
    return 'bus_docs/user_{0}/comments/%Y_%M_%D/{1}'.format(instance.user.username, filename)


#------------------------Bus
class Bus(models.Model):
    bus_image = models.FileField(upload_to=bus_image_path, verbose_name='Image')
    bus_id = models.CharField(max_length=25)
    plate_number = models.CharField(max_length=7)
    motor_number = models.CharField(max_length=30)

    def __str__(self):
        return self.bus_id


class BusService(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    service_date = models.DateField()
#------------------------Bus


