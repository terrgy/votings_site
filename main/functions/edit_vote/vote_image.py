from main.forms import ImageUploadForm


def process_image_upload_form(request):
    return ImageUploadForm(request.POST, request.FILES)


def collect_image_upload_form():
    return ImageUploadForm()
