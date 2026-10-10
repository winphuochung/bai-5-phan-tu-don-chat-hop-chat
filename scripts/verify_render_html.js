const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

// Mock DOM
const elements = {};
function getEl(id) {
  if (!elements[id]) {
    elements[id] = {
      id: id,
      textContent: '',
      innerHTML: '',
      classList: {
        add: () => {},
        remove: () => {}
      },
      disabled: false,
      style: {}
    };
  }
  return elements[id];
}

const mockDoc = {
  getElementById: getEl,
  createElement: () => ({ classList: { add: ()=>{}, remove: ()=>{} }, style: {} }),
  querySelectorAll: () => [],
  addEventListener: () => {}
};

const scriptStart = html.lastIndexOf('<script>');
const scriptEnd = html.lastIndexOf('</script>');
const script = html.substring(scriptStart + 8, scriptEnd);

const runEnv = new Function('document', 'window', 'localStorage', 'alert', 'confirm', script + `
  startQuizMode('all');
  return {
    qId: document.getElementById('quiz-current-idx').textContent,
    qTitle: document.getElementById('quiz-type-title').textContent,
    bodyHTML: document.getElementById('quiz-question-body').innerHTML.substring(0, 300)
  };
`);

const res = runEnv(mockDoc, { scrollTo: ()=>{}, addEventListener: ()=>{} }, { getItem: ()=>null, setItem: ()=>{} }, console.log, ()=>true);
console.log('Test result:');
console.log('Current Index:', res.qId);
console.log('Type Title:', res.qTitle);
console.log('Rendered Body Preview:\n', res.bodyHTML);
