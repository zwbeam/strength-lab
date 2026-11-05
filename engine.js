/* Strength Lab prescription engine. Pure functions, no browser dependencies. */
(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.StrengthEngine=api;})(typeof globalThis!=='undefined'?globalThis:this,function(){
'use strict';
const MOVES={
 swing:{name:'Two-hand swing',gear:'kb',unit:'kg',family:'hinge',method:'volume',reps:10,start:3,end:6,rest:90,sec:25,side:1,cues:['Hinge at the hips; keep your back stable.','Drive with the hips; arms guide the bell.','Stop when the bell no longer floats from hip power.'],avoid:'Do not turn the swing into a squat or shoulder raise.'},
 squat:{name:'Goblet squat',gear:'kb',unit:'kg',family:'squat',method:'volume',reps:6,start:3,end:5,rest:105,sec:30,side:1,cues:['Hold the bell close and brace.','Sit between the hips with heels planted.','Stand tall without leaning backward.'],avoid:'Reduce depth or load if you lose control.'},
 press:{name:'Single-arm strict press',gear:'kb',unit:'kg',family:'press',method:'volume',reps:5,start:2,end:4,rest:120,sec:45,side:2,cues:['Rack with wrist straight and ribs stacked.','Press without a knee dip or sideways lean.','Lower under control; train both sides.'],avoid:'Do not press through shoulder pain.'},
 row:{name:'Single-arm row',gear:'kb',unit:'kg',family:'pull',method:'volume',reps:8,start:2,end:4,rest:90,sec:40,side:2,cues:['Hinge with a stable torso.','Pull elbow toward your back pocket.','Lower without twisting.'],avoid:'Avoid rotating the trunk to finish the pull.'},
 clean:{name:'Single-arm clean',gear:'kb',unit:'kg',family:'hinge',method:'volume',reps:5,start:2,end:4,rest:105,sec:45,side:2,cues:['Start with a controlled hike and hip drive.','Keep the bell close and guide it around the hand.','Finish in a quiet rack without forearm impact.'],avoid:'Stop if the bell repeatedly crashes into your arm.'},
 carry:{name:'Suitcase carry',gear:'kb',unit:'kg',family:'carry',method:'volume',reps:30,start:2,end:4,rest:75,sec:70,side:2,timed:true,cues:['Stand tall with one bell at your side.','Walk slowly without leaning.','Change sides and match the time.'],avoid:'Do not continue if grip or posture fails.'},
 cast:{name:'Two-hand shield cast',gear:'club',unit:'lb',family:'rotation',method:'volume',reps:5,start:2,end:4,rest:90,sec:45,side:2,cues:['Begin with a light club and clear space.','Move smoothly around the head within comfortable range.','Return to the front under control; reverse direction.'],avoid:'Avoid forcing the shoulders or striking the body.'},
 circles:{name:'Two-hand club circles',gear:'club',unit:'lb',family:'rotation',method:'volume',reps:6,start:2,end:4,rest:90,sec:45,side:2,cues:['Brace and keep the feet planted.','Draw a controlled circle on each side.','Match the arc and tempo in both directions.'],avoid:'Do not chase speed at the expense of control.'},
 front:{name:'Two-hand club front swing',gear:'club',unit:'lb',family:'hinge',method:'volume',reps:8,start:3,end:5,rest:90,sec:30,side:1,cues:['Stand stable with hands secure.','Swing with a smooth hip-driven rhythm.','Control the return rather than letting the club pull you.'],avoid:'Avoid snapping the lower back.'}
};
const DAYS=[{name:'A · Squat / Press / Pull',focus:'Kettlebell strength',ids:['squat','press','row']},{name:'B · Hinge / Cast / Carry',focus:'Hinge and club control',ids:['swing','cast','carry']},{name:'C · Clean / Club / Squat',focus:'Skill and balanced strength',ids:['clean','front','circles']}];
const LOADS={kb:[4,6,8,10,12,14,16,18,20,22,24,28,32,36,40,44,48],club:[2,3,4,5,7,10,12,15,17,20,25,30,35]};
const clamp=(n,a,b)=>Math.min(b,Math.max(a,n));
function records(s,id){return(s.sessions||[]).flatMap((x,sessionIndex)=>(x.items||[]).map((y,itemIndex)=>({...y,date:x.date,_key:`${x.id||x.date+':'+sessionIndex}:${itemIndex}`})).filter(y=>y.id===id)).sort((a,b)=>String(a.date).localeCompare(String(b.date)));}
function successful(x){return x&&x.quality==='clean'&&!x.pain&&x.completed===true&&x.actualSets>=x.targetSets&&x.actualReps>=x.targetReps&&Number(x.weight)>0;}
function stateFor(s,id){const m=MOVES[id],h=records(s,id);let phase='volume',sets=m.start,rest=m.rest,weight=0,streak=0,fail=0,cycles=0,hold='';
 const resolvedKeys=s.painResolutions?.[id]?.painKeys||[];
 const reviewedIndex=h.reduce((last,x,index)=>resolvedKeys.includes(x._key)?index:last,-1);
 for(const [index,x] of h.entries()){
  if(Number(x.weight)>0&&Number(x.weight)!==weight){weight=Number(x.weight);phase='volume';sets=m.start;rest=m.rest;streak=0;fail=0;}
  if(x.pain||x.quality==='pain'){if(!resolvedKeys.includes(x._key))hold='Pain reported: stop and review this movement.';streak=0;fail++;continue;}
  // Recovery work may rebuild confidence but never counts toward advancement.
  if(x.performed&&['rebuild','reentry','recovery'].includes(x.mode)){streak=0;if(x.quality==='clean')fail=0;continue;}
  if(hold||phase==='ready')continue;
  if(successful(x)&&x.targetSets===sets&&x.targetReps===m.reps&&Math.abs(Number(x.rest)-rest)<1){streak++;fail=0;if(streak>=2){streak=0;if(sets<m.end)sets++;else{phase='ready';cycles++;}}}
  else if(x.completed===false||x.quality==='hard'||x.quality==='breakdown'){streak=0;fail++;}
 }
 const override=Number(s.nextWeights?.[id]);if(override>0&&override!==weight){weight=override;phase='volume';sets=m.start;rest=m.rest;streak=0;fail=0;}else if(!h.length){weight=Number(s.weights?.[id])||0;}
 const reviewRecovery=resolvedKeys.length>0&&!h.slice(reviewedIndex+1).some(x=>x.performed&&['reentry','recovery'].includes(x.mode)&&x.quality==='clean');
 return{phase,sets,rest,weight,streak,fail,cycles,hold,reviewRecovery,last:h.at(-1)||null,exposures:h.length};}
function resolvePain(s,id){if(!MOVES[id])throw Error('Unknown movement');return {...s,painResolutions:{...s.painResolutions,[id]:{painKeys:records(s,id).filter(x=>x.pain||x.quality==='pain').map(x=>x._key)}}};}
function movementGap(s,id,now=new Date()){const last=records(s,id).filter(x=>x.actualSets>0).at(-1);if(!last)return 0;return Math.max(0,Math.floor((new Date(now).setHours(12,0,0,0)-new Date(last.date+'T12:00:00'))/86400000));}
function prescription(s,id,opts={}){const m=MOVES[id],st=stateFor(s,id);let sets=st.sets,rest=st.rest,reason='',mode=st.phase,weight=st.weight;
 if(st.hold){reason=st.hold+' Resolve the review before resuming this movement.';mode='review';}
 else if(!weight){reason='Choose a comfortable working weight. Start light; do not test a maximum.';mode='baseline';}
 else if(st.fail>=2){sets=Math.max(m.start,sets-1);reason='Repeated difficulty: reduce one set and rebuild clean performance.';mode='rebuild';}
 else if(st.phase==='ready'){reason='Cycle complete. Maintain this load, or explicitly select your next available weight to begin a new volume cycle.';mode='milestone';}
 else if(st.phase==='density'){reason='Density phase: hold weight and work; reduce rest only after two clean, complete exposures.';}
 else{reason=`Volume phase: hold load and rest; complete ${sets} sets cleanly twice before increasing volume.`;}
 if(opts.readiness==='low'){sets=Math.max(1,Math.ceil(sets/2));reason='Low-readiness session: half the normal working sets; no advancement credit. '+reason;mode='recovery';}
 if(opts.reentry||st.reviewRecovery||movementGap(s,id,opts.now)>14){sets=Math.min(sets,Math.max(1,Math.floor(st.sets*0.7)));reason='Return after a break: ease back in; do not count this session toward advancement. '+reason;mode='reentry';}
 if(st.hold){mode='review';sets=0;reason=st.hold+' Resolve the review before resuming this movement.';}
 return{id,name:m.name,unit:m.unit,weight,sets,reps:m.reps,rest,side:m.side,timed:!!m.timed,mode,reason,phase:st.phase,streak:st.streak,cycle:st.cycles};}
function minutesFor(p){const m=MOVES[p.id];return(p.sets*(m.sec+Math.max(0,p.rest))/60)+.55;}
function timeBudget(minutes){
 const total=Number.isFinite(Number(minutes))?Number(minutes):45;
 if(!Number.isInteger(total)||total<15||total>120)throw Error('Workout duration must be 15–120 minutes');
 const warmup=total<=20?4:total<=35?5:total<=60?7:10;
 const cooldown=total<=20?3:total<=35?4:total<=60?7:10;
 return {total,warmup,cooldown,main:total-warmup-cooldown};
}
function plan(s,opts={}){
 const slot=(s.sessions||[]).filter(x=>x.slot!==undefined).length%3,day=DAYS[slot];
 const last=s.sessions?.at(-1),gap=last?Math.floor((new Date().setHours(12,0,0,0)-new Date(last.date+'T12:00:00'))/86400000):0;
 const reentry=gap>14,budget=timeBudget(opts.minutes??s.defaultMinutes??45);
 const ids=[...new Set([...(s.deferredIds||[]),...day.ids])];
 const items=[],deferred=[],held=[],unavailable=[];let used=0;
 for(const id of ids){
  if(!MOVES[id])continue;
  if(s.paused){deferred.push(id);continue;}
  if(Array.isArray(s.equipment?.[MOVES[id].gear])&&!s.equipment[MOVES[id].gear].length){unavailable.push(id);deferred.push(id);continue;}
  if(stateFor(s,id).hold){held.push(id);deferred.push(id);continue;}
  const rx=prescription(s,id,opts);
  const cost=minutesFor(rx);
  if(used+cost>budget.main+1e-8){deferred.push(id);continue;}
  items.push(rx);used+=cost;
 }
 return {slot,day,items,deferred,held,unavailable,paused:!!s.paused,estimated:Math.ceil(used),total:Math.ceil(used)+budget.warmup+budget.cooldown,reentry:items.some(x=>x.mode==='reentry'),cap:budget.main,budget};
}
function deferredAfter(plan,records){const pending=new Set(plan.deferred||[]);for(const record of records){if(!(record.performed??record.completed))pending.add(record.id);else pending.delete(record.id);}return [...pending];}
function completeRecord(rx,actual,quality,pain){
 const sets=(actual||[]).filter(x=>x.done),valid=x=>Number.isFinite(Number(x.weight))&&Number(x.weight)>0&&Number.isInteger(Number(x.reps))&&Number(x.reps)>0;
 const reps=sets.length?Math.min(...sets.map(x=>Number(x.reps)||0)):0;
 const weight=sets.length?Number(sets[0].weight):Number(rx.weight);
 const sameLoad=sets.every(x=>Number(x.weight)===weight);
 const bilateral=rx.side!==2||sets.every(x=>x.bothSides===true);
 const performed=rx.mode!=='review'&&sets.length>0&&sets.length>=rx.sets&&sets.every(valid)&&reps>=rx.reps&&sameLoad&&bilateral&&!['hard','breakdown','pain'].includes(quality)&&!pain;
 return{id:rx.id,name:rx.name,weight,unit:rx.unit,actualSets:sets.length,actualReps:reps,targetSets:rx.sets,targetReps:rx.reps,rest:rx.rest,quality,pain:!!pain,mode:rx.mode,performed,completed:performed&&weight===Number(rx.weight)&&!['baseline','recovery','reentry','time-fit','review','rebuild'].includes(rx.mode),sets:actual};
}
function validateBackup(input){
 const object=x=>x&&typeof x==='object'&&!Array.isArray(x);
 if(!object(input)||input.version!==33||!Array.isArray(input.sessions)||!object(input.weights)||!object(input.equipment))throw Error('Not a V33 backup');
 for(const gear of ['kb','club'])if(!Array.isArray(input.equipment[gear])||input.equipment[gear].some(x=>!Number.isFinite(x)||x<=0))throw Error('Invalid equipment');
 for(const map of [input.weights,input.nextWeights||{}]){
  if(!object(map))throw Error('Invalid working weights');
  for(const [id,weight] of Object.entries(map))if(!Object.hasOwn(MOVES,id)||!Number.isFinite(weight)||weight<0)throw Error('Invalid working weights');
 }
 for(const session of input.sessions){
  if(!object(session)||typeof session.id!=='string'||typeof session.title!=='string'||typeof session.date!=='string'||!/^\d{4}-\d{2}-\d{2}$/.test(session.date)||!Array.isArray(session.items))throw Error('Invalid training entry');
  for(const item of session.items){
   if(!object(item)||!Object.hasOwn(MOVES,item.id)||!Number.isFinite(item.weight)||item.weight<0||!Number.isInteger(item.actualSets)||item.actualSets<0||!Number.isFinite(item.actualReps)||item.actualReps<0||!Number.isInteger(item.targetSets)||item.targetSets<0||!Number.isFinite(item.targetReps)||item.targetReps<=0||!Number.isFinite(item.rest)||item.rest<0||!['clean','minor','hard','breakdown','pain'].includes(item.quality))throw Error('Invalid movement record');
  }
 }
 if(input.defaultMinutes!==undefined)timeBudget(input.defaultMinutes);
 if(input.deferredIds!==undefined&&(!Array.isArray(input.deferredIds)||input.deferredIds.some(id=>!Object.hasOwn(MOVES,id))))throw Error('Invalid deferred movements');
 if(input.painResolutions!==undefined){
  if(!object(input.painResolutions))throw Error('Invalid movement reviews');
  for(const [id,review] of Object.entries(input.painResolutions))if(!Object.hasOwn(MOVES,id)||!object(review)||!Array.isArray(review.painKeys)||review.painKeys.some(key=>typeof key!=='string'))throw Error('Invalid movement review');
 }
 return {...input,nextWeights:input.nextWeights||{},defaultMinutes:input.defaultMinutes??45,deferredIds:input.deferredIds||[]};
}
const policyFor=id=>({movement:id,kind:'app-default',volume:{start:MOVES[id].start,end:MOVES[id].end,reps:MOVES[id].reps,rest:MOVES[id].rest},promotion:'two clean complete exposures',endpoint:'explicit review',principleSources:[666],exactParametersSource:null});
return{MOVES,DAYS,LOADS,policyFor,validateBackup,records,successful,stateFor,prescription,minutesFor,timeBudget,plan,completeRecord,deferredAfter,resolvePain,movementGap};
});
