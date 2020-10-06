# Django RestFramework Dersleri - 2. Sezon
> BU DİZİN YOUTUBE DERSLERİ İÇİN YARATILMIŞTIR.  
> İLK SEZON VİDEO TUTORIAL SERİSİ İÇİN LİNK:    [Django RestFramework Dersleri - Bölüm 1 - YouTube](https://www.youtube.com/playlist?list=PLtf2C1UGjgPBgBLXvS61dDYJodJ4qhBRi)  
> BU SEZON  VİDEO TUTORIAL SERİSİ İÇİN LİNK:  [Django RestFramework Dersleri - Bölüm 2 - YouTube](https://www.youtube.com/playlist?list=PLtf2C1UGjgPB1rg4lggEu0qET8jy9FduQ)  


## Açıklama:
En çok kullanılan ve en güçlü Python Web Framework'ü olan Django’da, RestFrameWork kütüphanesini öğreniyoruz. Böylelikle, Django'nun gücünü kullanarak, web api akışları yaratabileceğiz. 

> 9 videodan oluşan ilk sezonun sonunda, hem Django RestFrameWork konusunda sağlam bir temeliniz oluştu; hem de listeleme, yaratma, güncelleme ve silme işlemlerini rahatlıkla yapabilecek ve hatta veri doğrulama yapabilecek seviyeye geldik.   

Bu serinin devamı niteliğindeki bu sezonda ise, RestFrameWork bilgi ve becerilerimizi biraz daha derinleştiriyoruz, derinleştirirken de aslında kolaylaştırıyoruz. Bu sezonun temel amacı, daha hatasız ve daha hızlı üretime geçebilmemiz ve üretirken de API’larımızın güvenliğini sağlamamız olacak.

Bu sezonda:
	1. ::GenericAPIView ve Mixins::’leri kullanmayı,
	2. ::Generic Class Based View::’leri (APIView Classın devamı) kullanmayı ve ihtiyacımız doğrultusunda modifiye etmeyi
	3. ::Pagination Sistem:: yani sayfalandırma ile, sonuca döktüğümüz Json beslemelerini gruplandırmayı
	4. Web API’larımızı ::permisson:: ve throttling ile daha güvenli hale getirmeyi öğreneceğiz (Authentication, yani kullancı yetkilendirme, bir sonraki sezonda).

Bu sezonumuzun hikayesi ise online bir kitap veri tabanı olacak.  Temel olarak aşağıdaki dersleri (videolar) yapacağız:

	1. **Proje Kurulumu:** Django 3.1 ile bir Kitap Veri tabanı projesi oluşturacağız (serimiz boyunca bu hikaye üzerinden gideceğiz).
	2.  **GenericAPIView:** Geçen sezonda öğrendiğimiz APIView classımızın bir üst versiyonu olan GenericAPIView ve ek olarak Mixinsleri göreceğiz.
	3. **Permissions (izinler):** İki videoda Pemissions yani izin  konusuna bakacağız.
	4. **Permissions  (izinler) Devam:**
	5. **Bonus:** Bonus videoda, Python Requests Library ve  Lxml kütüphaneleri ile books.toscrape.com sitesinde yer alan kitap bilgilerini çekerek, serializerımızı kullanarak veri tabanımıza aktaracağız.
	6. **Pagination:**Sonuçlalarımızı sayfalandıracağız. 

- - - -
#  1. DJANGO PROJEMİZİN KURULMASI
YouTube Tutorial Linki: [Django Restframework Bölüm -2 Ders -1 Proje Kurulumu - YouTube](https://youtu.be/3V7cvbvNWKg)

Hikayemiz online bir kitap veri tabanı kurmak. Hazırlayacağımız Rest API ile kullanıcılar,  veri tabanımızdaki kitapları listeleyebilecekler, yeni kitap kaydı yaratabilecekler ve mevcut kitaplar hakkında da yorum  yapabilecekler. 

Bu derste Django projemizi yaratıp, modellerimizi ve serializerlarımızı yaratalım.

## 1.1 Terminal İşlemleri
Öncelikle yarattığımız herhangi bir klasör içerisinde gelip, sanal ortamımızı yaratıyoruz ve aktive ediyoruz.  Devamında da aktive ettiğimiz sanal ortamımıza gerekli paketleri pip install ile yüklüyoruz. Sırasıyla aşağıdaki komutları terminalimize girmemiz lazım.

```Terminal (MAC OSX)
>>>virtualenv senv
>>>source senv/bin/activate
>>>pip install django
>>>pip install djangorestframework
>>>pip install django_extensions # bu kısım isteğe bağlı

```

Şimdi yapmamız gereken ise, bir django projesi başlatarak, dizin içeriğine girmek ve ilk appimizi yaratmak
```Terminal (MAC OSX)
>>>django-admin startproject kitap_pazari
>>>cd kitap_pazari
### manage.py dosyamızın olduğu dizine geldik
>>>python manage.py startapp Kitaplar
```

Appimizie de yarattığımıza göre artık settings.py içerisinde gerekli ayarları yapabiliriz, aşağıdaki gibi:

settings.py
```python
# Application definition


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', ##
    'django_extensions', ##
    'kitaplar.apps.KitaplarConfig', ##
]


```

Şimdi terminalimize `code .` komutunu girerek, VS Code’u (kod editörümüzü başlatıyoruz. Ve tabiki sanal ortamımızı (virtualenv) kod editörümüze tanıtmayı da unutmuyoruz).


## 1.2 Modellerimiz
Kitaplar/models.py
```python
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Kitap(models.Model):
    isim = models.CharField(max_length=255)
    yazar = models.CharField(max_length=255)
    aciklama = models.TextField(blank=True, null=True)

    yaratilma_tarihi = models.DateTimeField(auto_now_add=True)
    güncellenme_tarihi =  models.DateTimeField(auto_now=True)
    yayın_tarihi = models.DateTimeField()

    def __str__(self):
        return f'{self.isim} - {self.yazar}'




class Yorum(models.Model):
    kitap = models.ForeignKey(Kitap, on_delete=models.CASCADE, related_name='yorumlar')

    yorum_sahibi =  models.CharField(max_length=255)
    yorum = models.TextField(blank=True, null=True)

    yaratilma_tarihi = models.DateTimeField(auto_now_add=True)
    güncellenme_tarihi =  models.DateTimeField(auto_now=True)

    degerlendirme = models.PositiveIntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(5)],
    )


    def __str__(self):
        return str(self.degerlendirme)


```

Modellerimizi ::kitaplar/admin.py::  içerisinde kaydedelim ki, admin sayfamızda görebilelim:
```python
from django.contrib import admin
from kitaplar.models import Kitap, Yorum
# Register your models here.
admin.site.register(Kitap)
admin.site.register(Yorum)

```


## 1.2 Serializerlarımız
Öncelikle ::kitaplar/api:: klasörünü yaratıyoruz.  Ve bu klasörün içerisinde serializers.py dosyasını  yaratıyoruz.

kitaplar/api/serializers.py
```python
from rest_framework import serializers
from kitaplar.models import Kitap, Yorum


class YorumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Yorum
        fields = '__all__'

class KitapSerializer(serializers.ModelSerializer):
    yorumlar = YorumSerializer(many=True, read_only=True)
    class Meta:
        model = Kitap
        fields = '__all__'
```

### 1.2.1. Eğer VS Code -  AutoComplete özelliği çalışmıyorsa
> Sanal ortamımız ile dosyalarımız aynı dizinde olmadığı zaman, auto-complete yani otomatik tamamlama özelliği ile alakalı sıkıntılar yaşabiliriz. Bu durumda, dizimiz içerisinde bulunan .vscode klasörü içerisindeki json dosyasına  ::"python.autoComplete.extraPaths"::  şeklinde aşağıda gösterildiği gibi bir ekleme yapmamız gerekecek.  

.vscode/settings.json
```json
{
    "python.pythonPath": "<Bu satır zaten olmalı, oynamıyoruz>/Python.framework/Versions/3.8/bin/python3.8",
    "python.autoComplete.extraPaths": [
        "<Sanal Ortamın kurulu olduğu dizin>/lib/python3.8/site-packages",
      ]
}

```


    “python.autoComplete.extraPaths”: [
        “/Users/alperakbas/dev/Trainings/Django/DRF_SABA/DRF_VIDEO_BLOG/02_DRF_SEZON_2/senv/lib/python3.8/site-packages”,
      ]


## 1.3 Migrations
Artık modellerimiz ve serializerlarımız hazır olduğuna göre, migrationslarımızı yapıp, superuserımızı yaratabiliriz. 
```Terminal (MAC OSX)
>>>python manage.py makemigrations
>>>python manage.py migrate
>>>python manage.py createsuperuser
>>>python manage.py runserver
```

GenericAPIView Class’ı ve Mixins konseptini öğrenmeye hazırız, artık.

- - - -
#  2. GENERIC API VIEWS VE MIXINS’LER
Youtube Tutorial Linki: [Django Restframework Bölüm -2 Ders - 2 GenericAPIView - YouTube](https://youtu.be/VQYYzMG_nOs)

Django evreninde ve bir çok diğer CRUD (Create, Retrieve, Update, Delete) modellerinde, aynı ve benzer işlemler sırasıyla yapıldığı için, genel geliştirme senaryoları için bu işlemler de daha kısa hale getirilmiş. Aynı kodu tekrar tekrar yazmak, gereksiz ve aşırı derecede zaman alıcı  olurdu, zaten.

GenericAPIView ve Mixinsleri kullanmak, bu sebeple, bizlere arkaplanda bir çok kodu bedavaya getirecek ve bir çok yeni olanak sağlayabilecek. DRF, APIView class’tan türetilen, APIView class’ın mevcut olanak ve kabiliyetlerine yenilerini de ekleyen GenericAPIView classına ve bazı mixinslere sahip.

GenericAPIView genellikle mixinslerle kullanılmakta. Bu mixinsler, GenericAPIView’e .create() .list() gibi yeni yetenekler eklemekte. Bunları .get() ve .post() metodlarının evrimleşmiş hali olarak düşünebiliriz.

Ancak, bu dersin asıl önemi, çok daha hızlı proje oluşturmamıza sağlayacak olan Concrete Views’leri anlamamız. Çünkü, önümüzdeki ders göreceğimiz concrete viewler, arka planda şu an yapacağız işlemlere benzer işlemleri yürütüyor olacak.

GenericAPIView resmi  dokümantasyonu: [Generic views - Django REST framework](https://www.django-rest-framework.org/api-guide/generic-views/#genericapiview)

## 2.1. Views.py
kitaplar/api/views.py
```python
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from kitaplar.models import Kitap

from kitaplar.api.serializers import KitapSerializer, YorumSerializer


class KitapListCreateAPIView(ListModelMixin, CreateModelMixin,GenericAPIView):
    queryset = Kitap.objects.all()
    serializer_class = KitapSerializer

    # listelemek
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # yaratmak istiyorum
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

```

kitap_pazari/urls.py
```python
from django.urls import path
from kitaplar.api import views as api_views

urlpatterns = [
   path( 'kitaplar/', api_views.KitapListCreateAPIView.as_view(), name='kitap-listesi'),
]

```


kitap_pazari/urls.py
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('kitaplar.api.urls')),
]


```


- - - -
#  3. CONCRETE VIEWS
YouTube Tutorial Linki: [Django RestFramework- Bölüm 1 - Ders 3 ConcreteViews - YouTube](https://youtu.be/t5H8UEute14)

GenericAPIView sınıfını ve mixinleri de öğrendiğimize göre artık işimizi çok daha pratikleştirecek ve bize yeni kabiliyetler kazandıracak Concrete Views’e geçebiliriz.  

> Concrete (Türkçe karşılığı) somut, bütün, elle tutulur (ve beton) anlamlarına gelmekte. DRF resmi sitesinde ::“concrete”:: ifadesinin kullanılmasının sebebi de, bu concrete viewlerin, bir geliştiricinin ihtiyaç duyabileceği hemen hemen tüm işlevselliği, çok daha az kod ile ulaşılabilir kılması.  

Bir önceki dersimizde bahsettiğimiz üzere, her bir concrete view, GenericAPIVIEW ve ilgili mixinlerin birleştirilmesinden oluşuyor. Örneğin RetrieveUpdateAPIView, GenericAPIView ile ::RetrieveModelMixin:: ve ::UpdateModelMixin::’in birlikte kullanılmasıyla elde edilmiş. 

Bu soyutlama seviyesi sebebiyle de, Concrete Viewler, yazılması ve aynı zamanda okunması en kolay viewler. Aynı zamanda, bir çok ek kabiliyeti de beraberinde getirmekteler. Ancak,  concrete viewlerin ne zaman ve nasıl kullanılacağını, ve en önemlisi, ne zaman / ne şekilde uyarlanması gerektiğini bilebilmek için, şu ana kadar işlediğimiz konulara hakim olmamız gerekiyor.

## 3.1. Views.py - Concrete Views
### 3.1.1. Kitapları listeleme, yaratma & Kitap detayı görüntüleme, güncelleme ve silme işlemleri.
kitaplar/api/views.py
```python

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework import generics
from kitaplar.api.serializers import KitapSerializer, YorumSerializer
from kitaplar.models import Kitap



class KitapListCreateAPIView(generics.ListCreateAPIView):
    queryset = Kitap.objects.all()
    serializer_class = KitapSerializer


class KitapDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Kitap.objects.all()
    serializer_class = KitapSerializer
```

kitaplar/api/urls.py
```python
from django.urls import path
from kitaplar.api import views as api_views

urlpatterns = [
   path('kitaplar/',api_views.KitapListCreateAPIView.as_view(), name='kitap-listesi' ),
   path('kitaplar/<int:pk>',api_views.KitapDetailAPIView.as_view(), name='kitap-bilgileri' ),
]
```

- - - -
#  4. CONCRETE VIEWS - DEVAM - perform_create()
YouTube Tutorial Linki: [Django Restframework Bölüm -2 Ders -4 Concrete Views Devam - YouTube](https://youtu.be/ByAeczJ6Q3I)

### 4.1.Yorum yaratma işlemi 
İşlerin bir nebze karıştığı noktadayız.  Yukarıda da bahsettiğimiz üzere Concrete Viewler yazılması, okunması en kolay viewlerdir ve ayrıca hali hazırda birçok fonksiyonelliği içerisinde barındırır. Ancak, Concrete viewler GenericAPIView (dolayısıyla APIView) üzerinden  ve mixinsler de kullanılarak yaratıldığı için, aslında bir çok işlemi arka planda biz görmeden halletmekte. Dolayısıyla, bazı durumlarda arka planda çalışan bazı metodları overwrite ederek (tekrar yazarak ya da üzerine yazarak) manipüle etmemiz gerekmekte. Şimdi yapacağımız gibi.

> Yorum yaratma işlemi, kitap yaratma işleminden biraz farklı olacak. Nedeni ise, yorumu yaratırken bir kitap ile ilişkilendirmek zorunda olmamız. Hatırlarsanız eğer, Yorum modelimizin içerisinde  aşağıda gösterildiği şekilde bir ForeignKey alanımız vardı.  

Kitaplar/models.py
```python
class Yorum(models.Model):
    kitap = models.ForeignKey(Kitap, on_delete=models.CASCADE, related_name='yorumlar') ###########

    yorum_sahibi =  models.CharField(max_length=255)
    yorum = models.TextField(blank=True, null=True)

    yaratilma_tarihi = models.DateTimeField(auto_now_add=True)
    güncellenme_tarihi =  models.DateTimeField(auto_now=True)

    degerlendirme = models.PositiveIntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(5)],
    )


    def __str__(self):
        return str(self.degerlendirme)

```

Bu ::ForeignKey:: ya da ::one to many relation:: sebebiyle, yorum yaratma işlemi tamamlanmadan önce, ::bir şekilde hangi kitaba yorum yapılacaksa o kitap ile yaratacağımız yorumu ilişkilendirmemiz lazım.::  Aksi takdirde, veri tabanımız Integrity (bütünlük de diyebiliriz) hatası verecek, ve hiçbir şekilde yorum yaratamayacağız.  Bizim normal Django ORM’de bir yorum  yaratırken aşağıdakine benzer bir işlem yapmamız lazım:

```python
from kitaplar.models import Kitap, Yorum

kitap_instance = Kitap.objects.get(pk=1) # Birinci kitap nesnemizi çektik.
yorum = Yorum(kitap= kitap_instance, yorum_sahibi='Test User', degerlendirme=5) 
# diğer alanlar otomatik ya da blank=True olduğu için geçtik
yorum.save()

```

> Burada en büyük soru, hangi kitap ile ilişkilendireceğimizi DRF’e nasıl bildireceğimiz. Bu sorunun en bilinen ve en çok uygulanan cevabı URL yani API çağrısı yapacağımız URL içerisine ilgili kitabın  ID’sini eklememiz. Sonuçta browserdan da request yapılsa, başka bir app’ten de api call yapılsa url bilgisi request ile birlikte bizim ana makinemize ulaşmakta. Yani, bizim birinci kitap için yorum yaratmak amacıyla yaratacağımız url aşağıdaki gibi olmalı:  

```html
http://127.0.0.1:8000/kitaplar/1/yorum_yap
```

Dolayısıyla bizim urlpattern içerisinde şöyle bir path yaratmamız gerekecek:
kitaplar/api/urls.py
```python
from django.urls import path
from kitaplar.api import views as api_views

urlpatterns = [
   path('kitaplar/',api_views.KitapListCreateAPIView.as_view(), name='kitap-listesi' ),
   path('kitaplar/<int:pk>/', api_views.KitapDetailAPIView.as_view(), name='kitap-bilgileri'),
	######## AŞAĞIDAKİ URL ######
   path('kitaplar/<int:kitap_pk>/yorum_yap/', api_views.YorumCreateAPIView.as_view(), name='kitap-yorumla'),
]

```

Yani, `<int:kitap_pk>`  url parametresi ile biz, ilgili viewimizin içerisinde bu integer yapısını alacağız ve kitap ID’si olarak kullanacağız. Bunun için, yani URL deki parametreyi çekmek için  `kitap_pk = self.kwargs.get(‘kitap_pk’)` betik öbeğine ihtiyacımız olacak . Ama bu betik öbeğini nereye yazacağız. 

Bunun için perform_create metodunu **baştan yazmamız** lazım.  Bu perform_create metoduna müdahalede bulunmamızın sebebi ise içerisinde işlem görmekte olan serializer nesnemizi kayıt etmeden evvel, ilgili kitap bilgisini serialerımıza geçirmek. 

perform_create metodu aslında bizim RestFramework kütüphanemizde yer alan CreateModelMixin  (mixins.py) içerisinde yer almakta.  Aşağıda CreateModelMixin kaynak koduna bakalım:

mixins.py
```python
class CreateModelMixin:
    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

```

Yukarıda görüldüğü gibi, perform create metodu serializerı save etmekten başka bir işlem yapmıyor. Buradaki serializer tabiki bizim YorumSerializer’ımız (“serializer_class = YorumSerializer” şeklinde viewimiz içerisinde bildirdik. ). 

Yorum Modelimizin, dolayısıyla da serializerimizin içerisinde kitap alanı bulunmakta. İşte biz bu perform_create metodunu baştan yazarak, serialize işlemi sırasında eksik kalan bu kitap alanını, açık bir şekilde belirteceğiz.

Viewimizin son hali aşağıdaki gibi olmalı:

kitaplar/api/views.py
```python
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin

from rest_framework import generics

from kitaplar.api.serializers import KitapSerializer, YorumSerializer
from kitaplar.models import Kitap, Yorum

from rest_framework.generics import get_object_or_404

class KitapListCreateAPIView(generics.ListCreateAPIView):
    queryset = Kitap.objects.all()
    serializer_class = KitapSerializer


class KitapDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Kitap.objects.all()
    serializer_class = KitapSerializer

####### YORUM YARATMA VIEWIMIZ ########
class YorumDetailAPIView(generics.CreateAPIView):
    queryset = Yorum.objects.all()
    serializer_class = YorumSerializer

    #  Bir yorum yaratabilmek için bir kitap nesnesine bağlamamız lazım
    # Bu sebeple url içerisinde bir kitaba ait PK koyacağız ve buradan bu PK ile
    # ilgili kitap nesnesini çekip, yarattığımuz yoruma bağlayacağız  ==> http://127.0.0.1:8000/api/kitaplar/1/yorum_yap
    # Bu işlemleri yapabilmemiz için de perform_create metoduna müdahale etmemiz gerekiyor. 
    def perform_create(self, serializer):
        kitap_pk = self.kwargs.get('kitap_pk')
        kitap = get_object_or_404(Kitap, pk=kitap_pk)
        serializer.save(kitap=kitap)

```

Viewimizi ve url_patternimizi hallettik ancak, son bir hamlemiz daha kaldı. Eğer şu an, http://127.0.0.1:8000/api/kitaplar/1/yorum_yap adresini çağırırsak, browserımızdaki yorum_yap browsable api sayfasında  ilk alacağımız mesaj yani  render edilecek ilk json şu şekilde:

```json
{
    "detail": "Method \"GET\" not allowed."
}
```

Bu gayet normal, çünkü biz YorumDetailAPIView sınıfımızda, get request ile ilgili bir işlem yapmadık ve get requeste izin vermedik; çünkü, bu url endpointumuzun tek bir amacı var, yorum yaratmak yani post request yapmak. 

Ancak, browsable_api ile gelen HTML formumuzda hala farklı kitaplar seçebildiğimiz bir kitap alanı var çünkü biz, YorumSerializerımız içerisinde `fields= '__all__'`  betiğini kullandık, bu da bildiğiniz üzere, bütün alanları dahil et demek. Ancak, biz hali hazırdaki iş akış mantığımızda kitap alanını backendimizde hallediyoruz. Dolayısıyla, şu an en mantıklı hareketi, YorumSerializer içerisinde Meta altında  `fields= '__all__'`  ifadesini `exclude = [‘kitap’]` şeklinde yeniden yazarak, kitap alanını serializerımızdan çıkarmak.


- - - -
#  5. PERMISSIONS - İZİNLER - Birinci Bölüm
YouTube Tutorial Linki: [Django Restframework Bölüm -2 Ders-5 Permissions İzinler 1 - YouTube](https://youtu.be/SPhGAzF_ZWg)

* Get,  Post, Put, Delete Requestleri (isteklerini)  kullanıcılarımızın login olup olmama ya da Staff/Admin olup olmama durumuna göre kısıtlama
* DRF ile browsable api üzerinden login logout işlemleri.
* Kendi İzinlerimizi Yaratma

Resmi Sayfa: [Permissions - Django REST framework](https://www.django-rest-framework.org/api-guide/permissions/)

Bu dersimizde DRF’in bize sunmuş olduğu “permissions system” yani izinler sistemini ile API’larımızı nasıl daha güvenli hale getirebileceğimizi göreceğiz.  Bu bağlamda kitap projemiz üzerinde:
	* Sadece giriş yapmış (login) kullanıcılara  görüntüleme izni verme
	* Sadece belirli bir kullanıcı grubuna (admin ya da staff [personel]) yazma yetkisi verme (güncelleme ve yaratma işlemleri) gibi işlemleri yapacağız. 
Authentication yani yetkilendirme konusunun derinliklerine ise önümüzdeki video serisinde gireceğiz. 

API’larımızın ya da end pointlerimizin tamamını sadece giriş yapmış kullanıcılara açmak istiyorsak, aslında işimiz oldukça basit. settings.py dosyası içerisinde bir dictionary yaratmak, aşağıdaki gibi:

settings.py
```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}
```

Eğer DRF ayarlarına yukarıdaki gibi yaparsak, tüm end pointlerimizi yani urllerimizi aslında sadece üye girişi yapmış kullanıcılara açmış oluyoruz. Eğer yukarıdaki gibi bir belirleme yapmazsak, aşağıdaki ayarlar geçerli olacak ve tüm URL’lerimiz herkese açık olacak. Aslında yukarıdaki satırları yazarak “Global Policy” tanımlamış oluyoruz.

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny', # Allow any herkese ya da herşeye izin ver anlamına gelmekte
    ]
}
```

