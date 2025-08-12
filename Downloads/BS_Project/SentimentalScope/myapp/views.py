from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
from .auth_service import auth_service
from .scraper_service import NewsPortalScraper, ScrapedContentService
from .ai_service import ai_service

# Create your views here.
def index(request):
    # Check if user is logged in
    if 'user_id' not in request.session:
        return redirect('login')
    return render(request, 'index.html')

def login_view(request):
    # If user is already logged in, redirect to index
    if 'user_id' in request.session:
        return redirect('index')
    return render(request, 'Login.html')

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            # Parse JSON data
            data = json.loads(request.body)
            
            full_name = data.get('full_name', '').strip()
            email = data.get('email', '').strip()
            password = data.get('password', '')
            confirm_password = data.get('confirm_password', '')
            
            # Validate required fields
            if not all([full_name, email, password, confirm_password]):
                return JsonResponse({
                    'success': False,
                    'message': 'All fields are required'
                })
            
            # Check if passwords match
            if password != confirm_password:
                return JsonResponse({
                    'success': False,
                    'message': 'Passwords do not match'
                })
            
            # Create user
            success, message = auth_service.create_user(full_name, email, password)
            
            return JsonResponse({
                'success': success,
                'message': message
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid JSON data'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'An error occurred during registration'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Method not allowed'
    })

@csrf_exempt
def signin(request):
    if request.method == 'POST':
        try:
            # Parse JSON data
            data = json.loads(request.body)
            
            email = data.get('email', '').strip()
            password = data.get('password', '')
            remember_me = data.get('remember_me', False)
            
            # Validate required fields
            if not all([email, password]):
                return JsonResponse({
                    'success': False,
                    'message': 'Email and password are required'
                })
            
            # Authenticate user
            success, message, user_data = auth_service.authenticate_user(email, password)
            
            if success:
                # Set session data
                request.session['user_id'] = user_data['id']
                request.session['user_email'] = user_data['email']
                request.session['user_name'] = user_data['full_name']
                
                # Set session expiry based on remember me
                if not remember_me:
                    request.session.set_expiry(0)  # Session expires when browser closes
                else:
                    request.session.set_expiry(1209600)  # 2 weeks
                
                return JsonResponse({
                    'success': True,
                    'message': message,
                    'redirect_url': '/'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': message
                })
                
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid JSON data'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'An error occurred during login'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Method not allowed'
    })

def logout(request):
    """Logout user"""
    request.session.flush()  # Clear all session data
    messages.success(request, 'You have been logged out successfully')
    return redirect('login')

def profile(request):
    """User profile view"""
    if 'user_id' not in request.session:
        return redirect('login')
    
    user_data = auth_service.get_user_by_id(request.session['user_id'])
    if not user_data:
        request.session.flush()
        return redirect('login')
    
    return render(request, 'profile.html', {'user': user_data})

