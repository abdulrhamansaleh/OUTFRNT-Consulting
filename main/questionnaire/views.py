from django.shortcuts import render

# Create your views here.
def sales_and_management(request):
    sales_question = {
        "What is your key value proposition? (what problem are you solving, and what do you do better than others to solve this problem?)",
        "What is your brand and why?",
        "Who are your customers?",
        "How big is your market?",
        "How do you engage with customers/prospects?",
        "How do you position your brand ? (what is your competitive advantage behind your brand, is it driven by price, product/service characteristics, quality/luxury, use/application?)",
        "Who are your competitors?",
        "Walk us through your approach to promotion, advertising & communications.",
        "Tell us about your creative process.",
        "What market research has been completed, and what market research needs to happen?",
    }
    variables = {
        "Sales": sales_question
    }
    
    return render(request,'questionnaire/sales_form.html',variables)