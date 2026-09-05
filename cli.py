#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
تطبيق سطر الأوامر (CLI) المحسّن لأداة فحص التسريبات
"""

import argparse
import sys
import json
from datetime import datetime
from colorama import init, Fore, Style
from leak_checker import LeakChecker
from validators import EmailValidator, PasswordValidator

init(autoreset=True)

def print_banner():
    """طباعة شعار الأداة"""
    banner = f"""
    {Fore.CYAN}
    ╔═══════════════════════════════════════════════════════════╗
    ║  {Fore.YELLOW}🔐 DataTrollStealer Leak Checker{Fore.CYAN}              ║
    ║  {Fore.YELLOW}أداة فحص تسريبات البيانات{Fore.CYAN}                     ║
    ║  {Fore.YELLOW}Version 2.0.0 - مع واجهة رسومية وCLI{Fore.CYAN}          ║
    ╚═══════════════════════════════════════════════════════════╝
    {Style.RESET_ALL}
    """
    print(banner)

def print_info(message):
    print(f"{Fore.BLUE}[*]{Style.RESET_ALL} {message}")

def print_success(message):
    print(f"{Fore.GREEN}[✓]{Style.RESET_ALL} {message}")

def print_warning(message):
    print(f"{Fore.YELLOW}[!]{Style.RESET_ALL} {message}")

def print_error(message):
    print(f"{Fore.RED}[✗]{Style.RESET_ALL} {message}")

def display_email_results(results):
    """عرض نتائج فحص البريل"""
    print("\n" + "="*70)
    
    if results['found']:
        print_warning(f"تم العثور على {results['breaches_count']} تسريب!")
        print(f"إجمالي الحسابات المسربة: {results['total_exposed_data']:,}\n")
        
        print(f"{Fore.YELLOW}📋 قائمة التسريبات:{Style.RESET_ALL}")
        print("-"*70)
        
        for i, breach in enumerate(results['breaches'], 1):
            print(f"\n{i}. {Fore.RED}{breach.get('Name')}{Style.RESET_ALL}")
            print(f"   📅 التاريخ: {breach.get('BreachDate')}")
            print(f"   👥 عدد الحسابات: {breach.get('PwnCount'):,}")
            
            if breach.get('DataClasses'):
                print(f"   📊 البيانات المسربة: {', '.join(breach['DataClasses'])}")
            
            if breach.get('Description'):
                desc = breach['Description']
                if len(desc) > 100:
                    desc = desc[:100] + "..."
                print(f"   📝 {desc}")
    else:
        print_success("✅ البريد الإلكتروني آمن ولم يتم العثور عليه في أي تسريب معروف")
        print("\n🛡️  نصائح الأمان:")
        print("   ✓ استخدم كلمات مرور قوية ومختلفة")
        print("   ✓ فعّل المصادقة الثنائية (2FA)")
        print("   ✓ راقب حسابك بشكل منتظم")
    
    print(f"\n📡 المصادر المفحوصة: {', '.join(results['sources_checked'])}")
    print("="*70)

def display_password_results(results, password):
    """عرض نتائج فحص كلمة المرور"""
    print("\n" + "="*70)
    
    # تقيم قوة كلمة المرور
    validator = PasswordValidator()
    strength = validator.get_strength(password)
    is_common = validator.is_common(password)
    
    print(f"{Fore.CYAN}💪 قوة كلمة المرور: {strength['level']}{Style.RESET_ALL}")
    print(f"   النقاط: {strength['score']}/10")
    
    if strength['feedback']:
        print(f"\n{Fore.YELLOW}💡 نصائح للتحسين:{Style.RESET_ALL}")
        for tip in strength['feedback']:
            print(f"   • {tip}")
    
    print()
    
    if results['found']:
        print_warning(f"كلمة المرور مسربة!")
        print(f"ظهرت في {Fore.RED}{results['appearances']:,}{Style.RESET_ALL} مرة في التسريبات\n")
        print("إجراءات فورية:")
        print("   1. غيّر هذه الكلمة في جميع الحسابات")
        print("   2. تجنب استخدامها مجدداً")
        print("   3. استخدم كلمة مرور جديدة قوية")
    else:
        print_success(f"كلمة المرور آمنة: {results['status']}")
    
    if is_common:
        print_warning("\nهذه كلمة مرور شائعة جداً! استخدم كلمة مرور فريدة")
    
    print("\n" + "="*70)

def main():
    print_banner()
    
    parser = argparse.ArgumentParser(
        description='أداة فحص شاملة لكشف تسريبات بيانات DataTrollStealerLogs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
أمثلة الاستخدام:
  python3 cli.py --email user@example.com
  python3 cli.py --password "mypassword123"
  python3 cli.py --email user@example.com --export json
  python3 cli.py --email user@example.com --full-scan --verbose
        """
    )
    
    parser.add_argument('-e', '--email', type=str, help='البريد الإلكتروني للفحص')
    parser.add_argument('-p', '--password', type=str, help='كلمة المرور للفحص')
    parser.add_argument('--full-scan', action='store_true', help='فحص شامل متقدم')
    parser.add_argument('--export', type=str, choices=['json', 'csv', 'html'], help='تصدير النتائج')
    parser.add_argument('-v', '--verbose', action='store_true', help='عرض تفاصيل كاملة')
    parser.add_argument('--timeout', type=int, default=15, help='وقت انتظار الاتصال')
    parser.add_argument('--gui', action='store_true', help='فتح الواجهة الرسومية')
    
    args = parser.parse_args()
    
    # فتح الواجهة الرسومية إذا طُلب
    if args.gui:
        try:
            from gui import main as gui_main
            gui_main()
            return
        except ImportError:
            print_error("لم يتم العثور على tkinter. تثبيت: sudo apt-get install python3-tk")
            sys.exit(1)
    
    # فحص CLI
    if not args.email and not args.password:
        parser.print_help()
        print_error("\nيجب تحديد --email أو --password")
        sys.exit(1)
    
    try:
        checker = LeakChecker(timeout=args.timeout)
        results = {}
        
        # فحص البريد
        if args.email:
            print_info(f"جاري فحص البريد: {args.email}")
            email_results = checker.check_email(args.email, full_scan=args.full_scan)
            display_email_results(email_results)
            results['email'] = email_results
        
        # فحص كلمة المرور
        if args.password:
            print_info("جاري فحص كلمة المرور...")
            password_results = checker.check_password(args.password)
            display_password_results(password_results, args.password)
            results['password'] = password_results
        
        # تصدير النتائج
        if args.export and results:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{args.export}"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print_success(f"تم تصدير التقرير: {filename}")
        
        print_success("تم إكمال الفحص بنجاح!")
        
    except Exception as e:
        print_error(f"حدث خطأ: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
