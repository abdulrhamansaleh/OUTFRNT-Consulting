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
from reportlab.lib.pagesizes import * 

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
        text_container = canvas.Canvas(buff, pagesize = LEDGER , bottomup = 0)
        
        sales_page = text_container.beginText()
        sales_page.setTextOrigin(inch,inch)
        sales_page.setFont("Helvetica" , 15)
        
        peoples_page = text_container.beginText()
        peoples_page.setTextOrigin(inch,inch)
        peoples_page.setFont("Helvetica" , 15)
        
        accounting_page = text_container.beginText()
        accounting_page.setTextOrigin(inch,inch)
        accounting_page.setFont("Helvetica" , 15)
        
        business_page = text_container.beginText()
        business_page.setTextOrigin(inch,inch)
        business_page.setFont("Helvetica" , 15)
        
        legal_page = text_container.beginText()
        legal_page.setTextOrigin(inch,inch)
        legal_page.setFont("Helvetica" , 15)
        
        tech_page = text_container.beginText()
        tech_page.setTextOrigin(inch,inch)
        tech_page.setFont("Helvetica" , 15)
        
        
        # query client responses 
        client_responses = Response.objects.filter(responder = client)
        # list to hold all content for pdf display 
        pdf_content = []
        
        # sales 
        sales_page.textLine("Sales and Marketing Responses")
        sales_page.textLine("====================================================")
        for index in range (client_responses.count()):
            current = client_responses[index]
            question = current.question
            answer = current.answer
            if question.category == "sales":
                sales_page.textLine(f'Q){question}')
                sales_page.textLine(f'ans:{answer}')
        text_container.drawText(sales_page)
        text_container.showPage()
        
        # people 
        peoples_page.textLine("People and Culture")
        peoples_page.textLine("====================================================")
        for index in range (client_responses.count()):
            current = client_responses[index]
            question = current.question
            answer = current.answer
            if question.category == "sales":
                peoples_page.textLine(f'Q){question}')
                peoples_page.textLine(f'ans:{answer}')
        text_container.drawText(peoples_page)
        text_container.showPage()

        #accounting 
        accounting_page.textLine("Accounting and Finance")
        accounting_page.textLine("====================================================")
        for index in range (client_responses.count()):
            current = client_responses[index]
            question = current.question
            answer = current.answer
            if question.category == "accounting":
                accounting_page.textLine(f'Q){question}')
                accounting_page.textLine(f'ans:{answer}')
        text_container.drawText(accounting_page)
        text_container.showPage()
        
        #business 
        business_page.textLine("Business and Operations")
        business_page.textLine("====================================================")
        for index in range (client_responses.count()):
            current = client_responses[index]
            question = current.question
            answer = current.answer
            if question.category == "business":
                business_page.textLine(f'Q){question}')
                business_page.textLine(f'ans:{answer}')
        text_container.drawText(business_page)
        text_container.showPage()
        
        #legal 
        legal_page.textLine("Legal and Governance")
        legal_page.textLine("====================================================")
        for index in range (client_responses.count()):
            current = client_responses[index]
            question = current.question
            answer = current.answer
            if question.category == "legal":
                legal_page.textLine(f'Q){question}')
                legal_page.textLine(f'ans:{answer}')
        text_container.drawText(legal_page)
        text_container.showPage()
        
        #tech 
        tech_page.textLine("Technology")
        tech_page.textLine("====================================================")
        for index in range (client_responses.count()):
            current = client_responses[index]
            question = current.question
            answer = current.answer
            if question.category == "tech":
                tech_page.textLine(f'Q){question}')
                tech_page.textLine(f'ans:{answer}')
        text_container.drawText(tech_page)
        text_container.showPage()
                
    
        # convert all forms into a uniform data type for ease of display 
        for content in pdf_content: 
            content = str(content)
            text_obj.textLine(content)
        
        # populate the pdf container 
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
        print(questions)
        for index in range(questions.count()):
            Questionnaire.objects.get_or_create(
                provided_for = client, 
                question = questions[index],
                category_of_questionnaire = category
            )
        questions_to_answer = Questionnaire.objects.filter( provided_for = client , answered = False , category_of_questionnaire = category)
        question = questions_to_answer.first()
        form = AnswerForm(request.POST or None)
        if not question:
            if category == 'sales':
                client.completed_P1 = True
                client.save()
            elif category == 'people':
                client.completed_P2 = True
                client.save()
            elif category == 'accounting':
                client.completed_P3 = True
                client.save()
            elif category == 'business':
                client.completed_P4 = True
                client.save()
            elif category == 'legal':
                client.completed_P5 = True
                client.save()
            elif category == 'tech':
                client.completed_P6 = True
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

    
