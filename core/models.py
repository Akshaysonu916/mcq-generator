from django.db import models

class Candidate(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    resume_file = models.FileField(upload_to='resumes/')
    detected_domains = models.JSONField(default=list, blank=True)  # e.g. ["python", "mern"]
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} <{self.email}>"

class DomainQuestion(models.Model):
    domain = models.CharField(max_length=100)  # e.g. "python"
    question_text = models.TextField()
    options = models.JSONField()   # {"A":"...","B":"...","C":"...","D":"..."}
    correct_option = models.CharField(max_length=1)
    difficulty = models.CharField(max_length=20, default="medium")
    approved = models.BooleanField(default=False)  # admin QA
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.domain}] {self.question_text[:60]}"
    

class TestSession(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    domain = models.CharField(max_length=100)
    questions = models.ManyToManyField(DomainQuestion)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"TestSession {self.id} - {self.candidate.name}"
