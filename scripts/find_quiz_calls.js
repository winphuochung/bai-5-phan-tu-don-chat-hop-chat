const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const regex = /navigateSection\(['"]quiz-center['"]\)/g;
let match;
while ((match = regex.exec(html)) !== null) {
  const start = Math.max(0, match.index - 100);
  const end = Math.min(html.length, match.index + 100);
  console.log('--- CALL AT', match.index, '---');
  console.log(html.substring(start, end).replace(/\s+/g, ' '));
}
