# Add this to your existing blog/views.py file

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import markdown2

@login_required
@require_http_methods(["POST"])
def markdown_preview(request):
    """
    AJAX endpoint for markdown preview functionality.
    Converts markdown content to HTML and returns it as JSON.
    """
    try:
        data = json.loads(request.body)
        content = data.get('content', '')
        
        # Convert markdown to HTML
        html = markdown2.markdown(
            content,
            extras=[
                'fenced-code-blocks',
                'tables',
                'code-friendly',
                'strike',
                'task_list',
                'break-on-newline'
            ]
        )
        
        return JsonResponse({
            'html': html,
            'success': True
        })
    
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'success': False
        }, status=400)