const assert=require('node:assert/strict'),E=require('./engine.js');
function s(){return {sessions:[],weights:{squat:12},nextWeights:{},equipment:{kb:[8,12,16],club:[5,10]}}}
let a=s();assert.equal(E.plan(a).slot,0);assert.ok(E.plan(a).total<=45);assert.equal(E.prescription(a,'squat').sets,3);
function log(state,rx,quality='clean',reps=rx.reps,weight=rx.weight){const rec=E.completeRecord(rx,Array.from({length:rx.sets},()=>({done:true,reps,weight})),quality,false);state.sessions.push({date:'2026-11-04',slot:0,items:[rec]});return rec;}
log(a,E.prescription(a,'squat'));assert.equal(E.prescription(a,'squat').sets,3);log(a,E.prescription(a,'squat'));assert.equal(E.prescription(a,'squat').sets,4);
let b=s();log(b,E.prescription(b,'squat'),'hard');log(b,E.prescription(b,'squat'),'hard');assert.equal(E.prescription(b,'squat').mode,'rebuild');
let c=s();for(let i=0;i<14;i++)log(c,E.prescription(c,'squat'));assert.equal(E.stateFor(c,'squat').phase,'ready');assert.equal(E.stateFor(c,'squat').cycles,1);for(let i=0;i<4;i++)log(c,E.prescription(c,'squat'));assert.equal(E.stateFor(c,'squat').cycles,1);
c.nextWeights.squat=16;assert.equal(E.prescription(c,'squat').weight,16);assert.equal(E.prescription(c,'squat').sets,3);
let d=s();let p=E.plan(d,{readiness:'low'});assert.ok(p.items.every(x=>x.mode==='recovery'||x.mode==='time-fit'));assert.ok(p.total<=45);
let e=s();let x=E.prescription(e,'squat');let rec=E.completeRecord(x,[{done:true,reps:6,weight:12}],'clean',true);assert.equal(rec.completed,false);e.sessions.push({date:'2026-11-04',items:[rec]});assert.equal(E.prescription(e,'squat').mode,'review');
console.log('Engine tests passed');

// Adjustable session budgets never silently reduce a movement's prescribed sets.
for(const minutes of [15,20,30,45,60,90,120]){const plan=E.plan(s(),{minutes});assert.ok(plan.total<=minutes);assert.equal(plan.budget.total,minutes);for(const rx of plan.items)assert.equal(rx.sets,E.prescription(s(),rx.id).sets);}
let short=E.plan(s(),{minutes:15});assert.ok(short.deferred.length>0);
let carry=s();carry.deferredIds=['cast'];const carried=E.plan(carry,{minutes:45});assert.equal(carried.items[0].id,'cast');
assert.throws(()=>E.plan(s(),{minutes:10}));