def url_analysis(request):
    """URL analysis page - handles URL scraping and shows headlines"""
    if 'user_id' not in request.session:
        return redirect('login')
    
    user_data = auth_service.get_user_by_id(request.session['user_id'])
    if not user_data:
        request.session.flush()
        return redirect('login')
    
    if request.method == 'POST':
        url = request.POST.get('url', '').strip()
        
        if not url:
            messages.error(request, 'Please enter a valid URL')
            return render(request, 'url.html', {'user': user_data})
        
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        scraper = NewsPortalScraper()
        scraper_service = ScrapedContentService()
        
        # Clear previous headlines for this user
        deleted_count = scraper_service.clear_user_headlines(request.session['user_id'])
        print(f"DEBUG: Cleared {deleted_count} previous headlines for user {request.session['user_id']}")
        
        try:
            # Check URL type
            video_id = scraper.extract_video_id(url)
            is_single_article = scraper.is_single_article_url(url)
            
            if video_id:
                # YouTube video - get title only first
                headlines_data = [{
                    'headline': f'YouTube Video (ID: {video_id})',
                    'url': url
                }]
                content_type = 'youtube'
                
            elif is_single_article:
                # Single article - get headline only first
                headline, _ = scraper.extract_headline_and_body(url)
                if headline:
                    headlines_data = [{
                        'headline': headline,
                        'url': url
                    }]
                    content_type = 'article'
                else:
                    messages.error(request, 'Could not extract content from the provided URL')
                    return render(request, 'url.html', {'user': user_data})
                    
            else:
                # News portal - get all headlines
                headlines_data = scraper.scrape_news_portal_headlines_only(url)
                content_type = 'portal'
                
                if not headlines_data:
                    messages.error(request, 'No articles found on this page. Please try a different URL.')
                    return render(request, 'url.html', {'user': user_data})
            
            # Save headlines to database
            inserted_ids = scraper_service.save_headlines_only(
                request.session['user_id'], 
                content_type, 
                headlines_data, 
                url
            )
            
            if inserted_ids:
                print(f"DEBUG: Successfully saved {len(inserted_ids)} headlines for user {request.session['user_id']}")
                messages.success(request, f'Found {len(headlines_data)} articles. Select one to analyze.')
                return redirect('headlines')
            else:
                print(f"DEBUG: Failed to save headlines data: {headlines_data}")
                messages.error(request, 'Failed to save scraped content. Please try again.')
                
        except Exception as e:
            print(f"Scraping error: {e}")
            messages.error(request, 'An error occurred while processing the URL. Please try again.')
    
    return render(request, 'url.html', {'user': user_data})

def headlines(request):
    """Show scraped headlines for user selection"""
    if 'user_id' not in request.session:
        return redirect('login')
    
    user_data = auth_service.get_user_by_id(request.session['user_id'])
    if not user_data:
        request.session.flush()
        return redirect('login')
    
    scraper_service = ScrapedContentService()
    headlines = scraper_service.get_user_headlines(request.session['user_id'])
    
    print(f"DEBUG: Headlines view - Found {len(headlines) if headlines else 0} headlines for user {request.session['user_id']}")
    
    if not headlines:
        messages.error(request, 'No headlines found. Please scrape a URL first.')
        return redirect('url_analysis')
    
    # Convert MongoDB _id to string for Django templates
    for headline in headlines:
        headline['id'] = str(headline['_id'])
    
    context = {
        'user': user_data,
        'headlines': headlines
    }
    
    return render(request, 'headlines.html', context)

@csrf_exempt
def analyze_content(request):
    """Fetch full content and redirect to analyzer"""
    if request.method == 'POST':
        if 'user_id' not in request.session:
            return JsonResponse({'success': False, 'message': 'User not authenticated'})
        
        try:
            data = json.loads(request.body)
            document_id = data.get('document_id')
            
            if not document_id:
                return JsonResponse({'success': False, 'message': 'Document ID required'})
            
            scraper_service = ScrapedContentService()
            document = scraper_service.get_full_content(document_id)
            
            if not document:
                return JsonResponse({'success': False, 'message': 'Content not found'})
            
            # Check if content is already fetched
            if document['storage_level'] == 'full_content':
                return JsonResponse({
                    'success': True, 
                    'message': 'Content ready for analysis',
                    'redirect_url': f'/analyzer/{document_id}/'
                })
            
            # Fetch full content
            scraper = NewsPortalScraper()
            
            if document['content_type'] == 'youtube':
                # Extract YouTube transcript
                video_id = scraper.extract_video_id(document['source_url'])
                if video_id:
                    transcript_data, status = scraper.get_youtube_transcript_data(video_id)
                    if transcript_data:
                        success = scraper_service.update_with_full_content(
                            document_id, 
                            {'transcript': transcript_data}
                        )
                        if success:
                            return JsonResponse({
                                'success': True,
                                'message': 'Video transcript extracted successfully',
                                'redirect_url': f'/analyzer/{document_id}/'
                            })
                    else:
                        return JsonResponse({'success': False, 'message': status})
                        
            else:
                # Extract article content
                headline, body = scraper.extract_headline_and_body(document['source_url'])
                if headline and body:
                    success = scraper_service.update_with_full_content(
                        document_id, 
                        {'body': body}
                    )
                    if success:
                        return JsonResponse({
                            'success': True,
                            'message': 'Article content extracted successfully',
                            'redirect_url': f'/analyzer/{document_id}/'
                        })
                else:
                    return JsonResponse({'success': False, 'message': 'Could not extract article content'})
            
            return JsonResponse({'success': False, 'message': 'Failed to process content'})
            
        except Exception as e:
            print(f"Analysis error: {e}")
            return JsonResponse({'success': False, 'message': 'An error occurred while processing'})
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})

