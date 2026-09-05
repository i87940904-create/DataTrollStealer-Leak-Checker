#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
وحدة التحقق من صحة البيانات
"""

import re
import string
from typing import Dict, Any

class EmailValidator:
    """التحقق من صحة البريد الإلكتروني"""
    
    EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    def validate(self, email: str) -> bool:
        """التحقق من صحة البريد الإلكتروني"""
        if not email or len(email) > 254:
            return False
        return bool(re.match(self.EMAIL_REGEX, email))
    
    def is_disposable(self, email: str) -> bool:
        """التحقق من كون البريد مؤقتاً"""
        disposable_domains = [
            'tempmail.com', '10minutemail.com', 'guerrillamail.com',
            'mailinator.com', 'temp-mail.org', 'throwaway.email'
        ]
        domain = email.split('@')[1].lower() if '@' in email else ''
        return domain in disposable_domains

class PasswordValidator:
    """التحقق من قوة كلمة المرور"""
    
    def get_strength(self, password: str) -> Dict[str, Any]:
        """تقييم قوة كلمة المرور"""
        score = 0
        feedback = []
        
        # Length check
        if len(password) >= 8:
            score += 2
        elif len(password) >= 6:
            score += 1
        else:
            feedback.append('كلمة المرور قصيرة جداً (أقل من 6 أحرف)')
        
        # Uppercase check
        if any(c.isupper() for c in password):
            score += 1
        else:
            feedback.append('أضف أحرفاً كبيرة')
        
        # Lowercase check
        if any(c.islower() for c in password):
            score += 1
        else:
            feedback.append('أضف أحرفاً صغيرة')
        
        # Digits check
        if any(c.isdigit() for c in password):
            score += 2
        else:
            feedback.append('أضف أرقاماً')
        
        # Special characters check
        if any(c in string.punctuation for c in password):
            score += 2
        else:
            feedback.append('أضف رموزاً خاصة')
        
        # Determine level
        if score >= 8:
            level = 'قوية جداً 💪'
        elif score >= 6:
            level = 'قوية 👍'
        elif score >= 4:
            level = 'متوسطة ⚠️'
        elif score >= 2:
            level = 'ضعيفة ❌'
        else:
            level = 'ضعيفة جداً ❌❌'
        
        return {
            'score': min(score, 10),
            'level': level,
            'feedback': feedback,
            'is_strong': score >= 8
        }
    
    def is_common(self, password: str) -> bool:
        """التحقق من كون كلمة المرور شائعة"""
        common_passwords = [
            '123456', 'password', '12345678', 'qwerty', '123456789',
            '12345', '1234', '111111', '1234567', 'dragon', '123123',
            'passw0rd', '000000', 'abc123'
        ]
        return password.lower() in common_passwords
