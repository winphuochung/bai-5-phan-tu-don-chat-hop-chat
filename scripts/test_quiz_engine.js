const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

// Giả lập DOM
const elements = {};
function getEl(id) {
  if (!elements[id]) {
    elements[id] = {
      id: id,
      textContent: '',
      innerHTML: '',
      children: [],
      classList: {
        classes: new Set(),
        add: function(c) { this.classes.add(c); },
        remove: function(c) { this.classes.delete(c); },
        contains: function(c) { return this.classes.has(c); }
      },
      appendChild: function(child) {
        this.children.push(child);
      },
      style: {}
    };
  }
  return elements[id];
}

const mockDoc = {
  getElementById: getEl,
  createElement: function(tag) {
    return {
      tagName: tag,
      textContent: '',
      innerHTML: '',
      children: [],
      classList: {
        classes: new Set(),
        add: function(c) { this.classes.add(c); },
        remove: function(c) { this.classes.delete(c); }
      },
      appendChild: function(c) { this.children.push(c); },
      style: {}
    };
  },
  querySelectorAll: function() { return []; },
  addEventListener: function() {}
};

// Lấy script
const scriptStart = html.lastIndexOf('<script>');
const scriptEnd = html.lastIndexOf('</script>');
const script = html.substring(scriptStart + 8, scriptEnd);

const runEnv = new Function('document', 'window', 'localStorage', 'alert', 'confirm', script + `
  startQuizMode('all');
  return {
    activeCount: activeQuizQuestions.length,
    currIdx: currentQuestionIndex,
    bodyHTML: document.getElementById('quiz-question-body').innerHTML,
    bodyChildren: document.getElementById('quiz-question-body').children.length
  };
`);

const result = runEnv(mockDoc, { scrollTo: ()=>{}, addEventListener: ()=>{} }, { getItem: ()=>null, setItem: ()=>{} }, console.log, ()=>true);
console.log('Result of startQuizMode:', result);
