
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.core.paginator import Paginator
import datetime

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


def post_list(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)  # Hiển thị 10 bài viết trên mỗi trang

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'posts/list_post.html', {'page_obj': page_obj})


def post_detail(request, post_id):
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