DRF bize hali hazırda AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly gibi  hazır izin sınıfları tanıyor. Ancak, biz bu global policylere ek olarak, her bir viewimiz için ya da nesnemiz için ayrı izinler tanımlayabilir, ve hatta kendi izinlerimizi yazabiliriz. 

- - - -
#  6. PERMISSIONS - İZİNLER - İkinci Bölüm
Youtube Tutorial Linki: [Django Restframework Bölüm-2 Ders-6 Permissions İzinler 2 - YouTube](https://youtu.be/pI5oHpBorKk)

Peki, biz kullanımız admin ise yazma yetkisi (put/post/delete vb.) vermek, eğer admin değilse de sadece okuma yetkisi vermek istersek?

Öncelikle ana urls.py dosyamıza bir path ekleyerek, browsable api arayüzümüz (yani sayfamız) üzerinden login / logout işlemleri yapabilmemizin önünü açacağız. Bu da DRF ile hazır geliyor. Yapmamız gereken tek şey ana urls.py dosyamıza aşağıdaki satırı eklememiz. User Auth kısmına çok daha detaylıca önümüzde bölümde bakıyoruz, bunu da hatırlatalım.

kitap_pazari/kitap_pazari/urls.py
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('kitaplar.api.urls')),
    path('api-auth/', include('rest_framework.urls')),
]

