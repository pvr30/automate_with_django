from django.shortcuts import render, redirect
from .utils import get_all_custom_models, check_csv_errors
from django.conf import settings
from uploads.models import Upload
from django.contrib import messages
from dataentry.tasks import import_data_task, export_data_task


def import_data(request):
    if request.method == 'POST':
        file_path = request.FILES.get('file_path')
        model_name = request.POST.get('model_name')

        upload = Upload.objects.create(file=file_path, model_name=model_name)

        relative_path = str(upload.file.url)
        base_url = str(settings.BASE_DIR)

        file_path = base_url + relative_path

        try:
            check_csv_errors(file_path, model_name)
        except Exception as e:
            messages.error(request, str(e))
            return redirect('import_data')

        import_data_task.delay(file_path, model_name)

        messages.success(request, 'Your Data being imported successfully. '
                                  'you will be notify once it complete.')

        return redirect('import_data')
    else:
        custom_models = get_all_custom_models()
        context = {
            'custom_models': custom_models
        }
    return render(request, 'dataentry/import_data.html', context)


def export_data(request):
    if request.method == 'POST':
        model_name = request.POST.get('model_name')

        export_data_task.delay(model_name)

        messages.success(request, 'Your data is exported, '
                                  'you will be notify once it complete')
        return redirect('export_data')
    else:
        custom_models = get_all_custom_models()
        context = {
            'custom_models': custom_models
        }
    return render(request, 'dataentry/export_data.html', context)
