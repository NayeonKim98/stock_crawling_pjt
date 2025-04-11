from django.shortcuts import render, redirect
from .models import Comment, CommentAnalysis
from .crawling import crawl_and_save_comments

# 검색 입력 처리용 (폼에서 POST할 때만 사용)
def index(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        if not Comment.objects.filter(company_name=company_name).exists():
            try:
                crawl_and_save_comments(company_name)
            except Exception as e:
                messages.error(request, f'크롤링 중 오류가 발생했습니다: {e}')
                return redirect('crawlings:index')
        return redirect('crawlings:detail', company_name=company_name)
    return render(request, 'crawlings/stock_finder.html')


# 종목명 클릭 시 크롤링 후 분석 페이지로 이동
def detail(request, company_name):
    comments = Comment.objects.filter(company_name=company_name)

    # 댓글이 없다면 크롤링 수행
    if not comments.exists():
        try:
            crawl_and_save_comments(company_name)
            comments = Comment.objects.filter(company_name=company_name)  # 재조회
        except Exception as e:
            messages.error(request, f'크롤링 중 오류가 발생했습니다: {e}')
            return redirect('crawlings:index')

    # 분석 결과 최신 1개만 가져오기
    analysis = CommentAnalysis.objects.filter(company_name=company_name).order_by('-created_at').first()

    context = {
        'company_name': company_name,
        'comments': comments,
        'analysis': analysis,
    }
    return render(request, 'crawlings/stock_finder.html', context)


# 댓글 삭제
def delete_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    company_name = comment.company_name
    comment.delete()
    return redirect('crawlings:detail', company_name=company_name)