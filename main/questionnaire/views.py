# django imports
from django.shortcuts import render,redirect
# authentication imports
from django.contrib.auth.decorators import login_required
# data-models imports
from questionnaire.models import Question,Response,Questionnaire
from questionnaire.forms import AnswerForm,AddQuestions
from accounts.models import User
from accounts.views import home
# imports for pdf generation of user responses 
from django.http import FileResponse
import io 
from reportlab.pdfgen import canvas 
from reportlab.lib.units import inch 
from reportlab.lib.pagesizes import letter 

@login_required(login_url = '/signin/')
def add_questions(request):
    user = request.user
    if user.is_coach:
        questions = Question.objects.all()
        form = AddQuestions(request.POST)
        variables = {
            "questions":questions,
            "form":form
        }
        if request.POST and form.is_valid():
            question = form.cleaned_data['question_text']
            category = form.cleaned_data['category']
            Question.objects.create(
                question_text = question,
                category = category
            )
            form = AddQuestions()
            return render(request,'coach/addquestions.html', {"form":form , "questions":questions})
        else:
            return render(request,'coach/addquestions.html', variables )
    else:
        return home(request)

@login_required(login_url = '/signin/')
def questionnaire_responses_to_pdf(request, client_id ):
    client = User.objects.get(id = client_id)
    if request.user.is_coach:
            
        buff = io.BytesIO()
        text_container = canvas.Canvas(buff, pagesize = letter , bottomup = 0)
        text_obj = text_container.beginText()
        text_obj.setTextOrigin(inch,inch)
        text_obj.setFont("Helvetica" , 14)
        
        # list to hold all content for pdf display 
        pdf_content = []
        
        # convert all forms into a uniform data type for ease of display 
        for content in pdf_content: 
            content = str(content)
            text_obj.textLine(content)
        
        # populate the pdf container 
        text_container.drawText(text_obj)
        text_container.showPage()
        text_container.save()
        buff.seek(0)
        
        # return a pdf of the clients respective responses 
        return FileResponse(buff, as_attachment = True , filename = f'{client.username}-response.pdf' ) 
    elif request.user.is_coach:
        return redirect('accounts:manage')    
    else:
        return home(request)
    
@login_required(login_url = '/signin/')
def questionnaire_view(request):
    if request.user.is_newclient:
        return render(request,'questionnaire/main.html')
    else:
        return home(request)

@login_required(login_url = '/signin/')
def answer_question(request, category):
    client = request.user
    if client.is_newclient:
        questions = Question.objects.filter(category = category)
        for index in range(questions.count()):
            Questionnaire.objects.get_or_create(
                provided_for = client, 
                question = questions[index],
            )
        questions_to_answer = Questionnaire.objects.filter( provided_for = client , answered = False)
        question = questions_to_answer.first()
        form = AnswerForm(request.POST or None)
        if not question:
            if category == 'sales':
                client.completed_P1 = True
                client.categories_answered += 1
                client.save()
            elif category == 'people':
                client.completed_P2 = True
                client.categories_answered += 1
                client.save()
            elif category == 'accounting':
                client.completed_P3 = True
                client.categories_answered += 1
                client.save()
            elif category == 'business':
                client.completed_P4 = True
                client.categories_answered += 1
                client.save()
            elif category == 'legal':
                client.completed_P5 = True
                client.categories_answered += 1
                client.save()
            elif category == 'tech':
                client.completed_P6 = True
                client.categories_answered += 1
                client.save()
            return redirect("questionnaire:main")
        variables = {
            "form":form,
            "question":question.question
        }
        if question:
            if request.POST and form.is_valid():
                if 'continue' in request.POST:
                    answer = form.cleaned_data['answer']
                    Response.objects.create(
                        responder = client, 
                        answer = answer,
                        question = question.question
                    )
                    question.answered = True
                    question.save()
                    return redirect("questionnaire:answer", category = category)
                if 'save' in request.POST:
                    answer = form.cleaned_data['answer']
                    Response.objects.create(
                        responder = client, 
                        answer = answer,
                        question = question.question
                    )
                    question.answered = True
                    question.save()
                    return redirect("questionnaire:main")
        return render(request , f'questionnaire/{category}.html' , variables )
    else:
        return home(request)

    