```



Bu durumda kitaplar/api/permissions.py dosyasını yaratarak ve rest_framework.permissions.IsAdmin sınıfını kullanarak yeni bir permission sınıfı yaratmamız gerekecek, aşağıdaki gibi:

kitaplar/api/permissions.py 
```python
from rest_framework import permissions
from pprint import pprint

class IsAdminUserOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in permissions.SAFE_METHODS or is_admin

```

Daha sonra yapmamız gerek ise, yazdığımız izin sınıfını (IsAdminUserOrReadOnly) viewsimize dahil etmemiz.

Kitaplar/api/views.py
```python
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin

from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework import permissions 
from kitaplar.api.permissions import IsAdminUserOrReadOnly ### Yazdığımız izin sınıfını çektik

from kitaplar.api.serializers import KitapSerializer, YorumSerializer
from kitaplar.models import Kitap, Yorum


class KitapListCreateAPIView(generics.ListCreateAPIView):
    queryset = Kitap.objects.all()
    serializer_class = KitapSerializer
    permission_classes = [IsAdminUserOrReadOnly] ### viewimize dahil ettik


class KitapDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Kitap.objects.all()
    serializer_class = KitapSerializer
    permission_classes = [IsAdminUserOrReadOnly] ### viewimize dahil ettik

