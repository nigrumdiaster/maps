
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.core.paginator import Paginator
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.decorators.csrf import csrf_exempt
import datetime

class CreatePost(SuccessMessageMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = "posts/create_post.html"
    success_message = "Added Succesfully"
    def get_success_url(self):
        return reverse('create_post')

@csrf_exempt
def create_post(request):
    if request.method == 'GET':
        # Display the form for creating a post
        return render(request, "posts/create_post.html")
    
    elif request.method == 'POST':
        post_title = request.POST.get('postTitle')
        type_post = request.POST.get('postType')
        post_content = request.POST.get('postContent')
        post_source_url = request.POST.get('postSourceURL')
        post_notes = request.POST.get('postNotes')
        post_views = request.POST.get('postViews', 0)  # Default to 0 if not provided
        uploaded_images = request.FILES.getlist('file')
        
        # Tạo đối tượng Post mới và lưu vào cơ sở dữ liệu
        new_post = Post(
            title=post_title,
            post_type=type_post,
            content=post_content,
            source_url=post_source_url,
            notes=post_notes,
            views=post_views,
        )
        new_post.save()

        # Lưu từng hình ảnh vào cơ sở dữ liệu
        for image in uploaded_images:
            new_image = Post(post=new_post, image=image)
            new_image.save()
        
        # Chuyển hướng người dùng đến trang tạo bài viết với thông báo thành công
        context = {
            'message': 'Post created successfully!'
        }
        return render(request, "posts/create_post.html", context)


def list_post(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)  # Hiển thị 10 bài viết trên mỗi trang

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'posts/list_post.html', {'page_obj': page_obj})


def detail_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    session_key = f'post_{post_id}_viewed'
    
    # Lấy thời gian hiện tại
    now = timezone.now()
    
    # Kiểm tra xem session key đã tồn tại chưa
    last_view_time_str = request.session.get(session_key)
    
    if last_view_time_str:
        try:
            # Chuyển đổi thời gian từ chuỗi sang datetime object
            last_view_time = datetime.datetime.strptime(last_view_time_str, '%Y-%m-%d %H:%M:%S.%f')
            last_view_time = timezone.make_aware(last_view_time)  # Đảm bảo thời gian có timezone
            time_diff = now - last_view_time
            if time_diff.total_seconds() > 300:  # 300 giây = 5 phút
                post.views += 1
                post.save()
                # Cập nhật thời gian xem cuối cùng trong session
                request.session[session_key] = now.strftime('%Y-%m-%d %H:%M:%S.%f')
        except (ValueError, TypeError) as e:
            print(f"Error converting time: {e}")
            # Nếu có lỗi khi chuyển đổi thời gian, reset thời gian xem
            post.views += 1
            post.save()
            request.session[session_key] = now.strftime('%Y-%m-%d %H:%M:%S.%f')
    else:
        post.views += 1
        post.save()
        # Lưu thời gian xem cuối cùng vào session
        request.session[session_key] = now.strftime('%Y-%m-%d %H:%M:%S.%f')
    
     # Lấy 4 bài viết mới nhất
    latest_posts = Post.objects.exclude(id=post_id).order_by('-created_at')[:4]
    # lấy 4 bài tương tự
    related_posts = Post.objects.filter(post_type=post.post_type).exclude(id=post_id).order_by('-created_at')[:4]
    
    return render(request, 'posts/detail_post.html', {'post': post, 'latest_posts': latest_posts, 'related_posts': related_posts})