const fs=require('fs'),vm=require('vm'),assert=require('assert');
const app=fs.readFileSync(__dirname+'/app.js','utf8');
function boot(saved){
 const store={...(saved?{'strengthlab-data-v31':JSON.stringify(saved)}:{})};
 const elements={};const node=()=>({textContent:'',innerHTML:'',dataset:{},classList:{toggle(){}},querySelectorAll(){return []},addEventListener(){},value:'',style:{}});
 const document={body:{dataset:{}},getElementById(id){return elements[id]??=node()},querySelectorAll(){return []},addEventListener(){},createElement:node};
 const context={document,localStorage:{getItem:k=>store[k]||null,setItem:(k,v)=>store[k]=v},navigator:{onLine:false},window:{addEventListener(){}},location:{protocol:'file:'},Date,Math,Number,JSON,console,setInterval(){},clearInterval(){},alert(){},URL,Blob};
 vm.createContext(context);vm.runInContext(app,context);return {context,store};
}
const fresh=boot();
assert.equal(vm.runInContext('ROTATION_LENGTH',fresh.context),3);
assert.equal(vm.runInContext('slotPlan(5).title',fresh.context),'A · Squat / Press / Pull');
assert.equal(vm.runInContext('slotPlan(6).title',fresh.context),'B · Hinge / Club / Carry');
assert.equal(vm.runInContext('slotPlan(7).title',fresh.context),'C · Clean / Squat / Club');
assert.equal(vm.runInContext('slotPlan(8).title',fresh.context),'A · Squat / Press / Pull');
assert.equal(vm.runInContext('PREP.strength.length',fresh.context),3);
assert.equal(vm.runInContext('FINISH.strength.length',fresh.context),3);
assert.equal(vm.runInContext('estimateMainMinutes(slotPlan(5))>0',fresh.context),true);
assert.equal(vm.runInContext('state.sessions.length',fresh.context),0);
assert.equal(vm.runInContext('state.sequence',fresh.context),5);
console.log('V31 smoke tests passed: ABC sequence, preparation, time estimator and clean initial state.');