```



- - - -
#  7. PERMISSIONS - İZİNLER - Üçüncü Bölüm
YouTube Tutorial Linki: [Django Restframework Bölüm-2 Ders-7 Permissions İzinler 3 - YouTube](https://youtu.be/elKzQP8cqfA)

Permissions konusuna biraz vakıf olmaya başladığımıza göre artık işi bir seviye yukarıya taşıma vakti geldi. Şimdi hali hazırda yorum yapan kullanıcıların sadece kendi yorumlarını silip, güncellemeyebilmesi için gerekli işlemleri yapalım.

Bizim hali hazırda Yorum modelimiz içerisinde `yorum_sahibi =  models.CharField(*max_length*=255)` alanımız vardı. Öncelikle bu alanı, Django user modeli ile ilişkilendirmemiz gerekecek. Yorum modelimizide aşağıdaki değişikliği yapalım. Böylelikle sadece Django user modelinde kayıtlı kullanıcılar yorum yapabilecek. User modelimizi nasıl genişleteceğimizi önümüzdeki derslerde göreceğiz, ancak, şu an amacımız permissions’ı öğrenmek olduğu için bu şekilde devam edelim.

## 7.1 Modelimizi ve Serializerımızı güncelleme
kitap_pazari/kitaplar/models.py
```python
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User



