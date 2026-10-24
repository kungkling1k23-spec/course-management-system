<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ระบบจัดการรายวิชา และระบบสมาชิก</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Google Fonts: Prompt & Kanit -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600;700&family=Prompt:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Prompt', 'Kanit', 'sans-serif'],
                        heading: ['Kanit', 'sans-serif'],
                    }
                }
            }
        }
    </script>
    <style>
        body {
            font-family: 'Prompt', sans-serif;
            background-color: #f8fafc;
        }
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: #f1f5f9;
        }
        ::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }
    </style>
</head>
<body class="text-slate-700 min-h-screen flex flex-col justify-between relative bg-slate-50">

    <!-- Top Navigation Header -->
    <header class="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center text-white shadow-md shadow-indigo-200">
                    <i class="fa-solid fa-graduation-cap text-xl"></i>
                </div>
                <div>
                    <h1 class="text-lg sm:text-xl font-bold font-heading text-slate-800 leading-tight">ระบบจัดการรายวิชา</h1>
                    <p class="text-xs text-slate-500 hidden sm:block">Course Management System with Authentication</p>
                </div>
            </div>

            <!-- Profile & Auth Header Section -->
            <div id="userHeaderSection" class="flex items-center gap-3">
                <!-- Logged In State (Injected by JS) -->
            </div>
        </div>
    </header>

    <!-- Main Content Container -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full flex-grow relative">

        <!-- Unauthenticated Overlay Lock Banner -->
        <div id="authLockOverlay" class="hidden absolute inset-0 z-20 bg-slate-900/20 backdrop-blur-md rounded-3xl flex items-center justify-center p-4">
            <div class="bg-white rounded-3xl p-8 max-w-md w-full shadow-2xl text-center border border-slate-100">
                <div class="w-16 h-16 bg-indigo-100 text-indigo-600 rounded-2xl flex items-center justify-center mx-auto mb-4 text-2xl shadow-inner">
                    <i class="fa-solid fa-lock"></i>
                </div>
                <h2 class="text-xl font-bold text-slate-800 font-heading">เข้าสู่ระบบเพื่อใช้งาน</h2>
                <p class="text-xs text-slate-500 mt-2 mb-6 leading-relaxed">
                    กรุณาเข้าสู่ระบบหรือสมัครสมาชิกเพื่อเข้าจัดการรายวิชา ดูรายละเอียด และเข้าถึงฟีเจอร์ทั้งหมดในระบบ
                </p>
                <div class="flex flex-col gap-2.5">
                    <button onclick="openAuthModal('login')" class="w-full py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-xl shadow-md shadow-indigo-200 transition text-sm">
                        <i class="fa-solid fa-right-to-bracket mr-2"></i>เข้าสู่ระบบ (Login)
                    </button>
                    <button onclick="openAuthModal('register')" class="w-full py-3 bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium rounded-xl transition text-sm">
                        <i class="fa-solid fa-user-plus mr-2"></i>สมัครสมาชิก (Register)
                    </button>
                </div>
            </div>
        </div>

        <!-- Dashboard Content -->
        <div id="dashboardContent" class="transition-all duration-300">
            <!-- Stat Counter Cards -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                <!-- Card 1: Total Courses -->
                <div class="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm flex items-center justify-between">
                    <div>
                        <p class="text-xs font-medium text-slate-500 uppercase tracking-wider">จำนวนรายวิชาทั้งหมด</p>
                        <h3 id="statTotalCourses" class="text-2xl font-bold font-heading text-slate-800 mt-1">0</h3>
                    </div>
                    <div class="w-12 h-12 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center text-xl">
                        <i class="fa-solid fa-book"></i>
                    </div>
                </div>

                <!-- Card 2: Total Credits -->
                <div class="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm flex items-center justify-between">
                    <div>
                        <p class="text-xs font-medium text-slate-500 uppercase tracking-wider">รวมหน่วยกิตทั้งหมด</p>
                        <h3 id="statTotalCredits" class="text-2xl font-bold font-heading text-indigo-600 mt-1">0</h3>
                    </div>
                    <div class="w-12 h-12 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center text-xl">
                        <i class="fa-solid fa-award"></i>
                    </div>
                </div>

                <!-- Card 3: Major / Elective -->
                <div class="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm flex items-center justify-between">
                    <div>
                        <p class="text-xs font-medium text-slate-500 uppercase tracking-wider">วิชาเฉพาะ / วิชาเลือก</p>
                        <h3 id="statMajorCourses" class="text-2xl font-bold font-heading text-emerald-600 mt-1">0</h3>
                    </div>
                    <div class="w-12 h-12 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center text-xl">
                        <i class="fa-solid fa-layer-group"></i>
                    </div>
                </div>

                <!-- Card 4: GE Courses -->
                <div class="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm flex items-center justify-between">
                    <div>
                        <p class="text-xs font-medium text-slate-500 uppercase tracking-wider">วิชาศึกษาทั่วไป (GE)</p>
                        <h3 id="statGeCourses" class="text-2xl font-bold font-heading text-amber-600 mt-1">0</h3>
                    </div>
                    <div class="w-12 h-12 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center text-xl">
                        <i class="fa-solid fa-globe"></i>
                    </div>
                </div>
            </div>

            <!-- Section Layout: Form (Left) & Course Table (Right) -->
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
                
                <!-- Left Column: Add / Edit Form -->
                <div class="lg:col-span-4">
                    <div class="bg-white rounded-2xl border border-slate-200/80 shadow-sm p-6 sticky top-24">
                        <div class="flex items-center justify-between mb-5 pb-3 border-b border-slate-100">
                            <div class="flex items-center gap-2">
                                <i class="fa-solid fa-pen-to-square text-indigo-600 text-lg"></i>
                                <h2 id="formTitle" class="text-lg font-bold font-heading text-slate-800">เพิ่มรายวิชาใหม่</h2>
                            </div>
                            <span id="editBadge" class="hidden text-xs bg-amber-100 text-amber-700 px-2.5 py-1 rounded-full font-medium">
                                กำลังแก้ไข
                            </span>
                        </div>

                        <form id="courseForm" onsubmit="handleFormSubmit(event)" class="space-y-4">
                            <input type="hidden" id="editingId" value="">

                            <!-- รหัสวิชา -->
                            <div>
                                <label class="block text-xs font-medium text-slate-600 mb-1.5" for="courseCode">
                                    รหัสวิชา <span class="text-red-500">*</span>
                                </label>
                                <input type="text" id="courseCode" required placeholder="เช่น CS101 หรือ 01204111"
                                    class="w-full px-3.5 py-2.5 text-sm rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition">
                            </div>

                            <!-- ชื่อวิชา ภาษาไทย -->
                            <div>
                                <label class="block text-xs font-medium text-slate-600 mb-1.5" for="courseNameTh">
                                    ชื่อวิชา (ภาษาไทย) <span class="text-red-500">*</span>
                                </label>
                                <input type="text" id="courseNameTh" required placeholder="เช่น การเขียนโปรแกรมคอมพิวเตอร์"
                                    class="w-full px-3.5 py-2.5 text-sm rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition">
                            </div>

                            <!-- ชื่อวิชา ภาษาอังกฤษ -->
                            <div>
                                <label class="block text-xs font-medium text-slate-600 mb-1.5" for="courseNameEn">
                                    ชื่อวิชา (English)
                                </label>
                                <input type="text" id="courseNameEn" placeholder="e.g. Computer Programming"
                                    class="w-full px-3.5 py-2.5 text-sm rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition">
                            </div>

                            <!-- Row: หน่วยกิต & หมวดหมู่ -->
                            <div class="grid grid-cols-2 gap-3">
                                <div>
                                    <label class="block text-xs font-medium text-slate-600 mb-1.5" for="courseCredits">
                                        หน่วยกิต <span class="text-red-500">*</span>
                                    </label>
                                    <input type="number" id="courseCredits" min="1" max="12" required value="3"
                                        class="w-full px-3.5 py-2.5 text-sm rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition">
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-600 mb-1.5" for="courseCategory">
                                        หมวดหมู่วิชา <span class="text-red-500">*</span>
                                    </label>
                                    <select id="courseCategory" required
                                        class="w-full px-3 py-2.5 text-sm rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition bg-white">
                                        <option value="หมวดวิชาเฉพาะ">หมวดวิชาเฉพาะ</option>
                                        <option value="หมวดวิชาเลือก">หมวดวิชาเลือก</option>
                                        <option value="หมวดวิชาศึกษาทั่วไป (GE)">หมวดศึกษาทั่วไป (GE)</option>
                                        <option value="หมวดวิชาเสรี">หมวดวิชาเสรี</option>
                                    </select>
                                </div>
                            </div>

                            <!-- คำอธิบายรายวิชา -->
                            <div>
                                <label class="block text-xs font-medium text-slate-600 mb-1.5" for="courseDescription">
                                    คำอธิบายรายวิชา (Course Description)
                                </label>
                                <textarea id="courseDescription" rows="3" placeholder="รายละเอียดสังเขปเกี่ยวกับเนื้อหาในวิชา..."
                                    class="w-full px-3.5 py-2.5 text-sm rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition resize-none"></textarea>
                            </div>

                            <!-- Buttons Form Action -->
                            <div class="pt-2 flex items-center gap-2">
                                <button type="submit" id="btnSubmit" class="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2.5 px-4 rounded-xl shadow-md shadow-indigo-100 transition flex items-center justify-center gap-2 text-sm">
                                    <i class="fa-solid fa-plus"></i>
                                    <span>บันทึกรายวิชา</span>
                                </button>
                                <button type="button" onclick="resetForm()" class="bg-slate-100 hover:bg-slate-200 text-slate-600 font-medium py-2.5 px-4 rounded-xl transition text-sm">
                                    ล้างฟอร์ม
                                </button>
                            </div>
                        </form>
                    </div>
                </div>

                <!-- Right Column: Course Table & Actions -->
                <div class="lg:col-span-8">
                    <div class="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">
                        
                        <!-- Search & Filter Controls -->
                        <div class="p-5 border-b border-slate-100 bg-slate-50/50 flex flex-col md:flex-row gap-3 items-center justify-between">
                            <!-- Search Box -->
                            <div class="relative w-full md:w-72">
                                <i class="fa-solid fa-magnifying-glass absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 text-sm"></i>
                                <input type="text" id="searchInput" oninput="renderTable()" placeholder="ค้นหารหัสวิชา หรือชื่อวิชา..."
                                    class="w-full pl-9 pr-3.5 py-2 text-sm rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition bg-white">
                            </div>

                            <!-- Category Filter -->
                            <div class="flex items-center gap-2 w-full md:w-auto">
                                <label class="text-xs text-slate-500 whitespace-nowrap">กรองหมวดหมู่:</label>
                                <select id="categoryFilter" onchange="renderTable()"
                                    class="w-full md:w-auto px-3 py-2 text-sm rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition bg-white">
                                    <option value="ALL">ทั้งหมด</option>
                                    <option value="หมวดวิชาเฉพาะ">หมวดวิชาเฉพาะ</option>
                                    <option value="หมวดวิชาเลือก">หมวดวิชาเลือก</option>
                                    <option value="หมวดวิชาศึกษาทั่วไป (GE)">หมวดศึกษาทั่วไป (GE)</option>
                                    <option value="หมวดวิชาเสรี">หมวดวิชาเสรี</option>
                                </select>
                            </div>
                        </div>

                        <!-- Responsive Data Table -->
                        <div class="overflow-x-auto">
                            <table class="w-full text-left border-collapse">
                                <thead>
                                    <tr class="bg-slate-100/70 border-b border-slate-200 text-slate-600 text-xs font-semibold uppercase tracking-wider">
                                        <th class="py-3.5 px-4">รหัสวิชา</th>
                                        <th class="py-3.5 px-4">ชื่อรายวิชา</th>
                                        <th class="py-3.5 px-4 text-center">หน่วยกิต</th>
                                        <th class="py-3.5 px-4">หมวดหมู่</th>
                                        <th class="py-3.5 px-4 text-center">จัดการ</th>
                                    </tr>
                                </thead>
                                <tbody id="courseTableBody" class="divide-y divide-slate-100 text-sm">
                                    <!-- Table Rows injected via Javascript -->
                                </tbody>
                            </table>
                        </div>

                        <!-- Empty State Container -->
                        <div id="emptyState" class="hidden p-12 text-center">
                            <div class="w-16 h-16 bg-slate-100 text-slate-400 rounded-full flex items-center justify-center mx-auto mb-3 text-2xl">
                                <i class="fa-solid fa-folder-open"></i>
                            </div>
                            <h4 class="text-base font-semibold text-slate-700">ไม่พบข้อมูลรายวิชา</h4>
                            <p class="text-xs text-slate-500 mt-1">ลองเปลี่ยนคำค้นหา หรือเพิ่มรายการวิชาใหม่ผ่านแบบฟอร์มด้านซ้าย</p>
                        </div>

                        <!-- Footer Table Stats -->
                        <div class="p-4 bg-slate-50/50 border-t border-slate-100 text-xs text-slate-500 flex justify-between items-center">
                            <span id="showingCount">แสดง 0 จาก 0 รายการ</span>
                            <button onclick="loadSampleData()" class="text-indigo-600 hover:text-indigo-800 font-medium flex items-center gap-1">
                                <i class="fa-solid fa-rotate-right"></i>รีเซ็ตเป็นข้อมูลวิชาตั้งต้น
                            </button>
                        </div>

                    </div>
                </div>

            </div>
        </div>
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-slate-200 py-4 mt-8">
        <div class="max-w-7xl mx-auto px-4 text-center text-xs text-slate-400">
            © 2026 ระบบจัดการรายวิชา และระบบยืนยันตัวตน (Authentication System)
        </div>
    </footer>

    <!-- Auth Modal (Login / Register Modal) -->
    <div id="authModal" class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 flex items-center justify-center hidden p-4">
        <div class="bg-white rounded-3xl max-w-md w-full p-6 sm:p-8 shadow-2xl relative transform transition-all border border-slate-100">
            <button onclick="closeModal('authModal')" class="absolute top-5 right-5 text-slate-400 hover:text-slate-600 text-lg w-8 h-8 rounded-full flex items-center justify-center hover:bg-slate-100 transition">
                <i class="fa-solid fa-xmark"></i>
            </button>

            <!-- Login View Form -->
            <div id="loginFormView">
                <div class="text-center mb-6">
                    <div class="w-12 h-12 bg-indigo-50 text-indigo-600 rounded-2xl flex items-center justify-center mx-auto mb-3 text-xl">
                        <i class="fa-solid fa-right-to-bracket"></i>
                    </div>
                    <h3 class="text-xl font-bold font-heading text-slate-800">เข้าสู่ระบบ</h3>
                    <p class="text-xs text-slate-500 mt-1">ยินดีต้อนรับกลับเข้าสู่ระบบจัดการรายวิชา</p>
                </div>

                <form onsubmit="handleLogin(event)" class="space-y-4">
                    <div>
                        <label class="block text-xs font-medium text-slate-600 mb-1" for="loginEmail">อีเมล</label>
                        <input type="email" id="loginEmail" required placeholder="name@example.com"
                            class="w-full px-3.5 py-2.5 text-sm rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition">
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-slate-600 mb-1" for="loginPassword">รหัสผ่าน</label>
                        <input type="password" id="loginPassword" required placeholder="••••••••"
                            class="w-full px-3.5 py-2.5 text-sm rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition">
                    </div>
                    <button type="submit" class="w-full py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-xl shadow-md shadow-indigo-100 transition text-sm">
                        เข้าสู่ระบบ
                    </button>
                </form>

                <!-- Demo Account Selector -->
                <div class="mt-5 pt-4 border-t border-slate-100 text-center">
                    <p class="text-xs text-slate-400 mb-2">ทดสอบเข้าสู่ระบบด้วยบัญชี Demo:</p>
                    <div class="flex gap-2 justify-center">
                        <button type="button" onclick="fillDemoUser('teacher')" class="text-xs bg-indigo-50 hover:bg-indigo-100 text-indigo-700 px-3 py-1.5 rounded-lg transition font-medium">
                            <i class="fa-solid fa-user-gear mr-1"></i>อาจารย์ (Demo)
                        </button>
                        <button type="button" onclick="fillDemoUser('student')" class="text-xs bg-slate-100 hover:bg-slate-200 text-slate-700 px-3 py-1.5 rounded-lg transition font-medium">
                            <i class="fa-solid fa-user-graduate mr-1"></i>นักศึกษา (Demo)
                        </button>
                    </div>
                </div>

                <div class="mt-4 text-center">
                    <p class="text-xs text-slate-500">
                        ยังไม่มีบัญชีผู้ใช้? 
                        <button onclick="toggleAuthView('register')" class="text-indigo-600 font-semibold hover:underline ml-1">สมัครสมาชิกที่นี่</button>
                    </p>
                </div>
            </div>

            <!-- Register View Form -->
            <div id="registerFormView" class="hidden">
                <div class="text-center mb-6">
                    <div class="w-12 h-12 bg-emerald-50 text-emerald-600 rounded-2xl flex items-center justify-center mx-auto mb-3 text-xl">
                        <i class="fa-solid fa-user-plus"></i>
                    </div>
                    <h3 class="text-xl font-bold font-heading text-slate-800">สมัครสมาชิก</h3>
                    <p class="text-xs text-slate-500 mt-1">สร้างบัญชีผู้ใช้เพื่อเข้าจัดการรายวิชา</p>
                </div>

                <form onsubmit="handleRegister(event)" class="space-y-3">
                    <div>
                        <label class="block text-xs font-medium text-slate-600 mb-1" for="regFullName">ชื่อ-นามสกุล <span class="text-red-500">*</span></label>
                        <input type="text" id="regFullName" required placeholder="ดร. สมชาย ใจดี หรือ นายสมศักดิ์"
                            class="w-full px-3.5 py-2 text-sm rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition">
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-slate-600 mb-1" for="regEmail">อีเมล <span class="text-red-500">*</span></label>
                        <input type="email" id="regEmail" required placeholder="name@example.com"
                            class="w-full px-3.5 py-2 text-sm rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition">
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-slate-600 mb-1" for="regPassword">รหัสผ่าน <span class="text-red-500">*</span></label>
                        <input type="password" id="regPassword" required minlength="4" placeholder="อย่างน้อย 4 ตัวอักษร"
                            class="w-full px-3.5 py-2 text-sm rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition">
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-slate-600 mb-1" for="regRole">สิทธิ์ผู้ใช้งาน (Role)</label>
                        <select id="regRole" required class="w-full px-3 py-2 text-sm rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition bg-white">
                            <option value="student">นิสิต/นักศึกษา (Student)</option>
                            <option value="teacher">อาจารย์/เจ้าหน้าที่ (Teacher / Staff)</option>
                        </select>
                    </div>
                    <button type="submit" class="w-full py-2.5 mt-2 bg-emerald-600 hover:bg-emerald-700 text-white font-medium rounded-xl shadow-md shadow-emerald-100 transition text-sm">
                        ลงทะเบียนสมัครสมาชิก
                    </button>
                </form>

                <div class="mt-4 text-center border-t border-slate-100 pt-3">
                    <p class="text-xs text-slate-500">
                        มีบัญชีผู้ใช้งานแล้ว? 
                        <button onclick="toggleAuthView('login')" class="text-indigo-600 font-semibold hover:underline ml-1">เข้าสู่ระบบ</button>
                    </p>
                </div>
            </div>
        </div>
    </div>

    <!-- View Course Detail Modal -->
    <div id="detailModal" class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-50 flex items-center justify-center hidden p-4">
        <div class="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl transform transition-all">
            <div class="flex justify-between items-start mb-4">
                <div class="flex items-center gap-3">
                    <span id="modalCodeBadge" class="bg-indigo-100 text-indigo-700 text-xs font-bold px-2.5 py-1 rounded-lg"></span>
                    <h3 class="text-lg font-bold font-heading text-slate-800" id="modalTitleTh"></h3>
                </div>
                <button onclick="closeModal('detailModal')" class="text-slate-400 hover:text-slate-600 text-lg">
                    <i class="fa-solid fa-xmark"></i>
                </button>
            </div>
            
            <div class="space-y-3 border-t border-b border-slate-100 py-4 my-2 text-sm">
                <div>
                    <p class="text-xs text-slate-400 uppercase">ชื่อภาษาอังกฤษ</p>
                    <p id="modalTitleEn" class="text-slate-700 font-medium"></p>
                </div>
                <div class="grid grid-cols-2 gap-2">
                    <div>
                        <p class="text-xs text-slate-400 uppercase">หน่วยกิต</p>
                        <p id="modalCredits" class="text-slate-700 font-semibold"></p>
                    </div>
                    <div>
                        <p class="text-xs text-slate-400 uppercase">หมวดหมู่</p>
                        <p id="modalCategory" class="text-slate-700 font-semibold"></p>
                    </div>
                </div>
                <div>
                    <p class="text-xs text-slate-400 uppercase">คำอธิบายรายวิชา</p>
                    <p id="modalDescription" class="text-slate-600 bg-slate-50 p-3 rounded-xl mt-1 text-xs leading-relaxed"></p>
                </div>
            </div>

            <div class="flex justify-end pt-2">
                <button onclick="closeModal('detailModal')" class="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-sm font-medium rounded-xl transition">
                    ปิดหน้าต่าง
                </button>
            </div>
        </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div id="deleteModal" class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-50 flex items-center justify-center hidden p-4">
        <div class="bg-white rounded-2xl max-w-sm w-full p-6 shadow-2xl text-center transform transition-all">
            <div class="w-14 h-14 bg-red-100 text-red-500 rounded-full flex items-center justify-center mx-auto mb-4 text-2xl">
                <i class="fa-solid fa-triangle-exclamation"></i>
            </div>
            <h3 class="text-lg font-bold font-heading text-slate-800">ยืนยันการลบรายวิชา?</h3>
            <p class="text-xs text-slate-500 mt-2 mb-6">คุณต้องการลบวิชา <span id="deleteCourseName" class="font-semibold text-slate-700"></span> หรือไม่?</p>
            
            <div class="flex gap-3 justify-center">
                <button onclick="closeModal('deleteModal')" class="w-1/2 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-sm font-medium rounded-xl transition">
                    ยกเลิก
                </button>
                <button id="btnConfirmDelete" class="w-1/2 py-2.5 bg-red-600 hover:bg-red-700 text-white text-sm font-medium rounded-xl shadow-md shadow-red-200 transition">
                    ลบข้อมูล
                </button>
            </div>
        </div>
    </div>

    <!-- Toast Notification Box -->
    <div id="toast" class="fixed bottom-5 right-5 z-50 flex items-center gap-3 px-4 py-3 rounded-xl shadow-lg text-white text-sm transform transition-all duration-300 translate-y-20 opacity-0 pointer-events-none">
        <i id="toastIcon" class="fa-solid"></i>
        <span id="toastMessage"></span>
    </div>

    <!-- Application Script Logic -->
    <script>
        // Demo Initial Accounts
        const defaultUsers = [
            {
                id: 'usr_teacher',
                fullName: 'ดร. ประเสริฐ วิชาการ',
                email: 'teacher@demo.com',
                password: 'password',
                role: 'teacher'
            },
            {
                id: 'usr_student',
                fullName: 'สมชาย เรียนดี (นักศึกษา)',
                email: 'student@demo.com',
                password: 'password',
                role: 'student'
            }
        ];

        // Demo Initial Courses
        const initialCourses = [
            {
                id: '1',
                code: 'CS101',
                nameTh: 'การเขียนโปรแกรมคอมพิวเตอร์เบื้องต้น',
                nameEn: 'Fundamental Computer Programming',
                credits: 3,
                category: 'หมวดวิชาเฉพาะ',
                description: 'ศึกษาตรรกศาสตร์ในการแก้ปัญหา อัลกอริทึม โครงสร้างควบคุม ฟังก์ชัน และการจัดการข้อมูลเบื้องต้น'
            },
            {
                id: '2',
                code: 'GEN111',
                nameTh: 'ภาษาอังกฤษเพื่อการสื่อสาร',
                nameEn: 'English for Communication',
                credits: 3,
                category: 'หมวดวิชาศึกษาทั่วไป (GE)',
                description: 'การพัฒนาทักษะการฟัง พูด อ่าน เขียน เพื่อการสื่อสารในชีวิตประจำวันและการทำงาน'
            },
            {
                id: '3',
                code: 'CS204',
                nameTh: 'การพัฒนาเว็บแอปพลิเคชัน',
                nameEn: 'Web Application Development',
                credits: 3,
                category: 'หมวดวิชาเลือก',
                description: 'การออกแบบและพัฒนาเว็บส่วนหน้าและส่วนหลัง (Frontend & Backend) ด้วยเทคโนโลยีสมัยใหม่'
            },
            {
                id: '4',
                code: 'MATH102',
                nameTh: 'แคลคูลัสสำหรับวิทยาศาสตร์คอมพิวเตอร์',
                nameEn: 'Calculus for Computer Science',
                credits: 3,
                category: 'หมวดวิชาเฉพาะ',
                description: 'ลิมิต ความต่อเนื่อง อนุพันธ์ การประยุกต์ใช้อนุพันธ์ และอินทิกรัล'
            }
        ];

        // Application State Variables
        let users = JSON.parse(localStorage.getItem('cms_users')) || defaultUsers;
        let currentUser = JSON.parse(localStorage.getItem('cms_current_user')) || null;
        let courses = JSON.parse(localStorage.getItem('cms_courses')) || initialCourses;
        let pendingDeleteId = null;

        // Initialize App
        window.onload = function() {
            if (!localStorage.getItem('cms_users')) {
                localStorage.setItem('cms_users', JSON.stringify(defaultUsers));
            }
            updateAuthUI();
            renderTable();
            updateStats();
        };

        // --- AUTHENTICATION MODULE --- //

        // Toggle Modal Display
        function openAuthModal(view = 'login') {
            toggleAuthView(view);
            document.getElementById('authModal').classList.remove('hidden');
        }

        function toggleAuthView(view) {
            const loginView = document.getElementById('loginFormView');
            const regView = document.getElementById('registerFormView');
            if (view === 'login') {
                loginView.classList.remove('hidden');
                regView.classList.add('hidden');
            } else {
                loginView.classList.add('hidden');
                regView.classList.remove('hidden');
            }
        }

        // Fill Demo Account Credentials
        function fillDemoUser(role) {
            if (role === 'teacher') {
                document.getElementById('loginEmail').value = 'teacher@demo.com';
                document.getElementById('loginPassword').value = 'password';
            } else {
                document.getElementById('loginEmail').value = 'student@demo.com';
                document.getElementById('loginPassword').value = 'password';
            }
        }

        // Handle User Login
        function handleLogin(e) {
            e.preventDefault();
            const email = document.getElementById('loginEmail').value.trim();
            const password = document.getElementById('loginPassword').value.trim();

            const user = users.find(u => u.email.toLowerCase() === email.toLowerCase() && u.password === password);

            if (user) {
                currentUser = { id: user.id, fullName: user.fullName, email: user.email, role: user.role };
                localStorage.setItem('cms_current_user', JSON.stringify(currentUser));
                closeModal('authModal');
                updateAuthUI();
                showToast(`ยินดีต้อนรับคุณ ${user.fullName}`, 'success');
            } else {
                showToast('อีเมลหรือรหัสผ่านไม่ถูกต้อง', 'error');
            }
        }

        // Handle User Register
        function handleRegister(e) {
            e.preventDefault();
            const fullName = document.getElementById('regFullName').value.trim();
            const email = document.getElementById('regEmail').value.trim();
            const password = document.getElementById('regPassword').value.trim();
            const role = document.getElementById('regRole').value;

            if (users.some(u => u.email.toLowerCase() === email.toLowerCase())) {
                showToast('อีเมลนี้ถูกใช้งานแล้วในระบบ', 'error');
                return;
            }

            const newUser = {
                id: 'usr_' + Date.now(),
                fullName,
                email,
                password,
                role
            };

            users.push(newUser);
            localStorage.setItem('cms_users', JSON.stringify(users));

            // Auto Log-in
            currentUser = { id: newUser.id, fullName: newUser.fullName, email: newUser.email, role: newUser.role };
            localStorage.setItem('cms_current_user', JSON.stringify(currentUser));

            closeModal('authModal');
            updateAuthUI();
            showToast('ลงทะเบียนและเข้าสู่ระบบเรียบร้อยแล้ว', 'success');
        }

        // Handle Logout
        function handleLogout() {
            currentUser = null;
            localStorage.removeItem('cms_current_user');
            updateAuthUI();
            resetForm();
            showToast('ออกจากระบบเรียบร้อยแล้ว', 'info');
        }

        // Update Navigation Bar & Lock Overlay UI based on Login state
        function updateAuthUI() {
            const userHeader = document.getElementById('userHeaderSection');
            const lockOverlay = document.getElementById('authLockOverlay');

            if (currentUser) {
                lockOverlay.classList.add('hidden');

                const roleBadge = currentUser.role === 'teacher' 
                    ? `<span class="bg-indigo-100 text-indigo-700 text-[10px] px-2 py-0.5 rounded-full font-semibold">อาจารย์/เจ้าหน้าที่</span>`
                    : `<span class="bg-emerald-100 text-emerald-700 text-[10px] px-2 py-0.5 rounded-full font-semibold">นักศึกษา</span>`;

                userHeader.innerHTML = `
                    <div class="flex items-center gap-2.5">
                        <div class="w-9 h-9 rounded-full bg-indigo-50 border border-indigo-200 text-indigo-600 font-bold flex items-center justify-center text-sm shadow-sm">
                            <i class="fa-solid fa-user"></i>
                        </div>
                        <div class="hidden sm:block text-left">
                            <div class="text-xs font-bold text-slate-800 leading-tight">${escapeHtml(currentUser.fullName)}</div>
                            <div class="mt-0.5">${roleBadge}</div>
                        </div>
                    </div>
                    <button onclick="handleLogout()" class="text-xs px-3 py-2 rounded-xl bg-slate-100 text-slate-600 hover:bg-red-50 hover:text-red-600 font-medium transition flex items-center gap-1.5 ml-2">
                        <i class="fa-solid fa-right-from-bracket"></i>
                        <span class="hidden sm:inline">ออกจากระบบ</span>
                    </button>
                `;
            } else {
                lockOverlay.classList.remove('hidden');

                userHeader.innerHTML = `
                    <button onclick="openAuthModal('login')" class="text-xs sm:text-sm px-3.5 py-2 rounded-xl border border-slate-200 text-slate-700 hover:bg-slate-50 font-medium transition">
                        <i class="fa-solid fa-right-to-bracket mr-1.5"></i>เข้าสู่ระบบ
                    </button>
                    <button onclick="openAuthModal('register')" class="text-xs sm:text-sm px-3.5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-medium shadow-md shadow-indigo-100 transition">
                        <i class="fa-solid fa-user-plus mr-1.5"></i>สมัครสมาชิก
                    </button>
                `;
            }
        }

        // --- COURSE MANAGEMENT MODULE --- //

        function saveCourses() {
            localStorage.setItem('cms_courses', JSON.stringify(courses));
            updateStats();
        }

        function renderTable() {
            const tableBody = document.getElementById('courseTableBody');
            const searchKeyword = document.getElementById('searchInput').value.toLowerCase().trim();
            const selectedCategory = document.getElementById('categoryFilter').value;
            const emptyState = document.getElementById('emptyState');

            const filtered = courses.filter(c => {
                const matchSearch = c.code.toLowerCase().includes(searchKeyword) || 
                                    c.nameTh.toLowerCase().includes(searchKeyword) ||
                                    (c.nameEn && c.nameEn.toLowerCase().includes(searchKeyword));
                const matchCategory = selectedCategory === 'ALL' || c.category === selectedCategory;
                return matchSearch && matchCategory;
            });

            document.getElementById('showingCount').innerText = `แสดง ${filtered.length} จาก ${courses.length} รายการ`;

            if (filtered.length === 0) {
                tableBody.innerHTML = '';
                emptyState.classList.remove('hidden');
                return;
            }

            emptyState.classList.add('hidden');
            
            tableBody.innerHTML = filtered.map(course => {
                let categoryClass = "bg-slate-100 text-slate-700";
                if(course.category === 'หมวดวิชาเฉพาะ') categoryClass = "bg-indigo-50 text-indigo-700 border border-indigo-100";
                else if(course.category === 'หมวดวิชาเลือก') categoryClass = "bg-emerald-50 text-emerald-700 border border-emerald-100";
                else if(course.category === 'หมวดวิชาศึกษาทั่วไป (GE)') categoryClass = "bg-amber-50 text-amber-700 border border-amber-100";
                else if(course.category === 'หมวดวิชาเสรี') categoryClass = "bg-purple-50 text-purple-700 border border-purple-100";

                return `
                    <tr class="hover:bg-slate-50/80 transition duration-150">
                        <td class="py-3.5 px-4 font-semibold text-slate-800 whitespace-nowrap">${escapeHtml(course.code)}</td>
                        <td class="py-3.5 px-4">
                            <div class="font-medium text-slate-800">${escapeHtml(course.nameTh)}</div>
                            <div class="text-xs text-slate-400">${escapeHtml(course.nameEn || '-')}</div>
                        </td>
                        <td class="py-3.5 px-4 text-center">
                            <span class="inline-block bg-slate-100 text-slate-600 rounded-lg px-2 py-1 font-semibold text-xs">${course.credits}</span>
                        </td>
                        <td class="py-3.5 px-4 whitespace-nowrap">
                            <span class="text-xs px-2.5 py-1 rounded-full font-medium ${categoryClass}">${escapeHtml(course.category)}</span>
                        </td>
                        <td class="py-3.5 px-4 text-center whitespace-nowrap">
                            <div class="flex items-center justify-center gap-1.5">
                                <button onclick="viewDetails('${course.id}')" title="ดูรายละเอียด" class="w-8 h-8 rounded-lg bg-slate-100 text-slate-600 hover:bg-slate-200 transition flex items-center justify-center">
                                    <i class="fa-solid fa-eye text-xs"></i>
                                </button>
                                <button onclick="editCourse('${course.id}')" title="แก้ไข" class="w-8 h-8 rounded-lg bg-amber-50 text-amber-600 hover:bg-amber-100 transition flex items-center justify-center">
                                    <i class="fa-solid fa-pen text-xs"></i>
                                </button>
                                <button onclick="askDeleteCourse('${course.id}')" title="ลบ" class="w-8 h-8 rounded-lg bg-red-50 text-red-600 hover:bg-red-100 transition flex items-center justify-center">
                                    <i class="fa-solid fa-trash-can text-xs"></i>
                                </button>
                            </div>
                        </td>
                    </tr>
                `;
            }).join('');
        }

        function updateStats() {
            const totalCourses = courses.length;
            const totalCredits = courses.reduce((sum, item) => sum + Number(item.credits), 0);
            const majorCount = courses.filter(c => c.category === 'หมวดวิชาเฉพาะ' || c.category === 'หมวดวิชาเลือก').length;
            const geCount = courses.filter(c => c.category === 'หมวดวิชาศึกษาทั่วไป (GE)').length;

            document.getElementById('statTotalCourses').innerText = totalCourses;
            document.getElementById('statTotalCredits').innerText = totalCredits;
            document.getElementById('statMajorCourses').innerText = majorCount;
            document.getElementById('statGeCourses').innerText = geCount;
        }

        function handleFormSubmit(e) {
            e.preventDefault();

            if (!currentUser) {
                openAuthModal('login');
                return;
            }

            const editingId = document.getElementById('editingId').value;
            const code = document.getElementById('courseCode').value.trim();
            const nameTh = document.getElementById('courseNameTh').value.trim();
            const nameEn = document.getElementById('courseNameEn').value.trim();
            const credits = parseInt(document.getElementById('courseCredits').value);
            const category = document.getElementById('courseCategory').value;
            const description = document.getElementById('courseDescription').value.trim();

            if (!code || !nameTh) {
                showToast('กรุณากรอกข้อมูลที่จำเป็นให้ครบถ้วน', 'error');
                return;
            }

            if (!editingId) {
                const isDuplicate = courses.some(c => c.code.toLowerCase() === code.toLowerCase());
                if (isDuplicate) {
                    showToast(`รหัสวิชา ${code} มีในระบบแล้ว`, 'error');
                    return;
                }

                const newCourse = {
                    id: Date.now().toString(),
                    code,
                    nameTh,
                    nameEn,
                    credits,
                    category,
                    description
                };

                courses.unshift(newCourse);
                showToast('บันทึกรายวิชาเรียบร้อยแล้ว', 'success');
            } else {
                const index = courses.findIndex(c => c.id === editingId);
                if (index !== -1) {
                    courses[index] = { id: editingId, code, nameTh, nameEn, credits, category, description };
                    showToast('อัปเดตข้อมูลรายวิชาเรียบร้อยแล้ว', 'success');
                }
            }

            saveCourses();
            renderTable();
            resetForm();
        }

        function editCourse(id) {
            if (!currentUser) {
                openAuthModal('login');
                return;
            }

            const course = courses.find(c => c.id === id);
            if (!course) return;

            document.getElementById('editingId').value = course.id;
            document.getElementById('courseCode').value = course.code;
            document.getElementById('courseNameTh').value = course.nameTh;
            document.getElementById('courseNameEn').value = course.nameEn || '';
            document.getElementById('courseCredits').value = course.credits;
            document.getElementById('courseCategory').value = course.category;
            document.getElementById('courseDescription').value = course.description || '';

            document.getElementById('formTitle').innerText = 'แก้ไขรายวิชา';
            document.getElementById('editBadge').classList.remove('hidden');
            document.getElementById('btnSubmit').innerHTML = `<i class="fa-solid fa-floppy-disk"></i> <span>อัปเดตข้อมูล</span>`;
        }

        function resetForm() {
            document.getElementById('courseForm').reset();
            document.getElementById('editingId').value = '';
            document.getElementById('formTitle').innerText = 'เพิ่มรายวิชาใหม่';
            document.getElementById('editBadge').classList.add('hidden');
            document.getElementById('btnSubmit').innerHTML = `<i class="fa-solid fa-plus"></i> <span>บันทึกรายวิชา</span>`;
        }

        function viewDetails(id) {
            const course = courses.find(c => c.id === id);
            if (!course) return;

            document.getElementById('modalCodeBadge').innerText = course.code;
            document.getElementById('modalTitleTh').innerText = course.nameTh;
            document.getElementById('modalTitleEn').innerText = course.nameEn || 'N/A';
            document.getElementById('modalCredits').innerText = `${course.credits} หน่วยกิต`;
            document.getElementById('modalCategory').innerText = course.category;
            document.getElementById('modalDescription').innerText = course.description || 'ไม่มีคำอธิบายรายวิชา';

            document.getElementById('detailModal').classList.remove('hidden');
        }

        function askDeleteCourse(id) {
            if (!currentUser) {
                openAuthModal('login');
                return;
            }

            const course = courses.find(c => c.id === id);
            if (!course) return;

            pendingDeleteId = id;
            document.getElementById('deleteCourseName').innerText = `${course.code} - ${course.nameTh}`;
            
            const btnConfirm = document.getElementById('btnConfirmDelete');
            btnConfirm.onclick = function() {
                executeDelete();
            };

            document.getElementById('deleteModal').classList.remove('hidden');
        }

        function executeDelete() {
            if (!pendingDeleteId) return;

            courses = courses.filter(c => c.id !== pendingDeleteId);
            saveCourses();
            renderTable();
            closeModal('deleteModal');
            showToast('ลบรายวิชาออกจากระบบแล้ว', 'success');
            pendingDeleteId = null;
        }

        function closeModal(modalId) {
            document.getElementById(modalId).classList.add('hidden');
        }

        function loadSampleData() {
            courses = [...initialCourses];
            saveCourses();
            renderTable();
            showToast('รีเซ็ตข้อมูลวิชาตั้งต้นเรียบร้อย', 'info');
        }

        function showToast(message, type = 'success') {
            const toast = document.getElementById('toast');
            const toastMessage = document.getElementById('toastMessage');
            const toastIcon = document.getElementById('toastIcon');

            toastMessage.innerText = message;

            if (type === 'success') {
                toast.className = "fixed bottom-5 right-5 z-50 flex items-center gap-3 px-4 py-3 rounded-xl shadow-lg text-white text-sm bg-emerald-600 transition-all duration-300";
                toastIcon.className = "fa-solid fa-circle-check";
            } else if (type === 'error') {
                toast.className = "fixed bottom-5 right-5 z-50 flex items-center gap-3 px-4 py-3 rounded-xl shadow-lg text-white text-sm bg-red-600 transition-all duration-300";
                toastIcon.className = "fa-solid fa-circle-xmark";
            } else {
                toast.className = "fixed bottom-5 right-5 z-50 flex items-center gap-3 px-4 py-3 rounded-xl shadow-lg text-white text-sm bg-indigo-600 transition-all duration-300";
                toastIcon.className = "fa-solid fa-circle-info";
            }

            toast.classList.remove('translate-y-20', 'opacity-0', 'pointer-events-none');

            setTimeout(() => {
                toast.classList.add('translate-y-20', 'opacity-0', 'pointer-events-none');
            }, 3000);
        }

        function escapeHtml(str) {
            return String(str).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
        }
    </script>
</body>
</html>
