from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Job, Task
from .serializers import JobSerializer
from .coinmarketcap import CoinMarketCap
from django.conf import settings

@api_view(['POST'])
def start_scraping(request):
    coins = request.data.get('coins', [])
    if not all(isinstance(coin, str) for coin in coins):
        return Response({"error": "Invalid input. All elements must be strings."}, status=status.HTTP_400_BAD_REQUEST)

    job = Job.objects.create()
    
    cmc = CoinMarketCap(settings.CHROME_DRIVER_PATH)
    for coin in coins:
        task = Task.objects.create(job=job, coin=coin)
        try:
            task.output = cmc.scrape_data(coin)
            task.status = 'completed'
        except Exception as e:
            task.output = {"error": str(e)}
            task.status = 'failed'
        task.save()

    serializer = JobSerializer(job)
    return Response({"job_id": job.id, "tasks": serializer.data['tasks']}, status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
def scraping_status(request, job_id):
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = JobSerializer(job)
    return Response(serializer.data)
