from django.shortcuts import render,redirect
from questionnaire.models import Question,Response
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
        questions = Question.objects.filter(answered = False)
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

@login_required(login_url = '/signin/')
def sales_and_management(request, question_id):
    # check if user is allowed a quesitonnaire and if they have completed the category
    if request.user.is_newclient and (not request.user.completed_P1):
        # category variables
        current_category = "sales"
        next_category = "people"
        
        current_questions = Question.objects.filter(category = current_category, responder = None , question_answer = None)
        
        question_obj = Question.objects.get(id = question_id)
        
        form = AnswerForm(request.POST or None) 
                
        if request.POST and form.is_valid():
            form_responder = request.user
            form_answer = form.cleaned_data['answer']
            answer = Response.objects.create(
                responder = form_responder,
                answer = form_answer
            )
            Question.objects.get_or_create(
                    category = current_category,
                    question_text = question_obj.question_text,
                    responder = form_responder,
                    question_answer = answer,
                    answered = True
            ) 
            # check if all category questions have been answered 
            for question in current_questions :
                if len(Question.objects.filter(responder = form_responder, category = current_category, answered = True,)) == (len(current_questions)):
                    # set the new question set to the next category of questions 
                    next_question_obj = Question.objects.filter(category = next_category , answered = False).first()
                    variables = {
                        "question":next_question_obj,
                        "form":form
                    }
                    # set category to complete and answered 
                    form_responder.completed_P1 = True
                    form_responder.categories_answered += 1
                    form_responder.save()
                    # render the new category of questions 
                    return render (request,"questionnaire/people.html", variables)
                # if there remains questions increment to the next question in the same category 
                else:
                    question_obj = Question.objects.get(id = question_id + 1 , category = current_category , answered = False)         
                    variables = {
                        "question":question_obj,
                        "form":form, 
                    } 
                    # rerender with question
                    return render(request,"questionnaire/sales.html", variables)
        # render the original view 
        return render(request,"questionnaire/sales.html", { "form":form, "question":question_obj } )
    else:
        return home(request)

@login_required(login_url = '/signin/')
def people_and_culture(request,question_id):
    # check if user is allowed a quesitonnaire and if they have completed the category
    if request.user.is_newclient and (not request.user.completed_P2):
        # category variables
        current_category = "people"
        next_category = "accounting"
        
        current_questions = Question.objects.filter(category = current_category, responder = None , question_answer = None)
        
        question_obj = Question.objects.get(id = question_id)
        
        form = AnswerForm(request.POST or None) 
        
        # store client answer as a new question object         
        if request.POST and form.is_valid():
            form_responder = request.user
            form_answer = form.cleaned_data['answer']
            answer = Response.objects.create(
                responder = form_responder,
                answer = form_answer
            )
            Question.objects.get_or_create(
                    category = current_category,
                    question_text = question_obj.question_text,
                    responder = form_responder,
                    question_answer = answer,
                    answered = True
            ) 
            
            # check if all category questions have been answered 
            for question in current_questions :
                if len(Question.objects.filter(responder = form_responder, category = current_category, answered = True,)) == (len(current_questions)):
                    # set the new question set to the next category of questions 
                    next_question_obj = Question.objects.filter(category = next_category , answered = False).first()
                    variables = {
                        "question":next_question_obj,
                        "form":form
                    }
                    # set category to complete and answered 
                    form_responder.completed_P2 = True
                    form_responder.categories_answered += 1
                    form_responder.save()
                    # render the new category of questions 
                    return render (request,"questionnaire/accounting.html", variables)
                # if there remains questions increment to the next question in the same category 
                else:
                    question_obj = Question.objects.get(id = question_id + 1 , category = current_category , answered = False)         
                    variables = {
                        "question":question_obj,
                        "form":form, 
                    } 
                    # rerender with current category template
                    return render(request,"questionnaire/people.html", variables)
        # initial render of current category 
        return render(request,"questionnaire/people.html", { "form":form, "question":question_obj } )
    else:
        return home(request)

@login_required(login_url = '/signin/')
def accounting_and_finance(request,question_id):
    # check if user is allowed a quesitonnaire and if they have completed the category
    if request.user.is_newclient and (not request.user.completed_P3):
        # category variables
        current_category = "accounting"
        next_category = "business"
        
        current_questions = Question.objects.filter(category = current_category, responder = None , question_answer = None)
        
        question_obj = Question.objects.get(id = question_id)
        
        form = AnswerForm(request.POST or None) 
        
        # store client answer as a new question object         
        if request.POST and form.is_valid():
            form_responder = request.user
            form_answer = form.cleaned_data['answer']
            answer = Response.objects.create(
                responder = form_responder,
                answer = form_answer
            )
            Question.objects.get_or_create(
                    category = current_category,
                    question_text = question_obj.question_text,
                    responder = form_responder,
                    question_answer = answer,
                    answered = True
            ) 
            
            # check if all category questions have been answered 
            for question in current_questions :
                if len(Question.objects.filter(responder = form_responder, category = current_category, answered = True,)) == (len(current_questions)):
                    # set the new question set to the next category of questions 
                    next_question_obj = Question.objects.filter(category = next_category , answered = False).first()
                    variables = {
                        "question":next_question_obj,
                        "form":form
                    }
                    # set category to complete and answered 
                    form_responder.completed_P3 = True
                    form_responder.categories_answered += 1
                    form_responder.save()
                    # render the new category of questions 
                    return render (request,"questionnaire/business.html", variables)
                # if there remains questions increment to the next question in the same category 
                else:
                    question_obj = Question.objects.get(id = question_id + 1 , category = current_category , answered = False)         
                    variables = {
                        "question":question_obj,
                        "form":form, 
                    } 
                    # rerender with current category template
                    return render(request,"questionnaire/accounting.html", variables)
        # initial render of current category 
        return render(request,"questionnaire/accounting.html", { "form":form, "question":question_obj } )
    else:
        return home(request)
                