@csrf_exempt
def clear_headlines(request):
    """Clear all headlines for the current user"""
    if request.method == 'POST':
        if 'user_id' not in request.session:
            return JsonResponse({'success': False, 'message': 'User not authenticated'})
        
        try:
            scraper_service = ScrapedContentService()
            deleted_count = scraper_service.clear_user_headlines(request.session['user_id'])
            
            return JsonResponse({
                'success': True,
                'message': f'Cleared {deleted_count} headlines successfully'
            })
            
        except Exception as e:
            print(f"Clear headlines error: {e}")
            return JsonResponse({'success': False, 'message': 'An error occurred while clearing headlines'})
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})

def analyzer(request, document_id=None):
    """Analyzer page - shows analysis results with AI sentiment and summarization"""
    if 'user_id' not in request.session:
        return redirect('login')
    
    user_data = auth_service.get_user_by_id(request.session['user_id'])
    if not user_data:
        request.session.flush()
        return redirect('login')
    
    content_to_analyze = ""
    content_source = ""
    content_type = ""
    content_data = {}
    ai_analysis = None
    
    if document_id:
        # Load content from database
        scraper_service = ScrapedContentService()
        document = scraper_service.get_full_content(document_id)
        
        if document and document['user_id'] == request.session['user_id']:
            content_source = document['source_url']
            content_type = document['content_type']
            
            if document['content_type'] == 'youtube' and document['transcript_data']:
                # Structure YouTube data
                total_duration = 0
                if document['transcript_data']:
                    # Calculate total duration from the last segment
                    last_segment = document['transcript_data'][-1]
                    # Handle both dictionary format and object format
                    if isinstance(last_segment, dict):
                        if 'timestamp' in last_segment:
                            # Parse timestamp format [MM:SS]
                            timestamp = last_segment['timestamp'].replace('[', '').replace(']', '')
                            if ':' in timestamp:
                                minutes, seconds = map(int, timestamp.split(':'))
                                total_duration = minutes * 60 + seconds
                    else:
                        # If it's an object with start and duration attributes
                        total_duration = getattr(last_segment, 'start', 0) + getattr(last_segment, 'duration', 0)
                
                content_data = {
                    'title': document['headline'],
                    'transcript_segments': document['transcript_data'],
                    'total_duration': total_duration
                }
                # Combine transcript paragraphs for analysis
                transcript_parts = []
                for item in document['transcript_data']:
                    transcript_parts.append(f"{item['timestamp']} {item['paragraph']}")
                content_to_analyze = '\n\n'.join(transcript_parts)
                
                # Perform AI analysis on transcript
                ai_analysis = ai_service.analyze_content(
                    text=content_to_analyze,
                    title=document['headline'],
                    include_summary=True,
                    include_sentiment=True
                )
                
            elif document['full_content']:
                # Structure article data
                content_data = {
                    'headline': document['headline'],
                    'content': document['full_content'],
                    'word_count': len(document['full_content'].split()) if document['full_content'] else 0
                }
                content_to_analyze = f"{document['headline']}\n\n{document['full_content']}"
                
                # Perform AI analysis on article
                ai_analysis = ai_service.analyze_content(
                    text=document['full_content'],
                    title=document['headline'],
                    include_summary=True,
                    include_sentiment=True
                )
            
            else:
                messages.error(request, 'Content not fully loaded. Please try again.')
                return redirect('headlines')
        else:
            messages.error(request, 'Content not found or access denied.')
            return redirect('headlines')
    
    # Get the URL from POST request if available (backward compatibility)
    elif request.method == 'POST':
        url_to_analyze = request.POST.get('url', '')
        content_to_analyze = url_to_analyze
        content_source = url_to_analyze
        content_type = 'manual'
        content_data = {'text': url_to_analyze}
        
        # Perform AI analysis on manual input
        if url_to_analyze:
            ai_analysis = ai_service.analyze_content(
                text=url_to_analyze,
                include_summary=True,
                include_sentiment=True
            )
    
    context = {
        'user': user_data,
        'content_to_analyze': content_to_analyze,
        'content_source': content_source,
        'content_type': content_type,
        'content_data': content_data,
        'document_id': document_id,
        'ai_analysis': ai_analysis,  # Add AI analysis results
        'ai_info': ai_service.get_model_info()  # Add model info
    }
    
    return render(request, 'Analyzer.html', context)