class Yorum(*models*.*Model*):
    kitap = models.ForeignKey(Kitap, *on_delete*=models.CASCADE, *related_name*=‘yorumlar’)

    ##yorum_sahibi =  models.CharField(*max_length*=255)
    yorum_sahibi =  models.ForeignKey(User, *on_delete*=models.CASCADE, related_name='kullanici_yorumlari') ##### 
    yorum = models.TextField(*blank*=True, *null*=True)

    yaratilma_tarihi = models.DateTimeField(*auto_now_add*=True)
    güncellenme_tarihi =  models.DateTimeField(*auto_now*=True)

    degerlendirme = models.PositiveIntegerField(
        *validators* = [MinValueValidator(1), MaxValueValidator(5)],
    )


    def __str__(*self*):
        return *str*(*self*.degerlendirme)
```

> Yorum modelimizi değiştirdiğimiz için migrationslarımızı yapmamız gerekecek ama herhangi bir hata olmaması için, mevcut yorumlarımızı admine girerek silmeyi unutmayalım.  

Devamında YorumSerializerımız üzerinde ufak bir değişiklik yapmamız gerekecek. 

kitap_pazari/kitaplar/api/serializers.py
```python
from rest_framework import serializers
from kitaplar.models import Kitap, Yorum

class YorumSerializer(serializers.ModelSerializer):
    yorum_sahibi = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Yorum
        # fields = '__all__'
        exclude = ['kitap']


