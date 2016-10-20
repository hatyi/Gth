from django.contrib import admin
from app.models import *


admin.site.register(Profile)
admin.site.register(FileData)
admin.site.register(BusDriver)

admin.site.register(Comment)
admin.site.register(CommentFileUpload)

admin.site.register(ChoiceGroup)
admin.site.register(ChoiceModel)

admin.site.register(Report)
admin.site.register(Page)

admin.site.register(TextInputModel)
admin.site.register(DateInputModel)
admin.site.register(RangeInputModel)
admin.site.register(ChoicesInputModel)
admin.site.register(SignatureInputModel)
admin.site.register(ReportInputGroupModel)

admin.site.register(ReportResult)
admin.site.register(ReportResultInput)

admin.site.register(Bus)
admin.site.register(BusService)
