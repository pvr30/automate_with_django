from django.shortcuts import render, redirect
from .utils import get_all_custom_models
from django.conf import settings
from uploads.models import Upload
from django.core.management import call_command
from django.contrib import messages


def import_data(request):
    if request.method == 'POST':
        file_path = request.FILES.get('file_path')
        model_name = request.POST.get('model_name')

        upload = Upload.objects.create(file=file_path, model_name=model_name)

        relative_path = str(upload.file.url)
        base_url = str(settings.BASE_DIR)

        file_path = base_url + relative_path

        try:
            call_command('importdata', file_path, model_name)
            messages.success(request, 'Data imported successfully.')
        except Exception as ex:
            messages.error(request, str(ex))

        return redirect('import_data')
    else:
        custom_models = get_all_custom_models()
        context = {
            'custom_models': custom_models
        }
    return render(request, 'dataentry/import_data.html', context)
