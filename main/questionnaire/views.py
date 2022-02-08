from django.shortcuts import render,redirect
from questionnaire.models import Question,Response,Questionnaire
from questionnaire.forms import AnswerForm,AddQuestions
from accounts.models import User
from django.contrib.auth.decorators import login_required
from accounts.views import home

# imports for pdf generation of user responses 
from django.http import FileResponse
import io 
from reportlab.pdfgen import canvas 
from reportlab.lib.units import inch 
from reportlab.lib.pagesizes import letter 



# add questions to the database for new clients to answer 
@login_required(login_url = '/signin/')
def questions(request):
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
            return render(request,'coach/Question.html', {"form":form , "questions":questions})
        else:
            return render(request,'coach/Question.html', variables )
    else:
        return home(request)


# allow a generation of client responses into a pdf file 
@login_required(login_url = '/signin/')
def questionnaire_responses(request, client_id ):
    client = User.objects.get(id = client_id)
    # check if user can access coach questionnaire and if questionnaire is complete for display 
    if request.user.is_coach:
        
        # neccessary queries
        client_sales_responses = Question.objects.filter(responder = client , category = "sales")
        client_people_responses = Question.objects.filter(responder = client , category = "people")
        client_accounting_responses = Question.objects.filter(responder = client , category = "accounting")
        client_business_responses = Question.objects.filter(responder = client , category = "business")
        client_legal_responses = Question.objects.filter(responder = client , category = "legal")
        client_tech_responses = Question.objects.filter(responder = client , category = "tech")
        
        # buffer for 
        buff = io.BytesIO()
        text_container = canvas.Canvas(buff, pagesize = letter , bottomup = 0)
        text_obj = text_container.beginText()
        text_obj.setTextOrigin(inch,inch)
        text_obj.setFont("Helvetica" , 14)
        
        # list to hold all content for pdf display 
        pdf_content = []
        
        # populate the pdf content with all quesitonnaire categories and responses 
        for question in client_sales_responses:
            pdf_content.append("Sales Response")
            pdf_content.append(question)
            pdf_content.append(question.question_answer)
            pdf_content.append("------------------------------------------------------")
            
        for question in client_people_responses:
            pdf_content.append("People Response")
            pdf_content.append(question)
            pdf_content.append(question.question_answer)
            pdf_content.append("------------------------------------------------------")
        
        for question in client_accounting_responses:
            pdf_content.append("Accounting Response")
            pdf_content.append(question)
            pdf_content.append(question.question_answer)
            pdf_content.append("------------------------------------------------------")
        
        for question in client_business_responses:
            pdf_content.append("Business Response")
            pdf_content.append(question)
            pdf_content.append(question.question_answer)
            pdf_content.append("------------------------------------------------------")
        
        for question in client_legal_responses:
            pdf_content.append("Legal Response")
            pdf_content.append(question)
            pdf_content.append(question.question_answer)
            pdf_content.append("------------------------------------------------------")
        
        for question in client_tech_responses:
            pdf_content.append("Technology Response")
            pdf_content.append(question)
            pdf_content.append(question.question_answer)
            pdf_content.append("------------------------------------------------------")
        
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
    if request.user.is_newclient and (not (request.user.categories_answered == 6)):
        question = Question.objects.all().first()
        question_id = question.id 
        users = User.objects.all()
        variables = {
            "question":question,
            "users":users,
            "id": question_id
        }
        return render(request,'questionnaire/main.html',variables)
    else:
        return home(request)

def answer_question(request, category):
    client = request.user
    if client.is_client:
        # query category of questions 
        questions = Question.objects.filter(category=category)

        # populate questionnaire 
        for index in range(questions.count()):
            Questionnaire.objects.get_or_create(
                provided_for = client, 
                question = questions[index],
            )
        
        # query questionnaire for user 
        questions_to_answer = Questionnaire.objects.filter( provided_for = client , answered = False)

        # query question to respond to 
        question = questions_to_answer.first()

        # provide form for answering 
        form = AnswerForm(request.POST or None)

        # if no quesitons to answer 
        if not question:
            # check the category that was full answered 
            if category == 'sales':
                client.completed_P1 = True
                client.save()
            if category == 'people':
                client.completed_P2 = True
                client.save()
            if category == 'accounting':
                client.completed_P3 = True
                client.save()
            if category == 'business':
                client.completed_P4 = True
                client.save()
            if category == 'legal':
                client.completed_P5 = True
                client.save()
            if category == 'tech':
                client.completed_P6 = True
                client.save()
            return redirect("questionnaire:main")

        variables = {
            "form":form,
            "question":question.question
        }

        # if there is a question to answer 
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
        # inial render
        return render(request , f'questionnaire/{category}.html' , variables )
    else:
        return home(request)

    
