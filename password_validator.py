import re
from typing import List, Optional

# ----------------- 1. Custom Exception Block -----------------
class InvalidPasswordError(Exception):
    """
    Custom exception สำหรับรหัสผ่านที่ไม่ผ่านการตรวจสอบ
    เก็บรายการข้อผิดพลาดทั้งหมดไว้ใน attribute 'errors'
    """
    def __init__(self, message: str, errors: Optional[List[str]] = None):
        super().__init__(message)
        self.errors = errors if errors is not None else []

# ----------------- 2. PasswordValidator Class Block -----------------
class PasswordValidator:
    
    # กำหนด Whitelist ของอักขระที่อนุญาตทั้งหมด
    ALLOWED_CHARS_SET = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+=")
    
    # กำหนดความยาวมาตรฐาน
    MIN_LEN = 8
    MAX_LEN = 20

    def __init__(self, min_len: int = MIN_LEN, max_len: int = MAX_LEN):
        self.min_len = min_len
        self.max_len = max_len

    def _collect_structure_errors(self, password: str, errors: List[str]) -> None:
        """
        ตรวจสอบเงื่อนไขบังคับและ Whitelist และเพิ่มข้อผิดพลาดลงในรายการ errors
        """
        
        # 1. ตรวจสอบ Whitelist: ต้องไม่มีอักขระที่ไม่ได้รับอนุญาต
        invalid_chars = set(c for c in password if c not in self.ALLOWED_CHARS_SET)
        if invalid_chars:
            errors.append(f"มีอักขระที่ไม่ได้รับอนุญาต: {' '.join(sorted(invalid_chars))}")
        
        # 2. ตรวจสอบเงื่อนไขบังคับ
        if not re.search(r'[a-z]', password):
            errors.append("ต้องมีตัวอักษรภาษาอังกฤษตัวเล็ก (a-z) อย่างน้อย 1 ตัว")
            
        if not re.search(r'[A-Z]', password):
            errors.append("ต้องมีตัวอักษรภาษาอังกฤษตัวใหญ่ (A-Z) อย่างน้อย 1 ตัว")
            
        if not re.search(r'\d', password):
            errors.append("ต้องมีตัวเลข (0-9) อย่างน้อย 1 ตัว")
            
        # อักขระพิเศษ
        if not re.search(r'[!@#$%^&*()_+=]', password):
            errors.append("ต้องมีอักขระพิเศษ (!@#$%^&*()_+=) อย่างน้อย 1 ตัว")


    def validate(self, password: str) -> bool:
        """
        Public method ตรวจสอบรหัสผ่านตามเงื่อนไขทั้งหมด
        จะโยน InvalidPasswordError พร้อมรายการข้อผิดพลาด ถ้าไม่ผ่าน
        """
        errors: List[str] = []
        
        # 1. ตรวจสอบความยาวก่อน (Fail fast)
        current_len = len(password)
        if not (self.min_len <= current_len <= self.max_len):
            errors.append(f"ความยาวต้องอยู่ระหว่าง {self.min_len} ถึง {self.max_len} ตัวอักษร (ปัจจุบัน: {current_len})")
            raise InvalidPasswordError("รหัสผ่านไม่ผ่านการตรวจสอบความยาว.", errors)

        # 2. ตรวจสอบเงื่อนไขบังคับและ Whitelist
        self._collect_structure_errors(password, errors)
        
        # 3. สรุปผล
        if errors:
            raise InvalidPasswordError("รหัสผ่านไม่ผ่านการตรวจสอบเงื่อนไขบังคับหรือ Whitelist.", errors)
        
        return True
