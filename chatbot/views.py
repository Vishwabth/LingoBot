from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .nlp import analyze_text


def home_page(request):
    return render(request, "chatbot/home.html")


def chat_page(request):
    return render(request, "chatbot/chat.html")


@csrf_exempt
def get_response(request):
    """
    Endpoint that receives user input and returns processed analysis
    for grammar, spellcheck, sentiment, emotions, and feedback.
    """
    user_input = request.GET.get("message", "").strip()

    if not user_input:
        return JsonResponse({"reply": "⚠️ Please type something to analyze."})

    try:
        results = analyze_text(user_input)

        # ----------------------------
        # Construct Markdown-friendly bot reply
        # ----------------------------
        reply_parts = []

        # Before → After diff
        reply_parts.append("🔍 **Changes (Diff):**")
        reply_parts.append(results["diff"])

        # Grammar correction
        reply_parts.append(f"\n📝 **Corrected:** {results['grammar']}")

        # Spellcheck
        reply_parts.append(f"🔤 **Spellcheck:** {results['spellcheck']}")

        # Sentiment
        sent = results['sentiment']
        reply_parts.append(f"🙂 **Sentiment:** {sent['label']} (score: {round(sent['score'], 2)})")

        # Emotions
        emotions = ", ".join([f"{k} ({v})" for k, v in results['emotions'].items()])
        reply_parts.append(f"🎭 **Emotions:** {emotions}")

        # Feedback (grouped by severity)
        if results.get("feedback"):
            reply_parts.append("\n📌 **Feedback:**")
            for f in results["feedback"]:
                if f.startswith("❗"):
                    reply_parts.append(f"   {f}")  # Critical
                elif f.startswith("⚠️"):
                    reply_parts.append(f"   {f}")  # Warning
                else:
                    reply_parts.append(f"   {f}")  # Info

        # Final Markdown-ready response
        reply_text = "\n".join(reply_parts)

        return JsonResponse({"reply": reply_text})

    except Exception as e:
        return JsonResponse({"reply": f"⚠️ Error: {str(e)}"})
