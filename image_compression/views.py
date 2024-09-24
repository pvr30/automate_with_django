from django.shortcuts import render, redirect
from .forms import CompressImageForm
from PIL import Image
from django.http import HttpResponse
import io


def compress(request):
    user = request.user
    if request.method == 'POST':
        form = CompressImageForm(request.POST, request.FILES)
        if form.is_valid():
            original_img = form.cleaned_data['original_img']
            quality = form.cleaned_data['quality']

            compressed_image = form.save(commit=False)
            compressed_image.user = user

            img = Image.open(original_img)
            output_format = img.format
            buffer = io.BytesIO()
            img.save(buffer, format=output_format, quality=quality)
            buffer.seek(0)

            compressed_image.compressed_img.save(
                f'compressed_{original_img}', buffer
            )
            response = HttpResponse(buffer.getvalue(), content_type=f'image/{output_format.lower()}')
            response['Content-Disposition'] = f'attachment; filename=compressed_{original_img}'
            return response
    else:
        form = CompressImageForm()
        context = {
            'form': form
        }
        return render(request, 'image_compression/compression.html', context)
