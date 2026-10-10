const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

// Lấy block script
const scriptStart = html.lastIndexOf('<script>');
const scriptEnd = html.lastIndexOf('</script>');
const script = html.substring(scriptStart + 8, scriptEnd);

// Phân tích QUIZ_DATA
const qMatch = script.match(/const QUIZ_DATA = (\[[\s\S]*?\]);\s*let GOOGLE_SHEET_URL/);
if (!qMatch) {
  console.error('Could not find QUIZ_DATA in script!');
  process.exit(1);
}

const quizData = JSON.parse(qMatch[1]);
console.log('Quiz data parsed successfully, count =', quizData.length);
console.log('Question 1:', quizData[0]);