```

Yukarıda ::read_only = True:: ifadesini eklememizin bir sebebi var. Çünkü, biz arka tarafta, otomatik olarak request.user ile yorumu bağlamak istiyoruz.  Aslında, benzer bir işlemi, perform_create() metodu içerisinde serializerimizi save etmeden önce kitap objesini eklerken de yapmıştık. Yorum yaratma işlemi yaptığımız viewimizin son hali aşağıdaki gibi olacak.

kitap_pazari/kitaplar/api/views.py
```python
class YorumCreateAPIView(generics.CreateAPIView):
    queryset = Yorum.objects.all()
    serializer_class = YorumSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # 3. sadece login yapmış kullanıcılara yazma yetkisi verdik.

    
    def perform_create(self, serializer):
        #  path('kitaplar/<int:kitap_pk>/yorum_yap/', api_views.YorumCreateAPIView.as_view(), name='kitap-yorumla'),
        kitap_pk = self.kwargs.get('kitap_pk')
        kitap = get_object_or_404(Kitap, pk=kitap_pk)
        yorum_sahibi = self.request.user # 1. userımızı çektik
        serializer.save(kitap=kitap, yorum_sahibi = yorum_sahibi) # 2. userımızı yoruma bağladık

```

Öncelikle, request.user’ı serlializerımıza ekledik; böylelikle de user nesnesi ile yorum nesnesini bağlamış olmuş. Ancak, bunu yapabilmemiz için, login olmuş kullanıcılara ihtiyacımız var. Bu sebeple de, permisson_class listesi içerisine ::permissions.IsAuthenticatedOrReadOnly:: ifadesini ekledik. Bu iş mantığı ile, sadece admin statüsüne sahip kullanıcılar kitap yaratma, güncelleme ve silme işlemleri yapabilirken, login yapmış herhangi bir kullanıcı yorum yapabilecek ya da yorumlarını güncelleyip, silebilecek. 

Ama, bir sorun var: Herhangi bir kullanıcı, başka bir kullanıcının yorumunu güncelleyebilir ya da silebilir.  Daha da önemlisi, birden fazla yorum yapabilecek! Öncelikle birden fazla yorum yapmayı çözelim.


##   7.2 Aynı kullanıcının aynı kitaba birden fazla yorum yapmasını engelleme

Aynı kullanıcıdan birden fazla yorumu engellemek için, yine perform_create() metodumuz içerisinde bir validation check yapacağız. Eğer, kullanıcının yorumu varsa aynı kitapta, karşı tarafa bir HTTP 400 bad request ve mesaj göndermemiz gerekiyor.  Viewimizin yeni hali aşağıdaki gibi olacak:

kitap_pazari/kitaplar/api/views.py
```python
from rest_framework.exceptions import ValidationError  ### HTTP 400 Döndürebilmemiz için bunu import etmeyi unutmayalım

class YorumCreateAPIView(generics.CreateAPIView):
    queryset = Yorum.objects.all()
    serializer_class = YorumSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    
    def perform_create(self, serializer):
        #  path('kitaplar/<int:kitap_pk>/yorum_yap/', api_views.YorumCreateAPIView.as_view(), name='kitap-yorumla'),
        kitap_pk = self.kwargs.get('kitap_pk')
        kitap = get_object_or_404(Kitap, pk=kitap_pk)
        yorum_sahibi = self.request.user
        #### Kullanıcıya ait, aynı kitap için yorum var mı???
        yorumlar = Yorum.objects.filter(kitap=kitap, yorum_sahibi=yorum_sahibi) 
        if yorumlar.exists():
            raise ValidationError('Bu kitaba daha önce yorum yaptınız.')

        serializer.save(kitap=kitap, yorum_sahibi = yorum_sahibi)

```


- - - -
#  8. PERMISSIONS - İZİNLER - Dördüncü Bölüm
YouTube Tutorial Linki:  [Django Restframework Bölüm-2 Ders-8 Permissions İzinler 4 - YouTube](https://youtu.be/1f_kA0HJRPE)

##   Kullanıcının sadece kendi yorumlarını silip, güncelleyebilmesi
Bunu tahmin edebileceğiniz üzere, yapabilmek için yeni bir permission class yazmamız gerekecek.
```python
from rest_framework import permissions
from pprint import pprint

# SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

class IsAdminUserOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in permissions.SAFE_METHODS or is_admin


class IsYorumSahibiOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request in permissions.SAFE_METHODS:
            return True

        return request.user == obj.yorum_sahibi


```

 IsYorumSahibiOrReadOnly şeklinde yaratacağımız bir permission class ile,  yukarıdaki gibi, YorumDetailAPIView’imiz için gerekli izin sınıfını yaratmış oluyoruz. Bundan sonra yapmamız gereken, ilgili viewimiz içerisine bu izin sınıfımızı dahil etmek.

Viewimizin son hali:

kitap_pazari/kitaplar/api/views.py
```python
class YorumDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Yorum.objects.all()
    serializer_class = YorumSerializer  
    permission_classes = [IsYorumSahibiOrReadOnly]

