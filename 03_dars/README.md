# 3-dars: Routing va Path Operations and Dependency Injection
Bu darsda FastAPI da routing va path operations haqida tushuncha olasiz. Bu sizga API marshrutlash va path/query parametrlar bilan ishlashda yordam beradi.

Dars mavzulari:
* Path Operations va Path Parameters
* Query Parameters
* Dinamik Yo'llar Yaratish
* Path Operations Dekoratorlari

1. Path Operations va Path Parameters
Path operations - bu FastAPI da API marshrutlarini aniqlash usuli. Har bir path operation bitta HTTP metodiga (GET, POST, PUT, DELETE, va boshqalar) mos keladi.

### Oddiy Path Operations:
```shell
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}
```

Path Parameters (Dinamik Yo‘llar):
Path parametrlar yordamida yo‘llarni dinamik qilish mumkin. Masalan, foydalanuvchining id sini olish:
```shell
@app.get("/users/{user_id}")
def read_user(user_id: int):
    return {"user_id": user_id}

```

Yuqoridagi misolda user_id dinamik parametr bo‘lib, GET /users/123 kabi so‘rovlar uchun mos keladi va user_id=123 qiymatini qaytaradi.

2. Query Parameters
Query parametrlar URL ning so'ngida ? belgisidan keyin keladigan parametrlar. Ular HTTP so'rovlarida qo'shimcha ma'lumotlarni uzatish uchun ishlatiladi.

Oddiy Query Parameters:
```shell
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

```
Yuqoridagi misolda skip va limit query parametrlar hisoblanadi. Masalan, GET /items/?skip=5&limit=20 so‘rovi {"skip": 5, "limit": 20} ni qaytaradi.

3. Dinamik Yo'llar Yaratish
Path parametrlarni ishlatib, dinamik yo‘llar yaratish mumkin. Masalan, mahsulot turiga qarab turli xil yo‘llarni aniqlash:
```shell
@app.get("/products/{product_type}/{product_id}")
def read_product(product_type: str, product_id: int):
    return {"product_type": product_type, "product_id": product_id}

```

Yuqoridagi misolda product_type va product_id dinamik parametrlar sifatida ishlatiladi. Masalan, GET /products/electronics/42 so‘rovi {"product_type": "electronics", "product_id": 42} ni qaytaradi.

4. Path Operations Dekoratorlari
FastAPI da @app.get, @app.post, @app.put, @app.delete kabi dekoratorlar path operations deb ataladi. Ular HTTP metodlariga mos keladi va turli xil so'rovlarni aniqlash uchun ishlatiladi.

### GET Method:
```shell
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

```
### POST Method:
```shell
@app.post("/items/")
def create_item(name: str, price: float):
    return {"name": name, "price": price}

```
### PUT Method:
```shell
@app.put("/items/{item_id}")
def update_item(item_id: int, name: str, price: float):
    return {"item_id": item_id, "name": name, "price": price}

```
### DELETE Method:
```shell
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"message": f"Item {item_id} has been deleted"}

```
## Yakuniy Qo'shimchalar:
* Path Parameters - URL ichida dinamik qiymatlar olish uchun ishlatiladi.
* Query Parameters - URL query string orqali parametrlar uzatish uchun ishlatiladi.
* Path Operations Dekoratorlari - HTTP metodlariga mos keladi va API marshrutlarini aniqlash uchun ishlatiladi.

#  Dependency Injection

Ushbu darsda siz FastAPI da dependency injection tushunchasini o‘rganasiz. Dependency injection - bu kodni qayta foydalanish, modullikni oshirish va testlashni osonlashtirish uchun ishlatiladigan kuchli texnika.

Dars mavzulari:
* Dependency Injection tushunchasi
* Bir nechta dependency ni boshqarish
* Global va local dependency lar bilan ishlash

1. Dependency Injection tushunchasi
Dependency Injection - bu FastAPI'da komponentlar o'rtasida bog'lanishlarni boshqarish usuli bo'lib, funksiyalarga (yoki marshrutlarga) boshqa funksiyalarni yoki xizmatlarni "in'ektsiya" qilish imkonini beradi. Bu usul yordamida kodni modullashtirish, qayta foydalanish va testlash osonlashadi.
```shell
from fastapi import FastAPI, Depends

app = FastAPI()

def common_dependency():
    return {"message": "This is a common dependency"}

@app.get("/items/")
def read_items(common: dict = Depends(common_dependency)):
    return {"common": common}

```
Bu yerda common_dependency funksiyasi read_items marshrutiga dependency sifatida in'ektsiya qilinadi. Depends() funksiyasi yordamida dependency aniqlanadi.

2. Bir nechta dependency ni boshqarish
Bir nechta dependency ni boshqarish uchun bir necha Depends() chaqiruvlarini birgalikda ishlatishingiz mumkin.

Bir Nechta Dependency Misoli:
```shell
def query_params(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

def user_authentication(token: str):
    if token != "supersecrettoken":
        raise HTTPException(status_code=400, detail="Invalid token")
    return {"user": "authenticated"}

@app.get("/items/")
def read_items(common: dict = Depends(common_dependency), 
               query: dict = Depends(query_params), 
               user: dict = Depends(user_authentication)):
    return {"common": common, "query": query, "user": user}

```

Bu misolda read_items marshruti uchta dependency dan foydalanadi: common_dependency, query_params, va user_authentication. Bularning barchasi Depends() yordamida boshqariladi.

3. Global va Local Dependency lar bilan ishlash
FastAPI da dependency larni global yoki local darajada boshqarish mumkin.

### Global Dependency:
Global dependency - bu barcha marshrutlar uchun bir xil dependency ni qo‘llash usuli.
```shell
@app.middleware("http")
async def global_dependency(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Global-Dependency"] = "This is a global dependency"
    return response

```

Bu holatda, global_dependency barcha so‘rovlar uchun amal qiladi va HTTP javobiga qo‘shimcha header qo‘shadi.

### Local Dependency:
Local dependency - faqat bitta marshrut yoki funksiyaga in'ektsiya qilinadi, oldingi misollarda ko'rsatilganidek.
```shell
@app.get("/users/")
def read_users(user: dict = Depends(user_authentication)):
    return {"user": user}

```
Bu yerda user_authentication faqat read_users marshruti uchun qo‘llaniladi.

## Yakuniy Qo‘shimchalar:
* Dependency Injection - funksiyalarga boshqa xizmatlarni in'ektsiya qilish imkonini beradi.
* Bir nechta dependency birgalikda boshqarilishi mumkin.
* Global dependency barcha marshrutlar uchun qo‘llanadi, local dependency esa faqat tanlangan marshrutlar uchun.
