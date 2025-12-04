# Import Class และ Exception ที่สร้างไว้ในไฟล์ password_validator.py
from password_validator import PasswordValidator, InvalidPasswordError

def get_user_input():
    """รับชื่อผู้ใช้และรหัสผ่านจากผู้ใช้"""
    print("\n--- โปรแกรมตรวจสอบรหัสผ่าน ---")
    
    # 1. รับชื่อผู้ใช้
    username = input("กรุณาตั้งชื่อผู้ใช้ (Username): ")
    
    # 2. รับรหัสผ่าน
    password = input("กรุณาตั้งรหัสผ่าน (Password): ")
    
    return username, password

def display_validation_result(username: str, password: str, validator: PasswordValidator):
    """ตรวจสอบรหัสผ่านและแสดงผลลัพธ์พร้อม Error Handling"""
    
    print("-" * 40)
    print(f"กำลังตรวจสอบรหัสผ่านสำหรับผู้ใช้: {username}")
    
    try:
        # เรียกใช้เมธอดตรวจสอบจาก Class ที่ Import มา
        validator.validate(password)
        
        # ถ้ารหัสผ่านถูกต้อง
        print(f"✅ ยินดีด้วย! รหัสผ่าน '{password}' ถูกต้องตามเงื่อนไขทั้งหมด")
        
    except InvalidPasswordError as e:
        # จัดการข้อผิดพลาดเฉพาะที่เกี่ยวกับรหัสผ่าน
        print(f"❌ สถานะ: รหัสผ่านไม่ผ่าน ({e.args[0]})")
        print("   >>> จุดที่ต้องแก้ไข:")
        for error_message in e.errors:
            print(f"   - {error_message}")
            
    except Exception as e:
        # จัดการข้อผิดพลาดอื่นๆ ที่อาจเกิดขึ้น
        print(f"⚠️ เกิดข้อผิดพลาดที่ไม่คาดคิด: {e}")
        
    print("-" * 40)

if __name__ == "__main__":
    # 1. สร้าง Object ของ Validator
    validator = PasswordValidator()
    
    # 2. วนลูปเพื่อให้ผู้ใช้ลองตั้งรหัสผ่านได้หลายครั้ง
    while True:
        try:
            username, password = get_user_input()
            display_validation_result(username, password, validator)
            
            # ถามผู้ใช้ว่าต้องการลองอีกครั้งหรือไม่
            retry = input("ต้องการลองตรวจสอบรหัสผ่านอีกครั้งหรือไม่? (y/n): ").lower()
            if retry != 'y':
                break
                
        except EOFError:
            # จัดการเมื่อผู้ใช้กด Ctrl+D/Ctrl+Z
            print("\nปิดโปรแกรม...")
            break
