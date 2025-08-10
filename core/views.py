from django.shortcuts import render
from django.http import JsonResponse
from .utils.parse_resume import extract_text_from_resume
from .utils.domain_detector import detect_domain
import os

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

        # If browser → show results in template
        context = {
            "resume_text": resume_text,
            "detected_domain": detected_domain
        }
        return render(request, "upload_resume.html", context)

    # GET request → show upload form
    return render(request, "upload_resume.html", context)
