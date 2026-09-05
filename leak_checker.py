#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
وحدة المدقق الأساسية لفحص التسريبات
تتصل مباشرة بـ APIs حقيقية وموثوقة
"""

import requests
import hashlib
import time
from typing import Dict, List, Any, Optional
from datetime import datetime

class LeakChecker:
    """فئة رئيسية للتحقق من التسريبات"""
    
    # API endpoints حقيقية
    HIBP_API = "https://haveibeenpwned.com/api/v3"
    HIBP_PASSWORD_API = "https://api.pwnedpasswords.com"
    MOZILLA_API = "https://monitor.mozilla.org/api/v1/scan"
    
    def __init__(self, timeout: int = 15):
        """
        تهيئة المدقق
        
        Args:
            timeout: وقت انتظار الاتصال بالثواني
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'DataTrollStealer-Leak-Checker/1.0.0',
            'Accept': 'application/json'
        })
        self.cache = {}
        self.rate_limit_remaining = None
        self.rate_limit_reset = None
    
    def check_email(self, email: str, full_scan: bool = False) -> Dict[str, Any]:
        """
        فحص البريد الإلكتروني في التسريبات المعروفة
        يستخدم مصادر حقيقية وموثوقة
        
        Args:
            email: البريد الإلكتروني للفحص
            full_scan: فحص شامل من جميع المصادر
            
        Returns:
            قاموس بنتائج الفحص الفعلية
        """
        results = {
            'email': email,
            'found': False,
            'breaches_count': 0,
            'breaches': [],
            'pastes': [],
            'sources_checked': [],
            'total_exposed_data': 0,
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"🔍 جاري فحص البريد: {email}")
        
        # Check HIBP - المصدر الرئيسي والموثوق
        print("   📡 الاتصال بـ Have I Been Pwned...")
        hibp_results = self._check_hibp_email(email)
        if hibp_results:
            results['found'] = True
            results['breaches'].extend(hibp_results['breaches'])
            results['pastes'].extend(hibp_results['pastes'])
            results['sources_checked'].append('Have I Been Pwned')
            
            # عد السجلات المسربة
            for breach in hibp_results['breaches']:
                results['total_exposed_data'] += breach.get('PwnCount', 0)
        
        # Check Mozilla Monitor
        print("   📡 الاتصال بـ Mozilla Monitor...")
        mozilla_results = self._check_mozilla_email(email)
        if mozilla_results:
            results['found'] = True
            results['breaches'].extend(mozilla_results['breaches'])
            results['sources_checked'].append('Mozilla Monitor')
        
        # إزالة التكرارات
        results['breaches'] = self._remove_duplicate_breaches(results['breaches'])
        results['breaches_count'] = len(results['breaches'])
        
        # Sort by date
        results['breaches'].sort(
            key=lambda x: x.get('BreachDate', ''), 
            reverse=True
        )
        
        return results
    
    def check_password(self, password: str) -> Dict[str, Any]:
        """
        فحص كلمة المرور باستخدام Pwned Passwords API
        استخدام k-anonymity للأمان والخصوصية
        
        Args:
            password: كلمة المرور للفحص
            
        Returns:
            قاموس بنتائج الفحص
        """
        results = {
            'found': False,
            'appearances': 0,
            'secure': True,
            'status': 'آمنة ✓'
        }
        
        try:
            # Hash the password using SHA-1
            sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
            
            # Split hash: first 5 characters + rest
            prefix = sha1_hash[:5]
            suffix = sha1_hash[5:]
            
            # Query Pwned Passwords API
            url = f"{self.HIBP_PASSWORD_API}/range/{prefix}"
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                # البحث عن suffix في الإجابة
                for line in response.text.split('\r\n'):
                    if ':' in line:
                        hash_suffix, count = line.split(':')
                        if hash_suffix == suffix:
                            results['found'] = True
                            results['appearances'] = int(count)
                            results['secure'] = False
                            results['status'] = f'مسربة في {count} مرة ⚠️'
                            break
                
                if not results['found']:
                    results['status'] = 'لم تظهر في أي تسريب معروف ✓'
            else:
                results['error'] = f"خطأ API: {response.status_code}"
            
        except Exception as e:
            results['error'] = f"خطأ في الفحص: {str(e)}"
            results['status'] = 'خطأ في الاتصال'
        
        return results
    
    def _check_hibp_email(self, email: str) -> Optional[Dict[str, Any]]:
        """فحص البريد على HIBP - المصدر الموثوق"""
        results = {'breaches': [], 'pastes': []}
        
        try:
            # فحص التسريبات
            url = f"{self.HIBP_API}/breachedaccount/{email}"
            response = self.session.get(url, timeout=self.timeout)
            
            # حفظ معلومات Rate Limit
            if 'X-RateLimit-Remaining' in response.headers:
                self.rate_limit_remaining = response.headers['X-RateLimit-Remaining']\n            if 'X-RateLimit-Reset' in response.headers:
                self.rate_limit_reset = response.headers['X-RateLimit-Reset']
            
            if response.status_code == 200:
                breaches = response.json()
                results['breaches'] = [
                    {
                        'Name': b.get('Name', 'Unknown'),
                        'BreachDate': b.get('BreachDate', 'N/A'),
                        'Title': b.get('Title', b.get('Name')),
                        'Domain': b.get('Domain', 'N/A'),
                        'PwnCount': b.get('PwnCount', 0),
                        'Description': b.get('Description', 'لا توجد وصفة متاحة'),
                        'DataClasses': b.get('DataClasses', []),
                        'IsVerified': b.get('IsVerified', False),
                        'IsFabricated': b.get('IsFabricated', False),
                        'IsRetired': b.get('IsRetired', False),
                        'IsSpamList': b.get('IsSpamList', False),
                        'LogoPath': b.get('LogoPath', ''),
                        'source': 'HIBP'
                    }
                    for b in breaches
                ]
                print(f"✅ عثر على {len(breaches)} تسريب")
            
            elif response.status_code == 404:
                print("✅ لم يتم العثور على التسريبات")
                results['breaches'] = []
            
            elif response.status_code == 429:
                print("⚠️  عدد الطلبات كثير جداً - حاول لاحقاً")
                results['error'] = 'Rate limit exceeded'
            
            # فحص Pastes
            time.sleep(1)  # تجنب Rate Limiting
            paste_url = f"{self.HIBP_API}/pasteaccount/{email}"
            paste_response = self.session.get(paste_url, timeout=self.timeout)
            
            if paste_response.status_code == 200:
                pastes = paste_response.json()
                results['pastes'] = [
                    {
                        'Source': p.get('Source', 'N/A'),
                        'Id': p.get('Id', 'N/A'),
                        'Title': p.get('Title', 'N/A'),
                        'Date': p.get('Date', 'N/A'),
                        'EmailCount': p.get('EmailCount', 0)
                    }
                    for p in pastes
                ]
                if results['pastes']:
                    print(f"⚠️  عثر على {len(pastes)} في المعجنات")
            
            return results
            
        except requests.exceptions.Timeout:
            print("❌ انتهت مهلة الاتصال - تحقق من اتصالك بالإنترنت")
            return None
        except requests.exceptions.ConnectionError:
            print("❌ خطأ في الاتصال - تحقق من الإنترنت")
            return None
        except Exception as e:
            print(f"❌ خطأ: {str(e)}")
            return None
    
    def _check_mozilla_email(self, email: str) -> Optional[Dict[str, Any]]:
        """فحص البريد على Mozilla Monitor"""
        results = {'breaches': []}
        
        try:
            params = {'email': email}
            response = self.session.get(self.MOZILLA_API, params=params, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('breaches'):
                    results['breaches'] = [
                        {
                            'Name': b.get('name', 'Unknown'),
                            'BreachDate': b.get('date', 'N/A'),
                            'Title': b.get('name'),
                            'Description': b.get('description', ''),
                            'PwnCount': b.get('compromised_accounts', 0),
                            'source': 'Mozilla Monitor'
                        }
                        for b in data['breaches']
                    ]
                    print(f"✅ Mozilla عثر على {len(data['breaches'])} تسريب")
            
            return results
            
        except Exception as e:
            print(f"⚠️  خطأ في Mozilla Monitor: {str(e)}")
            return results
    
    def _remove_duplicate_breaches(self, breaches: List[Dict]) -> List[Dict]:
        """إزالة التسريبات المكررة"""
        seen = {}
        unique = []
        
        for breach in breaches:
            name = breach.get('Name', '')
            if name not in seen:
                seen[name] = True
                unique.append(breach)
        
        return unique
    
    def get_detailed_info(self, email: str) -> Dict[str, Any]:
        """الحصول على معلومات مفصلة عن التسريبات"""
        results = self.check_email(email)
        
        info = {
            'email': email,
            'is_breached': results['found'],
            'total_breaches': results['breaches_count'],
            'exposed_accounts': results['total_exposed_data'],
            'breaches': []
        }
        
        for breach in results['breaches']:
            info['breaches'].append({
                'name': breach.get('Name'),
                'date': breach.get('BreachDate'),
                'exposed_count': breach.get('PwnCount'),
                'data_types': breach.get('DataClasses', []),
                'description': breach.get('Description', '')
            })
        
        return info
    
    def clear_cache(self):
        """مسح الذاكرة المؤقتة"""
        self.cache.clear()
    
    def close(self):
        """إغلاق الجلسة"""
        self.session.close()
