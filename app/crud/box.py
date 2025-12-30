from sqlalchemy.orm import Session
from app.models.box import Box, BoxMovement

def get_box_by_user_id(db: Session, user_id: int):
    return db.query(Box).filter(Box.user_id == user_id).first()

def create_box(db: Session, user_id: int):
    db_box = Box(user_id=user_id, base_balance=0.0, insurance_balance=0.0)
    db.add(db_box)
    db.commit()
    db.refresh(db_box)
    return db_box

def update_box_balance(db: Session, box: Box, amount: float, is_insurance: bool = False):
    if is_insurance:
        box.insurance_balance += amount
    else:
        box.base_balance += amount
    db.add(box)
    db.commit()
    db.refresh(box)
    return box

def create_movement(
    db: Session, 
    box_id: int, 
    amount: float, 
    movement_type: str, 
    performed_by_id: int, 
    description: str = None, 
    is_insurance: bool = False
):
    db_movement = BoxMovement(
        box_id=box_id, amount=amount, movement_type=movement_type,
        description=description, is_insurance=is_insurance, performed_by_id=performed_by_id
    )
    db.add(db_movement)
    db.commit()
    db.refresh(db_movement)
    return db_movement