@login_required(login_url = '/signin/')
def buisness_and_operations(request,question_id):
    # check if user is allowed a quesitonnaire and if they have completed the category
    if request.user.is_newclient and (not request.user.completed_P4):
        # category variables
        current_category = "business"
        next_category = "legal"
        
        current_questions = Question.objects.filter(category = current_category, responder = None , question_answer = None)
        
        question_obj = Question.objects.get(id = question_id)
        
        form = AnswerForm(request.POST or None) 
        
        # store client answer as a new question object         
        if request.POST and form.is_valid():
            form_responder = request.user
            form_answer = form.cleaned_data['answer']
            answer = Response.objects.create(
                responder = form_responder,
                answer = form_answer
            )
            Question.objects.get_or_create(
                    category = current_category,
                    question_text = question_obj.question_text,
                    responder = form_responder,
                    question_answer = answer,
                    answered = True
            ) 
            
            # check if all category questions have been answered 
            for question in current_questions :
                if len(Question.objects.filter(responder = form_responder, category = current_category, answered = True,)) == (len(current_questions)):
                    # set the new question set to the next category of questions 
                    next_question_obj = Question.objects.filter(category = next_category , answered = False).first()
                    variables = {
                        "question":next_question_obj,
                        "form":form
                    }
                    # set category to complete and answered 
                    form_responder.completed_P4 = True
                    form_responder.categories_answered += 1
                    form_responder.save()
                    # render the new category of questions 
                    return render (request,"questionnaire/legal.html", variables)
                # if there remains questions increment to the next question in the same category 
                else:
                    question_obj = Question.objects.get(id = question_id + 1 , category = current_category , answered = False)         
                    variables = {
                        "question":question_obj,
                        "form":form, 
                    } 
                    # rerender with current category template
                    return render(request,"questionnaire/business.html", variables)
        # initial render of current category 
        return render(request,"questionnaire/business.html", { "form":form, "question":question_obj } )
    else:
        return home(request)
    
@login_required(login_url = '/signin/')
def legal_and_governance(request,question_id):
    # check if user is allowed a quesitonnaire and if they have completed the category
    if request.user.is_newclient and (not request.user.completed_P5):
        # category variables
        current_category = "legal"
        next_category = "tech"
        
        current_questions = Question.objects.filter(category = current_category, responder = None , question_answer = None)
        
        question_obj = Question.objects.get(id = question_id)
        
        form = AnswerForm(request.POST or None) 
        
        # store client answer as a new question object         
        if request.POST and form.is_valid():
            form_responder = request.user
            form_answer = form.cleaned_data['answer']
            answer = Response.objects.create(
                responder = form_responder,
                answer = form_answer
            )
            Question.objects.get_or_create(
                    category = current_category,
                    question_text = question_obj.question_text,
                    responder = form_responder,
                    question_answer = answer,
                    answered = True
            ) 
            
            # check if all category questions have been answered 
            for question in current_questions :
                if len(Question.objects.filter(responder = form_responder, category = current_category, answered = True,)) == (len(current_questions)):
                    # set the new question set to the next category of questions 
                    next_question_obj = Question.objects.filter(category = next_category , answered = False).first()
                    variables = {
                        "question":next_question_obj,
                        "form":form
                    }
                    # set category to complete and answered 
                    form_responder.completed_P5 = True
                    form_responder.categories_answered += 1
                    form_responder.save()
                    # render the new category of questions 
                    return render (request,"questionnaire/technology.html", variables)
                # if there remains questions increment to the next question in the same category 
                else:
                    question_obj = Question.objects.get(id = question_id + 1 , category = current_category , answered = False)         
                    variables = {
                        "question":question_obj,
                        "form":form, 
                    } 
                    # rerender with current category template
                    return render(request,"questionnaire/legal.html", variables)
        # initial render of current category 
        return render(request,"questionnaire/legal.html", { "form":form, "question":question_obj } )
    else:
        return home(request)

@login_required(login_url = '/signin/')
def technology(request,question_id):
    # check if user is allowed a quesitonnaire and if they have completed the category
    if request.user.is_newclient and (not request.user.completed_P6):
        current_category = "tech"
        
        current_questions = Question.objects.filter(category = current_category, responder = None , question_answer = None)
        num_of_questions = len(current_questions)
        question_obj = Question.objects.get(id = question_id)
    
        form = AnswerForm(request.POST or None)
        
        if request.POST and form.is_valid():
            form_responder = request.user
            form_answer = form.cleaned_data['answer']
            answer = Response.objects.create(
                responder = form_responder,
                answer = form_answer
            )
            Question.objects.get_or_create(
                    category = current_category,
                    question_text = question_obj.question_text,
                    responder = form_responder,
                    question_answer = answer,
                    answered = True
            ) 
            for queston in current_questions :
                if len(Question.objects.filter(responder = form_responder, category = current_category, answered = True,)) == (len(current_questions)) :
                    # set category to complete and answered 
                    form_responder.completed_P6 = True
                    form_responder.categories_answered += 1
                    form_responder.save()
                    return render (request,"questionnaire/finished.html")
                else:
                    question_obj = Question.objects.get(id = question_id + 1)         
                    variables = {
                        "form":form,
                        "question":question_obj,      
                    } 
                    return render(request,"questionnaire/technology.html", variables)
        return render(request,"questionnaire/technology.html", { "form":form, "question":question_obj } )
    else:
        return home(request)

    
