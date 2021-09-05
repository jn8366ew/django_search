from django.shortcuts import render
# postgres의 search기능을 사용하는데 필요한 모듈
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank, SearchHeadline
# postgres의 Trigram Similarity 와 TrigramDistance 모듈
from django.contrib.postgres.search import TrigramSimilarity, TrigramDistance
from django.db.models import Count

from book.forms import PostSearchForm
from book.models import Book


def post_search(request):

    form = PostSearchForm
    results = []
    q = None

    # take the information from HTML, which is 'q' from form.
    if 'q' in request.GET:
        form = PostSearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
            # print(q)

            # select ... from "book_book" where UPPER("book_book"."title"::text)
            # LIKE UPPER(%<value of q>%)

            """
            쿼리를 실행할 때. 
            1. 서버에 내가 어떤 데이터를 가져오려는 어떤 스크립트를 사용하여 
		    SQL에 쿼리를 쓴다고(write) 가정한다.
            2. 쿼리를 쓴 것을 바탕으로 우리가 요구한 데이터를 서버에서 모으는 방식은 
            매우 다양하다. Query planner라는 매카니즘이 실행된다. 쿼리 플래너란 
            우리의 쿼리에 실행되는 가장 빠른 방법을 찾는 메카니즘이다. 
            쿼리에 실행되는 방법들(plans)의 실행 시간(execution time)을 평가를 바탕으로 실행된다. 
            3. 실행시간이 가장 빠른 쿼리가 서버에서 실행된다.
            4. 서버가 결과물을 출력한다.     
            
            실행시간(Execution time): 3과 4의 단계를 거친 시간을 말한다. 
            계획시간(Planning time): 2단계만을 말한다. 
            
             # 쿼리의 실행시간, 계획시간을 분석한다.
            # print(Book.objects.filter(title__icontains=q).explain(analyze=True))
            """


            """
            # Standard textual queries (case sensitive)
            results = Book.objects.filter(title__contains=q)
            
            print(Book.objects.filter(title__contains=q).explain(verbose=True, analyze=True))
            print(Book.objects.filter(title__contains=q).query)
            

            """


            # # SearchVector 사용하기 (복수의 필드를 검색한다)
           
            # # q가 가진 string 값을 바탕으로 title과 authors 필드에 있는 
            # # objects를 가져와라 + 임시적으로 추가한 search 필드에 title과 author를
            # # 저장한다.

            # results = Book.objects.annotate(search=SearchVector('title', 'authors'),).filter(search=q)

            # # 삼천포: annotate
            # # 가령 작가 이름를 기준으로, 작가가 집필한 책의 수를 알고 싶다면 annotate를 이렇게 사용한다.
            # results = Book.objects.values('authors').annotate(num_books=Count('title')).order_by('-num_books')
            # print(results)


            # # Search Rank 사용하기
            # # 얼마나 document가 query에 상대적인지 가중치를 부여하는것을 바탕으로
            # # 가장 높은 연관성을 가진 document를 찾을 때 사용한다.
            # vector = SearchVector('title')
            # query = SearchQuery(q)
            # results = Book.objects.annotate(rank=SearchRank(vector, query)).order_by('-rank')



            # 가중치 랭킹 (점수가 높을수록 중요도가 높음)
            # D-weight: 0.1, C:0.2, B:0.4, A:1.0
            # Harris가 검색되는 이유는 Author내의 'Harr' 또한 가중치에 적용되기 때문임

            # vector = SearchVector('title', weight='B') + SearchVector('authors', weight='A')
            # query = SearchQuery(q)

            # vector = SearchVector('title', weight='B') + SearchVector('authors', weight='B')
            # query = SearchQuery(q)
            #
            # results = Book.objects.annotate(rank=SearchRank(vector, query, cover_density=True)).order_by('-rank')


            # text-search에는 normalization이 사용되기도 한다.
            # 정규화란 표현이 다른 단어를 통합시켜 같은 단어로 만든다.

            """
            Trigram 혹은 Trigraph 개념 
            문자열로 부터 받은 3개의 연속된 문자열들의 그룹
            
            Trigram에서 두개의 문자열이 공유하는 트라이그램의 수를 바탕으로 
            유사성을 측정한다.
            
            예: Dog -> "d", "do", "dog", "og"
            """

            print(q)
            
            # trigramSimilarity & trigramDistance 사용하기
            #results = Book.objects.annotate(similarity=TrigramSimilarity('title', q),).filter(similarity__gte=0.3).order_by('-similarity')
            #results = Book.objects.annotate(distance=TrigramDistance('title', q),).filter(distance__lte=0.8).order_by('distance')


            # Headline Search
            # query = SearchQuery(q)
            # vector = SearchVector('authors')
            # results = Book.objects.annotate(search=vector, headline=SearchHeadline('authors', query)).filter(search=query)

            # 결과 값에 나오는 authors의 값을 html의 span 클래스로 씌우기
            # results = Book.objects.annotate(search=vector, headline=SearchHeadline('authors', query, start_sel='<span>', stop_sel='</span>')).filter(search=query)



            print("#1")
            print(Book.objects.filter(title__trigram_similar=q).explain(analyze=True))
            print("#2")
            print(Book.objects.filter(
                title__trigram_similar=q).annotate(
                similar=TrigramSimilarity('title', q)).order_by('-similar').explain(analyze=True))

    return render(request, 'index.html', {'form':form, 'results':results, 'q':q})

""" 
GIN 인덱스를 사용하지 않고 query 하는 경우

# 1
Planning Time: 4.965 ms
Execution Time: 128.473 ms

#2
Planning Time: 2.511 ms
Execution Time: 142.305 ms


GIN 인덱스를 사용하는 경우

#1
Planning Time: 3.680 ms
Execution Time: 13.333 ms
#2

Planning Time: 2.112 ms
Execution Time: 15.078 ms

"""