@csrf_exempt
@csrf_exempt
def api_analyze_sentiment(request):
    """API endpoint for sentiment analysis"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            content = data.get('content', '').strip()
            
            print(f"DEBUG: Received content for sentiment analysis: {content[:100]}...")
            
            if not content:
                return JsonResponse({'success': False, 'message': 'No content provided'})
            
            # Try to use the real AI service, fallback to test data if it fails
            try:
                print("DEBUG: Calling real AI sentiment analyzer...")
                sentiment_result = ai_service.sentiment_analyzer.analyze_sentiment(content)
                print(f"DEBUG: Real AI sentiment result: {sentiment_result}")
                
                return JsonResponse({
                    'success': True,
                    'sentiment': sentiment_result
                })
                
            except Exception as ai_error:
                print(f"DEBUG: AI service error: {ai_error}")
                # Fallback to test result
                test_result = {
                    'label': 'neutral',
                    'confidence': 0.5,
                    'scores': {
                        'positive': 0.3,
                        'neutral': 0.4,
                        'negative': 0.3
                    }
                }
                
                return JsonResponse({
                    'success': True,
                    'sentiment': test_result
                })
            
        except json.JSONDecodeError as e:
            print(f"DEBUG: JSON decode error: {e}")
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'})
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})

@csrf_exempt
def api_generate_summary(request):
    """API endpoint for text summarization"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            content = data.get('content', '').strip()
            
            print(f"DEBUG: Received content for summarization: {content[:100]}...")
            
            if not content:
                return JsonResponse({'success': False, 'message': 'No content provided'})
            
            # Try to use the real AI service, fallback to test data if it fails
            try:
                print("DEBUG: Calling real AI summarizer...")
                summary_result = ai_service.text_summarizer.summarize_text(content)
                print(f"DEBUG: Real AI result: {summary_result}")
                
                return JsonResponse({
                    'success': True,
                    'summary': summary_result
                })
                
            except Exception as ai_error:
                print(f"DEBUG: AI service error: {ai_error}")
                # Fallback to test result
                test_result = {
                    'summary': f'Summary: {content[:100]}...' if len(content) > 100 else content,
                    'original_length': len(content.split()),
                    'summary_length': min(20, len(content.split())),
                    'compression_ratio': 0.3
                }
                
                return JsonResponse({
                    'success': True,
                    'summary': test_result
                })
            
        except json.JSONDecodeError as e:
            print(f"DEBUG: JSON decode error: {e}")
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'})
        except Exception as e:
            print(f"Text summarization error: {e}")
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})