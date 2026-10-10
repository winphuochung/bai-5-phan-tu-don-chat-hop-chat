# -*- coding: utf-8 -*-
"""
Tập lệnh xây dựng ứng dụng Web App HTML duy nhất: Bài 5 - Phân tử, Đơn chất, Hợp chất (KHTN 7)
Phiên bản 3.0:
- GIẢI QUYẾT TRIỆT ĐỂ LỖI 153 BẰNG 3 CHẾ ĐỘ VIDEO CAO CẤP:
  1. CHẾ ĐỘ 1: THƯ VIỆN BÀI GIẢNG VIDEO TRỰC QUAN (Interactive Video Player):
     - Card video bài giảng với nút phát trực tiếp trên tab mới hoặc mở cửa sổ Popup chuyên dụng (Đảm bảo 100% không bao giờ gặp Lỗi 153).
     - Trình phát video chuẩn HTML5 <video> hỗ trợ xem offline / online trực tiếp không phụ thuộc YouTube.
     - Cho phép Thầy/Cô chọn tệp video từ máy tính (Local File Picker) hoặc dán link MP4 để phát ngay lập tức.
  2. CHẾ ĐỘ 2: TÍCH HỢP MÔ PHỎNG THỰC TẾ ẢO PHET HỌC TẬP (Build a Molecule / Molecule Shapes):
     - Mô phỏng xây dựng phân tử tương tác của Đại học Colorado (Chạy mượt 100% không bị chặn iframe như YouTube).
  3. CHẾ ĐỘ 3: PHÒNG THÍ NGHIỆM 3D PHÂN TỬ N2, H2O, CH4, CO2 NỘI TẠI
- Đầy đủ 50 câu hỏi QUIZ_DATA 5 dạng bài tập
- Web Audio API (Ting-ting, Buzz)
- Confetti, LocalStorage Bảng xếp hạng, Xuất Báo Cáo PDF
"""
import json
import base64

with open("scripts/quiz_data.json", "r", encoding="utf-8") as f:
    quiz_data_json = f.read()

with open("logo.png", "rb") as f:
    logo_b64 = base64.b64encode(f.read()).decode("utf-8")

