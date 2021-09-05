from django.db import models
# 메세지를 번역하고 문자열타입으로 반환한다.
# https://docs.djangoproject.com/en/3.2/topics/i18n/translation/
from django.utils.translation import gettext as _
from django.contrib.postgres.indexes import GinIndex



class Book(models.Model):

    title = models.CharField(_("title"), max_length=1000, null=False, db_index=True)
    authors = models.CharField(_("authors"), max_length=1000)

    # Generalized Inverted Index(GIN index)를 사용하기 위한 설정

    class Meta:
        indexes = [
            # opclasses는 postgresql 연산자 클래스로 우리가 인덱싱 하려는 쿼리 중에 발생(hook) 한다.
            # gin_trgm_ops를 사용해서 title 필드의 gin index를 생성한다.
            GinIndex(name='NewGinIndex', fields=['title'], opclasses=['gin_trgm_ops'])
        ]