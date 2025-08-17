from django.db import models

# Create your models here.
class Client(models.Model):
    ip = models.CharField(max_length=200, primary_key=True)

class File(models.Model):
    file_name = models.CharField(max_length=200, primary_key=True)
    is_ready = models.BooleanField(default=False)

class LocalFilePosition(models.Model):
    file_hash = models.CharField(max_length=300, primary_key=True)
    global_file = models.ForeignKey(File, on_delete=models.CASCADE, related_name="local_file_position")
    client_position = models.ForeignKey(Client, on_delete=models.CASCADE)

    file_id = models.IntegerField()

    def __ge__(self, value):
        return self.file_id >= value.file_id

    def __le__(self, value):
        return self.file_id <= value.file_id
    
    def __lt__(self, value):
        return self.file_id < value.file_id