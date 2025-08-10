import os
import random
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .utils.parse_resume import extract_text_from_resume
from .utils.domain_detector import detect_domain
from .utils.mcq_bank import MCQ_DATA


def upload_resume(request):
    context = {}

    if request.method == "POST" and request.FILES.get("resume"):
        resume_file = request.FILES["resume"]

        # Save temporarily
        file_path = os.path.join("tmp_" + resume_file.name)
        with open(file_path, "wb") as f:
            for chunk in resume_file.chunks():
                f.write(chunk)

        try:
            resume_text = extract_text_from_resume(file_path)
            detected_domain = detect_domain(resume_text)
        except Exception as e:
            if request.headers.get("Accept") == "application/json":
                return JsonResponse({"error": str(e)}, status=400)
            context["error"] = str(e)
            return render(request, "upload_resume.html", context)

        # If API request → return JSON
        if request.headers.get("Accept") == "application/json":
            return JsonResponse({
                "resume_text": resume_text,
                "detected_domain": detected_domain
            })

        # Show detection result page with a Start Quiz button
        context = {
            "resume_text": resume_text,
            "detected_domain": detected_domain or "Unknown"
        }
        return render(request, "resume_result.html", context)

    # GET request → show upload form
    return render(request, "upload_resume.html", context)


def start_quiz(request, domain):
    questions = MCQ_DATA.get(domain.lower(), [])
    if not questions:
        return render(request, "quiz_not_found.html", {"domain": domain})

    selected_questions = random.sample(questions, min(10, len(questions)))
    request.session["quiz_questions"] = selected_questions
    request.session["domain"] = domain

    return render(request, "quiz.html", {
        "questions": selected_questions,
        "time_limit": 300  # 5 minutes
    })


def submit_quiz(request):
    if request.method != "POST":
        return redirect("upload_resume")

    questions = request.session.get("quiz_questions", [])
    score = 0
    for i, q in enumerate(questions):
        selected_answer = request.POST.get(f"q{i}")
        if selected_answer == q["answer"]:
            score += 1

    total = len(questions)
    pass_mark = max(1, round(total * 0.6))  # 60% required to pass
    result = "Pass" if score >= pass_mark else "Fail"

    return render(request, "quiz_result.html", {
        "score": score,
        "total": total,
        "result": result
    })
