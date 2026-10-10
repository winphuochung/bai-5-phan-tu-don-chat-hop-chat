const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

// Tìm tất cả các chỗ gọi navigateSection('quiz-center')
const matches = html.match(/navigateSection\(['"]quiz-center['"]\)/g);
console.log('Matches:', matches);

// Kiểm tra hàm navigateSection trong HTML
const navIdx = html.indexOf('function navigateSection(');
console.log('navigateSection code:\n', html.substring(navIdx, navIdx + 700));
