const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

// Sửa 1: Nút menu Luyện tập (50 câu) trên thanh điều hướng Header
html = html.replace(
  'onclick="navigateSection(\'quiz-center\')" id="nav-btn-quiz"',
  'onclick="startQuizMode(\'all\')" id="nav-btn-quiz"'
);

// Sửa 2: Khối Card "Phân khu 3: Trung tâm Bài tập (50 câu)" ở màn hình Dashboard
html = html.replace(
  'onclick="navigateSection(\'quiz-center\')"',
  'onclick="startQuizMode(\'all\')"'
);

// Sửa 3: Cải tiến logic trong hàm navigateSection để tự động khởi tạo quiz nếu đang trống
const oldNavCheck = "if (sectionId === 'dashboard') {";
const newNavCheck = `if (sectionId === 'quiz-center') {
                const bodyEl = document.getElementById('quiz-question-body');
                if (!bodyEl || bodyEl.children.length === 0 || !activeQuizQuestions || activeQuizQuestions.length === 0) {
                    startQuizMode('all');
                } else {
                    renderCurrentQuestion();
                }
            } else if (sectionId === 'dashboard') {`;

html = html.replace(oldNavCheck, newNavCheck);

fs.writeFileSync('index.html', html, 'utf8');
console.log('Successfully patched index.html for auto-rendering quiz questions!');
