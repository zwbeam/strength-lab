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
Object.assign(MOVES,{
 snatch:{name:'Single-arm snatch',gear:'kb',unit:'kg',family:'hinge',reps:5,start:4,end:20,rest:0,sec:30,side:2,cues:['Only practice a familiar snatch with a controlled overhead lockout.','Start with the weaker side; match the stronger side.','Stop if hand skin, grip or overhead control deteriorates.'],avoid:'Do not learn a snatch by testing a heavy or unfamiliar load.'},
 doublePress:{name:'Double clean and press',gear:'kb',pair:true,unit:'kg per bell',family:'press',reps:3,start:3,end:10,rest:150,sec:30,side:1,cues:['Use a matched pair you can rack and press with control.','Keep the trunk stable and lower into a quiet rack.'],avoid:'No maximum attempts or grinding repetitions.'},
 doubleSquat:{name:'Double front squat',gear:'kb',pair:true,unit:'kg per bell',family:'squat',reps:3,start:3,end:10,rest:150,sec:30,side:1,cues:['Use a familiar, secure double rack.','Keep depth and bracing repeatable.'],avoid:'Stop when rack position or controlled depth is lost.'}
});
const DAYS=[{name:'A · Squat / Press / Pull',focus:'Kettlebell strength',ids:['squat','press','row']},{name:'B · Hinge / Cast / Carry',focus:'Hinge and club control',ids:['swing','cast','carry']},{name:'C · Clean / Club / Squat',focus:'Skill and balanced strength',ids:['clean','front','circles']}];
const LOADS={kb:[4,6,8,10,12,14,16,18,20,22,24,28,32,36,40,44,48],club:[2,3,4,5,7,10,12,15,17,20,25,30,35]};
const clamp=(n,a,b)=>Math.min(b,Math.max(a,n));
function records(s,id){return(s.sessions||[]).flatMap((x,sessionIndex)=>(x.items||[]).map((y,itemIndex)=>({...y,date:x.date,_key:`${x.id||x.date+':'+sessionIndex}:${itemIndex}`})).filter(y=>y.id===id)).sort((a,b)=>String(a.date).localeCompare(String(b.date)));}
function successful(x){return x&&x.quality==='clean'&&!x.pain&&x.completed===true&&x.actualSets>=x.targetSets&&x.actualReps>=x.targetReps&&Number(x.weight)>0;}
// Each profile states exactly which parameters are examples from a transcript.
// Promotion, recovery and scheduling thresholds remain configurable app decisions.
const PROFILE_NAMES={legacy:'Existing volume defaults',wave:'Heavy / light volume wave',snatch:'Snatch EMOM example',grind:'Double-kettlebell strength example',club:'Two-hand club timed practice'};
function policyFor(id,s={}){
 const m=MOVES[id];if(!Object.hasOwn(MOVES,id))throw Error('Unknown movement');
 const c=s.programming?.[id]||{},profile=c.profile||(['snatch'].includes(id)?'snatch':['doublePress','doubleSquat'].includes(id)?'grind':'legacy');
 if(!availableProfiles(id).includes(profile))throw Error('Unsupported movement profile');
 if(c.stallStrategy!==undefined&&!['repeat','redistribute'].includes(c.stallStrategy))throw Error('Unknown stall strategy');
 const exposures=c.exposures??2;
 if(!Number.isInteger(exposures)||exposures<1||exposures>6)throw Error('Use 1–6 clean exposures');
 let start=m.start,end=m.end,reps=m.reps,rest=m.rest,step=1,timed=!!m.timed,roundSeconds=null,sources=[666],exactParametersSource=null,density=null;
 if(profile==='snatch'){start=4;end=20;reps=5;rest=0;roundSeconds=60;step=c.step??1;if(![1,2].includes(step))throw Error('Snatch set increment must be 1 or 2');sources=[411,410];exactParametersSource=411;density=[{sets:16,reps:6},{sets:14,reps:7},{sets:12,reps:8},{sets:11,reps:9},{sets:10,reps:10}];}
 if(profile==='grind'){start=3;end=10;reps=c.reps??3;if(![3,4,5].includes(reps))throw Error('Double-kettlebell reps must be 3, 4 or 5');rest=150;roundSeconds=180;sources=[366,120];exactParametersSource=366;}
 if(profile==='club'){start=2;end=6;reps=c.seconds??30;if(![15,30,45,60].includes(reps))throw Error('Choose a supported timed bout');timed=true;rest=60;sources=[3];}
 if(profile==='wave'){
  if(!Number.isFinite(c.lightWeight)||!Number.isFinite(c.heavyWeight)||c.lightWeight<=0||c.heavyWeight<=c.lightWeight)throw Error('Heavy weight must exceed the light weight');
  
  sources=[228,403];
 }
 const stages=[];for(let sets=start;sets<end;sets+=step)stages.push({sets,reps,rest});stages.push({sets:end,reps,rest});
 const key=profile==='legacy'&&Object.keys(c).length===0?'legacy-v1':JSON.stringify(['rules-20261105-1',id,profile,reps,step,exposures,c.lightWeight,c.heavyWeight,c.stallStrategy||'repeat']);
 return{movement:id,profile,label:PROFILE_NAMES[profile],key,kind:exactParametersSource===null?'app-default':'transcript-example',volume:{start,end,reps,rest},stages,density,roundSeconds,timed,exposures,principleSources:sources,exactParametersSource,promotion:`${exposures} clean complete exposures (app setting)`,endpoint:'explicit review',config:c};
}
function availableProfiles(id){if(id==='snatch')return ['snatch'];if(['doublePress','doubleSquat'].includes(id))return ['grind'];if(MOVES[id]?.gear==='club')return ['legacy','club'];if(['swing','squat','press','row','clean'].includes(id))return ['legacy','wave'];return ['legacy'];}
function configureMovement(s,id,config){if(config.profile==='legacy'&&(config.exposures??2)===2&&(!config.stallStrategy||config.stallStrategy==='repeat'))config={};const next={...s,programming:{...s.programming,[id]:config}};const policy=policyFor(id,next);if(policy.profile==='wave'&&![config.lightWeight,config.heavyWeight].every(w=>(s.equipment?.[MOVES[id].gear]||[]).includes(w)))throw Error('Both wave weights must be available');return next;}
function replay(s,id,policy,track='base'){
 const h=records(s,id).filter(x=>(x.policyKey||'legacy-v1')===policy.key&&(x.track||'base')===track);
 let stage=0,stagePhase='volume',ready=false,streak=0,fail=0,cycles=0,weight=policy.profile==='wave'?(track==='heavy'?policy.config.heavyWeight:policy.config.lightWeight):(Number(s.weights?.[id])||0),lastEligibleKey=null;
 const shape=()=>stagePhase==='density'?{...policy.density[stage],rest:0}:policy.stages[stage];
 for(const x of h){
  if(Number(x.weight)>0&&Number(x.weight)!==weight){weight=Number(x.weight);stage=0;stagePhase='volume';ready=false;streak=0;fail=0;}
  if(x.pain||x.quality==='pain'){streak=0;fail++;continue;}
  if(x.performed&&['rebuild','reentry','recovery','deload'].includes(x.mode)){streak=0;if(x.quality==='clean')fail=0;continue;}
  if(x.quality!=='clean'||x.completed===false){streak=0;if(x.actualSets>0||['hard','breakdown'].includes(x.quality))fail++;continue;}
  if(ready)continue;
  const target=shape();
  if(successful(x)&&x.targetSets===target.sets&&x.targetReps===target.reps&&Math.abs(Number(x.rest)-target.rest)<1){
   fail=0;streak++;
   if(streak>=policy.exposures){streak=0;lastEligibleKey=x._key;const steps=stagePhase==='density'?policy.density:policy.stages;
    if(stage<steps.length-1)stage++;else{ready=true;cycles++;if(stagePhase==='volume'&&policy.density&&s.cycleChoices?.[id]?.at===x._key){stagePhase='density';stage=0;ready=false;}}
   }
  }else streak=0;
 }
 const override=Number(s.nextWeights?.[id]);
 if(policy.profile!=='wave'&&override>0&&override!==weight){weight=override;stage=0;stagePhase='volume';ready=false;streak=0;fail=0;}
 return{...shape(),phase:ready?'ready':stagePhase,stagePhase,stage,weight,streak,fail,cycles,lastEligibleKey,last:h.at(-1)||null,exposures:h.length};
}
function stateFor(s,id){
 const policy=policyFor(id,s),h=records(s,id),resolvedKeys=s.painResolutions?.[id]?.painKeys||[];
 const reviewedIndex=h.reduce((last,x,index)=>resolvedKeys.includes(x._key)?index:last,-1);
 const hold=h.some(x=>(x.pain||x.quality==='pain')&&!resolvedKeys.includes(x._key))?'Pain reported: stop and review this movement.':'';
 const reviewRecovery=resolvedKeys.length>0&&!h.slice(reviewedIndex+1).some(x=>x.performed&&['reentry','recovery'].includes(x.mode)&&x.quality==='clean');
 let track='base';
 if(policy.profile==='wave'){const eligible=h.filter(x=>x.policyKey===policy.key&&successful(x));track=eligible.length%2?'heavy':'light';}
 let result=replay(s,id,policy,track);
 if(policy.profile==='wave'){
  const light=replay(s,id,policy,'light');
  if(track==='heavy'){
   const heavyReps=Math.max(1,Math.floor(policy.volume.reps*.6));
   // Whole sets; heavy work must stay strictly below light work (#228).
   const lastLight=records(s,id).filter(x=>x.policyKey===policy.key&&x.track==='light'&&successful(x)).at(-1);
   const lightWork=(lastLight?.targetSets??light.sets)*(lastLight?.targetReps??light.reps)*policy.config.lightWeight;
   const sets=Math.max(0,Math.ceil(lightWork/(heavyReps*policy.config.heavyWeight))-1);
   result={...result,sets,reps:heavyReps,phase:light.phase,streak:0};
  }
 }
 return{...result,hold,reviewRecovery,policy,track,allExposures:h.length};
}
function resolvePain(s,id){if(!MOVES[id])throw Error('Unknown movement');return {...s,painResolutions:{...s.painResolutions,[id]:{painKeys:records(s,id).filter(x=>x.pain||x.quality==='pain').map(x=>x._key)}}};}
function movementGap(s,id,now=new Date()){const last=records(s,id).filter(x=>x.actualSets>0).at(-1);if(!last)return 0;return Math.max(0,Math.floor(calendarDay(now)-calendarDay(last.date)));}
function prerequisites(s,id){
 const required=id==='snatch'?['swing','clean','overhead']:['doublePress','doubleSquat'].includes(id)?['rack',id]:[];
 return required.filter(skill=>s.skills?.[skill]!==true);
}
function prescription(s,id,opts={}){
 const m=MOVES[id],st=stateFor(s,id),policy=st.policy,defaults=s.trainingDefaults||{};
 let sets=st.sets,reps=st.reps,rest=st.rest,weight=st.weight,mode=st.phase==='ready'?'milestone':st.phase;
 let reason=policy.profile==='wave'?`${st.track==='heavy'?'Heavy: lower total work':'Light: higher total work'}; each movement advances independently.`:`${policy.label}: complete the prescription cleanly ${policy.exposures} time(s) before the next step.`;
 if(!weight){mode='baseline';reason='Choose a familiar working weight; do not test a maximum.';}
 else if(st.fail>=2){
  mode='rebuild';
  if(policy.config.stallStrategy==='redistribute'&&!policy.timed&&!policy.roundSeconds&&reps>=3){
   const failed=records(s,id).filter(x=>x.actualSets>0).at(-1),factor=failed?.quality==='breakdown'?.6:.8;
   reps=Math.max(1,Math.floor(st.reps*factor));sets=Math.ceil(st.sets*st.reps/reps);reason='Stall alternative: fewer reps per set, redistributed volume (#259). Fraction and rounding are app defaults; never rush the work.';
  }else{if(sets<=1)reps=Math.max(1,Math.floor(reps*.7));sets=Math.max(1,sets-1);reason='Repeated difficulty: reduce work and rebuild clean technique (app default).';}
 }
 else if(mode==='milestone')reason='Cycle endpoint reached. Maintain, choose an available load, or select the supported next cycle explicitly.';
 const gapDays=defaults.reentryDays??14;
 if(opts.readiness==='low'){sets=Math.max(1,Math.ceil(sets*(defaults.recoveryFraction??.5)));mode='recovery';reason='Reduced readiness: less work, no advancement credit. '+reason;}
 if(opts.reentry||st.reviewRecovery||movementGap(s,id,opts.now)>gapDays){sets=Math.min(sets,Math.max(1,Math.floor(st.sets*(defaults.reentryFraction??.7))));mode='reentry';reason='Return after absence or review: reduced work; no advancement credit. '+reason;}
 const deloadEvery=defaults.deloadEvery??0;
 const eligible=records(s,id).filter(x=>successful(x)&&!['recovery','reentry','rebuild','deload'].includes(x.mode)).length;
 const sinceDeload=records(s,id).filter(x=>x.actualSets>0).findLastIndex(x=>x.mode==='deload'&&x.performed);
 if(deloadEvery>0&&eligible>0&&eligible%deloadEvery===0&&sinceDeload!==records(s,id).filter(x=>x.actualSets>0).length-1&&mode==='volume'){sets=Math.max(1,Math.floor(sets*.5));mode='deload';reason='Planned lighter exposure (app-configured interval); no progression credit.';}
 let blocked='';const missing=prerequisites(s,id);
 if(sets<1)blocked='No whole heavy set fits below the last light exposure. Choose a closer heavy weight or build the light cycle first.';
 if(missing.length)blocked='Confirm familiar prerequisite skills in Settings: '+missing.join(', ');
 if(policy.profile==='wave'&&![policy.config.lightWeight,policy.config.heavyWeight].every(w=>(s.equipment?.[m.gear]||[]).includes(w)))blocked='A configured wave weight is no longer available. Review equipment and programming.';
 if(weight>0&&Array.isArray(s.equipment?.[m.gear])&&!s.equipment[m.gear].includes(weight))blocked='This working weight is not in your available equipment. Review Settings before training.';
 if(m.pair&&(!weight||!(s.equipment?.pairs||[]).includes(weight)))blocked='Confirm an available matched kettlebell pair at this weight in Settings.';
 if(st.hold)blocked=st.hold+' Resolve the review before resuming.';
 if(blocked){mode=st.hold?'review':'prerequisite';sets=0;reason=blocked;}
 const roundSeconds=policy.roundSeconds;
 const secondsPerSet=policy.timed?reps*m.side:m.sec;
 return{id,name:m.name,unit:m.unit,weight,sets,reps,rest,side:m.side,timed:policy.timed,mode,reason,phase:st.phase,streak:st.streak,cycle:st.cycles,policyKey:policy.key,profile:policy.profile,track:st.track,roundSeconds,secondsPerSet,sourceIds:policy.principleSources,sourceParameters:policy.exactParametersSource,exposureTarget:policy.exposures};
}
function chooseCycle(s,id,choice){
 const st=stateFor(s,id);
 if(st.hold||st.fail||st.phase!=='ready')throw Error('Complete a clean cycle and resolve any review first');
 if(choice!=='density'||!st.policy.density||st.stagePhase!=='volume')throw Error('This movement has no supported density transition');
 return {...s,cycleChoices:{...s.cycleChoices,[id]:{at:st.lastEligibleKey,type:choice}}};
}
function loadOptions(s,id){
 const st=stateFor(s,id),m=MOVES[id];
 if(st.hold||st.fail||st.phase!=='ready')return [];
 const equipment=m.pair?s.equipment?.pairs:s.equipment?.[m.gear];
 const cap=s.trainingDefaults?.maxLoadJump??.25;
 return (equipment||[]).filter(w=>Number.isFinite(w)&&w>st.weight&&w<=st.weight*(1+cap)).sort((a,b)=>a-b);
}
function selectLoad(s,id,weight){if(!loadOptions(s,id).includes(weight))throw Error('Load must be an available, permitted increment after a clean cycle. Adjust the configurable jump limit deliberately if needed.');if(stateFor(s,id).policy.profile==='wave')throw Error('Configure a new heavy/light pair in Settings instead.');return{...s,nextWeights:{...s.nextWeights,[id]:weight}};}
function minutesFor(p){const m=MOVES[p.id];return(p.sets*(p.roundSeconds||((p.secondsPerSet??m.sec)+Math.max(0,p.rest)))/60)+.55;}
function timeBudget(minutes){
 const total=Number.isFinite(Number(minutes))?Number(minutes):45;
 if(!Number.isInteger(total)||total<15||total>120)throw Error('Workout duration must be 15–120 minutes');
 const warmup=total<=20?4:total<=35?5:total<=60?7:10;
 const cooldown=total<=20?3:total<=35?4:total<=60?7:10;
 return {total,warmup,cooldown,main:total-warmup-cooldown};
}
const BLOCKS={
 abc:{name:'Rolling A / B / C',days:DAYS},
 snatch:{name:'Snatch EMOM block',days:[{name:'Snatch volume / density',focus:'Opt-in source example; familiar technique required',ids:['snatch']}]},
 double:{name:'Double-kettlebell strength block',days:[{name:'Double clean and press / front squat',focus:'Source #366 strength example; confirmed matched pair required',ids:['doublePress','doubleSquat']}]},
 club:{name:'Two-hand club practice block',days:[{name:'Two-hand club patterns',focus:'Familiar club patterns; choose timed profiles in Settings',ids:['front','cast','circles']}]}
};
const DEMANDS={hinge:['lower','grip'],squat:['lower'],press:['shoulder','grip'],pull:['shoulder','grip'],carry:['grip'],rotation:['shoulder','grip']};
function calendarDay(value){const text=typeof value==='string'&&/^\d{4}-\d{2}-\d{2}$/.test(value)?value:new Date(value??Date.now()).toLocaleDateString('sv-SE');return Date.parse(text+'T12:00:00Z')/86400000;}
function plan(s,opts={}){
 const block=s.programBlock||'abc';if(!BLOCKS[block])throw Error('Unknown program block');
 const days=BLOCKS[block].days,slot=(s.sessions||[]).filter(x=>x.slot!==undefined&&(x.block||'abc')===block).length%days.length,day=days[slot];
 const budget=timeBudget(opts.minutes??s.defaultMinutes??45),defaults=s.trainingDefaults||{};
 const allowed=new Set(days.flatMap(x=>x.ids)),pending=s.deferredByBlock?.[block]||(block==='abc'?s.deferredIds:[])||[];
 const ids=[...new Set([...pending.filter(id=>allowed.has(id)),...day.ids])];
 const items=[],deferred=[],held=[],unavailable=[],prerequisite=[],scheduled=[];let used=0,hard=0;
 const today=calendarDay(opts.now),history=(s.sessions||[]).filter(x=>calendarDay(x.date)<=today);
 const trainingDays=new Set(history.filter(x=>today-calendarDay(x.date)<7&&(x.items||[]).some(y=>y.actualSets>0)).map(x=>x.date));
 const alreadyToday=history.some(x=>calendarDay(x.date)===today&&(x.items||[]).some(y=>y.actualSets>0));
 const restDay=!alreadyToday&&trainingDays.size>=(defaults.maxTrainingDays??6);
 for(const id of ids){
  if(!MOVES[id])continue;
  if(s.paused){deferred.push(id);continue;}
  if(Array.isArray(s.equipment?.[MOVES[id].gear])&&!s.equipment[MOVES[id].gear].length){unavailable.push(id);deferred.push(id);continue;}
  if(stateFor(s,id).hold){held.push(id);deferred.push(id);continue;}
  const rx=prescription(s,id,opts);
  if(rx.mode==='prerequisite'){prerequisite.push(id);deferred.push(id);continue;}
  const demands=DEMANDS[MOVES[id].family]||[];
  const recent=history.some(x=>today-calendarDay(x.date)<(defaults.minGapDays??0)&&(x.items||[]).some(y=>y.actualSets>0&&MOVES[y.id]&&(DEMANDS[MOVES[y.id].family]||[]).some(d=>demands.includes(d))));
  const isHard=rx.track==='heavy'||rx.profile==='grind'||rx.mode==='density';
  if(restDay||recent||(isHard&&hard>=(defaults.maxHardMovements??3))){scheduled.push(id);deferred.push(id);continue;}
  const cost=minutesFor(rx);
  if(used+cost>budget.main+1e-8){deferred.push(id);continue;}
  items.push(rx);used+=cost;if(isHard)hard++;
 }
 return{block,slot,day,items,deferred,held,unavailable,prerequisite,scheduled,restDay,paused:!!s.paused,estimated:Math.ceil(used),total:Math.ceil(used)+budget.warmup+budget.cooldown,reentry:items.some(x=>x.mode==='reentry'),cap:budget.main,budget};
}
function deferredAfter(plan,records){const pending=new Set(plan.deferred||[]);for(const record of records){if(!(record.performed??record.completed))pending.add(record.id);else pending.delete(record.id);}return [...pending];}
function completeRecord(rx,actual,quality,pain){
 const sets=(actual||[]).filter(x=>x.done),valid=x=>Number.isFinite(Number(x.weight))&&Number(x.weight)>0&&Number.isInteger(Number(x.reps))&&Number(x.reps)>0;
 const reps=sets.length?Math.min(...sets.map(x=>(rx.side===2?Math.min(Number(x.leftReps??x.reps)||0,Number(x.rightReps??x.reps)||0):(Number(x.reps)||0)))):0;
 const weight=sets.length?Number(sets[0].weight):Number(rx.weight);
 const sameLoad=sets.every(x=>Number(x.weight)===weight);
 const bilateral=rx.side!==2||sets.every(x=>x.bothSides===true&&Number(x.leftReps??x.reps)===Number(x.rightReps??x.reps)&&Number.isInteger(Number(x.leftReps??x.reps))&&Number.isInteger(Number(x.rightReps??x.reps)));
 const exactIntensity=rx.sourceParameters===null||rx.sourceParameters===undefined||sets.length===rx.sets&&sets.every(x=>Number(x.reps)===rx.reps&&(rx.side!==2||Number(x.leftReps??x.reps)===rx.reps&&Number(x.rightReps??x.reps)===rx.reps));
 const cadence=!rx.roundSeconds||sets.every(x=>x.timingValid===true);
 const performed=cadence&&rx.mode!=='review'&&sets.length>0&&sets.length>=rx.sets&&sets.every(valid)&&reps>=rx.reps&&sameLoad&&bilateral&&!['hard','breakdown','pain'].includes(quality)&&!pain;
 return{id:rx.id,name:rx.name,weight,unit:rx.unit,actualSets:sets.length,actualReps:reps,targetSets:rx.sets,targetReps:rx.reps,rest:rx.rest,quality,pain:!!pain,mode:rx.mode,policyKey:rx.policyKey||'legacy-v1',profile:rx.profile||'legacy',track:rx.track||'base',roundSeconds:rx.roundSeconds||null,sourceIds:rx.sourceIds||[],sourceParameters:rx.sourceParameters??null,exposureTarget:rx.exposureTarget??2,performed,completed:performed&&exactIntensity&&weight===Number(rx.weight)&&!['baseline','recovery','reentry','time-fit','review','rebuild','deload','prerequisite'].includes(rx.mode),sets:actual};
}
function validateProgramming(s){
 const object=x=>x&&typeof x==='object'&&!Array.isArray(x);
 if(s.programBlock!==undefined&&!Object.hasOwn(BLOCKS,s.programBlock))throw Error('Invalid program block');
 if(s.programming!==undefined){if(!object(s.programming))throw Error('Invalid programming settings');for(const id of Object.keys(s.programming)){if(!object(s.programming[id]))throw Error('Invalid movement settings');policyFor(id,s);}}
 if(s.skills!==undefined&&(!object(s.skills)||Object.values(s.skills).some(x=>typeof x!=='boolean')))throw Error('Invalid prerequisite confirmations');
 if(s.cycleChoices!==undefined){if(!object(s.cycleChoices))throw Error('Invalid cycle choices');for(const [id,choice] of Object.entries(s.cycleChoices))if(!Object.hasOwn(MOVES,id)||!object(choice)||choice.type!=='density'||typeof choice.at!=='string')throw Error('Invalid cycle choice');}
 if(s.deferredByBlock!==undefined){if(!object(s.deferredByBlock))throw Error('Invalid pending blocks');for(const [block,ids] of Object.entries(s.deferredByBlock))if(!Object.hasOwn(BLOCKS,block)||!Array.isArray(ids)||ids.some(id=>!Object.hasOwn(MOVES,id)))throw Error('Invalid pending movements');}
 const ranges={minGapDays:[0,7],maxTrainingDays:[1,7],maxHardMovements:[1,12],reentryDays:[1,180],deloadEvery:[0,100]};
 if(s.trainingDefaults!==undefined){if(!object(s.trainingDefaults))throw Error('Invalid training defaults');for(const [key,value] of Object.entries(s.trainingDefaults)){if(Object.hasOwn(ranges,key)){const [lo,hi]=ranges[key];if(!Number.isInteger(value)||value<lo||value>hi)throw Error('Invalid '+key);}else if(['maxLoadJump','recoveryFraction','reentryFraction'].includes(key)){if(!Number.isFinite(value)||value<=0||value>1)throw Error('Invalid '+key);}else throw Error('Unknown training default');}}
 if(s.equipment?.pairs!==undefined&&(!Array.isArray(s.equipment.pairs)||s.equipment.pairs.some(w=>!Number.isFinite(w)||w<=0||!s.equipment.kb.includes(w))))throw Error('Matched pairs must be owned kettlebell weights');
 return s;
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
 validateProgramming(input);
 return {...input,nextWeights:input.nextWeights||{},defaultMinutes:input.defaultMinutes??45,deferredIds:input.deferredIds||[]};
}
return{MOVES,DAYS,BLOCKS,LOADS,PROFILE_NAMES,policyFor,availableProfiles,configureMovement,prerequisites,chooseCycle,loadOptions,selectLoad,validateProgramming,validateBackup,records,successful,stateFor,prescription,minutesFor,timeBudget,plan,completeRecord,deferredAfter,resolvePain,movementGap};
});