```



- - - -
#  9. FAKER Kütüphanesi ile Veri Tabanımızda Fake Kayıt Oluşturma - User Ekleme
YouTube Tutorial Linki:   [Django Restframework Bölüm -1 Ders - 9 İlişkiler - YouTube](https://youtu.be/ehcdctUrZk0)

Faker Docs: [Welcome to Faker’s documentation! — Faker 4.1.6 documentation](https://faker.readthedocs.io/en/master/)

İlk olarak pip install faker ile faker kütüphanesini kurmamız gerekiyor.

Düzenli olabilmek ve organize olabilmek maksadıyla ilk olarak, ana dizinimiz içerisinde scripts adında bir klasör oluşturuyoruz. Ve Bu klasörün içerisinde iki adet dosya  yaratıyoruz. Birinci dosyamız __init__.py. Böylelikle python ve django bu klasörün bir kütüphane olduğunu ve bu klasör altındaki python dosyalarından bazı sınıf ya da metodları çekeceğimizi anlamış oluyor.  Devamında da scriptlerimizi yazmamız için fake_data.py adında bir python dosyası oluşturuyoruz.  Dosya dizinimiz aşağıdaki gibi olmalı:

```terminal
├── db.sqlite3
├── kitap_pazari
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── kitaplar
│   ├── __init__.py
│   ├── __pycache__
│   ├── admin.py
│   ├── api
│   │   ├── __pycache__
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── apps.py
│   ├── migrations
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── manage.py
├── scripts ############
│   ├── __init__.py
│   └── fake_data.py
```

Şimdi user yaratabilmek için gerekli fonksiyonumuzu yazalım.
kitap_pazari/scripts/fake_data.py
```python
import os
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kitap_pazari.settings')

import django
django.setup()
### Modellerimize ve django içeriklerine erişmek için yukarıdaki gibi ayarlamaları yapmamız lazım
### SIRALAMA ÇOK ÖNEMLİ

from django.contrib.auth.models import User

from faker import Faker

def set_user(fakegen=None):
    if fakegen is None:
        fakegen = Faker(['en_US'])

    f_name = fakegen.first_name()
    l_name = fakegen.last_name()
    u_name = f_name.lower() + '_' + l_name.lower()
    email = f'{u_name}@{fakegen.domain_name()}'

    user_check = User.objects.filter(username=u_name)
	##### BÖYLE BİR USERNAME VARSA HATA ALACAĞIZ BUNUN İÇİN BİR VALIDATION YAPIYORUZ
    while user_check.exists():
        print(f'Böyle bir kullanıcı var zaten: {u_name}')
        u_name = f_name + '_' + l_name + str(random.randrange(1, 999))
        user_check = User.objects.filter(username=u_name)


    user = User(
        username =  u_name,
        first_name =  f_name,
        last_name = l_name,
        email =  email,
    )

    user.set_password('testing123')
    user.save()

    user_check = User.objects.filter(username=u_name)[0]
    print(f'Kullanici {user_check.username}, {user_check.id} id numarası ile kaydedildi. ')

```



- - - -
#  10. OpenLibrary.org sitesi üzerinden json’ları çekerek kitap kayıtları oluşturma
Aşağıda yazdığımız kod ile ilgili açıklamaları ve nasıl yazdığımızı ilgili YouTube videosundan izleyebilirsiniz.
YouTube Tutorial Linki:  [Django Restframework Bölüm-2 Ders-10 Harici API kullanarak Kitap Kayıtları Yaratma - YouTube](https://youtu.be/q5Nv1m_OZr8)

kitap_pazari/scripts/fake_data.py
```python

from pprint import pprint
from kitaplar.api.serializers import KitapSerializer

def kitap_ekle(konu):
    fake = Faker(['en_US'])
    url = 'http://openlibrary.org/search.json'
    payload = {'q': konu}
    response = requests.get(url, params=payload)
 
    if response.status_code != 200:
        print('Hatalı istek yapıldı', response.status_code)
        return

    jsn = response.json()
    kitaplar = jsn.get('docs')

    for kitap in kitaplar:
        kitap_adi = kitap.get('title')
        data = dict(
            isim = kitap_adi,
            yazar = kitap.get('author_name')[0],          
            aciklama = '-'.join(kitap.get('text')),
            yayın_tarihi = fake.date_time_between(start_date='-10y', end_date='now', tzinfo=None),
        )

        serializer = KitapSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print('kitap kaydedildi: ', kitap_adi)
        else:
            continue
        
```


- - - -
#  11. Pagination - Sayfalandırma
YouTube Tutorial Linki: [Django Restframework Bölüm-2 Ders-11 Pagination - YouTube](https://youtu.be/j6g7cOTOAlQ)
Resmi Docs: https://www.django-rest-framework.org/api-guide/pagination/
 
Onuncu bölümde yazdığımız kodu çalıştırdıktan sonra, artık veri tabanımızda en az 100 kitap kaydımız var.  Browsable API sayfasında bunları bir defada yazdırırsak, sayfamız baya bir uzun olacak. Ayrıca, iş akış modelimizi de düşünürsek, en mantıklısı API çıktılarımızı daha küçük gruplara bölmek. Bir milyondan fazla kaydınız olduğun düşünün bunu tek bir defada response olarak göndermek hiç tasarruflu bir hareket olmazdı. Aynı anda, 1000 kullanıcının bu isteği yaptığını düşünün!

Neyse ki, DRF ile hali hazırda gelen bir pagination / sayfalandırma sistemi var ve kullanımı da son derece basit. DRF ile gelen 3 ayrı sınıf var: 
		* PageNumberPagination
		* LimitOffsetPagination
		* CursorPagination

Biz dersimizde PageNumberPagination sınıfı üzerinde duracağız.  

Öcelikle şunu belirmekte fayda var: DRF ile halihazırda gelen ve bizim dersimizde işleyeceğimiz otomatik sayfalandırma işlemini kullanabilmek için generic view ya da viewsetler kullanmamız lazım. Eğer APIView kullanıyorsak,  pagination API’ını kendimiz çağırıp bir dizi işlemi kodlamamız gerekir. 

Eğer global policy yazmamız gerekiyorsa, yani viewlerimizden bağımsız genel bir sayfalandırma yapmak istiyorsak, işimiz gayet basit, yapmamız gereken tek şey,  settings.py dosyamız içerisinde aşağıdaki satırları eklemek:

settings.py
```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100
}

