from fastapi import Depends, HTTPException, UploadFile, File, APIRouter

from sqlalchemy.orm import Session
from datetime import datetime
import csv
import io

from app.repositories import models
from app.repositories.models import Lots, User, Order
from app.settings import engine, get_db
from app.api.auth.security import (
    authenticate_user, create_access_token,
    get_password_hash,
    get_current_user,
    get_current_active_user,
    get_current_admin_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.api.lots.data_validation import get_price_validation_ranges

create_lot_router = APIRouter()

@create_lot_router.post("/upload-csv")
async def upload_csv(
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        # current_user: User = Depends(get_current_user)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Загруженный файл должен быть в формате CSV")

    try:
        price_ranges = get_price_validation_ranges(db)

        contents = await file.read()
        decoded_content = contents.decode('utf-8')

        fieldnames = ['lot_date', 'ksss_nb_code', 'ksss_fuel_code', 'start_volume_liters', 'price', 'price_for_1ton']

        reader = csv.DictReader(io.StringIO(decoded_content), fieldnames=fieldnames)

        has_header = True
        try:
            first_line = next(reader)
            if first_line and all(key in first_line.values() for key in fieldnames):
                has_header = True
            else:
                reader = csv.DictReader(io.StringIO(decoded_content), fieldnames=fieldnames)
                has_header = False
        except StopIteration:
            return {"status": "error", "detail": "Загруженный файл не содержит данных"}

        processed_rows = 0
        skipped_rows = 0
        errors = []

        for row_num, row in enumerate(reader, 1):
            try:
                if row_num == 1 and has_header:
                    continue

                try:
                    date_formats = ['%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y']
                    lot_date = None

                    for date_format in date_formats:
                        try:
                            lot_date = datetime.strptime(row['lot_date'], date_format)
                            break
                        except ValueError:
                            continue

                    if lot_date is None:
                        raise ValueError(f"Неверный формат даты: {row['lot_date']}")

                    price = int(row['price'])
                    price_for_1ton = int(row['price_for_1ton'])

                    price_in_range = True
                    price_error_message = ""

                    if price_ranges['price']['min'] is not None and price_ranges['price']['max'] is not None:
                        if price < price_ranges['price']['min'] or price > price_ranges['price']['max']:
                            price_in_range = False
                            price_error_message += f"Цена ({price}) находится вне допустимого диапазона ({int(price_ranges['price']['min'])} - {int(price_ranges['price']['max'])}). "

                    if price_ranges['price_for_1ton']['min'] is not None and price_ranges['price_for_1ton'][
                        'max'] is not None:
                        if price_for_1ton < price_ranges['price_for_1ton']['min'] or price_for_1ton > \
                                price_ranges['price_for_1ton']['max']:
                            price_in_range = False
                            price_error_message += f"Цена за 1 тонну ({price_for_1ton}) находится вне допустимого диапазона ({int(price_ranges['price_for_1ton']['min'])} - {int(price_ranges['price_for_1ton']['max'])})."

                    if not price_in_range:
                        skipped_rows += 1
                        errors.append(f"Строка {row_num}: {price_error_message}")
                        continue

                    lot = models.Lots(
                        date=lot_date,
                        code_KSSS_NB=int(row['ksss_nb_code']),
                        code_KSSS_fuel=int(row['ksss_fuel_code']),
                        start_weight=int(row['start_volume_liters']),
                        current_weight=int(row['start_volume_liters']),
                        status="Подтвержден",
                        price=price,
                        price_for_1ton=price_for_1ton
                    )

                    db.add(lot)
                    processed_rows += 1

                except (ValueError, TypeError) as e:
                    skipped_rows += 1
                    errors.append(f"Строка {row_num}: {str(e)}")
                    continue

            except Exception as e:
                skipped_rows += 1
                errors.append(f"Строка {row_num}: Непредвиденная ошибка - {str(e)}")
                continue

        db.commit()

        price_info = {}
        if price_ranges['price']['avg'] is not None:
            price_info['price_avg'] = price_ranges['price']['avg']
            price_info['price_min'] = price_ranges['price']['min']
            price_info['price_max'] = price_ranges['price']['max']

        if price_ranges['price_for_1ton']['avg'] is not None:
            price_info['price_for_1ton_avg'] = price_ranges['price_for_1ton']['avg']
            price_info['price_for_1ton_min'] = price_ranges['price_for_1ton']['min']
            price_info['price_for_1ton_max'] = price_ranges['price_for_1ton']['max']

        response = {
            "status": "success",
            "filename": file.filename,
            "processed_rows": processed_rows,
            "skipped_rows": skipped_rows,
            "price_ranges": price_info
        }

        if errors:
            response["errors"] = errors[:10]
            if len(errors) > 10:
                response["errors"].append(f"... и еще {len(errors) - 10} ошибок")

        return response

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при обработке файла: {str(e)}")