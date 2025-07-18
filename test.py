import random
import string
from models import VerificationCode

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

with app.app_context():
    for _ in range(10):  # 這裡是產生 10 個
        code = generate_code()
        db.session.add(VerificationCode(code=code))
    db.session.commit()
    print("新增 10 組驗證碼成功")

with app.app_context():
    codes = VerificationCode.query.filter_by(used=False).all()
    for c in codes:
        print(c.code)