```

‘PAGE_SIZE’  içerisinde vereceğimi integer, bizim tüm viewlerimizdeki sayfalandırma sayısını belirleyecek, yani her bir istekte  100 kayıt (ya da belirleyeceğimiz) kadar kayıt gelecek. Böylelikle, hem jsonlarımızın belirlenen ölçüte göre gruplandırılıp sayfalandırma işlemini yaptık, hem de gönderidimiz json responselara aşağıdaki gibi bir next  (ya da previous) bilgisini eklemiş olduk:

```json
{
    "count": 100,
    "next": "http://127.0.0.1:8000/api/kitaplar/?page=2",
    "previous": null,
    "results": [
        {
            "id": 31,
            "yorumlar": [],
            "isim": "Small Hydroelectric Projects for Rural Development",
            "yazar": "Love",
            "aciklama": "OL9265680M-OL7311021M-9780080259666-0080259669-Love-OL2641989A-Planning and Management (Pergamon policy studies on international development)-Small Hydroelectric Projects for Rural Development-/works/OL285249W-Pergamon Pr",
            "yaratilma_tarihi": "2020-10-04T12:58:42.032723Z",
            "güncellenme_tarihi": "2020-10-04T12:58:42.032778Z",
            "yayın_tarihi": "2015-03-23T10:30:17Z"
        },
/// devamı alınmamıştır
```


 Burada dikkat etmemiz gereken nokta, pagination dan sonra PageNumberPagination sınıfını getirmemiz.  Aşağıdaki gibi bir global policy’de tanımlayabiliriz:

settings.py
```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
}
```

Yukarıdaki global policy’mizde LimitOffsetPagination’ı kullanarak daha farklı bir URL yapısı oluşturduk: 

```json
{
    "count": 100,
    "next": "http://127.0.0.1:8000/api/kitaplar/?limit=10&offset=10", ### URL Endpoint yapısı değişti
    "previous": null,
    "results": [
        {
            "id": 31,
            "yorumlar": [],
            "isim": "Small Hydroelectric Projects for Rural Development",
            "yazar": "Love",
            "aciklama": "OL9265680M-OL7311021M-9780080259666-0080259669-Love-OL2641989A-Planning and Management (Pergamon policy studies on international development)-Small Hydroelectric Projects for Rural Development-/works/OL285249W-Pergamon Pr",
            "yaratilma_tarihi": "2020-10-04T12:58:42.032723Z",
            "güncellenme_tarihi": "2020-10-04T12:58:42.032778Z",
            "yayın_tarihi": "2015-03-23T10:30:17Z"
        },
        {

/// devamı alınmamıştır
```

## 11.1 View Kapsamında Pagination Belirleme
Gerçek bir geliştirme senaryosunda yukarıdaki gibi global policy belirlemek yeterli olmayacaktır. Çoğu zaman kendi pagination sınıflarımızı yazmamız ya da hali hazırda yerleşik pagination sınıfları view bazında değiştirebilmemiz gerekecektir. Concrete viewleri kullanıyorsak, view bazında pagination ayarlamak oldukça basit yapmamız gereken sadece, ilgili yerleşik pagination sınıfını çekmek ve viewimiz içerisinde pagination_class attribute’ünü belirleyerek istediğimiz sınıfı buraya eklemek olacak. Ama biz öncelikle kendimiz iki adet pagination class yazalım ve bu yazdığımız yeni classları viewlerimize ekleyelim.

İlk olarak kitaplar/api klasörümüz içerisinde pagination.py isimli bir dosya yaratıyoruz, yazacağız pagination sınıflarını bu dosya içerisinde yazım, views dosyamızda import edeceğiz.

```python
from rest_framework.pagination import PageNumberPagination

class SmallPagination(PageNumberPagination):
    page_size = '5'
```


Kitaplar/api/views.py
```python
from kitaplar.api.pagination import SmallPagination

class KitapListCreateAPIView(generics.ListCreateAPIView):
    queryset = Kitap.objects.all().order_by('-id')
    serializer_class = KitapSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = LargePagination

```

Burada dikkat edilmesi gereken konu, pagination işleminin tutarsız sonuçlar vermesinin önüne geçebilmek maksadıyla, queryset’imizi mutlaka sıralandırmamız. Örnekte, en son kayıt başa gelecek şekilde, yani en büyük id numarasından en küçük id numarasına göre bir sıralandırma yaptık. 

Biz yukarıdaki örnekte, PageNumberPagination sınıfını kullanarak yeni bir Pagination sınıfı türettik, ama istersek LimitOffsetPagination sınıfını kullanarak da yeni sınıf türetebilirdik.

Eğer yukarıda yazdığımız sınıfı, global policy olarak tüm viewlerimizde kullanmak istiyorsak, settings.py dosyasında aşağıdaki gibi ayarlama yapmamız yeterli olacaktır.

settings.py
```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'kitaplar.api.pagination.LargePagination'
}
```


# djangorestframework_desleri_bolum_2
