#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
واجهة المستخدم الرسومية (GUI) لأداة فحص التسريبات
توفر واجهة سهلة وجميلة لفحص البيانات
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from leak_checker import LeakChecker
from validators import EmailValidator, PasswordValidator
from datetime import datetime
import json

class LeakCheckerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 DataTrollStealer Leak Checker")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        
        self.checker = LeakChecker()
        self.is_checking = False
        
        self.setup_ui()
    
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        # Header
        header_frame = tk.Frame(self.root, bg="#007bff", height=80)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            header_frame,
            text="🔐 أداة فحص تسريبات البيانات",
            font=("Arial", 20, "bold"),
            bg="#007bff",
            fg="white"
        )
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(
            header_frame,
            text="تحقق مما إذا تم تسريب بريدك أو كلمة مرورك",
            font=("Arial", 10),
            bg="#007bff",
            fg="white"
        )
        subtitle_label.pack()
        
        # Main content
        content_frame = tk.Frame(self.root, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Tab control
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Email Check
        self.email_tab = tk.Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(self.email_tab, text="🔍 فحص البريد الإلكتروني")
        self.setup_email_tab()
        
        # Tab 2: Password Check
        self.password_tab = tk.Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(self.password_tab, text="🔐 فحص كلمة المرور")
        self.setup_password_tab()
        
        # Tab 3: Results
        self.results_tab = tk.Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(self.results_tab, text="📊 النتائج")
        self.setup_results_tab()
    
    def setup_email_tab(self):
        """إعداد تبويب فحص البريد"""
        # Input frame
        input_frame = tk.LabelFrame(
            self.email_tab,
            text="إدخال البريد الإلكتروني",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            padx=15,
            pady=15
        )
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            input_frame,
            text="البريد الإلكتروني:",
            font=("Arial", 10),
            bg="#f0f0f0"
        ).pack(side=tk.LEFT)
        
        self.email_input = tk.Entry(
            input_frame,
            font=("Arial", 10),
            width=40,
            relief=tk.FLAT,
            bd=2
        )
        self.email_input.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        self.email_input.bind('<Return>', lambda e: self.check_email())
        
        # Checkbox for full scan
        self.full_scan_var = tk.BooleanVar()
        full_scan_check = tk.Checkbutton(
            self.email_tab,
            text="فحص شامل متقدم",
            variable=self.full_scan_var,
            font=("Arial", 10),
            bg="#f0f0f0"
        )
        full_scan_check.pack(padx=10, pady=5)
        
        # Button frame
        button_frame = tk.Frame(self.email_tab, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.check_email_btn = tk.Button(
            button_frame,
            text="🔍 فحص البريد",
            font=("Arial", 12, "bold"),
            bg="#28a745",
            fg="white",
            padx=20,
            pady=10,
            relief=tk.FLAT,
            command=self.check_email
        )
        self.check_email_btn.pack(side=tk.LEFT, padx=5)
        
        self.export_email_btn = tk.Button(
            button_frame,
            text="💾 تصدير التقرير",
            font=("Arial", 12, "bold"),
            bg="#007bff",
            fg="white",
            padx=20,
            pady=10,
            relief=tk.FLAT,
            command=self.export_email_report
        )
        self.export_email_btn.pack(side=tk.LEFT, padx=5)
        
        # Results display
        self.email_results = scrolledtext.ScrolledText(
            self.email_tab,
            font=("Arial", 10),
            height=15,
            relief=tk.FLAT,
            bd=2,
            bg="white"
        )
        self.email_results.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.email_results.config(state=tk.DISABLED)
    
    def setup_password_tab(self):
        """إعداد تبويب فحص كلمة المرور"""
        # Input frame
        input_frame = tk.LabelFrame(
            self.password_tab,
            text="إدخال كلمة المرور",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            padx=15,
            pady=15
        )
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            input_frame,
            text="كلمة المرور:",
            font=("Arial", 10),
            bg="#f0f0f0"
        ).pack(side=tk.LEFT)
        
        self.password_input = tk.Entry(
            input_frame,
            font=("Arial", 10),
            width=40,
            show="•",
            relief=tk.FLAT,
            bd=2
        )
        self.password_input.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        self.password_input.bind('<Return>', lambda e: self.check_password())
        
        # Show password checkbox
        self.show_password_var = tk.BooleanVar()
        show_pass_check = tk.Checkbutton(
            self.password_tab,
            text="إظهار كلمة المرور",
            variable=self.show_password_var,
            font=("Arial", 10),
            bg="#f0f0f0",
            command=self.toggle_password_visibility
        )
        show_pass_check.pack(padx=10, pady=5)
        
        # Button frame
        button_frame = tk.Frame(self.password_tab, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.check_password_btn = tk.Button(
            button_frame,
            text="🔐 فحص كلمة المرور",
            font=("Arial", 12, "bold"),
            bg="#dc3545",
            fg="white",
            padx=20,
            pady=10,
            relief=tk.FLAT,
            command=self.check_password
        )
        self.check_password_btn.pack(side=tk.LEFT, padx=5)
        
        # Results display
        self.password_results = scrolledtext.ScrolledText(
            self.password_tab,
            font=("Arial", 10),
            height=15,
            relief=tk.FLAT,
            bd=2,
            bg="white"
        )
        self.password_results.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.password_results.config(state=tk.DISABLED)
    
    def setup_results_tab(self):
        """إعداد تبويب النتائج"""
        self.results_display = scrolledtext.ScrolledText(
            self.results_tab,
            font=("Arial", 10),
            relief=tk.FLAT,
            bd=2,
            bg="white"
        )
        self.results_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.results_display.config(state=tk.DISABLED)
    
    def toggle_password_visibility(self):
        """تبديل رؤية كلمة المرور"""
        if self.show_password_var.get():
            self.password_input.config(show="")
        else:
            self.password_input.config(show="•")
    
    def check_email(self):
        """فحص البريد الإلكتروني"""
        email = self.email_input.get().strip()
        
        if not email:
            messagebox.showwarning("تحذير", "يرجى إدخال بريد إلكتروني")
            return
        
        # التحقق من صحة البريد
        validator = EmailValidator()
        if not validator.validate(email):
            messagebox.showerror("خطأ", "البريد الإلكتروني غير صحيح")
            return
        
        # بدء الفحص في thread منفصل
        self.is_checking = True
        self.check_email_btn.config(state=tk.DISABLED)
        self.email_results.config(state=tk.NORMAL)
        self.email_results.delete('1.0', tk.END)
        self.email_results.insert(tk.END, "⏳ جاري الفحص...\n")
        self.email_results.config(state=tk.DISABLED)
        
        thread = threading.Thread(target=self._check_email_thread, args=(email,))
        thread.daemon = True
        thread.start()
    
    def _check_email_thread(self, email: str):
        """الفحص في thread منفصل"""
        try:
            results = self.checker.check_email(email, full_scan=self.full_scan_var.get())
            self.display_email_results(results)
        except Exception as e:
            self.show_error(f"خطأ: {str(e)}")
        finally:
            self.is_checking = False
            self.check_email_btn.config(state=tk.NORMAL)
    
    def display_email_results(self, results: dict):
        """عرض نتائج فحص البريد"""
        output = ""
        
        if results['found']:
            output += "⚠️  تحذير: تم العثور على تسريبات!\n"
            output += "="*60 + "\n\n"
            output += f"البريد الإلكتروني: {results['email']}\n"
            output += f"عدد التسريبات: {results['breaches_count']}\n"
            output += f"إجمالي الحسابات المسربة: {results['total_exposed_data']:,}\n\n"
            
            output += "📋 التسريبات المكتشفة:\n"
            output += "-"*60 + "\n\n"
            
            for i, breach in enumerate(results['breaches'], 1):
                output += f"{i}. {breach.get('Name', 'Unknown')}\n"
                output += f"   📅 التاريخ: {breach.get('BreachDate', 'N/A')}\n"
                output += f"   👥 عدد الحسابات: {breach.get('PwnCount', 0):,}\n"
                
                data_classes = breach.get('DataClasses', [])
                if data_classes:
                    output += f"   📊 البيانات المسربة: {', '.join(data_classes)}\n"
                
                description = breach.get('Description', '')
                if description:
                    output += f"   📝 الوصف: {description[:100]}...\n"
                
                output += "\n"
        else:
            output += "✅ أخبار سارة!\n"
            output += "="*60 + "\n\n"
            output += f"البريد الإلكتروني: {results['email']}\n\n"
            output += "لم يتم العثور على هذا البريد في أي تسريب معروف!\n"
            output += "هذا يعني أن بريدك آمن (في الوقت الحالي)\n\n"
            output += "نصائح الأمان:\n"
            output += "✓ استخدم كلمات مرور قوية ومختلفة\n"
            output += "✓ فعّل المصادقة الثنائية (2FA)\n"
            output += "✓ راقب حسابك بشكل منتظم\n"
        
        output += f"\n\n⏱️ وقت الفحص: {results['timestamp']}\n"
        output += f"📡 المصادر المفحوصة: {', '.join(results['sources_checked'])}\n"
        
        # عرض النتائج
        self.email_results.config(state=tk.NORMAL)
        self.email_results.delete('1.0', tk.END)
        self.email_results.insert(tk.END, output)
        self.email_results.config(state=tk.DISABLED)
        
        # حفظ النتائج
        self.last_email_results = results
    
    def check_password(self):
        """فحص كلمة المرور"""
        password = self.password_input.get()
        
        if not password:
            messagebox.showwarning("تحذير", "يرجى إدخال كلمة مرور")
            return
        
        self.is_checking = True
        self.check_password_btn.config(state=tk.DISABLED)
        self.password_results.config(state=tk.NORMAL)
        self.password_results.delete('1.0', tk.END)
        self.password_results.insert(tk.END, "⏳ جاري الفحص...\n")
        self.password_results.config(state=tk.DISABLED)
        
        thread = threading.Thread(target=self._check_password_thread, args=(password,))
        thread.daemon = True
        thread.start()
    
    def _check_password_thread(self, password: str):
        """الفحص في thread منفصل"""
        try:
            results = self.checker.check_password(password)
            self.display_password_results(results, password)
        except Exception as e:
            self.show_error(f"خطأ: {str(e)}")
        finally:
            self.is_checking = False
            self.check_password_btn.config(state=tk.NORMAL)
    
    def display_password_results(self, results: dict, password: str):
        """عرض نتائج فحص كلمة المرور"""
        # تقيم قوة كلمة المرور
        validator = PasswordValidator()
        strength = validator.get_strength(password)
        is_common = validator.is_common(password)
        
        output = ""
        
        output += "🔐 نتائج فحص كلمة المرور\n"
        output += "="*60 + "\n\n"
        
        # قوة كلمة المرور
        output += f"💪 قوة كلمة المرور: {strength['level']}\n"
        output += f"   النقاط: {strength['score']}/10\n\n"
        
        if strength['feedback']:
            output += "💡 نصائح للتحسين:\n"
            for tip in strength['feedback']:
                output += f"   • {tip}\n"
            output += "\n"
        
        # فحص التسريب
        if results['found']:
            output += f"⚠️  تحذير: كلمة المرور مسربة!\n\n"
            output += f"❌ ظهرت في {results['appearances']:,} مرة في التسريبات\n\n"
            output += "إجراءات فورية:\n"
            output += "1. غيّر هذه الكلمة في جميع الحسابات\n"
            output += "2. تجنب استخدامها مجدداً\n"
            output += "3. استخدم كلمة مرور جديدة قوية\n"
        else:
            output += f"✅ {results['status']}\n\n"
            output += "هذه كلمة مرور آمنة (لم تظهر في التسريبات المعروفة)\n"
        
        if is_common:
            output += "\n⚠️  تحذير: هذه كلمة مرور شائعة جداً!\n"
            output += "استخدم كلمة مرور فريدة وقوية\n"
        
        # نصائح الأمان العامة
        output += "\n" + "="*60 + "\n"
        output += "🛡️  نصائح الأمان العامة:\n"
        output += "✓ استخدم كلمات مرور مختلفة لكل موقع\n"
        output += "✓ استخدم مدير كلمات مرور\n"
        output += "✓ فعّل المصادقة الثنائية (2FA)\n"
        output += "✓ تحديث كلمات المرور بانتظام\n"
        
        self.password_results.config(state=tk.NORMAL)
        self.password_results.delete('1.0', tk.END)
        self.password_results.insert(tk.END, output)
        self.password_results.config(state=tk.DISABLED)
        
        self.last_password_results = results
    
    def export_email_report(self):
        """تصدير تقرير البريل"""
        if not hasattr(self, 'last_email_results'):
            messagebox.showwarning("تحذير", "لم يتم إجراء فحص بعد")
            return
        
        filename = f"report_email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.last_email_results, f, ensure_ascii=False, indent=2)
        
        messagebox.showinfo("نجاح", f"تم تصدير التقرير: {filename}")
    
    def show_error(self, message: str):
        """عرض رسالة خطأ"""
        messagebox.showerror("خطأ", message)

def main():
    root = tk.Tk()
    app = LeakCheckerGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
