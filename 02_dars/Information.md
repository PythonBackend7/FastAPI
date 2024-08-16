# 2-dars Request va Response modellar

1. Pydantic Modellaridan Foydalanish
FastAPI Pydantic modellaridan foydalanadi, bu esa ma'lumotlar validatsiyasini va marshaling jarayonini soddalashtiradi. Pydantic yordamida biz ma'lumotlar turini va strukturani aniq belgilashimiz mumkin.

## Pydantic 
Pydantic - bu Python kutubxonasi bo‘lib, ma'lumotlar validatsiyasi va marshaling jarayonlarini soddalashtirish uchun ishlatiladi. Pydantic yordamida ma'lumotlarni aniqlangan turlarga moslashtirish, ularni validatsiyadan o‘tkazish, va avtomatik ravishda xatolarni qaytarish mumkin.

## Pydantic vazifalari:
1. Ma'lumotlarni validatsiya qilish: Pydantic orqali siz kiruvchi ma'lumotlarning to‘g‘ri turga ega ekanligini tekshirishingiz mumkin. Masalan, string sifatida kelgan ma'lumot float turiga mos kelmaydi, buni Pydantic aniqlaydi va xato qaytaradi.

2. Avtomatik konversiya: Agar kiruvchi ma'lumot noto'g'ri turda bo'lsa, lekin uni to'g'ri turga konvertatsiya qilish mumkin bo'lsa, Pydantic buni avtomatik amalga oshiradi. Masalan, "123" stringini integer (123) ga aylantirish.

3. Xatolarni boshqarish: Agar validatsiya muvaffaqiyatsiz bo‘lsa, Pydantic avtomatik ravishda aniq va tushunarli xato xabarlarini qaytaradi, bu esa dasturchilarga xatolarni tezda aniqlash va tuzatishga yordam beradi.

4. Ma'lumotlarni seriyalashtirish va deserializatsiya qilish: Pydantic yordamida ma'lumotlar modellari avtomatik ravishda JSON formatiga o‘tkaziladi yoki JSON formatidagi ma'lumotlar modellarga o‘tkaziladi.

## Pydantic ning qulayliklari:
1. Tez va qulay foydalanish: Pydantic ni o‘rganish va foydalanish oson, bu esa dasturchilarga validatsiya va marshaling jarayonlarini tezda qo‘llash imkonini beradi.

2. Moslashuvchanlik: Pydantic turli xil ma'lumot turlari va strukturasi bilan ishlashga moslashuvchan. Siz str, int, float, list, dict, va hatto boshqa Pydantic modellarini boshqa modellar ichida ishlatishingiz mumkin.

3. Avtomatik hujjatlar yaratish: FastAPI bilan birga foydalanilganda, Pydantic modellar avtomatik ravishda API hujjatlarida aks etadi, bu esa API foydalanuvchilariga kerakli ma'lumotlarni ko'rish va tushunish uchun qulaylik yaratadi.

4. Xatolarni oson tushunish: Pydantic xatolarni tushunarli va batafsil shaklda qaytaradi, bu esa debugging jarayonini yengillashtiradi.

```shell
from pydantic import BaseModel, Field

class User(BaseModel):
    id: int
    name: str
    age: int = Field(..., ge=18, description="User age must be 18 or older")

user = User(id="123", name="John Doe", age=20)
print(user)
```

Tushuntirish:

User modeli Pydantic asosida yaratilgan bo‘lib, id, name, va age maydonlarini o‘z ichiga oladi.
Field yordamida age maydoni uchun validatsiya qoidasi belgilangan: age kamida 18 ga teng yoki katta bo‘lishi kerak.
id="123" string sifatida berilgan bo‘lsa ham, Pydantic uni avtomatik ravishda integer ga o‘tkazadi.
```shell
# Output
User(id=123, name='John Doe', age=20)
```

Agar validatsiya muvaffaqiyatsiz bo‘lsa, Pydantic aniq xato xabarini qaytaradi, masalan, agar age qiymati 18 dan kichik bo‘lsa, "User age must be 18 or older" degan xabarni ko‘rasiz.
Pydantic kod sifatini oshirish va xatoliklarni kamaytirishga yordam beradigan kuchli vosita hisoblanadi.