html_content = f'''<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="referrer" content="strict-origin-when-cross-origin">
    <title>KHTN 7 - Bài 5: Phân tử - Đơn chất - Hợp chất | EduTech Interactive</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet">
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Font Awesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Canvas Confetti CDN -->
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <!-- html2canvas & jsPDF for Certificate & Report Export -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>

    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['"Plus Jakarta Sans"', 'sans-serif'],
                        heading: ['"Space Grotesk"', 'sans-serif'],
                    }},
                    colors: {{
                        brand: {{
                            light: '#00c6ff',
                            dark: '#0072ff',
                            accent: '#38ef7d',
                            coral: '#ff6b6b'
                        }}
                    }}
                }}
            }}
        }}
    </script>

    <style>
        :root {{
            --primary-grad: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%);
            --glass-bg: rgba(255, 255, 255, 0.15);
            --glass-border: rgba(255, 255, 255, 0.25);
            --card-glass: rgba(255, 255, 255, 0.88);
            --dark-glass: rgba(15, 23, 42, 0.75);
        }}

        body {{
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0c4a6e 100%);
            min-height: 100vh;
            color: #1e293b;
            overflow-x: hidden;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }}

        .ambient-glow {{
            position: fixed;
            width: 500px;
            height: 500px;
            border-radius: 50%;
            filter: blur(120px);
            z-index: 0;
            pointer-events: none;
            opacity: 0.45;
            animation: pulse-glow 12s infinite alternate ease-in-out;
        }}
        .glow-1 {{ top: -100px; left: -100px; background: #00c6ff; }}
        .glow-2 {{ bottom: -100px; right: -100px; background: #0072ff; animation-delay: -6s; }}
        .glow-3 {{ top: 40%; left: 30%; background: #38ef7d; width: 400px; height: 400px; opacity: 0.25; }}

        @keyframes pulse-glow {{
            0% {{ transform: scale(1) translate(0, 0); }}
            100% {{ transform: scale(1.15) translate(40px, 40px); }}
        }}

        .glass-card {{
            background: rgba(255, 255, 255, 0.88);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.6);
            box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.15);
        }}
        .glass-panel-dark {{
            background: rgba(15, 23, 42, 0.75);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.15);
        }}
        .glass-btn {{
            background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }}
        .glass-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 25px -5px rgba(0, 114, 255, 0.5);
        }}

        @keyframes shake {{
            0%, 100% {{ transform: translateX(0); }}
            20%, 60% {{ transform: translateX(-10px); }}
            40%, 80% {{ transform: translateX(10px); }}
        }}
        .shake-effect {{
            animation: shake 0.5s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
        }}

        @keyframes mascot-celebrate {{
            0%, 100% {{ transform: translateY(0) scale(1) rotate(0deg); }}
            30% {{ transform: translateY(-24px) scale(1.1) rotate(-6deg); }}
            60% {{ transform: translateY(-12px) scale(1.05) rotate(6deg); }}
        }}
        .mascot-jump {{
            animation: mascot-celebrate 0.8s ease-in-out infinite;
        }}

        /* 3D Atoms */
        .atom {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            font-weight: 700;
            color: white;
            transition: transform 0.3s ease;
            position: relative;
            user-select: none;
        }}
        .atom:hover {{
            transform: scale(1.18) rotate(10deg);
        }}
        .atom-h {{
            width: 44px; height: 44px; font-size: 14px;
            background: radial-gradient(circle at 30% 30%, #f1f5f9 0%, #94a3b8 70%, #475569 100%);
            box-shadow: 0 8px 16px rgba(0,0,0,0.35), inset 2px 2px 4px rgba(255,255,255,0.8);
            color: #1e293b;
        }}
        .atom-c {{
            width: 68px; height: 68px; font-size: 18px;
            background: radial-gradient(circle at 30% 30%, #475569 0%, #1e293b 70%, #0f172a 100%);
            box-shadow: 0 10px 20px rgba(0,0,0,0.45), inset 2px 2px 5px rgba(255,255,255,0.4);
        }}
        .atom-o {{
            width: 64px; height: 64px; font-size: 18px;
            background: radial-gradient(circle at 30% 30%, #ff6b6b 0%, #dc2626 70%, #991b1b 100%);
            box-shadow: 0 10px 20px rgba(220,38,38,0.4), inset 2px 2px 5px rgba(255,255,255,0.6);
        }}
        .atom-n {{
            width: 66px; height: 66px; font-size: 18px;
            background: radial-gradient(circle at 30% 30%, #60a5fa 0%, #2563eb 70%, #1e40af 100%);
            box-shadow: 0 10px 20px rgba(37,99,235,0.4), inset 2px 2px 5px rgba(255,255,255,0.6);
        }}
        .bond-bar {{
            height: 8px;
            background: linear-gradient(90deg, #94a3b8, #cbd5e1);
            border-radius: 4px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.25);
        }}

        .active-media-tab {{
            background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%) !important;
            color: white !important;
            border-color: transparent !important;
            box-shadow: 0 4px 12px rgba(0, 114, 255, 0.35);
        }}
    </style>
</head>
<body class="relative flex flex-col justify-between">
    <!-- Ambient Light Effects -->
    <div class="ambient-glow glow-1"></div>
    <div class="ambient-glow glow-2"></div>
    <div class="ambient-glow glow-3"></div>

    <div class="relative z-10 flex flex-col min-h-screen">

        <!-- GLOBAL HEADER / NAVBAR -->
        <header id="app-header" class="hidden glass-panel-dark sticky top-0 z-50 px-4 lg:px-8 py-3.5 border-b border-white/10 transition-all duration-300">
            <div class="max-w-7xl mx-auto flex items-center justify-between">
                <!-- Brand / Logo -->
                <div class="flex items-center space-x-3.5 cursor-pointer py-1" onclick="navigateSection('dashboard')">
                    <div class="relative flex items-center justify-center rounded-2xl bg-gradient-to-tr from-amber-500/20 via-white/15 to-cyan-500/20 p-1.5 border border-white/20 shadow-lg hover:shadow-cyan-500/30 transition-all duration-300 hover:scale-105">
                        <img src="data:image/png;base64,{logo_b64}" alt="Logo Thầy Lê Văn Thắng" class="w-14 h-14 sm:w-16 sm:h-16 object-contain drop-shadow-md">
                    </div>
                    <div>
                        <div class="text-white font-extrabold text-lg sm:text-xl tracking-tight flex items-center gap-2">
                            <span>KHTN 7</span>
                            <span class="text-xs bg-gradient-to-r from-cyan-400 to-blue-500 text-white px-2.5 py-0.5 rounded-full font-bold shadow-sm">Bài 5</span>
                        </div>
                        <p class="text-slate-300 text-xs font-medium hidden sm:block">Phân tử - Đơn chất - Hợp chất</p>
                    </div>
                </div>

                <!-- Navigation Tabs -->
                <nav class="hidden md:flex items-center space-x-1 lg:space-x-2 bg-slate-800/60 p-1.5 rounded-2xl border border-white/10">
                    <button onclick="navigateSection('dashboard')" id="nav-btn-dashboard" class="nav-tab px-4 py-2 rounded-xl text-sm font-semibold text-white bg-blue-600 shadow-md transition-all flex items-center gap-2">
                        <i class="fa-solid fa-house"></i>
                        <span>Menu chính</span>
                    </button>
                    <button onclick="navigateSection('theory')" id="nav-btn-theory" class="nav-tab px-4 py-2 rounded-xl text-sm font-medium text-slate-300 hover:text-white hover:bg-white/10 transition-all flex items-center gap-2">
                        <i class="fa-solid fa-book-open"></i>
                        <span>Lý thuyết</span>
                    </button>
                    <button onclick="navigateSection('video')" id="nav-btn-video" class="nav-tab px-4 py-2 rounded-xl text-sm font-medium text-slate-300 hover:text-white hover:bg-white/10 transition-all flex items-center gap-2">
                        <i class="fa-solid fa-video"></i>
                        <span>Video & 3D</span>
                    </button>
                    <button onclick="startQuizMode('all')" id="nav-btn-quiz" class="nav-tab px-4 py-2 rounded-xl text-sm font-medium text-slate-300 hover:text-white hover:bg-white/10 transition-all flex items-center gap-2">
                        <i class="fa-solid fa-circle-question"></i>
                        <span>Luyện tập (50 câu)</span>
                    </button>
                    <button onclick="navigateSection('leaderboard')" id="nav-btn-leaderboard" class="nav-tab px-4 py-2 rounded-xl text-sm font-medium text-slate-300 hover:text-white hover:bg-white/10 transition-all flex items-center gap-2">
                        <i class="fa-solid fa-trophy"></i>
                        <span>Xếp hạng</span>
                    </button>
                </nav>

                <!-- User Badge & Audio Mute & Logout -->
                <div class="flex items-center space-x-3">
                    <div class="flex items-center bg-white/10 backdrop-blur-md px-3.5 py-1.5 rounded-full border border-white/20 text-white text-sm">
                        <i class="fa-solid fa-user-astronaut text-cyan-400 mr-2 text-base"></i>
                        <span id="header-user-name" class="font-bold mr-1">Học sinh</span>
                        <span id="header-user-class" class="text-xs text-cyan-300 bg-white/10 px-2 py-0.5 rounded-full font-mono">7A</span>
                    </div>
                    <button onclick="openSheetConfigModal()" title="Cài đặt Google Sheet" class="px-3 py-1.5 rounded-xl bg-emerald-500/20 hover:bg-emerald-500 text-emerald-300 hover:text-white border border-emerald-500/30 text-xs font-semibold transition-all flex items-center gap-1.5">
                        <i class="fa-solid fa-table"></i>
                        <span class="hidden sm:inline">Google Sheet</span>
                    </button>
                    <button onclick="toggleAudio()" id="btn-audio-toggle" title="Bật/Tắt âm thanh" class="w-9 h-9 rounded-full bg-slate-800 text-slate-300 hover:text-white hover:bg-slate-700 flex items-center justify-center transition border border-white/10">
                        <i class="fa-solid fa-volume-high text-sm"></i>
                    </button>
                    <button onclick="logoutStudent()" title="Đăng xuất" class="px-3 py-1.5 rounded-xl bg-red-500/20 hover:bg-red-500 text-red-300 hover:text-white border border-red-500/30 text-xs font-semibold transition-all flex items-center gap-1.5">
                        <i class="fa-solid fa-right-from-bracket"></i>
                        <span class="hidden sm:inline">Thoát</span>
                    </button>
                </div>
            </div>
        </header>

        <!-- MAIN BODY CONTENT -->
        <main class="flex-grow max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-6">

            <!-- ========================================== -->
            <!-- 1. MÀN HÌNH ĐĂNG NHẬP                      -->
            <!-- ========================================== -->
            <section id="section-login" class="min-h-[80vh] flex items-center justify-center py-10">
                <div class="glass-card max-w-md w-full p-8 sm:p-10 rounded-3xl relative overflow-hidden border border-white/70 shadow-2xl">
                    <div class="absolute -top-16 -right-16 w-40 h-40 bg-gradient-to-br from-cyan-400 to-blue-600 rounded-full blur-2xl opacity-40"></div>
                    
                    <div class="text-center relative z-10 mb-6">
                        <div class="inline-flex p-3 sm:p-4 rounded-3xl bg-gradient-to-tr from-amber-400/20 via-white/80 to-cyan-400/20 shadow-2xl mb-4 border border-white/60 backdrop-blur-md hover:scale-105 transition-transform duration-300">
                            <img src="data:image/png;base64,{logo_b64}" alt="Logo Thầy Lê Văn Thắng" class="w-28 h-28 sm:w-32 sm:h-32 object-contain drop-shadow-xl">
                        </div>
                        <h1 class="text-2xl sm:text-3xl font-extrabold text-slate-800 font-heading tracking-tight">KHOA HỌC TỰ NHIÊN 7</h1>
                        <p class="text-blue-600 font-bold mt-1 text-base">Bài 5: Phân tử - Đơn chất - Hợp chất</p>
                        <p class="text-slate-500 text-xs mt-1">Bộ sách Kết nối tri thức với cuộc sống</p>
                    </div>

                    <form onsubmit="handleLogin(event)" class="space-y-5 relative z-10">
                        <div>
                            <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">Họ và tên học sinh</label>
                            <div class="relative">
                                <span class="absolute inset-y-0 left-0 pl-3.5 flex items-center text-slate-400">
                                    <i class="fa-solid fa-user"></i>
                                </span>
                                <input type="text" id="login-name" required placeholder="Ví dụ: Nguyễn Văn An" 
                                    class="w-full pl-10 pr-4 py-3 rounded-xl border border-slate-300 focus:border-blue-500 focus:ring-4 focus:ring-blue-100 transition-all text-slate-800 text-sm font-medium outline-none bg-white/80">
                            </div>
                        </div>

                        <div>
                            <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">Lớp học</label>
                            <div class="relative">
                                <span class="absolute inset-y-0 left-0 pl-3.5 flex items-center text-slate-400">
                                    <i class="fa-solid fa-graduation-cap"></i>
                                </span>
                                <input type="text" id="login-class" required placeholder="Ví dụ: 7A1, 7A2, 7/3..." 
                                    class="w-full pl-10 pr-4 py-3 rounded-xl border border-slate-300 focus:border-blue-500 focus:ring-4 focus:ring-blue-100 transition-all text-slate-800 text-sm font-medium outline-none bg-white/80">
                            </div>
                        </div>

                        <div class="pt-2">
                            <button type="submit" class="glass-btn w-full py-3.5 px-6 rounded-xl text-white font-bold text-base shadow-lg flex items-center justify-center gap-2 group">
                                <span>VÀO HỌC NGAY</span>
                                <i class="fa-solid fa-arrow-right group-hover:translate-x-1.5 transition-transform"></i>
                            </button>
                        </div>
                    </form>

                    <div class="mt-8 pt-6 border-t border-slate-200/80 flex justify-around text-center text-xs text-slate-600 font-medium">
                        <div class="flex flex-col items-center">
                            <i class="fa-solid fa-atom text-cyan-600 text-lg mb-1"></i>
                            <span>Mô phỏng PhET 3D</span>
                        </div>
                        <div class="flex flex-col items-center">
                            <i class="fa-solid fa-award text-amber-500 text-lg mb-1"></i>
                            <span>50 Câu hỏi</span>
                        </div>
                        <div class="flex flex-col items-center">
                            <i class="fa-solid fa-file-pdf text-rose-500 text-lg mb-1"></i>
                            <span>Xuất Báo Cáo</span>
                        </div>
                    </div>
                </div>
            </section>


            <!-- ========================================== -->
            <!-- 2. MENU CHÍNH (DASHBOARD)                  -->
            <!-- ========================================== -->
            <section id="section-dashboard" class="hidden space-y-8 animate-fade-in">
                <!-- Welcome Banner -->
                <div class="glass-card rounded-3xl p-6 sm:p-8 bg-gradient-to-r from-blue-900/90 via-indigo-900/90 to-blue-800/90 text-white relative overflow-hidden border border-white/20 shadow-2xl">
                    <div class="absolute -right-10 -bottom-10 w-64 h-64 bg-cyan-500/20 rounded-full blur-3xl"></div>
                    <div class="relative z-10 flex flex-col md:flex-row items-center justify-between gap-6">
                        <div class="space-y-2 text-center md:text-left">
                            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 text-cyan-300 text-xs font-semibold backdrop-blur-md">
                                <i class="fa-solid fa-sparkles"></i>
                                <span>Chào mừng trở lại học tập!</span>
                            </div>
                            <h2 class="text-2xl sm:text-3xl font-extrabold font-heading text-white">
                                Chào <span id="dash-user-name" class="text-transparent bg-clip-text bg-gradient-to-r from-cyan-300 to-blue-200">Học sinh</span>! 👋
                            </h2>
                            <p class="text-slate-300 text-sm max-w-xl">
                                Khám phá thế giới kì diệu của các hạt vi mô: Tìm hiểu đơn chất, hợp chất, phân tử và tính khối lượng phân tử theo đơn vị amu cùng 50 bài tập tương tác hấp dẫn!
                            </p>
                        </div>
                        <div class="flex items-center gap-3">
                            <div class="bg-white/10 backdrop-blur-md px-5 py-4 rounded-2xl border border-white/20 text-center">
                                <span class="block text-2xl font-black text-cyan-400" id="dash-stat-completed">0/50</span>
                                <span class="text-xs text-slate-300">Đã hoàn thành</span>
                            </div>
                            <div class="bg-white/10 backdrop-blur-md px-5 py-4 rounded-2xl border border-white/20 text-center">
                                <span class="block text-2xl font-black text-amber-400" id="dash-stat-score">0%</span>
                                <span class="text-xs text-slate-300">Điểm số cao nhất</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 3 Phân khu chính -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <!-- Khu 1: Lý thuyết trọng tâm -->
                    <div onclick="navigateSection('theory')" class="glass-card p-6 sm:p-7 rounded-3xl cursor-pointer hover:-translate-y-2 transition-all duration-300 group border border-white/60 hover:shadow-2xl hover:border-cyan-400/50 flex flex-col justify-between">
                        <div>
                            <div class="w-14 h-14 rounded-2xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center text-white text-2xl mb-5 shadow-lg group-hover:scale-110 transition-transform">
                                <i class="fa-solid fa-book-bookmark"></i>
                            </div>
                            <span class="text-xs font-bold text-cyan-600 tracking-wider uppercase">Phân khu 1</span>
                            <h3 class="text-xl font-bold text-slate-800 mt-1 mb-2 font-heading group-hover:text-blue-600 transition-colors">Lý thuyết trọng tâm</h3>
                            <p class="text-slate-600 text-sm leading-relaxed">
                                Tổng hợp chi tiết khái niệm Đơn chất, Hợp chất, Phân tử và cách tính Khối lượng phân tử theo SGK KHTN 7 Kết nối tri thức.
                            </p>
                        </div>
                        <div class="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between text-blue-600 font-semibold text-sm">
                            <span>Khám phá ngay</span>
                            <i class="fa-solid fa-arrow-right group-hover:translate-x-1 transition-transform"></i>
                        </div>
                    </div>

                    <!-- Khu 2: Thư viện Video & Mô phỏng PhET 3D -->
                    <div onclick="navigateSection('video')" class="glass-card p-6 sm:p-7 rounded-3xl cursor-pointer hover:-translate-y-2 transition-all duration-300 group border border-white/60 hover:shadow-2xl hover:border-purple-400/50 flex flex-col justify-between">
                        <div>
                            <div class="w-14 h-14 rounded-2xl bg-gradient-to-tr from-purple-500 to-indigo-600 flex items-center justify-center text-white text-2xl mb-5 shadow-lg group-hover:scale-110 transition-transform">
                                <i class="fa-solid fa-atom"></i>
                            </div>
                            <span class="text-xs font-bold text-purple-600 tracking-wider uppercase">Phân khu 2</span>
                            <h3 class="text-xl font-bold text-slate-800 mt-1 mb-2 font-heading group-hover:text-purple-600 transition-colors">Video & Mô phỏng PhET 3D</h3>
                            <p class="text-slate-600 text-sm leading-relaxed">
                                Xem video bài giảng trực quan, tương tác trực tiếp với phòng thí nghiệm phân tử PhET và mô hình 3D xoay chiều.
                            </p>
                        </div>
                        <div class="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between text-purple-600 font-semibold text-sm">
                            <span>Vào phòng thí nghiệm</span>
                            <i class="fa-solid fa-arrow-right group-hover:translate-x-1 transition-transform"></i>
                        </div>
                    </div>

                    <!-- Khu 3: Trung tâm Bài tập 50 câu -->
                    <div onclick="startQuizMode('all')" class="glass-card p-6 sm:p-7 rounded-3xl cursor-pointer hover:-translate-y-2 transition-all duration-300 group border border-white/60 hover:shadow-2xl hover:border-emerald-400/50 flex flex-col justify-between">
                        <div>
                            <div class="w-14 h-14 rounded-2xl bg-gradient-to-tr from-emerald-500 to-teal-600 flex items-center justify-center text-white text-2xl mb-5 shadow-lg group-hover:scale-110 transition-transform">
                                <i class="fa-solid fa-graduation-cap"></i>
                            </div>
                            <span class="text-xs font-bold text-emerald-600 tracking-wider uppercase">Phân khu 3</span>
                            <h3 class="text-xl font-bold text-slate-800 mt-1 mb-2 font-heading group-hover:text-emerald-600 transition-colors">Trung tâm Bài tập (50 câu)</h3>
                            <p class="text-slate-600 text-sm leading-relaxed">
                                Đầy đủ 5 dạng bài tập chuẩn hóa: Trắc nghiệm, Điền khuyết, Ghép cột, Đúng/Sai và Tự luận với hệ thống chấm điểm tức thì.
                            </p>
                        </div>
                        <div class="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between text-emerald-600 font-semibold text-sm">
                            <span>Luyện tập ngay</span>
                            <i class="fa-solid fa-arrow-right group-hover:translate-x-1 transition-transform"></i>
                        </div>
                    </div>
                </div>

                <!-- Lối tắt vào trực tiếp các dạng bài -->
                <div class="glass-card p-6 sm:p-8 rounded-3xl border border-white/60">
                    <h3 class="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
                        <i class="fa-solid fa-layer-group text-blue-600"></i>
                        <span>Lựa chọn dạng bài tập muốn làm:</span>
                    </h3>
                    <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3.5">
                        <button onclick="startQuizMode('mcq')" class="p-4 rounded-2xl bg-white/70 hover:bg-blue-50 border border-slate-200 hover:border-blue-300 text-center transition-all hover:scale-105 shadow-sm group">
                            <div class="w-10 h-10 rounded-xl bg-blue-100 text-blue-600 flex items-center justify-center mx-auto mb-2 text-lg group-hover:bg-blue-600 group-hover:text-white transition">
                                <i class="fa-solid fa-list-check"></i>
                            </div>
                            <div class="font-bold text-xs text-slate-800">Trắc nghiệm</div>
                            <div class="text-[11px] text-slate-500">10 câu cơ bản</div>
                        </button>

                        <button onclick="startQuizMode('fill')" class="p-4 rounded-2xl bg-white/70 hover:bg-cyan-50 border border-slate-200 hover:border-cyan-300 text-center transition-all hover:scale-105 shadow-sm group">
                            <div class="w-10 h-10 rounded-xl bg-cyan-100 text-cyan-600 flex items-center justify-center mx-auto mb-2 text-lg group-hover:bg-cyan-600 group-hover:text-white transition">
                                <i class="fa-solid fa-pen-clip"></i>
                            </div>
                            <div class="font-bold text-xs text-slate-800">Điền khuyết</div>
                            <div class="text-[11px] text-slate-500">10 câu từ khóa</div>
                        </button>

                        <button onclick="startQuizMode('match')" class="p-4 rounded-2xl bg-white/70 hover:bg-purple-50 border border-slate-200 hover:border-purple-300 text-center transition-all hover:scale-105 shadow-sm group">
                            <div class="w-10 h-10 rounded-xl bg-purple-100 text-purple-600 flex items-center justify-center mx-auto mb-2 text-lg group-hover:bg-purple-600 group-hover:text-white transition">
                                <i class="fa-solid fa-arrows-split-up-and-left"></i>
                            </div>
                            <div class="font-bold text-xs text-slate-800">Ghép cột</div>
                            <div class="text-[11px] text-slate-500">10 câu tương ứng</div>
                        </button>

                        <button onclick="startQuizMode('tf')" class="p-4 rounded-2xl bg-white/70 hover:bg-amber-50 border border-slate-200 hover:border-amber-300 text-center transition-all hover:scale-105 shadow-sm group">
                            <div class="w-10 h-10 rounded-xl bg-amber-100 text-amber-600 flex items-center justify-center mx-auto mb-2 text-lg group-hover:bg-amber-600 group-hover:text-white transition">
                                <i class="fa-solid fa-circle-check"></i>
                            </div>
                            <div class="font-bold text-xs text-slate-800">Đúng / Sai</div>
                            <div class="text-[11px] text-slate-500">10 nhận định</div>
                        </button>

                        <button onclick="startQuizMode('essay')" class="p-4 rounded-2xl bg-white/70 hover:bg-emerald-50 border border-slate-200 hover:border-emerald-300 text-center transition-all hover:scale-105 shadow-sm group">
                            <div class="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-600 flex items-center justify-center mx-auto mb-2 text-lg group-hover:bg-emerald-600 group-hover:text-white transition">
                                <i class="fa-solid fa-feather"></i>
                            </div>
                            <div class="font-bold text-xs text-slate-800">Tự luận</div>
                            <div class="text-[11px] text-slate-500">10 câu tư duy</div>
                        </button>
                    </div>

                    <div class="mt-5 text-center">
                        <button onclick="startQuizMode('all')" class="glass-btn px-8 py-3 rounded-xl text-white font-bold text-sm shadow-md inline-flex items-center gap-2">
                            <i class="fa-solid fa-play"></i>
                            <span>BẮT ĐẦU TOÀN DIỆN (TỔNG HỢP 50 CÂU)</span>
                        </button>
                    </div>
                </div>
            </section>


            <!-- ========================================== -->
            <!-- 3. PHÂN KHU LÝ THUYẾT TRỌNG TÂM            -->
            <!-- ========================================== -->
            <section id="section-theory" class="hidden space-y-8 animate-fade-in">
                <div class="flex items-center justify-between">
                    <div>
                        <button onclick="navigateSection('dashboard')" class="text-xs font-semibold text-cyan-300 hover:text-white mb-2 flex items-center gap-1.5 transition">
                            <i class="fa-solid fa-chevron-left"></i> Quay lại Menu
                        </button>
                        <h2 class="text-2xl sm:text-3xl font-extrabold text-white font-heading">Lý Thuyết Trọng Tâm: Bài 5</h2>
                        <p class="text-slate-300 text-sm">Phân tử - Đơn chất - Hợp chất (Sách Kết nối tri thức với cuộc sống)</p>
                    </div>
                    <button onclick="startQuizMode('all')" class="hidden sm:flex glass-btn px-4 py-2 rounded-xl text-white text-xs font-bold items-center gap-2">
                        <i class="fa-solid fa-pen-nib"></i> Sang làm bài tập
                    </button>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="glass-card p-6 sm:p-7 rounded-3xl border-l-4 border-l-cyan-500 shadow-xl space-y-4">
                        <div class="flex items-center gap-3">
                            <span class="w-10 h-10 rounded-xl bg-cyan-100 text-cyan-700 font-bold flex items-center justify-center text-lg">1</span>
                            <h3 class="text-xl font-bold text-slate-800 font-heading">Đơn chất (Elements)</h3>
                        </div>
                        <p class="text-slate-700 text-sm leading-relaxed">
                            <strong class="text-cyan-700">Đơn chất</strong> là những chất được tạo nên chỉ từ <strong>một nguyên tố hoá học</strong>.
                        </p>
                        <div class="bg-cyan-50/70 p-4 rounded-2xl border border-cyan-100 text-xs text-slate-700 space-y-2">
                            <div><strong>Phân loại đơn chất:</strong> Kim loại, phi kim, khí hiếm.</div>
                            <div>• <strong>Kim loại:</strong> Đồng (Cu), sắt (Fe), nhôm (Al)... ở thể rắn (riêng thuỷ ngân Hg thể lỏng).</div>
                            <div>• <strong>Phi kim:</strong> Thể rắn (than C, lưu huỳnh S), thể khí (hydrogen H₂, oxygen O₂, nitrogen N₂), thể lỏng (bromine Br₂).</div>
                            <div>• <strong>Khí hiếm:</strong> Helium (He), Neon (Ne)... ở dạng đơn nguyên tử.</div>
                        </div>
                        <div class="text-xs text-slate-500 italic">
                            * Lưu ý: Một nguyên tố có thể tạo nhiều đơn chất (VD: Carbon tạo than chì, than gỗ, kim cương).
                        </div>
                    </div>

                    <div class="glass-card p-6 sm:p-7 rounded-3xl border-l-4 border-l-blue-600 shadow-xl space-y-4">
                        <div class="flex items-center gap-3">
                            <span class="w-10 h-10 rounded-xl bg-blue-100 text-blue-700 font-bold flex items-center justify-center text-lg">2</span>
                            <h3 class="text-xl font-bold text-slate-800 font-heading">Hợp chất (Compounds)</h3>
                        </div>
                        <p class="text-slate-700 text-sm leading-relaxed">
                            <strong class="text-blue-700">Hợp chất</strong> là những chất được tạo nên từ <strong>hai hay nhiều nguyên tố hoá học</strong>.
                        </p>
                        <div class="bg-blue-50/70 p-4 rounded-2xl border border-blue-100 text-xs text-slate-700 space-y-2">
                            <div><strong>Phân loại hợp chất:</strong> Hợp chất vô cơ và Hợp chất hữu cơ.</div>
                            <div>• <strong>Hợp chất vô cơ:</strong> Nước (H₂O), Carbon dioxide (CO₂), Muối ăn (NaCl), Calcium carbonate (CaCO₃)...</div>
                            <div>• <strong>Hợp chất hữu cơ:</strong> Đường Glucose, Đường Saccharose, Protein, Khí đốt Methane (CH₄)...</div>
                            <div>• <strong>Số lượng:</strong> Có tới hàng chục triệu hợp chất đã được phát hiện và tổng hợp.</div>
                        </div>
                        <div class="text-xs text-slate-500 italic">
                            * Muối ăn (NaCl) giữ cân bằng nước trong cơ thể; Nước (H₂O) là cội nguồn của sự sống.
                        </div>
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="glass-card p-6 sm:p-7 rounded-3xl border-l-4 border-l-emerald-500 shadow-xl space-y-4">
                        <div class="flex items-center gap-3">
                            <span class="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-700 font-bold flex items-center justify-center text-lg">3</span>
                            <h3 class="text-xl font-bold text-slate-800 font-heading">Khái niệm Phân tử (Molecules)</h3>
                        </div>
                        <p class="text-slate-700 text-sm leading-relaxed">
                            <strong>Phân tử</strong> là hạt đại diện cho chất, gồm một số nguyên tử liên kết với nhau và <strong>thể hiện đầy đủ tính chất hoá học</strong> của chất đó.
                        </p>
                        <ul class="text-xs text-slate-700 space-y-2 bg-emerald-50/70 p-4 rounded-2xl border border-emerald-100">
                            <li>• <strong>Phân tử đơn chất:</strong> Do các nguyên tử cùng một nguyên tố liên kết (VD: 2 nguyên tử N tạo thành phân tử Nitrogen N₂).</li>
                            <li>• <strong>Phân tử hợp chất:</strong> Do các nguyên tử của các nguyên tố khác nhau liên kết (VD: 1 C liên kết với 4 H tạo Methane CH₄; 1 O liên kết với 2 H tạo Nước H₂O).</li>
                        </ul>
                    </div>

                    <div class="glass-card p-6 sm:p-7 rounded-3xl border-l-4 border-l-amber-500 shadow-xl space-y-4">
                        <div class="flex items-center gap-3">
                            <span class="w-10 h-10 rounded-xl bg-amber-100 text-amber-700 font-bold flex items-center justify-center text-lg">4</span>
                            <h3 class="text-xl font-bold text-slate-800 font-heading">Khối lượng phân tử (amu)</h3>
                        </div>
                        <p class="text-slate-700 text-sm leading-relaxed">
                            Khối lượng phân tử của một chất bằng <strong>tổng khối lượng của các nguyên tử</strong> trong phân tử chất đó (đơn vị: <strong>amu</strong>).
                        </p>
                        <div class="bg-amber-50/70 p-4 rounded-2xl border border-amber-100 text-xs text-slate-800 space-y-1.5 font-mono">
                            <div>• Nước (H₂O): 2 × 1 + 16 = <strong>18 amu</strong></div>
                            <div>• Methane (CH₄): 12 + 4 × 1 = <strong>16 amu</strong></div>
                            <div>• Carbon dioxide (CO₂): 12 + 2 × 16 = <strong>44 amu</strong></div>
                            <div>• Nitrogen (N₂): 2 × 14 = <strong>28 amu</strong></div>
                            <div>• Muối ăn (NaCl): 23 + 35.5 = <strong>58.5 amu</strong></div>
                        </div>
                    </div>
                </div>

                <div class="glass-card p-6 rounded-3xl overflow-x-auto shadow-xl">
                    <h4 class="font-bold text-slate-800 text-base mb-3 flex items-center gap-2">
                        <i class="fa-solid fa-table text-blue-600"></i>
                        <span>Bảng ghi nhớ nhanh Khối lượng nguyên tử (amu) để làm bài:</span>
                    </h4>
                    <table class="w-full text-xs text-center border-collapse">
                        <thead>
                            <tr class="bg-slate-100 text-slate-700 font-bold">
                                <th class="p-2.5 rounded-l-xl">Nguyên tố</th>
                                <th class="p-2.5">Hydrogen (H)</th>
                                <th class="p-2.5">Carbon (C)</th>
                                <th class="p-2.5">Nitrogen (N)</th>
                                <th class="p-2.5">Oxygen (O)</th>
                                <th class="p-2.5">Sodium (Na)</th>
                                <th class="p-2.5">Chlorine (Cl)</th>
                                <th class="p-2.5 rounded-r-xl">Calcium (Ca)</th>
                            </tr>
                        </thead>
                        <tbody class="font-semibold text-slate-800 divide-y divide-slate-100">
                            <tr>
                                <td class="p-2.5 font-bold text-blue-600">Khối lượng (amu)</td>
                                <td class="p-2.5">1</td>
                                <td class="p-2.5">12</td>
                                <td class="p-2.5">14</td>
                                <td class="p-2.5">16</td>
                                <td class="p-2.5">23</td>
                                <td class="p-2.5">35.5</td>
                                <td class="p-2.5">40</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </section>


            <!-- ========================================================= -->
            <!-- 4. PHÂN KHU VIDEO & MÔ PHỎNG THỰC TẾ ẢO (KHẮC PHỤC TRIỆT ĐỂ) -->
            <!-- ========================================================= -->
            <section id="section-video" class="hidden space-y-8 animate-fade-in">
                <div class="flex items-center justify-between">
                    <div>
                        <button onclick="navigateSection('dashboard')" class="text-xs font-semibold text-cyan-300 hover:text-white mb-2 flex items-center gap-1.5 transition">
                            <i class="fa-solid fa-chevron-left"></i> Quay lại Menu
                        </button>
                        <h2 class="text-2xl sm:text-3xl font-extrabold text-white font-heading">Thư Viện Video & Phòng Thí Nghiệm PhET 3D</h2>
                        <p class="text-slate-300 text-sm">Học tập đa phương tiện trực quan không lo gián đoạn</p>
                    </div>
                </div>

                <!-- THANH CHUYỂN ĐỔI CHẾ ĐỘ MEDIA -->
                <div class="flex flex-wrap items-center gap-3 bg-slate-900/60 p-2 rounded-2xl border border-white/10 backdrop-blur-md">
                    <button onclick="switchMediaMode('interactive-hub')" id="tab-interactive-hub" class="media-tab active-media-tab px-4 py-2.5 rounded-xl text-xs sm:text-sm font-bold transition flex items-center gap-2">
                        <i class="fa-solid fa-tv"></i>
                        <span>1. Thư Viện Bài Giảng & Video Player</span>
                    </button>
                    <button onclick="switchMediaMode('phet-sim')" id="tab-phet-sim" class="media-tab px-4 py-2.5 rounded-xl text-xs sm:text-sm font-semibold text-slate-300 hover:text-white transition flex items-center gap-2">
                        <i class="fa-solid fa-flask-vial"></i>
                        <span>2. Thí Nghiệm Xây Dựng Phân Tử (PhET 3D)</span>
                    </button>
                    <button onclick="switchMediaMode('model-3d')" id="tab-model-3d" class="media-tab px-4 py-2.5 rounded-xl text-xs sm:text-sm font-semibold text-slate-300 hover:text-white transition flex items-center gap-2">
                        <i class="fa-solid fa-cubes"></i>
                        <span>3. Mô Hình Phân Tử N₂ - H₂O - CH₄ - CO₂</span>
                    </button>
                </div>

                <!-- CHẾ ĐỘ 1: VIDEO BÀI GIẢNG VỚI NGUYÊN LÝ KHÔNG LỖI 153 -->
                <div id="media-content-interactive-hub" class="space-y-6">
                    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                        <!-- Cột Trình phát Video HTML5 & Video Picker -->
                        <div class="lg:col-span-2 glass-card p-6 sm:p-7 rounded-3xl shadow-xl space-y-4">
                            <div class="flex flex-wrap items-center justify-between gap-3">
                                <div>
                                    <span class="text-xs font-bold text-cyan-600 uppercase">Trình phát bài giảng trực tuyến</span>
                                    <h3 class="text-lg font-bold text-slate-800" id="current-player-title">Bài Giảng KHTN 7 - Bài 5: Phân tử, Đơn chất, Hợp chất</h3>
                                </div>
                                <div class="flex items-center gap-2">
                                    <label for="local-video-file" class="cursor-pointer px-3 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold border border-slate-300 transition flex items-center gap-1.5" title="Chọn file video mp4 có sẵn trong máy Thầy/Cô để phát ngay">
                                        <i class="fa-solid fa-folder-open text-blue-600"></i>
                                        <span>Phát file MP4 từ máy</span>
                                    </label>
                                    <input type="file" id="local-video-file" accept="video/*" class="hidden" onchange="playLocalVideo(event)">
                                </div>
                            </div>

                            <!-- Native HTML5 Video Player (Không bao giờ dính lỗi 153 của iframe YouTube) -->
                            <div class="relative w-full aspect-video rounded-2xl overflow-hidden shadow-2xl bg-black border border-slate-700 flex items-center justify-center group">
                                <video id="main-html5-player" class="w-full h-full object-cover" controls poster="Screenshot 2026-10-01 161043.png">
                                    <!-- Video nguồn khoa học mở dự phòng -->
                                    <source src="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4" type="video/mp4">
                                    Trình duyệt của bạn không hỗ trợ thẻ video HTML5.
                                </video>
                            </div>

                            <!-- Thanh công cụ điều khiển bài giảng nhanh -->
                            <div class="p-3.5 bg-blue-50/80 rounded-2xl border border-blue-200 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs">
                                <div class="text-slate-700 font-medium">
                                    <i class="fa-solid fa-circle-check text-emerald-600 mr-1"></i>
                                    Trình phát HTML5 chuyên dụng - Phát ổn định 100% trên máy tính cá nhân.
                                </div>
                                <div class="flex items-center gap-2">
                                    <button onclick="document.getElementById('main-html5-player').currentTime = 0; document.getElementById('main-html5-player').play();" class="px-3 py-1 rounded-lg bg-blue-600 text-white font-bold hover:bg-blue-700 transition">
                                        <i class="fa-solid fa-rotate-left"></i> Xem lại từ đầu
                                    </button>
                                </div>
                            </div>
                        </div>

                        <!-- Danh mục các bài giảng chất lượng cao trên YouTube (Mở 1-click an toàn tuyệt đối) -->
                        <div class="glass-card p-6 rounded-3xl shadow-xl flex flex-col justify-between space-y-4">
                            <div>
                                <h3 class="font-bold text-slate-800 text-base mb-1 flex items-center gap-2">
                                    <i class="fa-brands fa-youtube text-red-600 text-xl"></i>
                                    <span>Trung Tâm Video Bài Giảng Chuẩn</span>
                                </h3>
                                <p class="text-slate-600 text-xs leading-relaxed mb-4">
                                    Nhấp để mở bài giảng trực tiếp trong cửa sổ chuyên dụng hoặc tab mới. Không bao giờ bị chặn hay lỗi mã 153:
                                </p>

                                <div class="space-y-3">
                                    <!-- Link 1 -->
                                    <div class="p-3 rounded-2xl bg-slate-50 hover:bg-blue-50/70 border border-slate-200 transition group flex items-center justify-between">
                                        <div class="space-y-0.5">
                                            <div class="font-bold text-xs text-slate-800 group-hover:text-blue-600">Bài Giảng KHTN 7 (Thầy Liêm)</div>
                                            <div class="text-[11px] text-slate-500">Sách Kết nối tri thức - Chi tiết trang 32-35</div>
                                        </div>
                                        <button onclick="openSafeVideoPopup('https://www.youtube.com/results?search_query=KHTN+7+B%C3%A0i+5+Th%E1%BA%A7y+Li%C3%AAm')" class="px-3 py-1.5 rounded-xl bg-red-600 hover:bg-red-700 text-white text-xs font-bold shadow-md transition flex items-center gap-1">
                                            <i class="fa-solid fa-play text-[10px]"></i> Xem
                                        </button>
                                    </div>

                                    <!-- Link 2 -->
                                    <div class="p-3 rounded-2xl bg-slate-50 hover:bg-blue-50/70 border border-slate-200 transition group flex items-center justify-between">
                                        <div class="space-y-0.5">
                                            <div class="font-bold text-xs text-slate-800 group-hover:text-blue-600">Bài Giảng KHTN 7 (VietJack)</div>
                                            <div class="text-[11px] text-slate-500">Tóm tắt lý thuyết & Giải bài tập SGK</div>
                                        </div>
                                        <button onclick="openSafeVideoPopup('https://www.youtube.com/results?search_query=KHTN+7+B%C3%A0i+5+VietJack+K%E1%BA%BFt+n%E1%BB%91i+tri+th%E1%BB%A9c')" class="px-3 py-1.5 rounded-xl bg-red-600 hover:bg-red-700 text-white text-xs font-bold shadow-md transition flex items-center gap-1">
                                            <i class="fa-solid fa-play text-[10px]"></i> Xem
                                        </button>
                                    </div>

                                    <!-- Link 3 -->
                                    <div class="p-3 rounded-2xl bg-slate-50 hover:bg-blue-50/70 border border-slate-200 transition group flex items-center justify-between">
                                        <div class="space-y-0.5">
                                            <div class="font-bold text-xs text-slate-800 group-hover:text-blue-600">Video 3D Thú Vị (Trạng Education)</div>
                                            <div class="text-[11px] text-slate-500">Mô phỏng sinh động phân tử vi mô</div>
                                        </div>
                                        <button onclick="openSafeVideoPopup('https://www.youtube.com/results?search_query=KHTN+7+Tr%E1%BA%A1ng+Education+Ph%C3%A2n+t%E1%BB%AD+%C4%91%C6%A1n+ch%E1%BA%A5t+h%E1%BB%A3p+ch%E1%BA%A5t')" class="px-3 py-1.5 rounded-xl bg-red-600 hover:bg-red-700 text-white text-xs font-bold shadow-md transition flex items-center gap-1">
                                            <i class="fa-solid fa-play text-[10px]"></i> Xem
                                        </button>
                                    </div>
                                </div>
                            </div>

                            <div class="pt-4 border-t border-slate-200 text-center">
                                <a href="https://www.youtube.com/results?search_query=KHTN+7+B%C3%A0i+5+Ph%C3%A2n+t%E1%BB%AD+%C4%90%C6%A1n+ch%E1%BA%A5t+H%E1%BB%A3p+ch%E1%BA%A5t" target="_blank" class="text-xs font-bold text-blue-600 hover:underline flex items-center justify-center gap-1.5">
                                    <i class="fa-solid fa-magnifying-glass"></i>
                                    <span>Tìm kiếm thêm bài giảng khác trên YouTube</span>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- CHẾ ĐỘ 2: THÍ NGHIỆM XÂY DỰNG PHÂN TỬ 3D PHET (ĐẠI HỌC COLORADO) -->
                <div id="media-content-phet-sim" class="hidden space-y-4">
                    <div class="glass-card p-6 rounded-3xl shadow-xl space-y-4">
                        <div class="flex flex-wrap items-center justify-between gap-3">
                            <div>
                                <span class="text-xs font-bold text-purple-600 uppercase">Phòng thí nghiệm ảo quốc tế</span>
                                <h3 class="text-xl font-bold text-slate-800">Mô phỏng PhET: Xây Dựng & Ghép Nối Phân Tử (Build a Molecule)</h3>
                                <p class="text-slate-600 text-xs">Học sinh tự tay kéo thả các nguyên tử H, O, C, N để tạo thành các phân tử N₂, H₂O, CO₂, CH₄ theo đúng bài học.</p>
                            </div>
                            <a href="https://phet.colorado.edu/sims/html/build-a-molecule/latest/build-a-molecule_en.html" target="_blank" class="glass-btn px-4 py-2 rounded-xl text-white text-xs font-bold flex items-center gap-2">
                                <i class="fa-solid fa-expand"></i> Mở toàn màn hình
                            </a>
                        </div>

                        <!-- Iframe PhET HTML5 chuẩn (Hoạt động hoàn hảo trên file:/// và web) -->
                        <div class="relative w-full h-[620px] rounded-2xl overflow-hidden shadow-2xl border border-slate-300 bg-slate-900">
                            <iframe 
                                src="https://phet.colorado.edu/sims/html/build-a-molecule/latest/build-a-molecule_en.html" 
                                class="w-full h-full border-0" 
                                allowfullscreen>
                            </iframe>
                        </div>
                    </div>
                </div>

                <!-- CHẾ ĐỘ 3: MÔ HÌNH 4 PHÂN TỬ 3D CSS THUẦN -->
                <div id="media-content-model-3d" class="hidden space-y-6">
                    <div class="glass-card p-6 sm:p-8 rounded-3xl shadow-xl">
                        <h3 class="text-xl font-extrabold text-slate-800 font-heading mb-6 flex items-center gap-2">
                            <i class="fa-solid fa-shapes text-cyan-600"></i>
                            <span>Phòng Thí Nghiệm Mô Phỏng 3D: Cấu Trúc Các Phân Tử</span>
                        </h3>

                        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                            <!-- Model 1: Nitrogen N2 -->
                            <div class="bg-gradient-to-b from-slate-50 to-blue-50/50 p-6 rounded-2xl border border-slate-200 text-center flex flex-col justify-between hover:shadow-lg transition">
                                <div>
                                    <span class="text-[11px] font-bold text-blue-600 uppercase tracking-wide">Đơn chất</span>
                                    <h4 class="font-bold text-slate-800 text-base mt-1">Khí Nitrogen (N₂)</h4>
                                    <div class="h-36 flex items-center justify-center my-4">
                                        <div class="flex items-center gap-1">
                                            <div class="atom atom-n">N</div>
                                            <div class="bond-bar w-8"></div>
                                            <div class="atom atom-n">N</div>
                                        </div>
                                    </div>
                                </div>
                                <div class="text-xs text-slate-600 border-t border-slate-200 pt-3">
                                    <div>2 nguyên tử Nitrogen</div>
                                    <div class="font-bold text-blue-700 mt-1">KLPT: 28 amu</div>
                                </div>
                            </div>

                            <!-- Model 2: Nước H2O -->
                            <div class="bg-gradient-to-b from-slate-50 to-blue-50/50 p-6 rounded-2xl border border-slate-200 text-center flex flex-col justify-between hover:shadow-lg transition">
                                <div>
                                    <span class="text-[11px] font-bold text-rose-600 uppercase tracking-wide">Hợp chất</span>
                                    <h4 class="font-bold text-slate-800 text-base mt-1">Nước (H₂O)</h4>
                                    <div class="h-36 flex items-center justify-center my-4">
                                        <div class="relative w-36 h-28 flex items-center justify-center">
                                            <div class="atom atom-o absolute top-1">O</div>
                                            <div class="atom atom-h absolute bottom-1 left-2">H</div>
                                            <div class="atom atom-h absolute bottom-1 right-2">H</div>
                                        </div>
                                    </div>
                                </div>
                                <div class="text-xs text-slate-600 border-t border-slate-200 pt-3">
                                    <div>1 Oxygen + 2 Hydrogen</div>
                                    <div class="font-bold text-rose-700 mt-1">KLPT: 18 amu</div>
                                </div>
                            </div>

                            <!-- Model 3: Methane CH4 -->
                            <div class="bg-gradient-to-b from-slate-50 to-blue-50/50 p-6 rounded-2xl border border-slate-200 text-center flex flex-col justify-between hover:shadow-lg transition">
                                <div>
                                    <span class="text-[11px] font-bold text-emerald-600 uppercase tracking-wide">Hợp chất</span>
                                    <h4 class="font-bold text-slate-800 text-base mt-1">Khí Methane (CH₄)</h4>
                                    <div class="h-36 flex items-center justify-center my-4">
                                        <div class="relative w-32 h-32 flex items-center justify-center">
                                            <div class="atom atom-c">C</div>
                                            <div class="atom atom-h absolute -top-1">H</div>
                                            <div class="atom atom-h absolute -bottom-1">H</div>
                                            <div class="atom atom-h absolute -left-1">H</div>
                                            <div class="atom atom-h absolute -right-1">H</div>
                                        </div>
                                    </div>
                                </div>
                                <div class="text-xs text-slate-600 border-t border-slate-200 pt-3">
                                    <div>1 Carbon + 4 Hydrogen</div>
                                    <div class="font-bold text-emerald-700 mt-1">KLPT: 16 amu</div>
                                </div>
                            </div>

                            <!-- Model 4: Carbon Dioxide CO2 -->
                            <div class="bg-gradient-to-b from-slate-50 to-blue-50/50 p-6 rounded-2xl border border-slate-200 text-center flex flex-col justify-between hover:shadow-lg transition">
                                <div>
                                    <span class="text-[11px] font-bold text-amber-600 uppercase tracking-wide">Hợp chất</span>
                                    <h4 class="font-bold text-slate-800 text-base mt-1">Carbon Dioxide (CO₂)</h4>
                                    <div class="h-36 flex items-center justify-center my-4">
                                        <div class="flex items-center gap-1">
                                            <div class="atom atom-o">O</div>
                                            <div class="bond-bar w-5"></div>
                                            <div class="atom atom-c">C</div>
                                            <div class="bond-bar w-5"></div>
                                            <div class="atom atom-o">O</div>
                                        </div>
                                    </div>
                                </div>
                                <div class="text-xs text-slate-600 border-t border-slate-200 pt-3">
                                    <div>1 Carbon + 2 Oxygen</div>
                                    <div class="font-bold text-amber-700 mt-1">KLPT: 44 amu</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>


            <!-- ========================================== -->
            <!-- 5. TRUNG TÂM BÀI TẬP (50 CÂU TƯƠNG TÁC)     -->
            <!-- ========================================== -->
            <section id="section-quiz-center" class="hidden space-y-6 animate-fade-in">
                <div class="glass-card p-4 sm:p-6 rounded-3xl shadow-xl flex flex-col sm:flex-row items-center justify-between gap-4">
                    <div class="flex items-center gap-3 w-full sm:w-auto">
                        <button onclick="navigateSection('dashboard')" class="w-10 h-10 rounded-2xl bg-slate-100 hover:bg-slate-200 text-slate-700 flex items-center justify-center transition">
                            <i class="fa-solid fa-arrow-left"></i>
                        </button>
                        <div>
                            <div class="flex items-center gap-2">
                                <span id="quiz-filter-badge" class="px-3 py-0.5 rounded-full text-xs font-bold bg-blue-100 text-blue-700">Tất cả (50 câu)</span>
                                <span class="text-xs text-slate-500 font-semibold">Câu <span id="quiz-current-idx">1</span>/<span id="quiz-total-count">50</span></span>
                            </div>
                            <h3 class="text-lg font-bold text-slate-800" id="quiz-type-title">Trắc nghiệm 1 lựa chọn</h3>
                        </div>
                    </div>

                    <div class="flex flex-wrap items-center gap-3 w-full sm:w-auto justify-between sm:justify-end">
                        <div class="flex items-center gap-2 bg-slate-100 px-3 py-1.5 rounded-2xl text-xs font-bold text-slate-700">
                            <i class="fa-solid fa-stopwatch text-blue-600"></i>
                            <span id="quiz-timer-display">00:00</span>
                        </div>
                        <div class="flex items-center gap-2 bg-emerald-50 text-emerald-700 px-3 py-1.5 rounded-2xl text-xs font-bold border border-emerald-200">
                            <i class="fa-solid fa-star text-amber-500"></i>
                            <span>Đúng: <span id="quiz-correct-count">0</span></span>
                        </div>
                        <button onclick="submitAndSyncQuizEarly()" title="Nộp toàn bộ bài và đồng bộ kết quả lên Google Sheet" class="px-3.5 py-1.5 rounded-2xl bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white font-bold text-xs flex items-center gap-1.5 shadow-md hover:shadow-lg transition-all active:scale-95">
                            <i class="fa-solid fa-cloud-arrow-up"></i>
                            <span>Nộp bài & Đồng bộ</span>
                        </button>
                    </div>
                </div>

                <div class="w-full bg-slate-700/40 rounded-full h-2.5 overflow-hidden backdrop-blur-md">
                    <div id="quiz-progress-bar" class="bg-gradient-to-r from-cyan-400 to-blue-500 h-2.5 rounded-full transition-all duration-300" style="width: 2%;"></div>
                </div>

                <div id="quiz-card-container" class="glass-card p-6 sm:p-10 rounded-3xl shadow-2xl relative min-h-[400px] flex flex-col justify-between">
                    <div id="quiz-question-body" class="space-y-6"></div>

                    <div id="quiz-feedback-box" class="hidden mt-6 p-5 rounded-2xl transition-all">
                        <div class="flex items-start gap-3">
                            <div id="feedback-icon" class="text-2xl mt-0.5"></div>
                            <div class="flex-grow">
                                <h4 id="feedback-title" class="font-bold text-sm"></h4>
                                <p id="feedback-explanation" class="text-xs mt-1 leading-relaxed"></p>
                            </div>
                        </div>
                    </div>

                    <div class="mt-8 pt-6 border-t border-slate-200/80 flex flex-wrap items-center justify-between gap-3">
                        <button onclick="prevQuizQuestion()" id="btn-prev-question" class="px-5 py-2.5 rounded-xl border border-slate-300 text-slate-700 hover:bg-slate-100 font-semibold text-xs flex items-center gap-2 transition disabled:opacity-40 disabled:cursor-not-allowed">
                            <i class="fa-solid fa-arrow-left"></i>
                            <span>Câu trước</span>
                        </button>

                        <div class="flex flex-wrap items-center gap-3">
                            <button onclick="submitAndSyncQuizEarly()" class="px-4 py-2.5 rounded-xl border border-emerald-500/40 bg-emerald-50 hover:bg-emerald-100 text-emerald-800 font-bold text-xs flex items-center gap-2 transition">
                                <i class="fa-solid fa-paper-plane text-emerald-600"></i>
                                <span>Nộp bài & Đồng bộ Google Sheet</span>
                            </button>
                            <button onclick="submitCurrentAnswer()" id="btn-submit-answer" class="glass-btn px-7 py-3 rounded-xl text-white font-bold text-sm shadow-md flex items-center gap-2">
                                <i class="fa-solid fa-check"></i>
                                <span>Kiểm tra</span>
                            </button>
                            <button onclick="nextQuizQuestion()" id="btn-next-question" class="hidden px-7 py-3 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm shadow-md flex items-center gap-2 transition">
                                <span>Câu kế tiếp</span>
                                <i class="fa-solid fa-arrow-right"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </section>


            <!-- ========================================== -->
            <!-- 6. MÀN HÌNH KẾT QUẢ & BÁO CÁO               -->
            <!-- ========================================== -->
            <section id="section-result" class="hidden space-y-8 animate-fade-in">
                <div id="report-card-export" class="glass-card max-w-3xl mx-auto p-8 sm:p-12 rounded-3xl shadow-2xl relative overflow-hidden border border-white/80 bg-white">
                    <div class="text-center space-y-4">
                        <div class="flex items-center justify-center gap-4">
                            <div class="p-2 sm:p-2.5 rounded-3xl bg-amber-500/10 border border-amber-300/40 shadow-md">
                                <img src="data:image/png;base64,{logo_b64}" alt="Logo Thầy Lê Văn Thắng" class="w-16 h-16 sm:w-20 sm:h-20 object-contain drop-shadow-md">
                            </div>
                            <div id="result-mascot" class="inline-block p-4 rounded-3xl bg-gradient-to-tr from-cyan-400 to-blue-600 text-white text-4xl sm:text-5xl shadow-xl mascot-jump">
                                <i class="fa-solid fa-user-astronaut"></i>
                            </div>
                        </div>

                        <div>
                            <span class="px-3.5 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-blue-100 text-blue-700">CHỨNG NHẬN HOÀN THÀNH BÀI HỌC</span>
                            <h2 class="text-3xl sm:text-4xl font-extrabold text-slate-900 font-heading mt-2">BÁO CÁO KẾT QUẢ HỌC TẬP</h2>
                            <p class="text-slate-500 text-xs sm:text-sm mt-1">Bài 5: Phân tử - Đơn chất - Hợp chất (KHTN 7 Kết nối tri thức)</p>
                        </div>

                        <div id="result-stars" class="flex justify-center items-center gap-2 text-3xl sm:text-4xl text-amber-400"></div>
                    </div>

                    <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 my-8 text-center">
                        <div class="p-4 rounded-2xl bg-slate-50 border border-slate-200">
                            <span class="block text-xs text-slate-500 font-semibold">Học sinh</span>
                            <span id="report-name" class="font-bold text-slate-800 text-base">Học sinh</span>
                        </div>
                        <div class="p-4 rounded-2xl bg-slate-50 border border-slate-200">
                            <span class="block text-xs text-slate-500 font-semibold">Lớp</span>
                            <span id="report-class" class="font-bold text-slate-800 text-base">7A</span>
                        </div>
                        <div class="p-4 rounded-2xl bg-blue-50 border border-blue-200">
                            <span class="block text-xs text-blue-600 font-semibold">Điểm số</span>
                            <span id="report-score" class="font-black text-blue-700 text-xl">100/100</span>
                        </div>
                        <div class="p-4 rounded-2xl bg-slate-50 border border-slate-200">
                            <span class="block text-xs text-slate-500 font-semibold">Thời gian làm</span>
                            <span id="report-time" class="font-bold text-slate-800 text-base">02:45</span>
                        </div>
                    </div>

                    <div class="bg-gradient-to-r from-blue-50 to-cyan-50 p-5 rounded-2xl border border-blue-200 text-slate-800 text-sm">
                        <div class="flex items-center gap-2 font-bold text-blue-900 mb-1">
                            <i class="fa-solid fa-comment-dots text-blue-600"></i>
                            <span>Lời khen & Đánh giá năng lực:</span>
                        </div>
                        <p id="report-feedback-text" class="text-xs leading-relaxed text-slate-700">
                            Xuất sắc! Em đã nắm rất vững toàn bộ khái niệm về đơn chất, hợp chất và cách tính khối lượng phân tử. Tiếp tục phát huy nhé!
                        </p>
                    </div>

                    <div class="mt-8 pt-4 border-t border-slate-200 flex justify-between items-center text-[11px] text-slate-400">
                        <span>EduTech Science 7 Platform</span>
                        <span id="report-date-str">Ngày hoàn thành: --/--/----</span>
                    </div>
                </div>

                <div class="max-w-3xl mx-auto flex flex-wrap items-center justify-center gap-3">
                    <button onclick="downloadPdfReport()" class="glass-btn px-6 py-3 rounded-xl text-white font-bold text-xs sm:text-sm shadow-lg flex items-center gap-2">
                        <i class="fa-solid fa-file-pdf"></i>
                        <span>Tải Báo Cáo (PDF / Ảnh)</span>
                    </button>
                    <button onclick="syncGoogleSheets()" id="btn-sync-sheets" class="px-6 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs sm:text-sm shadow-lg flex items-center gap-2 transition">
                        <i class="fa-solid fa-cloud-arrow-up"></i>
                        <span>Nộp bài & Đồng bộ Google Sheet</span>
                    </button>
                    <button onclick="restartQuiz()" class="px-6 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs sm:text-sm shadow-lg flex items-center gap-2 transition">
                        <i class="fa-solid fa-rotate-right"></i>
                        <span>Làm lại bài tập</span>
                    </button>
                </div>
            </section>


            <!-- ========================================== -->
            <!-- 7. BẢNG XẾP HẠNG (LEADERBOARD)             -->
            <!-- ========================================== -->
            <section id="section-leaderboard" class="hidden space-y-6 animate-fade-in max-w-4xl mx-auto">
                <div class="flex items-center justify-between">
                    <div>
                        <button onclick="navigateSection('dashboard')" class="text-xs font-semibold text-cyan-300 hover:text-white mb-2 flex items-center gap-1.5 transition">
                            <i class="fa-solid fa-chevron-left"></i> Quay lại Menu
                        </button>
                        <h2 class="text-2xl sm:text-3xl font-extrabold text-white font-heading">Bảng Vinh Danh Top Học Sinh</h2>
                        <p class="text-slate-300 text-sm">Dữ liệu lưu trữ LocalStorage & Đồng bộ lớp học</p>
                    </div>
                    <button onclick="clearLeaderboard()" class="text-xs text-rose-400 hover:text-rose-200 underline">
                        Xoá lịch sử lưu máy
                    </button>
                </div>

                <div class="glass-card p-6 sm:p-8 rounded-3xl shadow-2xl overflow-hidden">
                    <div class="overflow-x-auto">
                        <table class="w-full text-left border-collapse text-sm">
                            <thead>
                                <tr class="bg-slate-100 text-slate-700 font-bold uppercase text-xs">
                                    <th class="p-3.5 rounded-l-xl">Hạng</th>
                                    <th class="p-3.5">Học sinh</th>
                                    <th class="p-3.5">Lớp</th>
                                    <th class="p-3.5 text-center">Điểm số</th>
                                    <th class="p-3.5 text-center">Thời gian</th>
                                    <th class="p-3.5 rounded-r-xl text-right">Ngày nộp</th>
                                </tr>
                            </thead>
                            <tbody id="leaderboard-body" class="divide-y divide-slate-100 text-slate-800 font-medium"></tbody>
                        </table>
                    </div>
                </div>
            </section>

        </main>

        <!-- FOOTER -->
        <footer class="glass-panel-dark mt-12 py-6 border-t border-white/10 text-center text-xs text-slate-400">
            <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
                <div class="flex items-center gap-2.5">
                    <img src="data:image/png;base64,{logo_b64}" alt="Logo Thầy Lê Văn Thắng" class="w-9 h-9 object-contain rounded-xl bg-white/10 p-1 shadow">
                    <span class="font-bold text-slate-200 text-sm">Thầy Lê Văn Thắng - EduTech KHTN 7</span>
                    <span class="hidden md:inline">- Sách Kết nối tri thức với cuộc sống</span>
                </div>
                <div class="flex items-center gap-4">
                    <button onclick="openSheetConfigModal()" class="text-cyan-400 hover:text-cyan-300 font-semibold underline flex items-center gap-1.5 transition">
                        <i class="fa-solid fa-gear"></i>
                        <span>Cài đặt URL Google Sheet (Dành cho Giáo viên)</span>
                    </button>
                    <span class="text-slate-600 hidden sm:inline">|</span>
                    <span class="hidden sm:inline">Chuẩn EdTech Senior Developer</span>
                </div>
            </div>
        </footer>
    </div>

    <!-- MODAL CẤU HÌNH GOOGLE SHEET APPS SCRIPT URL -->
    <div id="modal-sheet-config" class="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm hidden flex items-center justify-center p-4">
        <div class="glass-card max-w-lg w-full p-6 sm:p-8 rounded-3xl border border-white/80 shadow-2xl relative bg-white animate-fade-in">
            <button onclick="closeSheetConfigModal()" class="absolute top-4 right-4 w-9 h-9 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-500 flex items-center justify-center transition">
                <i class="fa-solid fa-xmark text-base"></i>
            </button>

            <div class="flex items-center gap-3 mb-4">
                <div class="w-12 h-12 rounded-2xl bg-emerald-100 text-emerald-700 flex items-center justify-center text-xl shadow">
                    <i class="fa-solid fa-file-excel"></i>
                </div>
                <div>
                    <h3 class="text-lg font-bold text-slate-900 font-heading">Cấu Hình Google Sheet Đồng Bộ</h3>
                    <p class="text-xs text-slate-500">Dành cho Thầy/Cô quản lý kết quả học sinh tự động</p>
                </div>
            </div>

            <div class="space-y-4 text-xs text-slate-700">
                <div class="p-3.5 rounded-2xl bg-slate-50 border border-slate-200 space-y-1.5">
                    <p class="font-bold text-slate-800 flex items-center gap-1.5">
                        <i class="fa-solid fa-circle-info text-blue-600"></i>
                        <span>Hướng dẫn nhanh cho Thầy/Cô:</span>
                    </p>
                    <p>1. Mở Google Sheet của lớp &gt; <strong>Tiện ích mở rộng</strong> &gt; <strong>Apps Script</strong>.</p>
                    <p>2. Dán mã tiếp nhận JSON dữ liệu (xem chi tiết cuối hướng dẫn).</p>
                    <p>3. Chọn <strong>Triển khai (Deploy)</strong> &gt; <strong>Ứng dụng web mới (Web App)</strong> &gt; Chọn quyền truy cập: <em>Bất kỳ ai (Anyone)</em>.</p>
                    <p>4. Dán đường link Web App (kết thúc bằng <code>/exec</code>) vào ô bên dưới:</p>
                </div>

                <div>
                    <label class="block font-bold text-slate-800 uppercase tracking-wide mb-1.5">Web App URL Google Apps Script:</label>
                    <input type="url" id="input-sheet-url" placeholder="https://script.google.com/macros/s/AKfycb.../exec"
                        class="w-full p-3.5 rounded-xl border border-slate-300 focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100 outline-none font-mono text-xs text-slate-800 bg-white">
                    <p class="text-[11px] text-slate-500 mt-1">* Nếu để trống hoặc mặc định, hệ thống sẽ chạy ở chế độ [MÔ PHỎNG AN TOÀN] thông báo kết quả chi tiết.</p>
                </div>

                <div class="flex items-center justify-between pt-3 border-t border-slate-100">
                    <button type="button" onclick="resetDefaultSheetUrl()" class="px-3.5 py-2 rounded-xl text-slate-500 hover:text-slate-800 text-xs font-semibold transition">
                        Khôi phục mẫu
                    </button>
                    <div class="flex items-center gap-2">
                        <button type="button" onclick="closeSheetConfigModal()" class="px-4 py-2 rounded-xl border border-slate-200 text-slate-700 hover:bg-slate-100 text-xs font-bold transition">
                            Đóng
                        </button>
                        <button type="button" onclick="saveSheetConfigUrl()" class="px-5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold shadow-md transition flex items-center gap-1.5">
                            <i class="fa-solid fa-floppy-disk"></i>
                            <span>Lưu cấu hình</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- ========================================================================= -->
    <!-- JAVASCRIPT LOGIC ENGINE                                                   -->
    <!-- ========================================================================= -->
    <script>
        const QUIZ_DATA = {quiz_data_json};

        let GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbxevY7vhagqdOp1onoVC9EI_nj4WV0bj0BBSrjNW04NfsmxxdXiE-qR3j8_i_Z2yTGb/exec";

        let currentUser = {{ name: "", className: "" }};
        let activeQuizQuestions = [...QUIZ_DATA];
        let currentQuestionIndex = 0;
        let userAnswers = {{}};
        let quizTimerInterval = null;
        let secondsElapsed = 0;
        let isAudioMuted = false;

        /* MEDIA SWITCHER CONTROLLER */
        function switchMediaMode(mode) {{
            playClickSound();
            document.querySelectorAll(".media-tab").forEach(tab => {{
                tab.classList.remove("active-media-tab");
                tab.classList.add("text-slate-300");
            }});

            const activeBtn = document.getElementById(`tab-${{mode}}`);
            if (activeBtn) {{
                activeBtn.classList.add("active-media-tab");
                activeBtn.classList.remove("text-slate-300");
            }}

            const modes = ['interactive-hub', 'phet-sim', 'model-3d'];
            modes.forEach(m => {{
                const el = document.getElementById(`media-content-${{m}}`);
                if (el) el.classList.add("hidden");
            }});

            const target = document.getElementById(`media-content-${{mode}}`);
            if (target) {{
                target.classList.remove("hidden");
            }}
        }}

        /* PHÁT FILE VIDEO NỘI BỘ TỪ MÁY TÍNH CỦA GIÁO VIÊN */
        function playLocalVideo(event) {{
            const file = event.target.files[0];
            if (!file) return;

            const videoPlayer = document.getElementById("main-html5-player");
            const fileUrl = URL.createObjectURL(file);
            videoPlayer.src = fileUrl;
            document.getElementById("current-player-title").textContent = `Đang phát từ máy: ${{file.name}}`;
            videoPlayer.play();
            playSuccessSound();
        }}

        /* MỞ VIDEO TRONG CỬA SỔ AN TOÀN TRÁNH 100% LỖI 153 */
        function openSafeVideoPopup(url) {{
            playClickSound();
            const width = 960;
            const height = 580;
            const left = (window.screen.width - width) / 2;
            const top = (window.screen.height - height) / 2;
            window.open(url, '_blank', `toolbar=yes,location=yes,status=yes,menubar=no,scrollbars=yes,resizable=yes,width=${{width}},height=${{height}},top=${{top}},left=${{left}}`);
        }}

        /* WEB AUDIO API */
        let audioCtx = null;
        function getAudioContext() {{
            if (!audioCtx) {{
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            }}
            if (audioCtx.state === 'suspended') {{
                audioCtx.resume();
            }}
            return audioCtx;
        }}

        function playSuccessSound() {{
            if (isAudioMuted) return;
            try {{
                const ctx = getAudioContext();
                const now = ctx.currentTime;
                const osc1 = ctx.createOscillator();
                const gain1 = ctx.createGain();
                osc1.type = "sine";
                osc1.frequency.setValueAtTime(1318.5, now);
                gain1.gain.setValueAtTime(0.2, now);
                gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
                osc1.connect(gain1);
                gain1.connect(ctx.destination);
                osc1.start(now);
                osc1.stop(now + 0.35);

                const osc2 = ctx.createOscillator();
                const gain2 = ctx.createGain();
                osc2.type = "triangle";
                osc2.frequency.setValueAtTime(1760.0, now + 0.12);
                gain2.gain.setValueAtTime(0.25, now + 0.12);
                gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.6);
                osc2.connect(gain2);
                gain2.connect(ctx.destination);
                osc2.start(now + 0.12);
                osc2.stop(now + 0.6);
            }} catch (e) {{}}
        }}

        function playErrorSound() {{
            if (isAudioMuted) return;
            try {{
                const ctx = getAudioContext();
                const now = ctx.currentTime;
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = "sawtooth";
                osc.frequency.setValueAtTime(160, now);
                osc.frequency.exponentialRampToValueAtTime(80, now + 0.3);
                gain.gain.setValueAtTime(0.25, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.3);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(now);
                osc.stop(now + 0.3);
            }} catch (e) {{}}
        }}

        function playClickSound() {{
            if (isAudioMuted) return;
            try {{
                const ctx = getAudioContext();
                const now = ctx.currentTime;
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = "sine";
                osc.frequency.setValueAtTime(800, now);
                gain.gain.setValueAtTime(0.08, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.06);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(now);
                osc.stop(now + 0.06);
            }} catch(e) {{}}
        }}

        function toggleAudio() {{
            isAudioMuted = !isAudioMuted;
            const btn = document.getElementById("btn-audio-toggle");
            if (isAudioMuted) {{
                btn.innerHTML = '<i class="fa-solid fa-volume-xmark text-sm text-rose-400"></i>';
            }} else {{
                btn.innerHTML = '<i class="fa-solid fa-volume-high text-sm"></i>';
                playSuccessSound();
            }}
        }}

        /* AUTH & NAVIGATION */
        function handleLogin(e) {{
            e.preventDefault();
            const name = document.getElementById("login-name").value.trim();
            const cls = document.getElementById("login-class").value.trim();
            if (!name || !cls) return;

            currentUser.name = name;
            currentUser.className = cls;
            localStorage.setItem("khtn7_user", JSON.stringify(currentUser));

            document.getElementById("header-user-name").textContent = name;
            document.getElementById("header-user-class").textContent = cls;
            document.getElementById("dash-user-name").textContent = name;

            document.getElementById("app-header").classList.remove("hidden");
            navigateSection("dashboard");
            playSuccessSound();
            fireConfettiBurst();
        }}

        function logoutStudent() {{
            if (confirm("Em có chắc chắn muốn đăng xuất không?")) {{
                localStorage.removeItem("khtn7_user");
                currentUser = {{ name: "", className: "" }};
                document.getElementById("app-header").classList.add("hidden");
                navigateSection("login");
            }}
        }}

        function navigateSection(sectionId) {{
            playClickSound();
            const sections = ["login", "dashboard", "theory", "video", "quiz-center", "result", "leaderboard"];
            sections.forEach(sec => {{
                const el = document.getElementById(`section-${{sec}}`);
                if (el) el.classList.add("hidden");
            }});

            const target = document.getElementById(`section-${{sectionId}}`);
            if (target) {{
                target.classList.remove("hidden");
                window.scrollTo({{ top: 0, behavior: 'smooth' }});
            }}

            document.querySelectorAll(".nav-tab").forEach(tab => {{
                tab.classList.remove("bg-blue-600", "text-white");
                tab.classList.add("text-slate-300");
            }});
            const activeTab = document.getElementById(`nav-btn-${{sectionId}}`);
            if (activeTab) {{
                activeTab.classList.add("bg-blue-600", "text-white");
                activeTab.classList.remove("text-slate-300");
            }}

            if (sectionId === 'dashboard') {{
                updateDashboardStats();
            }} else if (sectionId === 'leaderboard') {{
                renderLeaderboard();
            }}
        }}

        /* QUIZ ENGINE */
        function openQuizCenter(filterType = 'all') {{
            startQuizMode(filterType);
        }}
        function startQuizMode(filterType) {{
            if (filterType === 'all') {{
                activeQuizQuestions = [...QUIZ_DATA];
                document.getElementById("quiz-filter-badge").textContent = "Tất cả (50 câu)";
            }} else {{
                activeQuizQuestions = QUIZ_DATA.filter(q => q.type === filterType);
                const typeNames = {{
                    'mcq': 'Trắc nghiệm 1 lựa chọn (10 câu)',
                    'fill': 'Điền khuyết (10 câu)',
                    'match': 'Ghép cột tương ứng (10 câu)',
                    'tf': 'Đúng / Sai (10 câu)',
                    'essay': 'Tự luận ngắn (10 câu)'
                }};
                document.getElementById("quiz-filter-badge").textContent = typeNames[filterType] || filterType;
            }}

            currentQuestionIndex = 0;
            userAnswers = {{}};
            secondsElapsed = 0;
            startQuizTimer();
            navigateSection("quiz-center");
            renderCurrentQuestion();
        }}

        function startQuizTimer() {{
            clearInterval(quizTimerInterval);
            secondsElapsed = 0;
            quizTimerInterval = setInterval(() => {{
                secondsElapsed++;
                const mins = String(Math.floor(secondsElapsed / 60)).padStart(2, '0');
                const secs = String(secondsElapsed % 60).padStart(2, '0');
                document.getElementById("quiz-timer-display").textContent = `${{mins}}:${{secs}}`;
            }}, 1000);
        }}

        function renderCurrentQuestion() {{
            const q = activeQuizQuestions[currentQuestionIndex];
            if (!q) {{
                console.error("No question found at index", currentQuestionIndex);
                return;
            }}

            document.getElementById("quiz-current-idx").textContent = currentQuestionIndex + 1;
            document.getElementById("quiz-total-count").textContent = activeQuizQuestions.length;
            document.getElementById("quiz-type-title").textContent = q.type_label;

            const progressPct = ((currentQuestionIndex + 1) / activeQuizQuestions.length) * 100;
            document.getElementById("quiz-progress-bar").style.width = `${{progressPct}}%`;

            document.getElementById("btn-prev-question").disabled = currentQuestionIndex === 0;
            document.getElementById("btn-submit-answer").classList.remove("hidden");
            document.getElementById("btn-next-question").classList.add("hidden");
            document.getElementById("quiz-feedback-box").classList.add("hidden");

            const body = document.getElementById("quiz-question-body");
            let html = `
                <div class="text-base sm:text-lg font-bold text-slate-800 leading-snug">
                    <span class="text-blue-600 mr-2">Câu ${{q.id}}:</span> ${{q.question}}
                </div>
            `;

            if (q.type === 'mcq') {{
                html += `<div class="grid grid-cols-1 gap-3 mt-4">`;
                q.options.forEach((opt, idx) => {{
                    const isChecked = userAnswers[q.id] === idx;
                    const borderClass = isChecked 
                        ? 'border-blue-500 bg-blue-50/90 text-blue-900 shadow-sm ring-2 ring-blue-300 font-bold' 
                        : 'border-slate-200 bg-white hover:bg-slate-50 text-slate-700 font-semibold';
                    const circleClass = isChecked 
                        ? 'border-blue-600 bg-blue-600 text-white' 
                        : 'border-slate-300 bg-white text-transparent';
                    html += `
                        <button type="button" onclick="selectMcqOption(${{idx}})" 
                            class="p-4 rounded-2xl border text-left text-sm transition-all flex items-center justify-between ${{borderClass}}">
                            <span>${{opt}}</span>
                            <span class="w-6 h-6 rounded-full border flex items-center justify-center text-xs shadow-sm ${{circleClass}}">
                                ${{isChecked ? '✓' : ''}}
                            </span>
                        </button>
                    `;
                }});
                html += `</div>`;
            }}
            else if (q.type === 'fill') {{
                const currentVal = userAnswers[q.id] || "";
                html += `
                    <div class="mt-6 space-y-3">
                        <label class="block text-xs font-bold text-slate-600 uppercase">Nhập từ hoặc cụm từ thích hợp:</label>
                        <input type="text" id="fill-input-${{q.id}}" value="${{currentVal}}" 
                            placeholder="${{q.placeholder || 'Nhập câu trả lời...'}}" 
                            class="w-full p-4 rounded-2xl border border-slate-300 focus:border-blue-500 focus:ring-4 focus:ring-blue-100 outline-none text-base font-semibold text-slate-800 bg-white shadow-sm"
                            oninput="userAnswers[${{q.id}}] = this.value">
                    </div>
                `;
            }}
            else if (q.type === 'tf') {{
                const currentVal = userAnswers[q.id];
                const trueClass = currentVal === true 
                    ? 'border-emerald-500 bg-emerald-50 text-emerald-800 ring-2 ring-emerald-300 font-black shadow-md' 
                    : 'border-slate-200 bg-white hover:bg-emerald-50/50 text-slate-700 font-bold';
                const falseClass = currentVal === false 
                    ? 'border-rose-500 bg-rose-50 text-rose-800 ring-2 ring-rose-300 font-black shadow-md' 
                    : 'border-slate-200 bg-white hover:bg-rose-50/50 text-slate-700 font-bold';

                html += `
                    <div class="grid grid-cols-2 gap-4 mt-6 max-w-md mx-auto">
                        <button type="button" onclick="selectTfOption(true)" class="p-5 rounded-2xl border text-center text-base transition-all flex flex-col items-center gap-2 ${{trueClass}}">
                            <i class="fa-solid fa-circle-check text-2xl text-emerald-600"></i>
                            <span>ĐÚNG</span>
                        </button>
                        <button type="button" onclick="selectTfOption(false)" class="p-5 rounded-2xl border text-center text-base transition-all flex flex-col items-center gap-2 ${{falseClass}}">
                            <i class="fa-solid fa-circle-xmark text-2xl text-rose-600"></i>
                            <span>SAI</span>
                        </button>
                    </div>
                `;
            }}
            else if (q.type === 'match') {{
                const rightOptions = q.pairs.map(p => p.right);
                if (!userAnswers[q.id]) userAnswers[q.id] = {{}};

                html += `<div class="mt-4 space-y-3">`;
                q.pairs.forEach((pair, pIdx) => {{
                    const curMatch = userAnswers[q.id][pair.left] || "";
                    let optsSelect = `<option value="">-- Chọn nội dung ghép --</option>`;
                    rightOptions.forEach(opt => {{
                        optsSelect += `<option value="${{opt}}" ${{curMatch === opt ? 'selected' : ''}}>${{opt}}</option>`;
                    }});

                    html += `
                        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 p-3.5 rounded-2xl bg-slate-50 border border-slate-200">
                            <div class="font-bold text-slate-800 text-sm flex items-center gap-2">
                                <span class="w-6 h-6 rounded-lg bg-blue-100 text-blue-700 text-xs flex items-center justify-center font-black">${{pIdx + 1}}</span>
                                <span>${{pair.left}}</span>
                            </div>
                            <select onchange="updateMatchAnswer(${{q.id}}, '${{pair.left}}', this.value)" 
                                class="w-full sm:w-auto p-2.5 rounded-xl border border-slate-300 text-xs font-semibold text-slate-700 bg-white outline-none focus:border-blue-500">
                                ${{optsSelect}}
                            </select>
                        </div>
                    `;
                }});
                html += `</div>`;
            }}
            else if (q.type === 'essay') {{
                const currentVal = userAnswers[q.id] || "";
                html += `
                    <div class="mt-4 space-y-3">
                        <label class="block text-xs font-bold text-slate-600 uppercase">Trình bày câu trả lời của em:</label>
                        <textarea id="essay-input-${{q.id}}" rows="4" 
                            placeholder="Em hãy viết câu trả lời đầy đủ, nêu rõ các bước hoặc luận điểm..." 
                            class="w-full p-4 rounded-2xl border border-slate-300 focus:border-blue-500 focus:ring-4 focus:ring-blue-100 outline-none text-sm font-medium text-slate-800 bg-white shadow-sm leading-relaxed"
                            oninput="userAnswers[${{q.id}}] = this.value">${{currentVal}}</textarea>
                        <p class="text-[11px] text-slate-500">* Hệ thống sẽ tự động quét các từ khoá trọng tâm và hiển thị đáp án mẫu chi tiết.</p>
                    </div>
                `;
            }}

            body.innerHTML = html;
        }}

        function updateMatchAnswer(qId, leftKey, val) {{
            if (!userAnswers[qId]) userAnswers[qId] = {{}};
            userAnswers[qId][leftKey] = val;
        }}

        function selectMcqOption(idx) {{
            playClickSound();
            const q = activeQuizQuestions[currentQuestionIndex];
            userAnswers[q.id] = idx;
            renderCurrentQuestion();
        }}

        function selectTfOption(val) {{
            playClickSound();
            const q = activeQuizQuestions[currentQuestionIndex];
            userAnswers[q.id] = val;
            renderCurrentQuestion();
        }}

        function submitCurrentAnswer() {{
            const q = activeQuizQuestions[currentQuestionIndex];
            const ans = userAnswers[q.id];

            if (ans === undefined || ans === null || ans === "") {{
                alert("Em vui lòng chọn hoặc nhập câu trả lời trước khi kiểm tra nhé!");
                return;
            }}

            let isCorrect = false;

            if (q.type === 'mcq') {{
                isCorrect = ans === q.answer;
            }} 
            else if (q.type === 'fill') {{
                const cleanAns = ans.trim().toLowerCase();
                isCorrect = q.keywords.some(k => cleanAns.includes(k.toLowerCase()));
            }} 
            else if (q.type === 'tf') {{
                isCorrect = ans === q.answer;
            }} 
            else if (q.type === 'match') {{
                let allMatched = true;
                q.pairs.forEach(p => {{
                    if (ans[p.left] !== p.right) allMatched = false;
                }});
                isCorrect = allMatched;
            }} 
            else if (q.type === 'essay') {{
                const cleanAns = ans.trim().toLowerCase();
                let matchCount = 0;
                q.keywords.forEach(k => {{
                    if (cleanAns.includes(k.toLowerCase())) matchCount++;
                }});
                isCorrect = matchCount >= 1;
            }}

            const feedbackBox = document.getElementById("quiz-feedback-box");
            const fbIcon = document.getElementById("feedback-icon");
            const fbTitle = document.getElementById("feedback-title");
            const fbExplanation = document.getElementById("feedback-explanation");
            const quizCard = document.getElementById("quiz-card-container");

            feedbackBox.classList.remove("hidden");

            if (isCorrect) {{
                playSuccessSound();
                fireConfettiBurst();
                feedbackBox.className = "mt-6 p-5 rounded-2xl bg-emerald-50 border border-emerald-300 text-emerald-900";
                fbIcon.innerHTML = `<i class="fa-solid fa-circle-check text-emerald-600"></i>`;
                fbTitle.textContent = "Chính xác! Làm rất tốt! 🎉";
                fbExplanation.innerHTML = `<strong>Giải thích:</strong> ${{q.explanation}}`;
            }} else {{
                playErrorSound();
                quizCard.classList.add("shake-effect");
                setTimeout(() => quizCard.classList.remove("shake-effect"), 600);

                feedbackBox.className = "mt-6 p-5 rounded-2xl bg-rose-50 border border-rose-300 text-rose-900";
                fbIcon.innerHTML = `<i class="fa-solid fa-triangle-exclamation text-rose-600"></i>`;
                fbTitle.textContent = "Chưa chính xác rồi em ơi! Cùng xem giải thích nhé:";
                fbExplanation.innerHTML = `<strong>Giải thích chi tiết:</strong> ${{q.explanation}} ${{q.sample_answer ? '<br><strong>Đáp án mẫu:</strong> ' + q.sample_answer : ''}}`;
            }}

            updateLiveScore();

            document.getElementById("btn-submit-answer").classList.add("hidden");
            document.getElementById("btn-next-question").classList.remove("hidden");
        }}

        function updateLiveScore() {{
            let correct = 0;
            activeQuizQuestions.forEach(q => {{
                const ans = userAnswers[q.id];
                if (ans === undefined) return;
                if (q.type === 'mcq' && ans === q.answer) correct++;
                else if (q.type === 'fill' && q.keywords.some(k => (ans || "").toLowerCase().includes(k.toLowerCase()))) correct++;
                else if (q.type === 'tf' && ans === q.answer) correct++;
                else if (q.type === 'match') {{
                    let ok = true;
                    q.pairs.forEach(p => {{ if (ans[p.left] !== p.right) ok = false; }});
                    if (ok) correct++;
                }}
                else if (q.type === 'essay' && q.keywords.some(k => (ans || "").toLowerCase().includes(k.toLowerCase()))) correct++;
            }});
            document.getElementById("quiz-correct-count").textContent = correct;
        }}

        function nextQuizQuestion() {{
            playClickSound();
            if (currentQuestionIndex < activeQuizQuestions.length - 1) {{
                currentQuestionIndex++;
                renderCurrentQuestion();
            }} else {{
                finishQuizSession();
            }}
        }}

        function prevQuizQuestion() {{
            playClickSound();
            if (currentQuestionIndex > 0) {{
                currentQuestionIndex--;
                renderCurrentQuestion();
            }}
        }}

        function finishQuizSession() {{
            clearInterval(quizTimerInterval);
            playSuccessSound();
            fireConfettiBurst();

            let correct = 0;
            activeQuizQuestions.forEach(q => {{
                const ans = userAnswers[q.id];
                if (ans === undefined) return;
                if (q.type === 'mcq' && ans === q.answer) correct++;
                else if (q.type === 'fill' && q.keywords.some(k => (ans || "").toLowerCase().includes(k.toLowerCase()))) correct++;
                else if (q.type === 'tf' && ans === q.answer) correct++;
                else if (q.type === 'match') {{
                    let ok = true;
                    q.pairs.forEach(p => {{ if (ans[p.left] !== p.right) ok = false; }});
                    if (ok) correct++;
                }}
                else if (q.type === 'essay' && q.keywords.some(k => (ans || "").toLowerCase().includes(k.toLowerCase()))) correct++;
            }});

            const total = activeQuizQuestions.length;
            const score100 = Math.round((correct / total) * 100);
            const timeStr = document.getElementById("quiz-timer-display").textContent;

            let starsHtml = '';
            let feedback = '';
            if (score100 >= 80) {{
                starsHtml = '<i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i>';
                feedback = 'Xuất sắc! Em là một chuyên gia khoa học thực thụ! Đã nắm vững mọi quy luật về đơn chất, hợp chất và phân tử!';
            }} else if (score100 >= 50) {{
                starsHtml = '<i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-regular fa-star"></i>';
                feedback = 'Khá tốt! Em đã hiểu bài, chỉ cần cẩn thận hơn ở phần tính khối lượng phân tử và các đơn chất phi kim nhé!';
            }} else {{
                starsHtml = '<i class="fa-solid fa-star"></i><i class="fa-regular fa-star"></i><i class="fa-regular fa-star"></i>';
                feedback = 'Cần cố gắng thêm nhé! Em hãy đọc lại phần Phân khu Lý Thuyết và làm lại bài để đạt điểm 100 nhé!';
            }}

            document.getElementById("result-stars").innerHTML = starsHtml;
            document.getElementById("report-name").textContent = currentUser.name || "Học sinh";
            document.getElementById("report-class").textContent = currentUser.className || "7A";
            document.getElementById("report-score").textContent = `${{score100}}/100`;
            document.getElementById("report-time").textContent = timeStr;
            document.getElementById("report-feedback-text").textContent = feedback;
            document.getElementById("report-date-str").textContent = `Ngày hoàn thành: ${{new Date().toLocaleDateString('vi-VN')}} ${{new Date().toLocaleTimeString('vi-VN')}}`;

            saveRecordToLeaderboard({{
                name: currentUser.name || "Học sinh",
                className: currentUser.className || "7A",
                score: score100,
                correctCount: correct,
                totalCount: total,
                time: timeStr,
                date: new Date().toLocaleDateString('vi-VN')
            }});

            navigateSection("result");
        }}

        function restartQuiz() {{
            startQuizMode('all');
        }}

        /* LOCALSTORAGE & LEADERBOARD */
        function saveRecordToLeaderboard(record) {{
            let history = JSON.parse(localStorage.getItem("khtn7_leaderboard") || "[]");
            history.push(record);
            history.sort((a, b) => b.score - a.score);
            localStorage.setItem("khtn7_leaderboard", JSON.stringify(history));
            updateDashboardStats();
        }}

        function renderLeaderboard() {{
            const list = JSON.parse(localStorage.getItem("khtn7_leaderboard") || "[]");
            const tbody = document.getElementById("leaderboard-body");
            tbody.innerHTML = "";

            if (list.length === 0) {{
                tbody.innerHTML = `<tr><td colspan="6" class="text-center py-6 text-slate-400">Chưa có kết quả nào được lưu. Hãy làm bài để ghi danh nhé!</td></tr>`;
                return;
            }}

            list.slice(0, 15).forEach((item, idx) => {{
                const tr = document.createElement("tr");
                tr.className = "hover:bg-slate-50 transition";
                let badge = `<span class="font-bold text-slate-600">${{idx + 1}}</span>`;
                if (idx === 0) badge = `<span class="w-6 h-6 rounded-full bg-amber-400 text-white font-bold flex items-center justify-center text-xs shadow">🥇</span>`;
                else if (idx === 1) badge = `<span class="w-6 h-6 rounded-full bg-slate-300 text-slate-800 font-bold flex items-center justify-center text-xs shadow">🥈</span>`;
                else if (idx === 2) badge = `<span class="w-6 h-6 rounded-full bg-amber-600 text-white font-bold flex items-center justify-center text-xs shadow">🥉</span>`;

                tr.innerHTML = `
                    <td class="p-3.5">${{badge}}</td>
                    <td class="p-3.5 font-bold text-slate-800">${{item.name}}</td>
                    <td class="p-3.5"><span class="px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-600 font-mono text-xs">${{item.className}}</span></td>
                    <td class="p-3.5 text-center font-black text-blue-600">${{item.score}}đ</td>
                    <td class="p-3.5 text-center font-mono text-slate-500 text-xs">${{item.time}}</td>
                    <td class="p-3.5 text-right text-slate-400 text-xs">${{item.date}}</td>
                `;
                tbody.appendChild(tr);
            }});
        }}

        function clearLeaderboard() {{
            if (confirm("Em có muốn xóa toàn bộ lịch sử điểm trên máy này không?")) {{
                localStorage.removeItem("khtn7_leaderboard");
                renderLeaderboard();
                updateDashboardStats();
            }}
        }}

        function updateDashboardStats() {{
            const list = JSON.parse(localStorage.getItem("khtn7_leaderboard") || "[]");
            let highest = 0;
            list.forEach(i => {{ if (i.score > highest) highest = i.score; }});
            document.getElementById("dash-stat-score").textContent = `${{highest}}%`;
            document.getElementById("dash-stat-completed").textContent = `${{list.length}} lần`;
        }}

        /* CONFETTI */
        function fireConfettiBurst() {{
            if (typeof confetti === 'function') {{
                confetti({{
                    particleCount: 80,
                    spread: 70,
                    origin: {{ y: 0.6 }}
                }});
            }}
        }}

        /* EXPORT PDF / IMAGE */
        async function downloadPdfReport() {{
            const element = document.getElementById("report-card-export");
            playClickSound();

            try {{
                const canvas = await html2canvas(element, {{
                    scale: 2,
                    useCORS: true,
                    backgroundColor: '#ffffff'
                }});

                const imgData = canvas.toDataURL('image/png');
                const {{ jsPDF }} = window.jspdf;
                const pdf = new jsPDF('p', 'mm', 'a4');
                const imgWidth = 190;
                const imgHeight = (canvas.height * imgWidth) / canvas.width;
                
                pdf.addImage(imgData, 'PNG', 10, 15, imgWidth, imgHeight);
                pdf.save(`KHTN7_Bai5_BaoCao_${{currentUser.name || 'HocSinh'}}.pdf`);
                playSuccessSound();
                alert("Đã tải báo cáo kết quả PDF thành công!");
            }} catch (error) {{
                console.error("Lỗi xuất PDF", error);
                alert("Không thể xuất PDF trực tiếp, vui lòng thử lại hoặc sử dụng tính năng In của trình duyệt (Ctrl + P).");
            }}
        }}

        /* MODAL CẤU HÌNH GOOGLE SHEET */
        function openSheetConfigModal() {{
            playClickSound();
            const input = document.getElementById("input-sheet-url");
            if (input) {{
                const stored = localStorage.getItem("khtn7_sheets_url");
                input.value = stored || (GOOGLE_SHEET_URL.includes("PLACEHOLDER") ? "" : GOOGLE_SHEET_URL);
            }}
            document.getElementById("modal-sheet-config").classList.remove("hidden");
        }}

        function closeSheetConfigModal() {{
            playClickSound();
            document.getElementById("modal-sheet-config").classList.add("hidden");
        }}

        function saveSheetConfigUrl() {{
            playClickSound();
            const input = document.getElementById("input-sheet-url");
            const val = input.value.trim();
            if (val) {{
                if (!val.startsWith("https://script.google.com/macros/s/")) {{
                    alert("Đường dẫn Web App của Google Apps Script thường bắt đầu bằng: https://script.google.com/macros/s/.../exec\\nThầy/Cô hãy kiểm tra lại nhé!");
                    return;
                }}
                GOOGLE_SHEET_URL = val;
                localStorage.setItem("khtn7_sheets_url", val);
                playSuccessSound();
                alert("Đã lưu URL Google Sheet thành công! Từ bây giờ kết quả làm bài của học sinh sẽ tự động gửi về bảng tính này.");
            }} else {{
                localStorage.removeItem("khtn7_sheets_url");
                GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbxevY7vhagqdOp1onoVC9EI_nj4WV0bj0BBSrjNW04NfsmxxdXiE-qR3j8_i_Z2yTGb/exec";
                alert("Đã khôi phục URL Google Sheet chính thức của Thầy.");
            }}
            closeSheetConfigModal();
        }}

        function resetDefaultSheetUrl() {{
            const input = document.getElementById("input-sheet-url");
            input.value = "";
        }}

        /* NỘP BÀI SỚM & ĐỒNG BỘ TRỰC TIẾP TỪ PHÂN KHU LUYỆN TẬP */
        async function submitAndSyncQuizEarly() {{
            playClickSound();
            const total = activeQuizQuestions.length;
            const answeredCount = Object.keys(userAnswers).length;
            
            let confirmMsg = `Em có chắc chắn muốn nộp bài và đồng bộ kết quả lên Google Sheet không?`;
            if (answeredCount < total) {{
                confirmMsg = `Em mới trả lời ${{answeredCount}}/${{total}} câu hỏi. Em có chắc chắn muốn nộp bài sớm và gửi kết quả lên Google Sheet không?`;
            }}

            if (!confirm(confirmMsg)) return;

            // Kết thúc lượt làm bài và chuyển tới màn hình kết quả
            finishQuizSession();

            // Tự động gọi đồng bộ ngay lập tức
            setTimeout(() => {{
                syncGoogleSheets();
            }}, 500);
        }}

        /* SYNC GOOGLE SHEETS */
        async function syncGoogleSheets() {{
            const btn = document.getElementById("btn-sync-sheets");
            playClickSound();
            if (btn) {{
                btn.disabled = true;
                btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Đang nộp bài & đồng bộ...`;
            }}

            const activeUrl = localStorage.getItem("khtn7_sheets_url") || GOOGLE_SHEET_URL;

            const payload = {{
                studentName: currentUser.name || "Học sinh",
                studentClass: currentUser.className || "7A",
                score: document.getElementById("report-score") ? document.getElementById("report-score").textContent : "0/100",
                correctCount: document.getElementById("quiz-correct-count") ? document.getElementById("quiz-correct-count").textContent : "0",
                totalQuestions: activeQuizQuestions ? activeQuizQuestions.length : 50,
                timeSpent: document.getElementById("report-time") ? document.getElementById("report-time").textContent : "00:00",
                completedAt: new Date().toLocaleString('vi-VN')
            }};

            try {{
                if (activeUrl.includes("PLACEHOLDER")) {{
                    await new Promise(r => setTimeout(r, 1000));
                    playSuccessSound();
                    fireConfettiBurst();
                    alert(`✅ [ĐÃ GỬI BÁO CÁO THÀNH CÔNG]\\n\\nThông tin đã nộp:\\n- Học sinh: ${{payload.studentName}}\\n- Lớp: ${{payload.studentClass}}\\n- Điểm số: ${{payload.score}}\\n- Thời gian: ${{payload.timeSpent}}\\n\\n💡 Ghi chú dành cho Thầy/Cô:\\nỨng dụng đang chạy ở chế độ mô phỏng an toàn. Thầy/Cô hãy nhấn nút "Google Sheet" trên thanh điều hướng hoặc ở chân trang để dán đường link Web App triển khai từ Google Sheets để bảng tính tự động ghi nhận học sinh.`);
                }} else {{
                    await fetch(activeUrl, {{
                        method: "POST",
                        mode: "no-cors",
                        headers: {{ "Content-Type": "application/json" }},
                        body: JSON.stringify(payload)
                    }});
                    playSuccessSound();
                    fireConfettiBurst();
                    alert(`🎉 Chúc mừng ${{payload.studentName}}!\\nBài thi của em đã được nộp và đồng bộ thành công vào Google Sheet của lớp!\\nĐiểm số ghi nhận: ${{payload.score}}`);
                }}
            }} catch (err) {{
                console.error("Lỗi đồng bộ Sheets:", err);
                alert("Đồng bộ thất bại, vui lòng kiểm tra kết nối Internet!");
            }} finally {{
                if (btn) {{
                    btn.disabled = false;
                    btn.innerHTML = `<i class="fa-solid fa-cloud-arrow-up"></i> Nộp bài & Đồng bộ Google Sheet`;
                }}
            }}
        }}

        /* INIT */
        window.addEventListener("DOMContentLoaded", () => {{
            const savedUrl = localStorage.getItem("khtn7_sheets_url");
            if (savedUrl) {{
                GOOGLE_SHEET_URL = savedUrl;
            }}

            const saved = localStorage.getItem("khtn7_user");
            if (saved) {{
                try {{
                    const u = JSON.parse(saved);
                    if (u.name && u.className) {{
                        currentUser = u;
                        document.getElementById("header-user-name").textContent = u.name;
                        document.getElementById("header-user-class").textContent = u.className;
                        document.getElementById("dash-user-name").textContent = u.name;
                        document.getElementById("app-header").classList.remove("hidden");
                        navigateSection("dashboard");
                        return;
                    }}
                }} catch(e) {{}}
            }}
            navigateSection("login");
        }});
    </script>
</body>
</html>
'''

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"File index.html built successfully with Version 3.0! Size: {len(html_content)} chars")
