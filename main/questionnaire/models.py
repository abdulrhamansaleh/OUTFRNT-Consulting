from django.db import models
from accounts.models import User

class Response(models.Model):
    responder = models.ForeignKey(User, on_delete = models.CASCADE)
    answer = models.TextField()
    
    def __str__(self):
        return self.answer

class Question(models.Model):
    category_choices = [
        ('sales', 'Sales & Marketing'),
        ('people', 'People & Culture'),
        ('accounting', 'Accounting & Finance'),
        ('business', 'Business & Operations'),
        ('legal', 'Legal & Governance'),
        ('tech','Technology')
    ]
    
    question_text = models.CharField(max_length = 255)
    question_answer = models.ForeignKey(Response, on_delete = models.CASCADE,null=True , blank = True) 
    responder = models.ForeignKey(User, on_delete = models.CASCADE, null=True ,blank = True)
    
    category = models.CharField(
        max_length = 60, 
        choices = category_choices,
        blank = False,
        default = "Select Only One Category"
        )
    
    # track answered questions 
    answered = models.BooleanField(default = False)
    
    def __str__(self):
        return self.question_text


    
