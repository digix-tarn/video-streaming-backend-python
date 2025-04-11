

def seconds_to_hms(seconds):
    hours = int(seconds // 3600)  # หาชั่วโมง
    minutes = int((seconds % 3600) // 60)  # หานาที
    remaining_seconds = int(seconds % 60)  # หาวินาทีที่เหลือ

    # ถ้าชั่วโมงเป็น 0 ให้ไม่แสดงชั่วโมง
    if hours > 0:
        return f"{hours:02}:{minutes:02}:{remaining_seconds:02}"
    else:
        return f"{minutes:02}:{remaining_seconds:02}"