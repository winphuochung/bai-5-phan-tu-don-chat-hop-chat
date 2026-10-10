const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const id1 = html.indexOf('id="section-quiz-center"');
const id2 = html.lastIndexOf('id="section-quiz-center"');
console.log('section-quiz-center matches:', (html.match(/id="section-quiz-center"/g) || []).length);
console.log('quiz-question-body matches:', (html.match(/id="quiz-question-body"/g) || []).length);
console.log('quiz-card-container matches:', (html.match(/id="quiz-card-container"/g) || []).length);
