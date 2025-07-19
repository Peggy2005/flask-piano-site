# test1.py
from app import db, app
from models import VerificationCode

codes = [
    "ml45Fc", "14y7vE", "agaqXN", "21GyNJ", "R9vunp", "taWAqn", "gr33nX", "vw2pgk", "p5N0Z4", "fCv6jI",
    "r2EiCZ", "AazIxH", "rA8dwM", "Jrf6dj", "0MG523", "YAay67", "fjbC9r", "yDYZhf", "apZ89N", "eFCm32",
    "iqaFOr", "JamzPB", "7C953W", "Ugrl9i", "45sUNp", "ynJBT8", "FRTG7J", "Q07zLK", "M1eF2r", "e13yL9",
    "Se9qlk", "BtsMvJ", "EaApwi", "D8lYUL", "gHyyp1", "nOaqO6", "ClSIBE", "fzmtdm", "jxD8dK", "mSLUdo",
    "cwwDq0", "TjH8EA", "UnJbGs", "qZgnmA", "eCx2Fu", "v092RF", "kKOCnB", "AGDAKh", "HqCg1M", "kiJi7h"
]

with app.app_context():
    for code in codes:
        if not VerificationCode.query.filter_by(code=code).first():
            db.session.add(VerificationCode(code=code, used=False))
    db.session.commit()
    print("驗證碼寫入完成！")
